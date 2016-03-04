#!/usr/bin/env python
import ast
import json
import ssl

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import greenado
import traceback
from biomio.mysql_storage.mysql_data_store import MySQLDataStore
from biomio.protocol.data_stores.application_data_store import ApplicationDataStore
from biomio.protocol.data_stores.condition_data_store import ConditionDataStore
from biomio.protocol.probes.probe_plugin_manager import ProbePluginManager
from biomio.protocol.rpc.app_connection_manager import AppConnectionManager
from biomio.protocol.rpc.plugins.pgp_extension_plugin.pgp_extension_jobs import generate_pgp_keys_job

from biomio.protocol.settings import settings
from biomio.protocol.engine import BiomioProtocol
from biomio.protocol.connectionhandler import ConnectionTimeoutHandler
from biomio.protocol.rpc.bioauthflow import BioauthFlow

import logging
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.tries_simulator.tries_simulator_manager import TriesSimulatorManager
from biomio.tries_simulator.try_simulator_store import TrySimulatorStore
from biomio.worker.worker_interface import WorkerInterface

logger = logging.getLogger(__name__)

ssl_options = {
    "certfile": "prod_certs/biom.io.crt",
    "keyfile": "prod_certs/biom.io.key",
    "ssl_version": ssl.PROTOCOL_TLSv1
}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.biomio_protocol = BiomioProtocol(
            close_callback=self.close,
            send_callback=self.write_message,
            start_connection_timer_callback=self.start_connection_timer,
            stop_connection_timer_callback=self.stop_connection_timer,
            check_connected_callback=self.check_connected
        )
        self.start_connection_timer()

    def on_message(self, message_string):
        tornado.ioloop.IOLoop.current().add_future(self.biomio_protocol.process_next(message_string),
                                                   callback=WebSocketHandler.message_processed)

    @staticmethod
    def message_processed(future):
        if future.exception():
            info = future.exc_info()
            logger.exception(
                msg='Error during next message processing: %s' % ''.join(traceback.format_exception(*info)))
        else:
            logger.debug(msg='--- Message processed successfully')

    def on_close(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)
        self.biomio_protocol.connection_closed()

    def stop_connection_timer(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)

    def start_connection_timer(self):
        ConnectionTimeoutHandler.instance().start_connection_timer(connection=self,
                                                                   timeout_callback=self.on_connection_timeout)

    def on_connection_timeout(self):
        logger.warning('Connection timeout')
        self.biomio_protocol.close_connection(status_message='Connection timeout')

    def check_connected(self):
        return bool(self.ws_connection)


class InitialProbeRestHandler(tornado.web.RequestHandler):
    def post(self):
        BioauthFlow.start_training(probe_id=self.get_query_argument('device_id'), code=self.get_query_argument('code'))
        self.write('<html><head><title>BIOMIO: Initial Probes</title></head><body>'
                   'Please, use BIOMIO probe application to input initial probes. PROBE_ID - %s'
                   '</body></html>' % self.get_query_argument('device_id'))


class TryRequestsSimulator(tornado.web.RequestHandler):
    _simulator_option_value = '<option value="%s">%s</option>'

    def get(self, *args, **kwargs):
        active_devices = TriesSimulatorManager.instance().get_active_connections()
        active_devices_list = ''
        for active_device_id, user_email in active_devices.iteritems():
            active_devices_list += self._simulator_option_value % (active_device_id, '%s - %s' % (user_email,
                                                                                                  active_device_id))
        with open('./tries_simulator.html') as f:
            simulator_html = f.read()
        if len(simulator_html):
            if not len(active_devices_list):
                active_devices_list = self._simulator_option_value % ('No active devices', 'No active devices')
            simulator_html = simulator_html % active_devices_list
        self.write(simulator_html)

    def post(self, *args, **kwargs):
        request_body = self.request.body
        logger.debug('TRY SIMULATOR: Request Body: %s' % request_body)
        try_data = dict(
            condition='any',
            auth_types=[],
            app_id=''
        )
        request_body = request_body.split('&')
        for request_param in request_body:
            param_attrs = request_param.split('=')
            if 'skip_' in param_attrs[0]:
                continue
            try_param = try_data.get(param_attrs[0])
            if isinstance(try_param, list):
                try_param.append(param_attrs[1])
            else:
                try_param = param_attrs[1]
            try_data.update({param_attrs[0]: try_param})
        if try_data.get('app_id') != 'No active devices':
            TriesSimulatorManager.instance().send_try_request(**try_data)
        self.get(*args, **kwargs)


class GetUserProviders(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        app_id = self.get_query_argument('app_id')
        providers = MySQLDataStore.instance().get_providers_by_device(app_id=app_id)
        self.write(json.dumps(dict(result=providers)))


class StartSimulatorAuth(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        app_id = self.get_query_argument('app_id')
        auth_status = RedisStorage.persistence_instance().get_data(key='simulator_auth_status:%s' % app_id)
        auth_status = ast.literal_eval(auth_status) if auth_status is not None else {}
        if auth_status.get('status') == 'finished' and 'result' in auth_status:
            result = auth_status.get('result')
            try:
                user_info = TrySimulatorStore.instance().get_user_info(user_id=int(result))
                if user_info is not None:
                    auth_status.update({'result': '%s - %s' % (user_info.get('email'), result)})
            except ValueError:
                pass
        self.write(json.dumps(auth_status))

    def post(self, *args, **kwargs):
        request_body = json.loads(self.request.body)
        TriesSimulatorManager.instance().start_regular_auth(app_id=request_body.get('selected_device'),
                                                            provider_id=request_body.get('selected_provider'))


class SetRecognitionType(tornado.web.RequestHandler):
    app_rec_type_key = 'app_rec_type:%s'

    def get(self, *args, **kwargs):
        app_id = self.get_query_argument('app_id')
        rec_type_data = RedisStorage.persistence_instance().get_data(key=self.app_rec_type_key % app_id)
        response_data = dict(verification=True)
        if rec_type_data is not None:
            rec_type_data = ast.literal_eval(rec_type_data)
            if rec_type_data.get('rec_type', 'verification') != 'verification':
                response_data.update({'verification': False})

        self.write(json.dumps(response_data))

    def post(self, *args, **kwargs):
        request_body = json.loads(self.request.body)
        app_id = request_body.get('selected_device')
        rec_type = request_body.get('rec_type')
        RedisStorage.persistence_instance().store_data(key=self.app_rec_type_key % app_id, rec_type=rec_type)


class NewEmailPGPKeysHandler(tornado.web.RequestHandler):
    def post(self, email, *args, **kwargs):
        logger.info('Received new_email request from AI with email - %s' % email)
        WorkerInterface.instance().run_job(generate_pgp_keys_job, email=email)


class SetTryTypeHandler(tornado.web.RequestHandler):
    def post(self, try_type, *args, **kwargs):
        logger.info('Received new try_type - %s' % try_type)
        from biomio.protocol.settings import settings
        settings.policy_try_type = str(try_type)


class SetKeypointsCoffHandler(tornado.web.RequestHandler):
    def post(self, coff, *args, **kwargs):
        logger.info('Received new keypoints coff - %s' % coff)
        with open('keypoints.conf', 'w') as f:
            f.write(str(coff))


class SetUserCondition(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write(json.dumps(dict(auth_types=ProbePluginManager.instance().get_available_auth_types())))

    def post(self, *args, **kwargs):
        try:
            request_body = json.loads(self.request.body)
            logger.info('Received set condition request with parameters: %s' % request_body)
            user_id = request_body.get('user_id')
            condition = request_body.get('condition')
            auth_types = request_body.get('auth_types')
            face_algo_type = request_body.get('face_algo_type', '')
            missing_params = []
            if user_id is None:
                missing_params.append('user_id')
            if condition is None:
                missing_params.append('condition')
            if auth_types is None:
                missing_params.append('auth_types')
            if len(missing_params):
                self.clear()
                self.set_status(400)
                self.finish('{"error":"Missing parameter(s): %s"}' % ','.join(missing_params))
            else:
                ConditionDataStore.instance().store_data(user_id=user_id, condition=condition, auth_types=auth_types,
                                                         face_algo_type=face_algo_type)
        except ValueError as e:
            self.clear()
            self.set_status(400)
            self.finish('{"error":"Missing parameter(s): %s"}' % str(e))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


class HttpApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/training.*', InitialProbeRestHandler),
            (r'/new_email/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})', NewEmailPGPKeysHandler),
            (r'/set_try_type/(?P<try_type>[\w\-]+)', SetTryTypeHandler),
            (r'/set_keypoints_coff/(?P<coff>\d+\.\d{2})', SetKeypointsCoffHandler),
            (r'/set_condition.*', SetUserCondition),
            (r'/tries_simulator.*', TryRequestsSimulator),
            (r'/set_recognition_type.*', SetRecognitionType),
            (r'/get_user_providers.*', GetUserProviders),
            (r'/start_auth.*', StartSimulatorAuth)
        ]
        tornado.web.Application.__init__(self, handlers)


def run_tornado():
    app = Application()
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    logger.info('Running tornado server on port %s ...' % settings.port)
    server.listen(settings.port)

    http_app = HttpApplication()
    http_server = tornado.httpserver.HTTPServer(http_app)
    logger.info('Running REST tornado server on port %s ...' % settings.rest_port)
    http_server.listen(settings.rest_port)

    https_app = HttpApplication()
    https_server = tornado.httpserver.HTTPServer(https_app, ssl_options=ssl_options)
    logger.info('Running REST SSL tornado server on port %s ...' % settings.rest_ssl_port)
    https_server.listen(settings.rest_ssl_port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    # Run tornado application
    run_tornado()
