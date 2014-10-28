#!/usr/bin/env python

# import python_jsonschema_objects as pjs
import biomio.third_party.python_jsonschema_objects as pjs

import logging

BIOMIO_protocol_json_schema = {
    "title": "Biomio Schema",
    "id": "http://biom.io/entry-schema#",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "schema of BIOMIO communication protocol",
    "type": "object",
    "required": ["header", "msg"],
    "properties": {
        "header": {
            "oneOf": [
                {"$ref": "#/definitions/client_header"},
                {"$ref": "#/definitions/server_header"}
            ]
        },
        "msg": {
            "oneOf": [
                {"$ref": "#/definitions/bye"},
                {"$ref": "#/definitions/nop"},
                {"$ref": "#/definitions/status"},
                # {"$ref": "#/definitions/resources"},
                {"$ref": "#/definitions/again"},
                {"$ref": "#/definitions/auth"},
                # {"$ref": "#/definitions/probe"},
                {"$ref": "#/definitions/client_hello"},
                {"$ref": "#/definitions/verify"},
                {"$ref": "#/definitions/identify"},
                {"$ref": "#/definitions/getData"},
                {"$ref": "#/definitions/setData"},
                {"$ref": "#/definitions/server_hello"},
                {"$ref": "#/definitions/try"},
                {"$ref": "#/definitions/data"}
            ]
        }
    },
    "definitions": {
        "nop": {"enum": ["nop"]},
        "bye": {"enum": ["bye"]},
        "status": {"type": "string"},
        "resource": {
            "type": "object",
            "required": ["rType", "rProperties"],
            "properties": {
                "rType": {"enum": ["video", "fp-scanner", "mic"]},
                "rProperties": {"type": "string"}
            }
        },
        "server_header": {
            "type": "object",
            "required": ["protoVer", "token"],
            "properties": {
                "seq": {"type": "number"},
                "protoVer": {"type": "string"},
                "token": {"type": "string"}
            }
        },
        "server_hello": {
            "type": "object",
            "required": ["refreshToken", "ttl"],
            "properties": {
                "refreshToken": {"type": "string"},
                "ttl": {"type": "number"},
                "key": {"type": "string"}
            }
        },
        "try": {
            "type": "object",
            "required": ["resource"],
            "properties": {
                "resource": {"$ref": "#/definitions/resource"},
                "samples": {"type": "number"}
            }
        },
        "data": {
            "type": "object",
            "required": ["keys", "values"],
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "values": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "client_header": {
            "type": "object",
            "required": ["seq", "id", "protoVer", "osId", "appId"],
            "properties": {
                "seq": {"type": "number"},
                "protoVer": {"type": "string"},
                "id": {"type": "string"},
                "appId": {"type": "string"},
                "osId": {"type": "string"},
                "devId": {"type": "string"},
                "token": {"type": "string"}
            }
        },
        "client_hello": {
            "type": "object",
            "properties": {
                "secret": {"type": "string"}
            }
        },
        "auth": {"type": "string"},
        "again": {"enum": ["again"]},
        # "resources": {
        #     "type": "object",
        #     "required": ["resources"],
        #     "properties": {
        #         "resources": {
        #             "type": "array",
        #             "items": {"$ref": "#/definitions/resource"}
        #         }
        #     }
        # },
        "image": {
            "media": {
                "type": "image/png",
                "binaryEncoding": "base64"
            },
            "type": "string"
        },
        "sound": {
            "media": {
                "type": "sound/waw",
                "binaryEncoding": "base64"
            },
            "type": "string"
        },
        # "probe": {
        #     "type": "object",
        #     "required": ["probeId", "samples"],
        #     "properties": {
        #         "probeId": {"type": "number"},
        #         "samples": {
        #             "oneOf": [
        #                 {
        #                     "type": "array",
        #                     "items": {"$ref": "#/definitions/image"}
        #                 },
        #                 {
        #                     "type": "array",
        #                     "items": {"$ref": "#/definitions/sound"}
        #                 }
        #             ]
        #         }
        #     }
        # },
        "verify": {
            "type": "object",
            "required": ["id"],
            "properties": {
                "id": {"type": "string"}
            }
        },
        "identify": {"enum": ["identify"]},
        "getData": {
            "type": "object",
            "required": ["keys"],
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "onBehalfOf": {"type": "string"}
            }
        },
        "setData": {
            "type": "object",
            "required": ["keys", "values"],
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "values": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "rect": {
            "type": "object",
            "required": ["x", "y", "width", "height"],
            "properties": {
                "x": {"type": "number"},
                "y": {"type": "number"},
                "height": {"type": "number"},
                "width": {"type": "number"}
            }
        },
        "detected": {
            "type": "object",
            "required": ["rects"],
            "properties": {
                "distance": {"type": "number"},
                "rects": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/rect"}
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    }
}

obj = {"msg": {"hello": {"secret": "secret"}},
       "header": {"osId": "os id", "appId": "app id", "id": "id", "seq": 0, "protoVer": "1.0"}}


def main():
    # logging.basicConfig(level=logging.DEBUG)
    builder = pjs.ObjectBuilder(BIOMIO_protocol_json_schema)
    # builder = pjs.ObjectBuilder(some_schema_1)
    # builder = pjs.ObjectBuilder(some_schema_3)
    ns = builder.build_classes()
    biomio_message = ns.BiomioSchema(**obj)


    print biomio_message.header.seq
    print biomio_message.header.id
    print biomio_message.header.appId
    print biomio_message.header.osId
    print biomio_message.header.protoVer

    biomio_message.header.seq = 1
    biomio_message.header.id = 'id'
    biomio_message.header.appId = 'application id'
    biomio_message.header.osId = 'operation system id'
    biomio_message.header.protoVer = '0.1'

    print '   '
    print biomio_message.header.seq
    print biomio_message.header.id
    print biomio_message.header.appId
    print biomio_message.header.osId
    print biomio_message.header.protoVer

    print biomio_message.msg.__dict__



if __name__ == '__main__':
    main()
