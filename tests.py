#!/usr/bin/env python

from websocket import create_connection, WebSocketTimeoutException
from biomio.protocol.message import BiomioMessageBuilder
from nose.tools import ok_, eq_, nottest, raises
from nose.plugins.attrib import attr
import time
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

    @attr('slow')
    def test_connection_timeout(self):
        websocket = self.new_connection(socket_timeout=60)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    @attr('slow')
    def test_connection_timer_restart(self):
        self.setup_test_with_handshake()
        message_timeout = 4
        for i in range(10):
            time.sleep(message_timeout)
            connection = self.get_curr_connection()
            ok_(connection.connected, msg='Socket is not in connected state')
            message = self.create_next_message(oid='nop')
            self.send_message(websocket=connection, message=message, close_connection=False, wait_for_responce=False)

        # Finish test, send bye message
        message = self.create_next_message(oid='bye')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)

    def test_session_ttl_not_zero(self):
        self.setup_test()
        message = self.create_next_message(oid='clientHello', secret='secret')
        response = self.send_message(message=message)
        ok_(not response.msg.ttl == 0, msg='Session TTL == 0')

    def test_session_expire(self):
        self.setup_test_with_handshake()
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)


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
        websocket = self.new_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.new_connection()
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

    def test_token_generation(self):
        message = self.create_next_message(oid='clientHello', secret='secret')
        first_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(first_response.header.token, msg='Server returns empty token string')

        second_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(second_response.header.token, msg='Server returns empty token string')
        ok_(not str(first_response.header.token) == str(second_response.header.token), msg='Token string sould be unique for every connection')

    def test_refresh_token_generation(self):
        message = self.create_next_message(oid='clientHello', secret='secret')
        first_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(first_response.msg.refreshToken, msg='Server returns empty refresh token string')

        second_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(second_response.msg.refreshToken, msg='Server returns empty refresh token string')
        ok_(not str(first_response.msg.refreshToken) == str(second_response.msg.refreshToken), msg='Refresh token string sould be unique for every connection')

class TestHandshakeState(BiomioTest):
    def setup(self):
        self.setup_test_with_hello()

    def teardown(self):
        self.teardown_test()

    def test_ack_message(self):
        # Send ack message
        message = self.create_next_message(oid='ack')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)

    @attr('slow')
    @raises(WebSocketTimeoutException)
    def test_ack_message_responce(self):
        message = self.create_next_message(oid='ack')
        # Send message and wait for responce,
        # server should not respond and close connection,
        # so WebsocketTimeoutException will be raised
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=True)

    def test_invalid_message(self):
        websocket = self.get_curr_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.get_curr_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_sequence(self):
        message = self.create_next_message(oid='ack')
        message.header.seq = 1
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')
        pass

    def test_invalid_protocol_ver(self):
        message = self.create_next_message(oid='ack')
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_any_other_message_received(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status message')

    def test_auth_message(self):
        message = self.create_next_message(oid='auth', key='authkey')
        websocket = self.get_curr_connection()
        self.send_message(websocket=websocket, message=message, wait_for_responce=False, close_connection=False)

    @attr('slow')
    @raises(WebSocketTimeoutException)
    def test_auth_message_responce(self):
        message = self.create_next_message(oid='auth', key='authkey')
        websocket = self.get_curr_connection()
        # Send message and wait for responce,
        # server should not respond and close connection,
        # so WebsocketTimeoutException will be raised
        self.send_message(websocket=websocket, message=message, close_connection=False)


class TestReadyState(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake()

    def teardown(self):
        self.teardown_test()

    def test_nop_message(self):
        # Send nop message
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)

    @attr('slow')
    @raises(WebSocketTimeoutException)
    def test_nop_message_responce(self):
        message = self.create_next_message(oid='nop')
        # Send message and wait for responce,
        # server should not respond and close connection,
        # so WebsocketTimeoutException will be raised
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=True)

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

    def test_invalid_message(self):
        websocket = self.get_curr_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.get_curr_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_invalid_protocol_ver(self):
        message = self.create_next_message(oid='nop')
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status string')

    def test_message_sequence_with_bye(self):
        # Handshake done (setup method)
        # Send few nop's in a row
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_responce=False)

        # Send 'bye' and check sequence number
        message = self.create_next_message(oid='bye')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status'), msg='Response does not contains status message')
        eq_(response.header.seq, int(message.header.seq) + 1, msg='Bye responce has invalid sequence number')

def main():
    pass

# Suppress logging in  python_jsonschema_objects module for bettter tests results readability
logger = logging.getLogger("python_jsonschema_objects.classbuilder")
logger.disabled = True
logger = logging.getLogger("python_jsonschema_objects")
logger.disabled = True



if __name__ == '__main__':
    main()