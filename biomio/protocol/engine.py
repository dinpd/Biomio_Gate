

from biomio.protocol.message import BiomioMessageBuilder
from biomio.third_party.fysom import Fysom, FysomError
from jsonschema import ValidationError

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
            print e.status

        if not e.protocol_instance.is_protocol_version_valid(e.request.header.protoVer):
            is_valid = False
            e.status = 'Protocol version is invalid'
            print e.status

        return is_valid

    @staticmethod
    def verifyHelloMessage(e):
        if MessageHandler._is_header_valid(e) \
                and (e.src == STATE_CONNECTED):
            # "hello" received in connected state
            # and header is valid
            return STATE_HANDSHAKE

        return STATE_DISCONNECTED

    @staticmethod
    def verifyAckMessage(e):
        if MessageHandler._is_header_valid(e):
            return STATE_READY

        return STATE_DISCONNECTED

    @staticmethod
    def verifyNopMessage(e):
        if MessageHandler._is_header_valid(e) \
                and (e.src == STATE_READY):
            return STATE_READY

        return STATE_DISCONNECTED

    @staticmethod
    def verifyByeMessage(e):
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
        {'name': 'clientHello', 'src': STATE_CONNECTED, 'dst': [STATE_HANDSHAKE, STATE_DISCONNECTED], 'decision': MessageHandler.verifyHelloMessage },
        {'name': 'ack', 'src': STATE_HANDSHAKE, 'dst': [STATE_READY, STATE_DISCONNECTED], 'decision': MessageHandler.verifyAckMessage },
        {'name': 'nop', 'src': STATE_READY, 'dst': [STATE_READY, STATE_DISCONNECTED], 'decision': MessageHandler.verifyNopMessage },
        {'name': 'bye', 'src': [STATE_CONNECTED, STATE_HANDSHAKE, STATE_READY], 'dst': STATE_DISCONNECTED, 'decision': MessageHandler.verifyByeMessage }
    ],
    'callbacks': {
        'onhandshake': handshake,
        'ondisconnected': disconnect
    }
}

class BiomioProtocol:
    @staticmethod
    def printstatechange(e):
        print 'STATE_TRANSITION: event: %s, %s -> %s' % (e.event, e.src, e.dst)


    def __init__(self, close_callback, send_callback, start_connection_timer_callback, stop_connection_timer_callback):
        self._error = ''
        self._close_callback = close_callback
        self._send_callback = send_callback
        self._start_connection_timer_callback = start_connection_timer_callback
        self._stop_connection_timer_callback = stop_connection_timer_callback
        self._builder = BiomioMessageBuilder(oid='serverHeader', seq=1, protoVer='0.1', token='token')

        # Initialize state machine
        self._state_machine_instance = Fysom(biomio_states)
        self._state_machine_instance.onchangestate = BiomioProtocol.printstatechange
        #TODO: use some kind of logger instead
        print ' --------- '

    def process_next(self, msg_string):
        responce = None
        input_msg = None

        try:
            input_msg = self._builder.create_message_from_json(msg_string)
        except ValidationError, e:
            print e

        if input_msg:
            print 'RECEIVED: "%s" ' % msg_string
            make_transition = getattr(self._state_machine_instance, '%s' % (input_msg.msg.oid), None)
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
        print 'SENT: %s' % responce.serialize()
        self._send_callback(responce.serialize())

    def close_connection(self, status_message=None):
        print 'CLOSING CONNECTION...'
        self._stop_connection_timer_callback()

        # Send bye message
        message = self.create_next_message(status=status_message, oid='bye')

        self.send_message(responce=message)

        # Close connection
        self._close_callback()

    def is_sequence_valid(self, seq):
        #TODO: fix sequence validation
        return ((self._builder.get_header_field_value(field_str='seq') < seq) \
            or (seq == 0)) and (int(seq) % 2 == 0)

    def is_protocol_version_valid(self, version):
        """Checks protocol version. Return true if it is current version; false otherwise"""
        return version == '1.0'

