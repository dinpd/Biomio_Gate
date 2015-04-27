#!/usr/bin/env python

from nose.tools import ok_, eq_, nottest, raises
from nose.plugins.attrib import attr

from websocket import WebSocketTimeoutException, WebSocket
from ssl import SSLError
import time
from itertools import izip
import threading
from binascii import b2a_base64

import ssl
import urllib2

from biomio.protocol.message import BiomioMessageBuilder
from biomio.protocol.settings import settings
from biomio.protocol.crypt import Crypto

from setup_default_user_data import probe_app_id, probe_app_type, probe_key, probe_pub_key, \
    extension_app_id, extension_app_type, extension_key, extension_pub_key

import logging


DEFAULT_SOCKET_TIMEOUT = 5  # seconds
SSL_OPTIONS = {
    "ca_certs": "server.pem"
}
FR_TRAINING_IMG_FOLDER_PATH = '/home/alexchmykhalo/ios_screens/algorithms_learning/'
FR_TRAINING_IMG_NAMES = [
    'yaleB11_P00A+000E+00.pgm', 'yaleB11_P00A+000E+20.pgm', 'yaleB11_P00A+000E+45.pgm',
    'yaleB11_P00A+000E-20.pgm', 'yaleB11_P00A+000E-35.pgm',
    'yaleB11_P00A+005E+10.pgm', 'yaleB11_P00A+005E-10.pgm', 'yaleB11_P00A+010E-20.pgm',
    'yaleB11_P00A+015E+20.pgm', 'yaleB11_P00A+020E+10.pgm'
    ]

# Set convenient for testing values
settings.connection_timeout = 15
settings.session_ttl = 25

@nottest
def get_rpc_msg_field(message, key):
    for k, v in izip(list(message.msg.data.keys), list(message.msg.data.values)):
        if str(k) == key:
            return str(v)


class BiomioTest:
    def __init__(self):
        self._ws = None
        self._builder = None
        self.last_server_message = None
        self.current_session_token = None
        self.session_refresh_token = None
        self._app_id = None
        self._app_type = None
        self._handshake_key = None

    @nottest
    def setup_test(self, app_id, app_type, os_id='', dev_id='', key=None, secret=None):
        """
        Default setup for test methods.
        :param app_id: Application id.
        :param app_type: Application type (e.g. "extension", "probe")
        :param key: Private key, used for digest generation.
        :param os_id: OS id (optional)
        :param dev_id: Device id (optional)
        """
        self._builder = BiomioMessageBuilder(oid='clientHeader', seq=0, protoVer='1.0', osId=os_id,
                                             devId=dev_id, appId=app_id, appType=app_type)
        self.last_server_message = None
        self.session_refresh_token = None
        self.current_session_token = None
        self._app_id = app_id
        self._app_type = app_type
        self._handshake_key = key

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
        self._app_id = None
        self._app_type = None
        self._handshake_key = None

    @nottest
    def set_session_token(self, token):
        """
        Sets session token for BiomioTest object. Token will be used in further
        communication with server. Method raises exception if appropriate setup method
        was not called before.
        :param token: Session token.
        """
        if self._builder:
            self._builder.set_header(token=token)
            self.current_session_token = token
        else:
            raise 'Run BiomioTest.setup_test() first to prepare for communication with server'


    @staticmethod
    @nottest
    def new_connection(socket_timeout=DEFAULT_SOCKET_TIMEOUT):
        """
        Creates connection and returns socket that could be used for further
        communication with server.
        :param: socket_timeout Timeout for socket operations.
        :return: WebSocket connected to server.
        """
        socket = WebSocket(sslopt=SSL_OPTIONS)
        socket.connect("wss://{host}:{port}/websocket".format(host=settings.host, port=settings.port))
        socket.settimeout(socket_timeout)
        return socket

    @nottest
    def get_curr_connection(self):
        """
        Helper method to get current connected websocket object.
        Could be used to get current websocket after some setup methods
        (e.g. setup_test_with_handshake) that creates connection with server
        and send messages to prepare test case.
        """
        if not self._ws:
            self._ws = self.new_connection()
        return self._ws

    @nottest
    def create_next_message(self, **kwargs):
        """
        Helper method to create next new client message.
        Test object should be initialized with appropriate setup method
        before using this method. Method takes values for new msg fields as
        named parameters.
        """
        message = self._builder.create_message(**kwargs)
        return message

    @nottest
    def read_message(self, websocket):
        """
        Reads message from given websocket and memorizes session and refresh tokens
        as well as the last received message. Memorized tokens will be used in further
        communication with server.
        :param: Websocket connected to server to listen.
        :return: BIOMIO message responce object.
        """
        response_str = websocket.recv()
        response = BiomioMessageBuilder.create_message_from_json(response_str)

        self.last_server_message = response
        if response and not str(response.header.token) == self.current_session_token:
            self.set_session_token(str(response.header.token))
        if response and response.msg.oid == 'serverHello':
            self.session_refresh_token = str(response.msg.refreshToken)

        return response

    @nottest
    def send_message(self, message, websocket=None, wait_for_response=True, close_connection=False):
        """
        Sends given message to server using given connected to server websocket. This method also could be used
        to listen to server responce.
        :param: message BIOMIO message object.
        :param: websocket Connected to server WebSocket object. If not specified - new connection will be established.
        :param: wait_for_response If True method will wait for responce and return BIOMIO message response object.
        :param: close_connection Closes connection after method execution if True; leaves connection open otherwise.
        :return: WebSocket connected to server.
        """
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
    def setup_test_with_hello(self, **kwargs):
        """
        Setup test case and send "clientHello" message and leaves connection in touch.
        Method also check respond got from server. Method takes same parameters as setup() method.
        """
        self.setup_test(**kwargs)

        # Send hello message
        message = self.create_next_message(oid='clientHello')
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains helloServer message')
        eq_(response.header.seq, int(message.header.seq) + 1,
            'Response sequence number is invalid (expected: %d, got: %d)' % (
                int(message.header.seq) + 1, response.header.seq))

    @nottest
    def get_digest_for_next_message(self):
        """
        Creates digest for next message.
        """
        header_str = self._builder.header_string()
        return Crypto.create_digest(data=header_str, key=self._handshake_key)

    @nottest
    def setup_test_with_handshake(self, **kwargs):
        """
        Setup method for tests that performs handshake and leaves connection in touch.
        Method takes same parameters as setup_test_with_hello() method.
        """
        self.setup_test_with_hello(**kwargs)

        digest = self.get_digest_for_next_message()
        message = self.create_next_message(oid='auth', key=digest)
        self.send_message(websocket=self.get_curr_connection(), message=message, wait_for_response=False)

    @staticmethod
    @nottest
    def probe_job(samples, probe_type="touchIdSamples"):
        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "probe: NOP"
            elif str(message.msg.oid) == 'try':
                print "probe: TRY"
                sample_num = int(message.msg.resource[0].samples)
                samples_to_sent = samples[:sample_num]
                probe_msg = test_obj.create_next_message(oid='probe', probeId=0,
                                         probeData={"oid": probe_type, "samples": samples_to_sent})

                test_obj.send_message(websocket=test_obj.get_curr_connection(), message=probe_msg,
                                             close_connection=False, wait_for_response=False)
                close_connection_callback()

        test_obj = BiomioTest()
        test_obj.setup_test_with_handshake(app_id=probe_app_id, app_type=probe_app_type, key=probe_key)
        TestRpcCalls.keep_connection_and_communicate(biomio_test=test_obj, message_callback=on_message)

        # BYE ->
        # BYE <-
        message = test_obj.create_next_message(oid='bye')
        response = test_obj.send_message(websocket=test_obj.get_curr_connection(), message=message)
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
                if e is not WebSocketTimeoutException and e is not SSLError:
                    print e

            nop_message = biomio_test.create_next_message(oid='nop')
            nop_message.header.token = biomio_test.session_refresh_token

            try:
                response = biomio_test.send_message(websocket=biomio_test.get_curr_connection(), message=nop_message)
                process_message(biomio_test, message_callback, response)

                ok_(str(response.msg.oid) == 'nop', msg='No responce on nop message')
            except BiomioBye, e:
                is_quit = True
                break
            except Exception, e:
                if e is not WebSocketTimeoutException and e is not SSLError:
                    print e

        return is_quit

    @staticmethod
    @nottest
    def photo_data(photo_path):
        data = None
        with open(photo_path, "rb") as f:
            data = b2a_base64(f.read())
        return data


class TestConnectedState(BiomioTest):
    """
    Tests server in connected state for appropriate handling "clientHello" message and different kind of
     possible errors.
    """
    def setup(self):
        self.setup_test(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

    def teardown(self):
        self.teardown_test()

    def test_hello_server_responce(self):
        # Server should respond with "serverHello" message if correct "clientHello" message
        # without secret was received.
        message = self.create_next_message(oid='clientHello')
        response = self.send_message(message=message, close_connection=True)
        eq_(response.msg.oid, 'serverHello', msg='Response does not contains serverHello message')

    def test_invalid_message_error_handling(self):
        websocket = self.new_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_json_error_handling(self):
        websocket = self.new_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_sequence_error_handling(self):
        message = self.create_next_message(oid='clientHello')
        message.header.seq = 1
        response = self.send_message(message=message, close_connection=True)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')
        pass

    def test_invalid_protocol_ver_error_handling(self):
        message = self.create_next_message(oid='clientHello')
        message.header.protoVer = '2.0'
        response = self.send_message(message=message, close_connection=True)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_nop_message_without_handshake_error_handling(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(message=message, close_connection=True)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    #TODO: def test_invalid_fingerprint_error_handling(self):

    def test_token_generation(self):
        message = self.create_next_message(oid='clientHello')
        first_response = self.send_message(message=message, close_connection=True)
        ok_(first_response.header.token, msg='Server returns empty token string')

        second_response = self.send_message(message=message, close_connection=True)
        ok_(second_response.header.token, msg='Server returns empty token string')
        ok_(not str(first_response.header.token) == str(second_response.header.token),
            msg='Token string sould be unique for every connection')

    def test_refresh_tokens_unique(self):
        message = self.create_next_message(oid='clientHello')
        first_response = self.send_message(message=message, close_connection=True)
        ok_(first_response.msg.refreshToken, msg='Server returns empty refresh token string')

        second_response = self.send_message(message=message, close_connection=True)
        ok_(second_response.msg.refreshToken, msg='Server returns empty refresh token string')
        ok_(not str(first_response.msg.refreshToken) == str(second_response.msg.refreshToken),
            msg='Refresh token string should be unique for every connection')


class TestHandshakeState(BiomioTest):
    def setup(self):
        self.setup_test_with_hello(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

    def teardown(self):
        self.teardown_test()

    def test_invalid_message_error_handling(self):
        websocket = self.get_curr_connection()
        invalid_message_str = '{}'
        websocket.send(invalid_message_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_json_error_handling(self):
        websocket = self.get_curr_connection()
        invalid_json_str = ''
        websocket.send(invalid_json_str)
        response = self.read_message(websocket=websocket)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_sequence_error_handling(self):
        message = self.create_next_message(oid='auth', key=self.get_digest_for_next_message())
        message.header.seq = 1
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_invalid_protocol_ver_error_handling(self):
        message = self.create_next_message(oid='auth', key=self.get_digest_for_next_message())
        message.header.protoVer = '2.0'
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status string')

    def test_nop_instead_auth_error_handling(self):
        message = self.create_next_message(oid='nop')
        response = self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False)
        eq_(response.msg.oid, 'bye', msg='Response does not contains bye message')
        ok_(hasattr(response, 'status') and response.status, msg='Response does not contains status message')

    @attr('slow')
    @raises(WebSocketTimeoutException, SSLError)
    def test_auth_message(self):
        message = self.create_next_message(oid='auth', key=self.get_digest_for_next_message())
        websocket = self.get_curr_connection()
        response = self.send_message(websocket=websocket, message=message, wait_for_response=True, close_connection=False)
        ok_(not response.msg.oid == 'bye', msg='Server closes connection')
        ok_(response is None, msg='Got unexpected message from server')


class TestReadyState(BiomioTest):
    def setup(self):
        self.setup_test_with_handshake(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

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


class TestRpcCalls(BiomioTest):
    def setup(self):
        # self.setup_test_with_handshake(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)
        pass

    def teardown(self):
        self.teardown_test()

    def test_rpc_call(self):
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func',
                                           onBehalfOf='test@test.com',
                                           data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status: %s' % response.status)

    def test_rpc_ns_list(self):
        message = self.create_next_message(oid='rpcEnumNsReq')
        response = self.send_message(websocket=self.get_curr_connection(), message=message)
        ok_(str(response.msg.oid) != 'bye', msg='Connection closed. Status: %s' % response.status)

    @attr('slow')
    def test_rpc_with_auth(self):
        results = {'rpcResp': None }

        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "NOP"
            elif str(message.msg.oid) == 'rpcResp':
                if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
                        or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
                    results['rpcResp'] = message
                    close_connection_callback()

        self.setup_test_with_handshake(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
            data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
            wait_for_response=True)

        # Separate thread with connection for
        samples = ['True']
        t = threading.Thread(target=TestRpcCalls.probe_job, kwargs={'samples': samples, 'probe_type': 'touchIdSamples'})
        t.start()
        time.sleep(1)

        self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)
        rpcResp = results['rpcResp']
        ok_(rpcResp is not None, msg='No RPC response on auth.')
        eq_(str(rpcResp.msg.rpcStatus), 'complete', msg='RPC authentication failed, but result is positive')


class TestFaceRecognition(BiomioTest):
    def setup(self):
        pass
        # self.setup_test_with_handshake(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

    def teardown(self):
        self.teardown_test()

    @attr('slow')
    @attr('fr')
    def test_face_recognition_training_process(self):
        # Use REST request to server to start training process
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib2.urlopen("https://{host}:{port}/training".format(host=settings.host, port=settings.port)).read()

        # Prerare list of samples for training
        samples = []
        images_path = FR_TRAINING_IMG_FOLDER_PATH
        for image in FR_TRAINING_IMG_NAMES:
            samples.append(TestRpcCalls.photo_data(images_path + image))

        # Communicate as a probe app
        TestRpcCalls.probe_job(samples=samples, probe_type='imageSamples')

    @attr('slow')
    @attr('fr')
    def test_face_recognition_rpc_auth_proceed(self):
        results = {'rpcResp': None }

        # Message handler for extension emulation
        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "."
            elif str(message.msg.oid) == 'rpcResp':
                if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
                        or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
                    results['rpcResp'] = message
                    close_connection_callback()

        # Make handshake sa extension
        self.setup_test_with_handshake(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

        # Send rpc call that requires auth
        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
            data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
            wait_for_response=True)

        # Run probe connection and communicate as a probe
        samples = []
        images_path = FR_TRAINING_IMG_FOLDER_PATH
        for image in FR_TRAINING_IMG_NAMES:
            samples.append(TestRpcCalls.photo_data(images_path + image))

        t = threading.Thread(target=TestRpcCalls.probe_job, kwargs={'samples': samples, 'probe_type': 'imageSamples'})
        t.start()

        # Communicate as an extension
        self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)

        rpcResp = results['rpcResp']
        ok_(rpcResp is not None, msg='No RPC response on auth.')
        eq_(str(rpcResp.msg.rpcStatus), 'complete', msg='RPC authentication failed, but result is positive')


    @attr('slow')
    @attr('fr')
    def test_face_recognition_rpc_auth_proceed_when_probe_first(self):
        results = {'rpcResp': None }

        # Message handler for extension emulation
        def on_message(message, close_connection_callback):
            if str(message.msg.oid) == 'nop':
                print "."
            elif str(message.msg.oid) == 'rpcResp':
                if TestRpcCalls.is_rpc_response_status(message=message, status='complete') \
                        or TestRpcCalls.is_rpc_response_status(message=message, status='fail'):
                    results['rpcResp'] = message
                    close_connection_callback()

        # Run probe at FIRST
        samples = []
        images_path = FR_TRAINING_IMG_FOLDER_PATH
        for image in FR_TRAINING_IMG_NAMES:
            samples.append(TestRpcCalls.photo_data(images_path + image))

        t = threading.Thread(target=TestRpcCalls.probe_job, kwargs={'samples': samples, 'probe_type': 'imageSamples'})
        t.start()

        # Make handshake, rpc call, then communicate as an extension
        self.setup_test_with_handshake(app_id=extension_app_id, app_type=extension_app_type, key=extension_key)

        message = self.create_next_message(oid='rpcReq', namespace='extension_plugin', call='test_func_with_auth',
            data={'keys': ['val1', 'val2'], 'values': ['1', '2']})
        self.send_message(websocket=self.get_curr_connection(), message=message, close_connection=False,
            wait_for_response=True)

        self.keep_connection_and_communicate(biomio_test=self, message_callback=on_message)

        rpcResp = results['rpcResp']
        ok_(rpcResp is not None, msg='No RPC response on auth.')
        eq_(str(rpcResp.msg.rpcStatus), 'complete', msg='RPC authentication failed, but result is positive')


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