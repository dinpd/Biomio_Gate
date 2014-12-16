
import json
import python_jsonschema_objects as pjs
from biomio.protocol.schema import BIOMIO_protocol_json_schema

import logging
logger = logging.getLogger(__name__)


class BiomioMessageBuilder:
    _ns = None

    def __init__(self, **kwargs):
        self._header = {}
        self.set_header(**kwargs)

    def set_header(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._header[k] = v

    def get_header_field_value(self, field_str):
        return self._header.get(field_str, None)

    @classmethod
    def _get_ns(cls):
        if not cls._ns:
            # Suppress logging inside of python_jsonschema_objects module
            logger = logging.getLogger("python_jsonschema_objects.classbuilder")
            logger.disabled = True

            builder = pjs.ObjectBuilder(BIOMIO_protocol_json_schema)
            cls._ns = builder.build_classes()
        return cls._ns

    @staticmethod
    def create_message_from_json(json_string):
        biomio_message = None
        try:
            obj = json.loads(json_string)
            ns = BiomioMessageBuilder._get_ns()
            biomio_message = ns.BiomioSchema(**obj)
        except ValueError:
            return None

        return biomio_message

    def header_str(self):
        return json.dumps(self._header, ensure_ascii=False).decode('utf-8')

    @staticmethod
    def header_from_message(message):
        json_str = '{'
        json_str += '"oid":"{oid}","seq":{seq},"protoVer":"{protoVer}","id":"{id}","appId":"{appId}","osId":"{osId}","devId":"{devId}","token":"{token}"'\
            .format(oid=str(message.header.oid),
                    seq=int(message.header.seq),
                    protoVer=str(message.header.protoVer),
                    id=str(message.header.id),
                    appId=str(message.header.appId),
                    osId=str(message.header.osId),
                    devId=str(message.header.devId),
                    token=str(message.header.token))
        json_str += '}'
        return json_str

    def header_string(self):
        json_str = '{'
        json_str += '"oid":"{oid}","seq":{seq},"protoVer":"{protoVer}","id":"{id}","appId":"{appId}","osId":"{osId}","devId":"{devId}","token":"{token}"'\
            .format(oid=str(self._header['oid']),
                    seq=int(self._header['seq']),
                    protoVer=str(self._header['protoVer']),
                    id=str(self._header['id']),
                    appId=str(self._header['appId']),
                    osId=str(self._header['osId']),
                    devId=str(self._header['devId']),
                    token=str(self._header['token']))
        json_str += '}'
        return json_str

    def create_message(self, status=None, **kwargs):
        msg = {}

        for k, v in kwargs.iteritems():
            msg[k] = v

        obj = {
            'header': self._header,
            'msg': msg
        }

        if status:
            obj['status'] = status

        ns = self._get_ns()
        biomio_message = ns.BiomioSchema(**obj)
        self._header['seq'] += 2

        return biomio_message
