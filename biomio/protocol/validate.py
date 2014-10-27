from jsonschema import validate, ValidationError, SchemaError

BIOMIO_protocol_json_schema = {
    "id": "http://biom.io/entry-schema#",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "schema of BIOMIO communication protocol",
    "type": "object",
    "required": [ "header",
                  "msg"
                  # "action",   #fixed
                  # "seq"
    ],
    "properties": {
        "header": {
            "type": "object",
            "oneOf": [
                { "$ref": "#/definitions/client/definitions/header" },
                { "$ref": "#/definitions/server/definitions/header" }
            ]
        },
        "msg": {
            "type": "object",
            "oneOf": [
                { "$ref": "#/definitions/common/definitions/bye" },
                { "$ref": "#/definitions/common/definitions/nop" },
                { "$ref": "#/definitions/common/definitions/status" },
                { "$ref": "#/definitions/client/definitions/again" },
                { "$ref": "#/definitions/client/definitions/ack" }, # ack message to confirm handshake
                { "$ref": "#/definitions/client/definitions/auth" },
                { "$ref": "#/definitions/client/definitions/resources" },
                { "$ref": "#/definitions/client/definitions/probe" },
                { "$ref": "#/definitions/client/definitions/hello" },
                { "$ref": "#/definitions/client/definitions/verify" },
                { "$ref": "#/definitions/client/definitions/identify" },
                { "$ref": "#/definitions/client/definitions/getData" },
                { "$ref": "#/definitions/client/definitions/setData" },
                { "$ref": "#/definitions/server/definitions/hello" },
                { "$ref": "#/definitions/server/definitions/try" },
                { "$ref": "#/definitions/server/definitions/data" }
            ]
        }
    },

    "definitions": {
        "common": {
            "definitions" : {
                "nop": { "enum": [ "nop" ] },
                "bye": { "enum": [ "bye" ] },
                "status": { "type": "string" },
                "resource": {
                    "type": "object",
                    "required": [ "rType", "rProperties" ],
                    "properties": {
                        "rType": { "enum": [ "video", "fp-scanner", "mic" ] },
                        "rProperties": { "type": "string" }
                    }
                }
            }
        },
        "server": {
            "definitions" : {
                "header": {
                    "type": "object",
                    "required": [ "protoVer", "token" ],
                    "properties": {
                        "seq": { "type": "number" },
                        "protoVer": { "type": "string" },
                        "token": { "type": "string" }
                    }
                },
                "hello": {
                    "type": "object",
                    "required": [ "refreshToken", "ttl" ],
                    "properties": {
                        "refreshToken": { "type": "string" },
                        "ttl": { "type": "number" },
                        "key": { "type": "string" }
                    }
                },
                "try": {
                    "type": "object",
                    "required": [ "resource" ],
                    "properties": {
                        "resource": { "$ref": "#/definitions/common/definitions/resource" },
                        "samples": { "type": "number" }
                    }
                },
                "data": {
                    "type": "object",
                    "required": [ "keys", "values" ],
                    "properties": {
                        "keys": {
                            "type": "array",
                            "items": { "type": "string" }
                        },
                        "values": {
                            "type": "array",
                            "items": { "type": "string" }
                        }
                    }
                }
            }
        },
        "client": {
            "definitions": {
                "header": {
                    "type": "object",
                    "required": [ "seq", "id", "protoVer", "osId", "appId" ],
                    "properties": {
                        "seq": { "type": "number" },
                        "protoVer": { "type": "string" },
                        "id": { "type": "string" },
                        "appId": { "type": "string" },
                        "osId": { "type": "string" },
                        "devId": { "type": "string" },
                        "token": { "type": "string" }
                    }
                },
                "hello": {
                    "type": "object",
                    "properties": {
                        "secret": { "type": "string" }
                    }
                },
                "auth": { "type": "string" },
                "again": { "enum": [ "again" ] },
                "ack": { "enum": [ "ack" ] }, # ack message to confirm handshake
                "resources": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/common/definitions/resource"
                    }
                },
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
                "probe": {
                    "type": "object",
                    "required": [ "probeId", "samples" ],
                    "properties": {
                        "probeId": {
                            "type": "number"  # fixed
                        },
                        "samples": {
                            "type": "array",
                            "items": {
                                "oneOf": [
                                    { "$ref": "#/definitions/server/definitions/image" },
                                    { "$ref": "#/definitions/server/definitions/sound" }
                                ]
                            }
                        }
                    }
                },
                "verify": {
                    "type": "object",
                    "required": [ "id" ],
                    "properties": {
                        "id": { "type": "string" }
                    }
                },
                "identify": { "enum": [ "identify" ] },
                "getData": {
                    "type": "object",
                    "required": [ "keys" ],
                    "properties": {
                        "keys": {
                            "type": "array",
                            "items": { "type": "string" }
                        },
                        "onBehalfOf": { "type": "string" }
                    }
                },
                "setData": {
                    "type": "object",
                    "required": [ "keys", "values" ],
                    "properties": {
                        "keys": {
                            "type": "array",
                            "items": { "type": "string" }
                        },
                        "values": {
                            "type": "array",
                            "items": { "type": "string" }
                        }
                    }
                },
                "rect": {
                    "type": "object",
                    "required": [ "x", "y", "width", "height" ],
                    "properties": {
                        "x": { "type": "number" },
                        "y": { "type": "number" },
                        "height": { "type": "number" },
                        "width": { "type": "number" }
                    }
                },
                "detected": {
                    "type": "object",
                    "required": [ "rects" ],
                    "properties": {
                        "distance": { "type": "number" },
                        "rects": {
                            "type": "array",
                            "items": { "$ref": "#/definitions/server/definitions/rect" }
                        },
                        "labels": {
                            "type": "array",
                            "items": { "type": "string" }
                        }
                    }
                }
            }
        }
    }
}

def verify_json(obj):
    try:
        validate(obj, BIOMIO_protocol_json_schema)
    except (ValidationError, SchemaError):
        return False

    return True
