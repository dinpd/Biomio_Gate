from itertools import izip
from functools import wraps
import logging

from jsonschema import ValidationError

from biomio.protocol.message import BiomioMessageBuilder
from biomio.third_party.fysom import Fysom, FysomError
from biomio.protocol.sessionmanager import SessionManager
from biomio.protocol.settings import settings
from biomio.protocol.crypt import Crypto
from biomio.protocol.storage.redisstore import RedisStore
from biomio.protocol.rpc.rpchandler import RpcHandler
from biomio.protocol.storage.applicationdatastore import ApplicationDataStore

import tornado.gen

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = '1.0'

# States
STATE_CONNECTED = 'connected'
STATE_HANDSHAKE = 'handshake'
STATE_REGISTRATION = 'registration'
STATE_APP_REGISTERED = 'appregistered'
STATE_READY = 'ready'
STATE_DISCONNECTED = 'disconnected'
STATE_PROBE_TRYING = 'probetry'
STATE_GETTING_PROBES = 'probeget'


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
        # "hello" should be received in connected state
        # and message does not contain refresh token
        if e.src == STATE_CONNECTED:
            if not hasattr(e.request.header, "token") \
                    or not e.request.header.token:

                # Create new session
                # TODO: move to some state handling callback
                e.protocol_instance.start_new_session()
                app_data = ApplicationDataStore.instance().get_app_data(
                    account_id=e.request.header.id,
                    application_id=e.request.header.appId,
                    key='public_key'
                )
                if hasattr(e.request.msg, "secret") \
                        and e.request.msg.secret:
                    if app_data is None:
                        return STATE_REGISTRATION
                    e.status = "Registration handshake is inappropriate. Given app is already registered."
                else:
                    if app_data is not None:
                        return STATE_HANDSHAKE
                    e.status = "Regular handshake is inappropriate. It is required to run registration handshake first."
        return STATE_DISCONNECTED

    @staticmethod
    @verify_header
    def on_ack_message(e):
        return STATE_READY

    @staticmethod
    @verify_header
    def on_nop_message(e):
        if e.src == STATE_READY:
            message = e.protocol_instance.create_next_message(
                request_seq=e.request.header.seq,
                oid='nop'
            )
            e.protocol_instance.send_message(responce=message)
            return STATE_READY

        return STATE_DISCONNECTED

    @staticmethod
    def on_bye_message(e):
        return STATE_DISCONNECTED

    @staticmethod
    @verify_header
    def on_auth_message(e):
        key = ApplicationDataStore.instance().get_app_data(
            account_id=e.request.header.id,
            application_id=e.request.header.appId,
            key='public_key'
        )

        header_str = BiomioMessageBuilder.header_from_message(e.request)

        if Crypto.check_digest(key=key, data=header_str, digest=str(e.request.msg.key)):
            return STATE_READY

        e.status = 'Handshake failed. Invalid signature.'
        return STATE_DISCONNECTED

    @staticmethod
    def on_registered(e):
        return STATE_APP_REGISTERED

    @staticmethod
    def on_probe_trying(e):
        return STATE_PROBE_TRYING

    @staticmethod
    @verify_header
    def on_getting_probe(e):
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


def registration(e):
    key, pub_key = Crypto.generate_keypair()

    ApplicationDataStore.instance().store_app_data(
        account_id=e.request.header.id,
        application_id=e.request.header.appId,
        public_key=pub_key
    )
    e.fsm.registered(protocol_instance=e.protocol_instance, request=e.request, key=key)


def app_registered(e):
    # Send serverHello responce after entering handshake state
    session = e.protocol_instance.get_current_session()

    message = e.protocol_instance.create_next_message(
        request_seq=e.request.header.seq,
        oid='serverHello',
        refreshToken=session.refresh_token,
        ttl=settings.session_ttl,
        key=e.key
    )
    e.protocol_instance.send_message(responce=message)


def probe_trying(e):
    pass


def getting_probe(e):
    pass


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
            'dst': [STATE_HANDSHAKE, STATE_REGISTRATION, STATE_DISCONNECTED],
            'decision': MessageHandler.on_client_hello_message
        },
        {
            'name': 'ack',
            'src': STATE_APP_REGISTERED,
            'dst': [STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.on_ack_message
        },
        {
            'name': 'registered',
            'src': STATE_REGISTRATION,
            'dst': [STATE_APP_REGISTERED, STATE_DISCONNECTED],
            'decision': MessageHandler.on_registered
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
        },
        {
            'name': 'try',
            'src': STATE_READY,
            'dst': [STATE_PROBE_TRYING, STATE_DISCONNECTED],
            'decision': MessageHandler.on_probe_trying
        },
        {
            'name': 'probe',
            'src': STATE_PROBE_TRYING,
            'dst': [STATE_GETTING_PROBES, STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.on_getting_probe
        }
    ],
    'callbacks': {
        'onhandshake': handshake,
        'ondisconnected': disconnect,
        'onregistration': registration,
        'onappregistered': app_registered,
        'onprobetry': probe_trying,
        'onprobeget': getting_probe,
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
        self._builder = BiomioMessageBuilder(oid='serverHeader', seq=1, protoVer=PROTOCOL_VERSION)

        self._rpc_handler = RpcHandler()

        # Initialize state machine
        self._state_machine_instance = Fysom(biomio_states)

        logger.debug(' --------- ')  # helpful to separate output when auto tests is running

    @tornado.gen.engine
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
            if self._session and hasattr(input_msg.header,
                                         'token') and self._session.refresh_token == input_msg.header.token:
                self._refresh_session()

            # Restore session and state (if no session, and message contains token)
            if not self._session and hasattr(input_msg.header, 'token') and input_msg.header.token:
                self._restore_state(str(input_msg.header.token))

            # Try to process RPC request subset, if message is RCP request - exit after processing

            if input_msg.msg.oid in ('rpcReq', 'rpcEnumNsReq', 'rpcEnumCallsReq'):
                self.process_rpc_request(input_msg)
                return

            # Process protocol message
            if not self._state_machine_instance.current == STATE_DISCONNECTED:
                self._process_message(input_msg)
        else:
            self._state_machine_instance.bye(protocol_instance=self,
                                             status='Invalid message sent (message string:%s)' % msg_string)

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
                self._state_machine_instance.bye(request=input_msg, protocol_instance=self,
                                                 status='Could not process message: %s' % input_msg.msg.oid)
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
        return version == PROTOCOL_VERSION

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
            SessionManager.instance().set_protocol_state(token=self._session.refresh_token,
                                                         current_state=self._state_machine_instance.current)
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
                self._state_machine_instance.bye(protocol_instance=self,
                                                 status='Internal error: Could not restore protpcol state after last disconnection')
        else:
            self._state_machine_instance.bye(protocol_instance=self, status='Invalid token')

    @tornado.gen.engine
    def process_rpc_request(self, input_msg):
        message_id = str(input_msg.msg.oid)

        if message_id == 'rpcReq':
            data = {}
            if input_msg.msg.data:
                for k,v in izip(list(input_msg.msg.data.keys), list(input_msg.msg.data.values)):
                    data[str(k)] = str(v)

            # result = self._rpc_handler.process_rpc_call(
            #     call=str(input_msg.msg.call),
            #     namespace=str(input_msg.msg.namespace),
            #     data=data
            # )
            result = yield tornado.gen.Task(self._rpc_handler.process_rpc_call, str(input_msg.header.id), str(input_msg.msg.call), str(input_msg.msg.namespace), data)

            res_keys = []
            res_values = []

            res_params = {
                'oid': 'rpcResp',
                'namespace': str(input_msg.msg.namespace),
                'call': str(input_msg.msg.call),
            }

            if result:
                for k, v in result.iteritems():
                    res_keys.append(k)
                    res_values.append(str(v))

                res_params['data'] = {'keys': res_keys, 'values': res_values}

            message = self.create_next_message(
                request_seq=input_msg.header.seq,
                **res_params
            )
            self.send_message(responce=message)
        elif message_id == 'rpcEnumNsReq':
            namespaces = self._rpc_handler.get_available_namespaces()
            message = self.create_next_message(request_seq=input_msg.header.seq, oid='rpcEnumNsReq', namespaces=namespaces)
            self.send_message(responce=message)
        elif message_id == 'rpcEnumCallsReq':
            self._rpc_handler.get_available_calls(namespace=input_msg.msg.namespace)
