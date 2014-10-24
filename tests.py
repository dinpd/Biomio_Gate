#!/usr/bin/env python

from websocket import create_connection
from biomio.protocol.message import BiomioMessage
from biomio.protocol.validate import verify_json

def biomio_send(message, websocket=None, close_connection=True):

    if websocket is None:
        websocket = create_connection("ws://127.0.0.1:8080/websocket")

    websocket.send(message.toJson())
    result = websocket.recv()

    if close_connection:
        websocket.close()

    return BiomioMessage.fromJson(result)

class TestServerHandshake:
    def __init__(self):
        self.ws = None

    def test_hello_server(self):
        message = BiomioMessage(seq=0, protoVer='0.1', id='id', osId='os id', appId='app id')
        message.set_client_hello_message(secret='secret')
        verify_json(obj=message.toDict())
        response = biomio_send(message=message)
        verify_json(obj=response.toDict())

def main():
    pass

if __name__ == '__main__':
    main()