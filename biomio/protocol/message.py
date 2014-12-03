
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
