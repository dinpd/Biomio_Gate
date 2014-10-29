#!/usr/bin/env python

from websocket import create_connection
from biomio.protocol.message import BiomioMessage
from biomio.protocol.validate import verify_json

def new_connection():
    return create_connection("ws://127.0.0.1:8080/websocket")

def biomio_send(message, websocket=None, close_connection=True, wait_for_responce=True):

    if websocket is None:
        websocket = new_connection()

    verify_json(obj=message.toDict())
    websocket.send(message.toJson())

    responce = None
    if wait_for_responce:
        result = websocket.recv()
        responce = BiomioMessage.fromJson(result)
        verify_json(obj=responce.toDict())

    if close_connection:
        websocket.close()

    return responce

class TestServerHandshake:
    def __init__(self):
        self.ws = None

    def test_hello_server(self):
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_client_hello_message(secret='secret')
        response = biomio_send(message=message)

    def test_invalid_protocol_ver(self):
        invalid_proto_ver_string = '2.0'
        message = BiomioMessage(seq=0, protoVer=invalid_proto_ver_string, id='id', osId='os id', appId='app id')
        message.set_client_hello_message(secret='secret')

        response = biomio_send(message=message)
        assert response.msg_string() == 'bye'

    def test_ack_message(self):

        websocket = new_connection()

        # Send hello message
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_client_hello_message(secret='secret')
        response = biomio_send(websocket=websocket, message=message, close_connection=False)

        # Send ack message
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_ack_message()
        biomio_send(websocket=websocket, message=message, close_connection=False, wait_for_responce=False)

    def test_nop_message(self):
        websocket = new_connection()

        # Send hello message
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_client_hello_message(secret='secret')
        response = biomio_send(websocket=websocket, message=message, close_connection=False)

        # Send ack message
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_ack_message()
        biomio_send(websocket=websocket, message=message, close_connection=False, wait_for_responce=False)

        # Send nop message
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_nop_message()
        biomio_send(websocket=websocket, message=message, close_connection=False, wait_for_responce=False)

def main():
    pass

if __name__ == '__main__':
    main()