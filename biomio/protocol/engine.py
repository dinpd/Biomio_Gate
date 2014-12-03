
from biomio.protocol.message import BiomioMessageBuilder
from biomio.third_party.fysom import Fysom, FysomError
from biomio.protocol.sessionmanager import SessionManager, Session
from biomio.protocol.settings import settings

from jsonschema import ValidationError
from functools import wraps

import logging
logger = logging.getLogger(__name__)

# States
STATE_CONNECTED = 'connected'
STATE_HANDSHAKE = 'handshake'
STATE_READY = 'ready'
STATE_DISCONNECTED = 'disconnected'


def _is_header_valid(e):
    """Helper method to verify header.
    Returns true if header information is valid, false otherwise
    Method attaches status attribute to the event parameter passed.
    Status contains error string in case when validation fails."""

    is_valid = True
    if not e.protocol_instance.is_sequence_valid(e.request.header.seq):
        is_valid = False
        e.status = 'Message sequence number is invalid'

    if not e.protocol_instance.is_protocol_version_valid(e.request.header.protoVer):
        is_valid = False
        e.status = 'Protocol version is invalid'

    return is_valid


def verify_header(verify_func):
    """
    Decorator that performs message header verification.
    :param verify_func: Callbacks used to make decision about next protocol state.
     Should take single parameter e - state event object.
    """
    def _decorator(e, *args, **kwargs):
        if not _is_header_valid(e, *args, **kwargs):
            return STATE_DISCONNECTED
        return verify_func(e, *args, **kwargs)
    return wraps(verify_func)(_decorator)


class MessageHandler:

    @staticmethod
    @verify_header
    def on_client_hello_message(e):
        if e.src == STATE_CONNECTED:
            # "hello" received in connected state
            # and message does not contain refresh token
            if not hasattr(e.request.header, "token")\
                    or not e.request.header.token:
                e.protocol_instance.start_new_session()
                return STATE_HANDSHAKE

        return STATE_DISCONNECTED

    @staticmethod
    @verify_header
    def on_ack_message(e):
        return STATE_READY

    @staticmethod
    @verify_header
    def on_nop_message(e):
        if e.src == STATE_READY:
            return STATE_READY

        return STATE_DISCONNECTED

    @staticmethod
    def on_bye_message(e):
        return STATE_DISCONNECTED

    @staticmethod
    @verify_header
    def on_auth_message(e):
        return STATE_READY


def handshake(e):
    # Send serverHello responce after entering handshake state
    session = e.protocol_instance.get_current_session()
    message = e.protocol_instance.create_next_message(
        request_seq=e.request.header.seq,
        oid='serverHello',
        refreshToken=session.refresh_token,
        ttl=settings.session_ttl
    )
    e.protocol_instance.send_message(responce=message)


def disconnect(e):
    # If status parameter passed to state change method
    # we will add it as a status for message
    status = None
    if hasattr(e, 'status'):
        status = e.status

    # In a case of reaching disconnected state due to invalid message,
    # request could not be passed to state change method
    request_seq = None
    if hasattr(e, 'request'):
        request_seq = e.request.header.seq

    e.protocol_instance.close_connection(request_seq=request_seq, status_message=status)


def print_state_change(e):
    """Helper function for printing state transitions to log."""
    logger.debug('STATE_TRANSITION: event: %s, %s -> %s' % (e.event, e.src, e.dst))

biomio_states = {
    'initial': STATE_CONNECTED,
    'events': [
        {
            'name': 'clientHello',
            'src': STATE_CONNECTED,
            'dst': [STATE_HANDSHAKE, STATE_DISCONNECTED],
            'decision': MessageHandler.on_client_hello_message
        },
        {
            'name': 'ack',
            'src': STATE_HANDSHAKE,
            'dst': [STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.on_ack_message
        },
        {
            'name': 'nop',
            'src': STATE_READY,
            'dst': [STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.on_nop_message
        },
        {
            'name': 'bye',
            'src': [STATE_CONNECTED, STATE_HANDSHAKE, STATE_READY],
            'dst': STATE_DISCONNECTED,
            'decision': MessageHandler.on_bye_message
        },
        {
            'name': 'auth',
            'src': STATE_HANDSHAKE,
            'dst': [STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.on_auth_message
        }
    ],
    'callbacks': {
        'onhandshake': handshake,
        'ondisconnected': disconnect,
        'onchangestate': print_state_change
    }
}


class BiomioProtocol:
    """ The BiomioProtocol class is an abstraction for protocol implementation.
        For every client connection unique instance of BiomioProtocol is created.
    """

    def __init__(self, **kwargs):
        """
        BiomioProtocol constructor.

        :param close_callback: Will be called when connection should be closed.
        :param send_callback: Will be called when connection should be called with single parameter - message string to send.
        :param start_connection_timer_callback: Will be called when connection timer should be started.
        :param stop_connection_timer_callback: Will be called when connection timer should be stoped.
        :param check_connected_callback: Will be called to check if connected to socket. Should return True if connected.
        """
        self._close_callback = kwargs['close_callback']
        self._send_callback = kwargs['send_callback']
        self._start_connection_timer_callback = kwargs['start_connection_timer_callback']
        self._stop_connection_timer_callback = kwargs['stop_connection_timer_callback']
        self._check_connected_callback = kwargs['check_connected_callback']

        self._session = None
        self._builder = BiomioMessageBuilder(oid='serverHeader', seq=1, protoVer='0.1')

        # Initialize state machine
        self._state_machine_instance = Fysom(biomio_states)

        logger.debug(' --------- ')  # helpful to separate output when auto tests is running

    def process_next(self, msg_string):
        """ Processes next message received from client.
        :param msg_string: String containing next message.
        """
        # Next message received - stop connection timer.
        self._stop_connection_timer_callback()

        # Create BiomioMessage instance form message string
        input_msg = None
        try:
            input_msg = self._builder.create_message_from_json(msg_string)
        except ValidationError, e:
            logger.exception(e)

        # If message is valid, perform necessary actions
        if input_msg and input_msg.msg and input_msg.header:
            logger.debug('RECEIVED: "%s" ' % msg_string)

            # Refresh session if necessary
            if self._session and hasattr(input_msg.header, 'token') and self._session.refresh_token == input_msg.header.token:
                self._refresh_session()

            # Restore session and state (if no session, and message contains token)
            if not self._session and hasattr(input_msg.header, 'token') and input_msg.header.token:
                self._restore_state(str(input_msg.header.token))

            if not self._state_machine_instance.current == STATE_DISCONNECTED:
                self._process_message(input_msg)
        else:
            self._state_machine_instance.bye(protocol_instance=self, status_message='Invalid message sent')

    def _process_message(self, input_msg):
        """ Processes next message, performs state machine transitions.
        :param input_msg: BiomioMessage instance received from client.
        """
        try:
            # State machine instance has callback with the same name as possible messages, that it could
            # receive from client. Retrieve function object (callback) for message and perform transition.
            make_transition = getattr(self._state_machine_instance, '%s' % input_msg.msg.oid, None)
            if make_transition:
                if self._state_machine_instance.current == STATE_DISCONNECTED:
                    return

                make_transition(request=input_msg, protocol_instance=self)

                # Start connection timer, if state machine does no reach its final state
                if not (self._state_machine_instance.current == STATE_DISCONNECTED):
                    self._start_connection_timer_callback()
            else:
                self._state_machine_instance.bye(request=input_msg, protocol_instance=self, status='Could not process message: %s' % input_msg.msg.oid)
        except FysomError, e:
            logger.exception('State event for method not defined')
            self._state_machine_instance.bye(request=input_msg, protocol_instance=self, status=str(e))
        except AttributeError:
            status_message = 'Internal error during processing next message'
            logger.exception(status_message)
            self._state_machine_instance.bye(request=input_msg, protocol_instance=self, status=status_message)

    def create_next_message(self, request_seq=None, status=None, **kwargs):
        """ Helper method to create message for responce.
        :param request_seq: Sequence num of request, got from client. (Will be increased to got next sequence number)
        :param status: Status string for next message.
        :param kwargs: Message parameters.
        :return: BiomioMessage instance.
        """
        if request_seq:
            self._builder.set_header(seq=int(request_seq) + 1)
        message = self._builder.create_message(status=status, **kwargs)
        return message

    def send_message(self, responce):
        """ Helper method for sending given message to client.
        :param responce: BiomioMessage instance to send.
        """
        self._send_callback(responce.serialize())
        logger.debug('SENT: %s' % responce.serialize())

    def close_connection(self, request_seq=None, status_message=None):
        """ Sends bye message and closes session.

        :note Temporary session object will be created to send bye message with status if necessary.

        :param request_seq: Sequence num of request, got from client. (Will be increased to got next sequence number)
        :param status_message: Status string for next message.
        """
        logger.debug('CLOSING CONNECTION...')
        self._stop_connection_timer_callback()

        # Send bye message
        if self._check_connected_callback():
            if not self._session:
                # Create temporary session object to send bye message if necessary
                self.start_new_session()
            message = self.create_next_message(request_seq=request_seq, status=status_message, oid='bye')
            self.send_message(responce=message)

        if self._session and self._session.is_open:
            SessionManager.instance().close_session(session=self._session)

        # Close connection
        self._close_callback()

    def get_current_session(self):
        """ Returns current session.
        :return: Session instance.
        """
        return self._session

    def _refresh_session(self):
        """ Used for session refresh and updating session token.
        """
        SessionManager.instance().refresh_session(self._session)
        self._builder.set_header(token=self._session.session_token)

    def is_sequence_valid(self, seq):
        """Checks sequeence number for responce. Return true if it is valid; false otherwise"""
        curr_seq = self._builder.get_header_field_value(field_str='seq')
        return ((int(curr_seq) - 2 < seq)
                or (seq == 0)) and (int(seq) % 2 == 0)

    def is_protocol_version_valid(self, version):
        """Checks protocol version. Return true if it is current version; false otherwise"""
        return version == '1.0'

    def on_session_closed(self):
        """ Should be called, when session expired.
        """
        self._state_machine_instance.bye(protocol_instance=self, status='Session expired')

    def start_new_session(self):
        """ Starts new session for protocol.
        """
        self._session = SessionManager.instance().create_session(close_callback=self.on_session_closed)
        self._builder.set_header(token=self._session.session_token)

    def connection_closed(self):
        """Should be called in cases when connection is closed by client."""
        if self._session:
            self._session.close_callback = None
            SessionManager.instance().set_protocol_state(token=self._session.refresh_token, current_state=self._state_machine_instance.current)
        logger.debug('Connection closed by client')

    def _restore_state(self, refresh_token):
        """ Restores session and state machine state using given refresh token. Closes connection with appropriate message otherwice.
        :param refresh_token: Session refresh token string.
        """
        session_manager = SessionManager.instance()
        self._session = session_manager.restore_session(refresh_token)

        if self._session:
            logger.debug('Continue session %s...' % refresh_token)
            self._builder.set_header(token=self._session.session_token)
            state = session_manager.get_protocol_state(token=self._session.refresh_token)
            if state:
                # Restore state
                logger.debug('State : %s' % state)
                self._state_machine_instance.current = state
            else:
                self._state_machine_instance.bye(protocol_instance=self, status='Internal error: Could not restore protpcol state after last disconnection')
        else:
            self._state_machine_instance.bye(protocol_instance=self, status='Invalid token')