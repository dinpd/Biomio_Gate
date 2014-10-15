
import json
import jsonschema


### Common definitions

### Client definitions
MSG_HEADER = 'header'
MSG_OBJECT = 'msg'

# Header
CLIENT_MSG_HEADER_SEQ = 'seq'
CLIENT_MSG_HEADER_ID = 'id'
CLIENT_MSG_HEADER_PROTO_VER = 'protoVer'
CLIENT_MSG_HEADER_OS_ID = 'osId'
CLIENT_MSG_HEADER_APP_ID = 'appId'

# Hello
CLIENT_MSG_HELLO = 'hello'
CLIENT_MSG_HELLO_PUBLIC_KEY = 'pubKey'
CLIENT_MSG_HELLO_SECRET_KEY = 'secret'

### Server definitions

# Header
SERVER_MSG_HEADER_SEQ = 'seq'
SERVER_MSG_HEADER_PROTO_VER = 'protoVer'
SERVER_MSG_HEADER_TOKEN = 'token'

# Hello
SERVER_MSG_HELLO = 'hello'
SERVER_MSG_HELLO_REFRESH_TOKEN = 'refreshToken'
SERVER_MSG_HELLO_TTL = 'ttl'

class BiomioMessage:

    def __init__(self):
        self._header = ''
        self._msg = ''
        self._msg_object = {}

    def _construct_message(self, msg_name, _msg_object):
        obj = {
            MSG_HEADER: self._header,
            MSG_OBJECT: {msg_name: self._msg_object}
        }
        return obj

    def msg_sting(self):
        return self._msg

    @classmethod
    def from_string(cls, message_string):
        """
        Creates Biomio message instance by string contaning JSON.
        Method should be overridden by subclass
        """
        raise NotImplementedError


    def json_obj(self):
        return self._construct_message(self._msg, self._msg_object)

    def dumps(self):
        obj = self.json_obj()
        return json.dumps(obj)


class BiomioServerMessage(BiomioMessage):

    def __init__(self, seq, proto_ver, token):
        self._init_header(seq=seq, proto_ver=proto_ver, token=token)

    @classmethod
    def from_string(cls, message_string):
        obj = json.loads(message_string)

        # Get header
        header_obj = obj[MSG_HEADER]
        message = BiomioServerMessage(
            header_obj[SERVER_MSG_HEADER_SEQ],
            header_obj[SERVER_MSG_HEADER_PROTO_VER],
            header_obj[SERVER_MSG_HEADER_TOKEN]
        )

        # Get message string and message object
        (message._msg, message._msg_object) = obj[MSG_OBJECT].popitem()

        return message

    def _init_header(self, seq, proto_ver, token):
        self._header = {
            SERVER_MSG_HEADER_SEQ: seq,
            SERVER_MSG_HEADER_PROTO_VER: proto_ver,
            SERVER_MSG_HEADER_TOKEN: token
        }

    def hello(self, refresh_token, ttl):
        self._msg = SERVER_MSG_HELLO
        self._msg_object = {
            SERVER_MSG_HELLO_REFRESH_TOKEN: refresh_token,
            SERVER_MSG_HELLO_TTL: ttl
        }


class BiomioClientMessage(BiomioMessage):

    def __init__(self, seq, message_id, proto_ver, os_id, app_id):
        self._init_header(seq=seq, message_id=message_id, proto_ver=proto_ver, os_id=os_id, app_id=app_id)
        self._msg = ''
        self._msg_object = {}

    @classmethod
    def from_string(cls, message_string):
        obj = json.loads(message_string)

        # Get header
        header_obj = obj.pop(MSG_HEADER)
        message = cls(
            header_obj[CLIENT_MSG_HEADER_SEQ],
            header_obj[CLIENT_MSG_HEADER_ID],
            header_obj[CLIENT_MSG_HEADER_PROTO_VER],
            header_obj[CLIENT_MSG_HEADER_OS_ID],
            header_obj[CLIENT_MSG_HEADER_APP_ID]
        )

        # Get message string and message object
        (message._msg, message._msg_object) = obj[MSG_OBJECT].popitem()

        return message


    def _init_header(self, seq, message_id, proto_ver, os_id, app_id):
        self._header = {
            CLIENT_MSG_HEADER_SEQ: seq,
            CLIENT_MSG_HEADER_ID: message_id,
            CLIENT_MSG_HEADER_PROTO_VER: proto_ver,
            CLIENT_MSG_HEADER_OS_ID: os_id,
            CLIENT_MSG_HEADER_APP_ID: app_id
        }

    def hello(self, public_key, private_key):
        self._msg = CLIENT_MSG_HELLO
        self._msg_object = {
            CLIENT_MSG_HELLO_PUBLIC_KEY: public_key,
            CLIENT_MSG_HELLO_SECRET_KEY: private_key
        }


