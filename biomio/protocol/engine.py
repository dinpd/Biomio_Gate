

from biomio.protocol.message import BiomioMessage
from biomio.third_party.fysom import Fysom
from biomio.protocol.validate import verify_json

# States
STATE_CONNECTED = 'connected'
STATE_HANDSHAKE = 'handshake'
STATE_READY = 'ready'
STATE_DISCONNECTED = 'disconnected'

MESSAGE_HELLO = 'hello'
MESSAGE_NOP = 'nop'
MESSAGE_BYE = 'bye'


class MessageHandler:
    pass


class HelloMessageHandler:

    @staticmethod
    def onhello(e):
        e.responce.set_server_hello_message(refreshToken='token', ttl=0)

    @staticmethod
    def verify(e):
        if e.protocol_instance.is_connection_timeout():
            # CONNECTION TIMEOUT
            return STATE_DISCONNECTED

        # Verify client message
        if not e.request: #or not verify_json(e.request):
            # JSON VALIDATION FAILED
            return STATE_DISCONNECTED

        # Verify header
        if not e.protocol_instance.is_header_valid(request=e.request):
            # INVALID HEADER INFO
            return STATE_DISCONNECTED

        # Process message
        if e.request.msg_string() == MESSAGE_HELLO:
            # "HELLO" RECEIVED
            return STATE_HANDSHAKE
        elif e.request.msg_string() == MESSAGE_NOP:
            # "NOP" RECEIVED
            return STATE_CONNECTED
        else:
            # ANY OTHER MESSAGE RECEIVED (EXCEPT "HELLO")
            return STATE_DISCONNECTED

class NopMessageHandler:

    @staticmethod
    def onnop(e):
        print 'onnop'

    @staticmethod
    def verify(e):
        return STATE_HANDSHAKE


class AckMessageHandler:
    @staticmethod
    def onack():
        print 'onack'

    @staticmethod
    def verify(e):
        # TODO: add real verification if session created without errors
        return STATE_READY

class ByeMessageHandler:

    @staticmethod
    def onbye(e):
        print 'onbye'


def disconnect(e):
    e.protocol_instance.close_connection()

biomio_states = {
    'initial': STATE_CONNECTED,
    'events': [
        {'name': 'hello', 'src': STATE_CONNECTED, 'dst': [STATE_HANDSHAKE, STATE_DISCONNECTED], 'decision': HelloMessageHandler.verify},
        {'name': 'ack', 'src': STATE_HANDSHAKE, 'dst': [STATE_READY, STATE_DISCONNECTED], 'decision': AckMessageHandler.verify },
        {'name': 'nop', 'src': STATE_READY, 'dst': [STATE_READY, STATE_DISCONNECTED], 'decision': NopMessageHandler.verify},
        {'name': 'bye', 'src': [STATE_CONNECTED, STATE_HANDSHAKE, STATE_READY], 'dst': STATE_DISCONNECTED}
    ],
    'callbacks': {
        'onhello': HelloMessageHandler.onhello,
        'onnop': NopMessageHandler.onnop,
        'onbye': ByeMessageHandler.onbye,
        'ondisconnected': disconnect
    }
}


class BiomioProtocol:
    @staticmethod
    def printstatechange(e):
        print 'STATE_TRANSITION: event: %s, %s -> %s' % (e.event, e.src, e.dst)


    def __init__(self, close_callback, send_callback):
        self._seq = 0
        self._proto_ver = '0.0'
        self._token = 'token'
        self._error = ''
        self._close_callback = close_callback
        self._send_callback = send_callback

        # Initialize state machine
        self._state_machine_instance = Fysom(biomio_states)
        self._state_machine_instance.onchangestate = BiomioProtocol.printstatechange
        #TODO: use some kind of logger instead
        print ' --------- '

    def process_next(self, input_msg):
        responce = None

        if input_msg:
            print 'RECEIVED: "%s" ' % input_msg.toJson()
            make_transition = getattr(self._state_machine_instance, '%s' % (input_msg.msg_string()), None)
            if make_transition:
                responce = BiomioMessage(seq=self._seq, protoVer=self._proto_ver, token=self._token)
                make_transition(request=input_msg, responce=responce, protocol_instance=self)
            else:
                error_str = 'Could not process message: %s' % input_msg.msg_string()
                responce = self.create_status_message(str=error_str)
        else:
            error_str = 'Invalid message sent'
            print error_str
            responce = self.create_status_message(str=error_str)

        if not self._state_machine_instance.isstate(STATE_DISCONNECTED):
            print 'SENT: %s' % responce.toJson()
            self._send_callback(responce.toJson())

    def close_connection(self):
        print 'CLOSING CONNECTION...'
        message = BiomioMessage(seq=self._seq, protoVer=self._proto_ver, token=self._token)
        message.set_bye_message()
        # print '  &&& ', message.msg()
        # print '  &&& ', message.msg_string()
        self._send_callback(message.toJson())
        print 'SENT: %s' % message.toJson()
        self._close_callback()

    def is_header_valid(self, request):
        """Return True if header information is valid; false otherwise"""
        #TODO: implement header validation
        return self._is_protocol_version_valid(request.header.protoVer)

    def is_connection_timeout(self):
        """Return True if connection lifetime is over; False otherwise"""
        return False #TODO: implement connection timer

    def create_status_message(self, str):
        """Helper method to create status responce"""
        responce = BiomioMessage(seq=self._seq, protoVer=self._proto_ver, token=self._token)
        responce.set_status_message(status_str=str)
        return responce

    def _is_protocol_version_valid(self, version):
        """Checks protocol version. Return true if it is current version; false otherwise"""
        if version == '0.1':
            return True
        else:
            return False

    def _is_sequence_is_valid(self, seq):
        if seq % 2 == 0 and (seq > self._seq or self,_seq == 0):
            return True
        else:
            return False
