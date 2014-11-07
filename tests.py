#!/usr/bin/env python

from websocket import create_connection
from biomio.protocol.message import BiomioMessageBuilder
from nose.tools import ok_, eq_, nottest
import logging

class BiomioTest:
    def __init__(self):
        self._ws = None
        self._builder = None

    @nottest
    def new_connection(self, socket_timeout=5):
        socket = create_connection("ws://127.0.0.1:8080/websocket")
        socket.settimeout(socket_timeout)
        return socket

    @nottest
    def read_message(self, websocket):
        result = websocket.recv()
        responce = BiomioMessageBuilder.create_message_from_json(result)
        return responce

    @nottest
    def send_message(self, message, websocket=None, close_connection=True, wait_for_responce=True):

        if websocket is None:
            websocket = self.new_connection()

        websocket.send(message.serialize())

        responce = None
        if wait_for_responce:
            responce = self.read_message(websocket=websocket)

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
        message = self._builder.create_message(**kwargs)
        return message

    @nottest
    def setup_test(self):
        """Default setup for test methods."""
        self._builder = BiomioMessageBuilder(oid='clientHeader', seq=0, protoVer='1.0', id='id', osId='os id', appId='app Id')

    @nottest
    def teardown_test(self):
        """Default teardown for test methods"""
        if self._ws:
            if self._ws.connected:
                self._ws.close()
        self._ws = None
        self._builder = None

    @nottest
    def setup_test_with_hello(self):
        self.setup_test()

        # Send hello message
        message = self.create_next_message(oid='clientHello', secret='secret')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains helloServer message')
        eq_(response.header.seq, int(message.header.seq) + 1,
            'Responce sequence number is invalid (expected: %d, got: %d)' % (int(message.header.seq) + 1, response.header.seq))

    @nottest
    def setup_test_with_handshake(self):
        """Setup method for tests to perform handshake"""
        self.setup_test_with_hello()

        # Send ack message
        message = self.create_next_message(oid='ack')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)

class TestTimeouts(BiomioTest):
    def setup(self):
        self.setup_test()

    def teardown(self):
        self.teardown_test()

    def test_connection_timeout(self):
        websocket = self.new_connection(socket_timeout=60)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

class TestConnectedState(BiomioTest):
    def setup(self):
        self.setup_test()

    def teardown(self):
        self.teardown_test()

    def test_hello_server(self):
        message = self.create_next_message(oid='clientHello', secret='secret')
        response = self.send_message(message=message)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains serverHello message')

    def test_invalid_message(self):
        websocket = self.new_connection(socket_timeout=60)
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.new_connection(socket_timeout=60)
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_sequence(self):
        message = self.create_next_message(oid='clientHello', secret='secret')
        message.header.seq = 1
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')
        pass

    def test_invalid_protocol_ver(self):
        message = self.create_next_message(oid='clientHello', secret='secret')
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_nop_message_sent(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

class TestHandshakeState(BiomioTest):
    def setup(self):
        self.setup_test_with_hello()

    def teardown(self):
        self.teardown_test()

    def test_ack_message(self):
        # Send ack message
        message = self.create_next_message(oid='ack')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)

    def test_any_other_message_received(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status message')

class TestReadyState(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake()

    def teardown(self):
        self.teardown_test()

    def test_nop_message(self):
        # Send nop message
        message = self.create_next_message(oid='nop')
        #TODO: add some test for existing connection
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)

    def test_bye_message(self):
        # Send bye message
        message = self.create_next_message(oid='bye')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status message')

    def test_invalid_sequence(self):
        message = self.create_next_message(oid='nop')
        message.header.seq = 1
        socket = self.get_curr_connection()
        response = self.send_message(websocket=socket, message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status message')

def main():
    pass

logger = logging.getLogger("python_jsonschema_objects.classbuilder")
logger.disabled = True
logger = logging.getLogger("python_jsonschema_objects")
logger.disabled = True

if __name__ == '__main__':
    main()