

from biomio.protocol.message import BiomioMessageBuilder
from biomio.third_party.fysom import Fysom, FysomError
from jsonschema import ValidationError

import logging
logger = logging.getLogger(__name__)

# States
STATE_CONNECTED = 'connected'
STATE_HANDSHAKE = 'handshake'
STATE_READY = 'ready'
STATE_DISCONNECTED = 'disconnected'

class MessageHandler:
    @staticmethod
    def _is_header_valid(e):
        """Helper method to verify header.
        Returns true if header information is valid, false otherwise
        Method attaches status attribute to the event parameter passed,
        which contains error string in case when """
        #TODO: implement header validation

        is_valid = True
        if not e.protocol_instance.is_sequence_valid(e.request.header.seq):
            is_valid = False
            e.status = 'Message sequence number is invalid'

        if not e.protocol_instance.is_protocol_version_valid(e.request.header.protoVer):
            is_valid = False
            e.status = 'Protocol version is invalid'

        return is_valid

    @staticmethod
    def verify_hello_message(e):
        if MessageHandler._is_header_valid(e) \
                and (e.src == STATE_CONNECTED):
            # "hello" received in connected state
            # and header is valid
            return STATE_HANDSHAKE

        return STATE_DISCONNECTED

    @staticmethod
    def verify_ack_message(e):
        if MessageHandler._is_header_valid(e):
            return STATE_READY

        return STATE_DISCONNECTED

    @staticmethod
    def verify_nop_message(e):
        if MessageHandler._is_header_valid(e) \
                and (e.src == STATE_READY):
            return STATE_READY

        return STATE_DISCONNECTED

    @staticmethod
    def verify_bye_message(e):
        return STATE_DISCONNECTED

def handshake(e):
    message = e.protocol_instance.create_next_message(oid='serverHello', refreshToken='token', ttl=0)
    e.protocol_instance.send_message(responce=message)

def disconnect(e):
    #TODO: send status on disconnect
    status = None
    if hasattr(e, 'status'):
        status = e.status
    e.protocol_instance.close_connection(status_message=status)

biomio_states = {
    'initial': STATE_CONNECTED,
    'events': [
        {
            'name': 'clientHello',
            'src': STATE_CONNECTED,
            'dst': [STATE_HANDSHAKE, STATE_DISCONNECTED],
            'decision': MessageHandler.verify_hello_message
        },
        {
            'name': 'ack',
            'src': STATE_HANDSHAKE,
            'dst': [STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.verify_ack_message
        },
        {
            'name': 'nop',
            'src': STATE_READY,
            'dst': [STATE_READY, STATE_DISCONNECTED],
            'decision': MessageHandler.verify_nop_message
        },
        {
            'name': 'bye',
            'src': [STATE_CONNECTED, STATE_HANDSHAKE, STATE_READY],
            'dst': STATE_DISCONNECTED,
            'decision': MessageHandler.verify_bye_message
        }
    ],
    'callbacks': {
        'onhandshake': handshake,
        'ondisconnected': disconnect
    }
}


class BiomioProtocol:
    @staticmethod
    def print_state_change(e):
        logger.debug('STATE_TRANSITION: event: %s, %s -> %s' % (e.event, e.src, e.dst))

    def __init__(self, **kwargs):
        self._close_callback = kwargs['close_callback']
        self._send_callback = kwargs['send_callback']
        self._start_connection_timer_callback = kwargs['start_connection_timer_callback']
        self._stop_connection_timer_callback = kwargs['stop_connection_timer_callback']

        self._builder = BiomioMessageBuilder(oid='serverHeader', seq=1, protoVer='0.1', token='token')

        # Initialize state machine
        self._state_machine_instance = Fysom(biomio_states)
        self._state_machine_instance.onchangestate = BiomioProtocol.print_state_change
        #TODO: use some kind of logger instead
        logger.debug(' --------- ')  # helpful to separate output when auto tests is running

    def process_next(self, msg_string):
        input_msg = None
        try:
            input_msg = self._builder.create_message_from_json(msg_string)
        except ValidationError, e:
            logger.debug(str(e))

        if input_msg:
            logger.debug('RECEIVED: "%s" ' % msg_string)
            make_transition = getattr(self._state_machine_instance, '%s' % input_msg.msg.oid, None)
            if make_transition:
                try:
                    #TODO: add restating connection timer on next correct message from client
                    make_transition(request=input_msg, protocol_instance=self)
                except FysomError, e:
                    self.close_connection(status_message=str(e))
            else:
                self.close_connection(status_message='Could not process message: %s' % input_msg.msg.oid)
        else:
            self.close_connection(status_message='Invalid message sent')

    def create_next_message(self, status=None, **kwargs):
        message = self._builder.create_message(status=status, **kwargs)
        return message

    def send_message(self, responce):
        logger.debug('SENT: %s' % responce.serialize())
        self._send_callback(responce.serialize())

    def close_connection(self, status_message=None):
        logger.debug('CLOSING CONNECTION...')
        self._stop_connection_timer_callback()

        # Send bye message
        message = self.create_next_message(status=status_message, oid='bye')

        self.send_message(responce=message)

        # Close connection
        self._close_callback()

    def is_sequence_valid(self, seq):
        return ((self._builder.get_header_field_value(field_str='seq') < seq)
                or (seq == 0)) and (int(seq) % 2 == 0)

    def is_protocol_version_valid(self, version):
        """Checks protocol version. Return true if it is current version; false otherwise"""
        return version == '1.0'

