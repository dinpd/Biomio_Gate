#!/usr/bin/env python

from websocket import create_connection
from biomio.protocol.message import BiomioMessage
from biomio.protocol.validate import verify_json
from nose.tools import ok_, eq_, nottest, with_setup

class BiomioTest:
    def __init__(self):
        self._ws = None
        self._curr_seq = 0

    @nottest
    def new_connection(self, socket_timeout = 5):
        socket = create_connection("ws://127.0.0.1:8080/websocket")
        socket.settimeout(socket_timeout)
        return socket

    @nottest
    def send_message(self, message, websocket=None, close_connection=True, wait_for_responce=True):

        if websocket is None:
            websocket = self.new_connection()

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

    @nottest
    def get_curr_connection(self):
        """Helper method to get current connected websocket.
           Should be used to get current websocket after some setup methods
          (e.g. setup_test_with_handshake) that creates connection with server
          and send messages to prepare test case.
        """
        if not self._ws:
            self._ws = self.new_connection()
        return self._ws

    @nottest
    def create_next_message(self, **kwargs):
        """Helper method to create next new client message.
        By default (if no parameters passed) it is initializes
        client message header with correct default values and correct next
        sequence number.
        """
        default_args = {
            'seq': self._curr_seq,
            'protoVer': '0.1',
            'id': 'id',
            'osId': 'os id',
            'appId': 'app id'
        }

        for (k, v) in default_args.iteritems():
            if not k in kwargs:
                kwargs[k] = v

        message = BiomioMessage(**kwargs)
        self._curr_seq += 2
        return message

    @nottest
    def setup_test(self):
        """Default setup for test methods."""
        self._curr_seq = 0

    @nottest
    def teardown_test(self):
        """Default teardown for test methods"""
        self._curr_seq = 0
        if self._ws:
            if self._ws.connected:
                self._ws.close()
        self._ws = None

    @nottest
    def setup_test_with_hello(self):
        self.setup_test()

        # Send hello message
        message = self.create_next_message()
        message.set_client_hello_message(secret='secret')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg_string(), 'hello', msg='Response does not contains hello message')
        eq_(response.header.seq, message.header.seq + 1,
            'Responce sequence number is invalid (expected: %d, got: %d)' % (message.header.seq + 1, response.header.seq))

    @nottest
    def setup_test_with_handshake(self):
        """Setup method for tests to perform handshake"""
        self.setup_test_with_hello()

        # Send ack message
        message = self.create_next_message()
        message.set_ack_message()
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)


class TestConnectedState(BiomioTest):
    def setup(self):
        self.setup_test()

    def teardown(self):
        self.teardown_test()

    def test_hello_server(self):
        message = self.create_next_message()
        message.set_client_hello_message(secret='secret')
        response = self.send_message(message=message)
        eq_(response.msg_string(), 'hello', msg='Response does not contains hello message')

    def test_invalid_protocol_ver(self):
        invalid_proto_ver_string = '2.0'
        message = self.create_next_message(protoVer=invalid_proto_ver_string)
        message.set_client_hello_message(secret='secret')

        response = self.send_message(message=message)
        eq_(response.msg_string(), 'bye', msg='Response does not contains bye message')


class TestHandshakeState(BiomioTest):
    def setup(self):
        self.setup_test_with_hello()

    def teardown(self):
        self.teardown_test()

    def test_ack_message(self):
        # Send ack message
        message = self.create_next_message()
        message.set_ack_message()
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)


class TestReadyState(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake()

    def teardown(self):
        self.teardown_test()

    def test_nop_message(self):
        # Send nop message
        message = self.create_next_message()
        message.set_nop_message()
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=True, wait_for_responce=False)

    def test_bye_message(self):
        # Send bye message
        message = self.create_next_message()
        message.set_bye_message()
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)

        eq_(response.msg_string(), 'bye', msg='Response does not contains bye message')

    def test_invalid_sequence(self):
        message = self.create_next_message(seq=1)
        message.set_nop_message()
        socket = self.get_curr_connection()
        response = self.send_message(websocket=socket, message=message, close_connection=False)

def main():
    pass

if __name__ == '__main__':
    main()