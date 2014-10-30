#!/usr/bin/env python

from websocket import create_connection
from biomio.protocol.message import BiomioMessage
from biomio.protocol.validate import verify_json
from nose.tools import ok_, eq_, nottest, with_setup

class BiomioTest:
    _ws = None
    _curr_seq = 0

    @classmethod
    @nottest
    def new_connection(cls):
        return create_connection("ws://127.0.0.1:8080/websocket")

    @classmethod
    @nottest
    def send_message(cls, message, websocket=None, close_connection=True, wait_for_responce=True):

        if websocket is None:
            websocket = cls.new_connection()

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


    @classmethod
    @nottest
    def get_curr_connection(cls):
        """Helper method to get current connected websocket.
           Should be used to get current websocket after some setup methods
          (e.g. setup_test_with_handshake) that creates connection with server
          and send messages to prepare test case.
        """
        if not cls._ws:
            cls._ws = cls.new_connection()
        return cls._ws

    @classmethod
    @nottest
    def create_next_message(cls, **kwargs):
        """Helper method to create next new client message.
        By default (if no parameters passed) it is initializes
        client message header with correct default values and correct next
        sequence number.
        """
        default_args = {
            'seq': cls._curr_seq,
            'protoVer': '0.1',
            'id': 'id',
            'osId': 'os id',
            'appId': 'app id'
        }

        for (k, v) in default_args.iteritems():
            if not k in kwargs:
                kwargs[k] = v

        message = BiomioMessage(**kwargs)
        cls._curr_seq += 1
        return message

    @classmethod
    @nottest
    def setup_test(cls):
        """Default setup for test methods."""
        cls._curr_seq = 0

    @classmethod
    @nottest
    def teardown_test(cls):
        """Default teardown for test methods"""
        cls._curr_seq = 0
        if cls._ws:
            if cls._ws.open:
                cls._ws.close()
            cls._ws = None

    @classmethod
    @nottest
    def setup_test_with_handshake(cls):
        """Setup method for tests to perform handshake"""
        cls.setup_test()

        # Send hello message
        message = cls.create_next_message()
        message.set_client_hello_message(secret='secret')
        response = BiomioTest.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg_string(), 'hello', msg='Response does not contains hello message')

        # Send ack message
        message = cls.create_next_message()
        message.set_ack_message()
        BiomioTest.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)


class TestServerHandshake(BiomioTest):
    @with_setup(setup=BiomioTest.setup_test)
    def test_hello_server(self):
        message = self.create_next_message()
        message.set_client_hello_message(secret='secret')
        response = BiomioTest.send_message(message=message)
        eq_(response.msg_string(), 'hello', msg='Response does not contains hello message')

    @with_setup(setup=BiomioTest.setup_test, teardown=BiomioTest.teardown_test)
    def test_invalid_protocol_ver(self):
        invalid_proto_ver_string = '2.0'
        message = self.create_next_message(protoVer=invalid_proto_ver_string)
        message.set_client_hello_message(secret='secret')

        response = BiomioTest.send_message(message=message)
        eq_(response.msg_string(), 'bye', msg='Response does not contains bye message')

    @with_setup(setup=BiomioTest.setup_test_with_handshake, teardown=BiomioTest.teardown_test)
    def test_ack_message(self):
        pass

    @with_setup(setup=BiomioTest.setup_test_with_handshake, teardown=BiomioTest.teardown_test)
    def test_nop_message(self):
        # Send nop message
        message = self.create_next_message()
        message.set_nop_message()
        BiomioTest.send_message(websocket=self.get_curr_connection(), message=message, close_connection=True, wait_for_responce=False)

    @with_setup(setup=BiomioTest.setup_test_with_handshake, teardown=BiomioTest.teardown_test)
    def test_bye_message(self):
        # Send bye message
        message = self.create_next_message()
        message.set_bye_message()
        response = BiomioTest.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)

        eq_(response.msg_string(), 'bye', msg='Response does not contains bye message')

def main():
    pass

if __name__ == '__main__':
    main()