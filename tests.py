#!/usr/bin/env python
import random

from ssl import SSLError
import string
from websocket import create_connection, WebSocketTimeoutException, WebSocket

from biomio.protocol.message import BiomioMessageBuilder
from biomio.protocol.settings import settings
from biomio.protocol.crypt import Crypto

from nose.tools import ok_, eq_, nottest, raises
from nose.plugins.attrib import attr

import time
import logging
from hashlib import sha1
from os import urandom
import threading
from itertools import izip


ssl_options = {
    "ca_certs": "server.pem"
}


APP_TEST_ID = 'test_app_id'
USER_TEST_EMAIL = 'test@mail.com'
TEST_PUB_PGP_KEY = 'test_pub_pgp_key'

class BiomioTest:
    _registered_key = None
    _registered_user_id = None
    _registered_app_id = None

    @classmethod
    def set_registered_user_id(cls):
        cls._registered_user_id = None

    @classmethod
    def init_db_test_data(cls, app_id=None):
        from biomio.protocol.data_stores.user_data_store import UserDataStore
        from biomio.protocol.data_stores.application_data_store import ApplicationDataStore
        from biomio.protocol.data_stores.email_data_store import EmailDataStore
        # from biomio.protocol.data_stores.base_data_store import BaseDataStore

        key, pub_key = Crypto.generate_keypair()

        UserDataStore.instance().store_data(1)
        store_keywords = {ApplicationDataStore.APP_TYPE_ATTR: 'extension',
                          ApplicationDataStore.PUBLIC_KEY_ATTR: str(pub_key),
                          ApplicationDataStore.USER_ATTR: 1}

        if app_id is None:
            app_id = APP_TEST_ID
        ApplicationDataStore.instance().store_data(app_id, **store_keywords)

        store_keywords = {
            EmailDataStore.PASS_PHRASE_ATTR: 'test_pass_phrase',
            EmailDataStore.PUBLIC_PGP_KEY_ATTR: 'test_pub_pgp_key',
            EmailDataStore.PRIVATE_PGP_KEY_ATTR: None,
            EmailDataStore.USER_ATTR: 1
        }
        EmailDataStore.instance().store_data(USER_TEST_EMAIL, **store_keywords)
        # BaseDataStore.instance().delete_custom_lru_redis_data(UserDataStore.get_data_key(1))
        # BaseDataStore.instance().delete_custom_lru_redis_data(ApplicationDataStore.get_data_key('test_app_id'))
        # BaseDataStore.instance().delete_custom_lru_redis_data(EmailDataStore.get_data_key(USER_TEST_EMAIL))
        BiomioTest._registered_key = key
        BiomioTest._registered_app_id = app_id

    def __init__(self):
        self._ws = None
        self._builder = None
        self.last_server_message = None
        self.current_session_token = None
        self.session_refresh_token = None

    @nottest
    def new_connection(self, socket_timeout=5):
        # socket = WebSocket()
        socket = WebSocket(sslopt=ssl_options)
        # socket.connect("wss://gb.vakoms.com:{port}/websocket".format(port=settings.port))
        socket.connect("wss://{host}:{port}/websocket".format(host=settings.host, port=settings.port))
        socket.settimeout(socket_timeout)
        return socket

    @nottest
    def read_message(self, websocket):
        result = websocket.recv()
        response = BiomioMessageBuilder.create_message_from_json(result)
        self.last_server_message = response
        if response and not str(response.header.token) == self.current_session_token:
            self.set_session_token(str(response.header.token))
        if response and response.msg.oid == 'serverHello':
            self.session_refresh_token = str(response.msg.refreshToken)
        return response

    @nottest
    def send_message(self, message, websocket=None, close_connection=True, wait_for_response=True):

        if websocket is None:
            websocket = self.new_connection()

        websocket.send(message.serialize())

        response = None
        if wait_for_response:
            response = self.read_message(websocket=websocket)
            self.last_server_message = response

        if close_connection:
            websocket.close()

        return response

    @nottest
    def set_session_token(self, token):
        if self._builder:
            self._builder.set_header(token=token)
            self.current_session_token = token
        else:
            raise 'Run BiomioTest.setup_test() first to prepare for communication with server'

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
        self._builder = BiomioMessageBuilder(oid='clientHeader', seq=0, protoVer='1.0', osId='os id',
                                             devId='devid', appId=APP_TEST_ID, appType='extension')
        self.last_server_message = None
        self.session_refresh_token = None
        self.current_session_token = None

    @nottest
    def teardown_test(self):
        """Default teardown for test methods"""
        if self._ws:
            if self._ws.connected:
                self._ws.close()
        self._ws = None
        self._builder = None
        self.last_server_message = None
        self.session_refresh_token = None
        self.current_session_token = None

    @nottest
    def setup_test_with_hello(self, secret=None, is_registration_required=True):
        self.setup_test()

        # Send hello message
        params = {
            'oid': 'clientHello'
        }

        if is_registration_required and not secret:
            self.check_app_registered()
            self._builder.set_header(id=BiomioTest._registered_user_id)
            self._builder.set_header(appId=BiomioTest._registered_app_id)
        elif secret:
            params['secret'] = secret

        message = self.create_next_message(**params)
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains helloServer message')
        eq_(response.header.seq, int(message.header.seq) + 1,
            'Response sequence number is invalid (expected: %d, got: %d)' % (
                int(message.header.seq) + 1, response.header.seq))

    @nottest
    def setup_test_with_handshake(self, secret=None, is_registration_required=False):
        """Setup method for tests to perform handshake"""
        if BiomioTest._registered_key is None or BiomioTest._registered_app_id is None:
            BiomioTest.init_db_test_data()

        self.setup_test_with_hello(secret=secret, is_registration_required=is_registration_required)

        if secret:
            # Send ack message during registration
            message = self.create_next_message(oid='ack')
        else:
            digest = self.get_digest_for_next_message()
            message = self.create_next_message(oid='auth', key=digest)

        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=False)

    @nottest
    def setup_with_session_restore(self, secret=None):
        """Performs handshake and closes connection without 'bye',
        so we could restore connection further"""
        # Perform handshake
        self.setup_test_with_handshake(secret=secret, is_registration_required=False)

        # Close websocket on client side,
        # without sending bye message,
        # so we could restore session further
        websocket = self.get_curr_connection()
        websocket.close()

    @nottest
    def get_digest_for_next_message(self):
        header_str = self._builder.header_string()
        return Crypto.create_digest(data=header_str, key=BiomioTest._registered_key)

    @nottest
    def check_app_registered(self, id_to_create=None, app_id_prefix='extension'):
        if not self._registered_key or id_to_create is not None:
            # id_to_create = '1amxHFtymG7tIHfj96zbzgbTY'
            self._builder.set_header(id=sha1(urandom(64)).hexdigest() if id_to_create is None else id_to_create,
                                     appId='%s_%s' % (app_id_prefix, str(sha1(urandom(64)).hexdigest())))
            message = self.create_next_message(oid='clientHello', secret='secret')
            response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                         wait_for_response=True)
            message = self.create_next_message(oid='ack')
            self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                              wait_for_response=False)
            message = self.create_next_message(oid='bye')
            self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                              wait_for_response=False)
            BiomioTest._registered_key = str(response.msg.key)
            BiomioTest._registered_user_id = str(message.header.id)
            BiomioTest._registered_app_id = str(message.header.appId)

            self.teardown_test()
            self.setup_test()

    @nottest
    def setup_test_for_for_new_id(self, app_id=None):
        self.setup_test()
        if app_id is None:
            app_id = sha1(urandom(64)).hexdigest()
        self._builder.set_header(appId=app_id)


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
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    @attr('slow')
    def test_connection_timer_restart(self):
        self.setup_test_with_handshake()

        message_timeout = 3  # Send a message every 3 seconds
        message_count = (settings.connection_timeout / message_timeout) + 1

        for i in range(message_count):
            time.sleep(message_timeout)
            connection = self.get_curr_connection()
            ok_(connection.connected, msg='Socket is not in connected state')
            message = self.create_next_message(oid='nop')
            self.send_message(websocket=connection, message=message, close_connection=False, wait_for_response=False)

        # Finish test, send bye message
        message = self.create_next_message(oid='bye')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)

    def test_session_ttl_not_zero(self):
        self.setup_test()
        message = self.create_next_message(oid='clientHello')
        response = self.send_message(message=message)
        ok_(not response.msg.ttl == 0, msg='Session TTL == 0')

    @attr('slow')
    def test_session_expire(self):

        message_timeout = settings.connection_timeout / 2  # Send a message every 3 seconds
        message_count = (settings.session_ttl / message_timeout) + 2

        # We will wait for message from server,
        # so we set timeout for blocking read socket operation to
        # message_timeout value (we will use that timeout
        # as a delay between messages)
        self.setup_test_with_handshake()

        expired = False
        for i in range(message_count):
            # Need to send nop messages to continue connection ttl,
            # but messages will be sent with the same session token, so
            # after a while session will be expired
            message = self.create_next_message(oid='nop')
            time.sleep(message_timeout)
            try:
                response = self.send_message(websocket=self.get_curr_connection(), message=message,
                                             close_connection=False, wait_for_response=True)
                if str(response.msg.oid) == 'bye':
                    expired = True
                    break
            except Exception, e:
                expired = True
                break

        ok_(expired, msg='Session does not expired %s' % self.current_session_token)


class TestRegistration(BiomioTest):
    def setup(self):
        self.setup_test()

    def teardown(self):
        self.teardown_test()

    def test_registration(self):
        self.setup_test_for_for_new_id()
        message = self.create_next_message(oid='clientHello', secret='secret')
        response = self.send_message(message=message)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains serverHello message')
        ok_(hasattr(response.msg, 'key') and response.msg.key, msg="Responce does not contains generated private key.")

    def test_ack_message(self):
        # Send ack message
        message = self.create_next_message(oid='clientHello', secret='secret')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        message = self.create_next_message(oid='ack')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=False)

    @attr('slow')
    @raises(WebSocketTimeoutException, SSLError)
    def test_ack_message_response(self):
        self.setup_test_for_for_new_id()
        message = self.create_next_message(oid='clientHello', secret='secret')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        message = self.create_next_message(oid='ack')
        # Send message and wait for response,
        # server should not respond and close connection,
        # so WebsocketTimeoutException will be raised
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=True)



class TestConnectedState(BiomioTest):
    def setup(self):
        self.setup_test()

    def teardown(self):
        self.teardown_test()

    def test_hello_server(self):
        message = self.create_next_message(oid='clientHello')
        response = self.send_message(message=message)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains serverHello message')

    def test_invalid_message(self):
        websocket = self.new_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.new_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_sequence(self):
        message = self.create_next_message(oid='clientHello')
        message.header.seq = 1
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')
        pass

    def test_invalid_protocol_ver(self):
        message = self.create_next_message(oid='clientHello')
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_nop_message_sent(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_token_generation(self):
        message = self.create_next_message(oid='clientHello')
        first_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(first_response.header.token, msg='Server returns empty token string')

        second_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(second_response.header.token, msg='Server returns empty token string')
        ok_(not str(first_response.header.token) == str(second_response.header.token),
            msg='Token string sould be unique for every connection')

    def test_refresh_tokens_unique(self):
        message = self.create_next_message(oid='clientHello')
        first_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(first_response.msg.refreshToken, msg='Server returns empty refresh token string')

        second_response = self.send_message(message=message, close_connection=True, websocket=self.new_connection())
        ok_(second_response.msg.refreshToken, msg='Server returns empty refresh token string')
        ok_(not str(first_response.msg.refreshToken) == str(second_response.msg.refreshToken),
            msg='Refresh token string sould be unique for every connection')

    @attr('slow')
    def test_session_restore(self):
        self.setup_with_session_restore()
        # token = str(self.session_refresh_token)
        #
        # self.teardown_test()
        # self.setup_test()
        #
        # self.set_session_token(token)
        # message = self.create_next_message(oid='nop')
        # try:
        #     self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
        #                       wait_for_response=True)
        # except (WebSocketTimeoutException, SSLError):
        #     pass
        #
        # time.sleep(settings.connection_timeout / 2)
        # message = self.create_next_message(oid='bye')
        # response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        # eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')

    def test_session_restore_error_with_invalid_token(self):
        self.setup_with_session_restore()

        self.teardown_test()
        self.setup_test()

        invalid_token = 'invalid_token_123'
        self.set_session_token(invalid_token)
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_inappropriate_regular_handshake(self):
        self.setup_with_session_restore()

        self.teardown_test()
        self.setup_test()

        invalid_id = sha1(urandom(64)).hexdigest()
        self._builder.set_header(id=invalid_id)
        message = self.create_next_message(oid='clientHello')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_inappropriate_registration_handshake(self):
        self.setup_with_session_restore()

        self.teardown_test()
        self.setup_test()

        message = self.create_next_message(oid='clientHello', secret='secret')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')


class TestHandshakeState(BiomioTest):
    def setup(self):
        self.setup_test_with_hello()

    def teardown(self):
        self.teardown_test()

    def test_invalid_message(self):
        websocket = self.get_curr_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.get_curr_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_sequence(self):
        message = self.create_next_message(oid='ack')
        message.header.seq = 1
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')
        pass

    def test_invalid_protocol_ver(self):
        message = self.create_next_message(oid='ack')
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_any_other_message_received(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status message')

    def test_auth_message(self):
        message = self.create_next_message(oid='auth', key=self.get_digest_for_next_message())
        websocket = self.get_curr_connection()
        self.send_message(websocket=websocket, message=message, wait_for_response=False, close_connection=False)

    @attr('slow')
    @raises(WebSocketTimeoutException, SSLError)
    def test_auth_message_response(self):
        message = self.create_next_message(oid='auth', key=self.get_digest_for_next_message())
        websocket = self.get_curr_connection()
        # Send message and wait for response,
        # server should not respond and close connection,
        # so WebsocketTimeoutException will be raised
        response = self.send_message(websocket=websocket, message=message, close_connection=False,
                                     wait_for_response=True)


class TestReadyState(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake()

    def teardown(self):
        self.teardown_test()

    def test_nop_message(self):
        # Send nop message
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=False)

    def test_nop_message_response(self):
        message = self.create_next_message(oid='nop')
        # Send message and wait for response,
        # server should not respond and close connection,
        # so WebsocketTimeoutException will be raised
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        eq_(response.msg.oid, 'nop', msg='Response does not contains nop message')

    def test_bye_message(self):
        # Send bye message
        message = self.create_next_message(oid='bye')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')

    def test_invalid_sequence(self):
        message = self.create_next_message(oid='nop')
        message.header.seq = 1
        socket = self.get_curr_connection()
        response = self.send_message(websocket=socket, message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status message')

    def test_invalid_message(self):
        websocket = self.get_curr_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_json(self):
        websocket = self.get_curr_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_protocol_ver(self):
        message = self.create_next_message(oid='nop')
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_message_sequence_with_bye(self):
        # Handshake done (setup method)
        # Send few nop's in a row
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=True)
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=True)
        message = self.create_next_message(oid='nop')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=True)

        # Send 'bye' and check sequence number
        message = self.create_next_message(oid='bye')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        eq_(response.header.seq, int(message.header.seq) + 1, msg='Bye response has invalid sequence number')

    @attr('slow')
    def test_session_refresh(self):
        message_timeout = settings.connection_timeout / 2
        message_count = (settings.session_ttl / message_timeout) - 1

        old_session_token = self.current_session_token

        expired = False
        for i in range(message_count):
            # Need to send nop messages to continue connection ttl,
            # but messages will be sent with the same session token, so
            # after a while session will be expired
            message = self.create_next_message(oid='nop')
            time.sleep(message_timeout)
            try:
                self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
            except Exception, e:
                expired = True
                break

        message = self.create_next_message(oid='nop')
        message.header.token = self.session_refresh_token
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)

        for i in range(message_count):
            # Need to send nop messages to continue connection ttl,
            # but messages will be sent with the same session token, so
            # after a while session will be expired
            message = self.create_next_message(oid='nop')
            time.sleep(message_timeout)
            try:
                self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
            except Exception, e:
                expired = True
                break

        ok_(not expired, msg='Session expired instead of refresh')
        ok_(not old_session_token == self.current_session_token,
            msg='New session token not generated (old one present).')

@nottest
def get_rpc_msg_field(message, key):
    for k,v in izip(list(message.msg.data.keys), list(message.msg.data.values)):
        if str(k) == key:
            return str(v)


class TestRpcCalls(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake()#is_registration_required=True)

    def teardown(self):
        self.teardown_test()

    def test_rpc_call(self):
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func',
                                           onBehalfOf='test@test.com',
                                           data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status: %s' % response.status)

    def test_rpc_ns_list(self):
        message = self.create_next_message(oid='rpcEnumNsReq')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status: %s' % response.status)

    @staticmethod
    @nottest
    def probe_job(sample, probe_type="touchIdSamples"):
        test_obj = BiomioTest()
        app_id = 'probe_id'
        test_obj.setup_test_for_for_new_id(app_id=app_id)
        test_obj.init_db_test_data(app_id=app_id)
        test_obj._builder.set_header(appType='probe', appId=app_id)

        # CLIENT HELLO ->
        message = test_obj.create_next_message(oid='clientHello')
        response = test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message, close_connection=False, wait_for_response=True)

        # # RESOURCES ->
        # message = test_obj.create_next_message(oid='resources', data=[{"rType": "video", "rProperties": "1500x1000"},
        #     {"rType": "fp-scanner", "rProperties": "true"}, {"rType": "mic", "rProperties": "true"}])
        # SERVER HELLO <-
        # response = test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message, close_connection=False, wait_for_response=True)

        # # ACK ->
        # message = test_obj.create_next_message(oid='ack')
        # test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message, close_connection=False,
        #                   wait_for_response=False)
        message = test_obj.create_next_message(oid='auth', key=test_obj.get_digest_for_next_message())
        test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=False)


        message_timeout = settings.connection_timeout / 2  # Send a message every 3 seconds
        max_message_count = 10
        rpc_responce_message = None
        for i in range(max_message_count):
            try:
                message = test_obj.read_message(websocket=test_obj.get_curr_connection())

                # TRY <-
                if message and message.msg and str(message.msg.oid) == 'try':
                    # PROBE ->
                    probe_msg = test_obj.create_next_message(oid='probe', probeId=0,
                                                             probeData={"oid": probe_type, "samples": [sample]})

                    test_obj.send_message(websocket=test_obj.get_curr_connection(), message=probe_msg,
                                                 close_connection=False, wait_for_response=False)
                    break
            except Exception, e:
                print e
                pass

            message = test_obj.create_next_message(oid='nop')
            message.header.token = test_obj.session_refresh_token
            try:
                # NOP ->
                # NOP <-
                response = test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message,
                                             close_connection=False, wait_for_response=True)
                ok_(str(response.msg.oid) == 'nop', msg='No responce on nop message')
            except Exception, e:
                pass

        message = test_obj.create_next_message(oid='bye')
        # BYE ->
        # BYE <-
        response = test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')

    @staticmethod
    @nottest
    def is_rpc_response_status(message, status):
        return message and message.msg and str(message.msg.oid) == 'rpcResp' and str(message.msg.rpcStatus) == status

    @staticmethod
    @nottest
    def keep_connection_and_communicate(biomio_test, message_callback=None, max_message_count=10):
        class BiomioBye(Exception):
            pass

        def close_connection_callback():
            raise BiomioBye

        def process_message(biomio_test, message_callback, response):
            if message_callback:
                message = message_callback(response, close_connection_callback)
                if message:
                    biomio_test.send_message(websocket=biomio_test.get_curr_connection(), message=message, close_connection=False,
                        wait_for_response=True)

        is_quit = False
        for i in range(max_message_count):
            try:
                response = biomio_test.read_message(websocket=biomio_test.get_curr_connection())
                process_message(biomio_test, message_callback, response)

            except BiomioBye, e:
                is_quit = True
                break
            except Exception, e:
                if not e == WebSocketTimeoutException:
                    print e

            nop_message = biomio_test.create_next_message(oid='nop')
            nop_message.header.token = biomio_test.session_refresh_token

            try:
                response = biomio_test.send_message(websocket=biomio_test.get_curr_connection(), message=nop_message,
                    close_connection=False, wait_for_response=True)
                process_message(biomio_test, message_callback, response)

                ok_(str(response.msg.oid) == 'nop', msg='No responce on nop message')
            except BiomioBye, e:
                is_quit = True
                break
            except Exception, e:
                print e

        return is_quit

    @attr('slow')
    def test_rpc_with_auth(self):

        # results = {'rpcResp': None }
        #
        # def on_message(message, close_connection_callback):
        #     if str(message.msg.oid) == 'nop':
        #         print "NOP"
        #     elif str(message.msg.oid) == 'rpcResp':
        #         if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
        #                 or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
        #             results['rpcResp'] = message
        #             close_connection_callback()
        #
        # message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
        #     data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        # self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
        #     wait_for_response=True)

        # Separate thread with connection for
        t = threading.Thread(target=TestRpcCalls.probe_job, kwargs={'sample': 'True'})
        t.start()
        t.join()

        time.sleep(1)

        # self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)
        # rpcResp = results['rpcResp']
        # ok_(rpcResp is not None, msg='No RPC response on auth.')
        # eq_(str(rpcResp.msg.rpcStatus), 'complete', msg='RPC authentication failed, but result is positive')

    @nottest
    def photo_data(self, photo_path):
        from binascii import b2a_base64
        data = None
        with open(photo_path, "rb") as f:
            data = b2a_base64(f.read())
        return data

    @attr('slow')
    def test_rpc_with_photo(self):

        #TODO: refactor test
        results = {'rpcResp': None }

        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "NOP"
            elif str(message.msg.oid) == 'rpcResp':
                if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
                        or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
                    results['rpcResp'] = message
                    close_connection_callback()

        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
            data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
            wait_for_response=True)

        # Separate thread with connection for
        sample = self.photo_data(photo_path='/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.pgm')
        t = threading.Thread(target=TestRpcCalls.probe_job, kwargs={'sample': sample, 'probe_type': 'imageSamples'})
        t.start()

        time.sleep(1)

        self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)
        rpcResp = results['rpcResp']
        ok_(rpcResp is not None, msg='No RPC response on auth.')
        eq_(str(rpcResp.msg.rpcStatus), 'complete', msg='RPC authentication failed, but result is positive')


    @attr('slow')
    def test_rpc_with_auth_failed(self):

        results = {'rpcResp': None }

        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "NOP"
            elif str(message.msg.oid) == 'rpcResp':
                if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
                        or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
                    results['rpcResp'] = message
                    close_connection_callback()

        # Separate thread with connection for
        t = threading.Thread(target=TestRpcCalls.probe_job, args=(False,))
        t.start()

        time.sleep(1)

        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
            data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
            wait_for_response=True)

        self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)
        rpcResp = results['rpcResp']
        ok_(rpcResp is not None, msg='No RPC response on auth.')
        eq_(str(rpcResp.msg.rpcStatus), 'fail', msg='RPC authentication succeeded, but result is negative')


    @attr('slow')
    def test_rpc_with_auth_probe_first(self):
        results = {'rpcResp': None }

        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "NOP"
            elif str(message.msg.oid) == 'rpcResp':
                if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
                        or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
                    results['rpcResp'] = message
                    close_connection_callback()

        # Separate thread with connection for
        t = threading.Thread(target=TestRpcCalls.probe_job)
        t.start()

        time.sleep(1)

        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
            data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
            wait_for_response=True)

        self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)
        rpcResp = results['rpcResp']
        ok_(rpcResp is not None, msg='No RPC response on auth.')
        eq_(str(rpcResp.msg.rpcStatus), 'complete', msg='RPC authentication failed, but result is positive')



    def test_rpc_pass_phrase_keys_generation(self):
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin',
                                           call='get_pass_phrase',
                                           data={'keys': ['email'], 'values': ['test@mail.com']})
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status %s' % response.status)
        ok_('private_pgp_key' in response.msg.data.keys, msg='Response does not contain private pgp key.')

    def test_rpc_get_pass_phrase(self):
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin',
                                           call='get_pass_phrase',
                                           onBehalfOf='test@mail.com',
                                           data={'keys': ['email'], 'values': ['test@mail.com']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=True)
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin',
                                           call='get_pass_phrase',
                                           onBehalfOf='test@mail.com',
                                           data={'keys': ['email'], 'values': ['test@mail.com']})
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status %s' % response.status)
        ok_('private_pgp_key' not in response.msg.data.keys, msg='Response contains private pgp key.')
        ok_('pass_phrase' in response.msg.data.keys, msg='Response does not contain pass phrase.')

    @attr('slow')
    def test_rpc_get_users_pgp_keys_generation(self):
        fake_email = ['%s@mail.com' % ''.join(random.choice(string.lowercase) for _ in range(10)) for x in range(2)]
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin',
                                           call='get_users_public_pgp_keys',
                                           data={'keys': ['emails'], 'values': [','.join(fake_email)]})
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status %s' % response.status)
        ok_('public_pgp_keys' in response.msg.data.keys, msg='Response does not contain public pgp key.')

    def test_rpc_get_users_public_pgp_keys(self):
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin',
                                           call='get_users_public_pgp_keys',
                                           data={'keys': ['emails'], 'values': ['test@mail.com, test1@mail.com']})
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                                     wait_for_response=True)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status %s' % response.status)
        ok_('public_pgp_keys' in response.msg.data.keys, msg='Response does not contain public pgp key.')


class TestProbes(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake(is_registration_required=True)

    def teardown(self):
        self.teardown_test()

    def test_send_resources(self):
        self.setup_test_for_for_new_id()
        self._builder.set_header(appId='probe_%s' % (sha1(urandom(64)).hexdigest()))

        message = self.create_next_message(oid='clientHello', secret='secret')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_response=False)

        message = self.create_next_message(oid='resources', data=[{"rType": "video", "rProperties": "1500x1000"},
            {"rType": "fp-scanner", "rProperties": "true"}, {"rType": "mic", "rProperties": "true"}])
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False, wait_for_response=True)

        message = self.create_next_message(oid='ack')
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
                          wait_for_response=False)

        # response = self.read_message(websocket=self.get_curr_connection())

        # message = self.create_next_message(oid='nop')
        # response = self.send_message(websocket=self.get_curr_connection(), message=message,
        #                              close_connection=False, wait_for_response=True)
        # eq_(response.msg.oid, 'serverHello', msg='Response does not contains serverHello message')
        # ok_(hasattr(response.msg, 'key') and response.msg.key, msg="Responce does not contains generated private key.")


def main():
    pass

# Suppress logging in  python_jsonschema_objects module for bettter tests results readability
logger = logging.getLogger("python_jsonschema_objects.classbuilder")
logger.disabled = True
logger = logging.getLogger("biomio.protocol.data_stores.storage_jobs_processor")
logger.disabled = True
logger = logging.getLogger("python_jsonschema_objects")
logger.disabled = True

if __name__ == '__main__':
    main()
