

from biomio.protocol.message import BiomioMessage
from biomio.third_party.fysom import Fysom

# States
STATE_READY = 'ready'
STATE_HELLO = 'hello'
STATE_END = 'end_session'

class MessageHandler:
    pass


class HelloMessageHandler(MessageHandler):

    @staticmethod
    def onhello(e):
        e.responce.set_server_hello_message(refreshToken='', ttl=0)
        print 'onhello'

    @staticmethod
    def verify(e):
        if e.request.msg_string() == 'hello':
            return STATE_HELLO
        else:
            return STATE_END


biomio_states = {
    'initial': STATE_READY,
    'events': [
        {'name': 'hello', 'src': STATE_READY, 'dst': [STATE_HELLO, STATE_END], 'decision': HelloMessageHandler.verify}
    ],
    'callbacks': {
        'onhello': HelloMessageHandler.onhello
    }
}


class BiomioProtocol:
    @staticmethod
    def printstatechange(e):
        print 'event: %s, src: %s, dst: %s' % (e.event, e.src, e.dst)

    def __init__(self):
        self._state_machine = Fysom(biomio_states)
        self._state_machine.onchangestate = BiomioProtocol.printstatechange
        self._seq = 0
        self._proto_ver = '0.0'
        self._token = 'token'

    def process_next(self, input_msg):
        print ' ------ '
        print 'Processing message: "%s" ' % input_msg.toJson(), input_msg.msg_string()
        make_transition = getattr(self._state_machine, '%s' % (input_msg.msg_string()), None)
        responce = BiomioMessage(seq=self._seq, protoVer=self._proto_ver, token=self._token)
        make_transition(request=input_msg, responce=responce)
        print 'Send responce %s' % responce.toJson()
        return responce