
import json
from bunch import Bunch, toJSON, bunchify

class BiomioMessage(Bunch):
    def __init__(self, obj={}, **kwargs):
        if obj:
            super(BiomioMessage, self).__init__(**obj)
        else:
            self.init_header(**kwargs)

    def init_header(self, **kwargs):
        self.header = Bunch()
        for k, v in kwargs.iteritems():
            self.header.__setattr__(k, v)

    def _set_message(self, message, value=None):
        self.msg = Bunch()
        if not value:
            value = Bunch()
        self.msg.__setattr__(message, value)

    def set_client_hello_message(self, secret=None):
        self._set_message(message='hello')
        if secret:
            self.msg.hello.secret = secret

    def set_server_hello_message(self, refreshToken, ttl, key=None):
        self._set_message(message='hello')
        self.msg.hello.refreshToken = refreshToken
        self.msg.hello.ttl = ttl
        if key:
            self.msg.hello.key = key

    def set_status_message(self, status_str):
        self._set_message(message='status', value=status_str)

    def set_bye_message(self):
        self.msg = 'bye'

    def set_ack_message(self):
        self.msg = 'ack'

    def msg_string(self):
            try:
                if isinstance(self.msg, basestring):
                    return self.msg
                else:
                    for k,v in self.msg.iteritems():
                        return k
            except AttributeError:
                return ''

    def toJson(self, **options):
        return toJSON(self=self, **options)

    @staticmethod
    def fromJson(message_str):
        obj = json.loads(message_str)

        b = BiomioMessage(obj=bunchify(obj))
        return b
