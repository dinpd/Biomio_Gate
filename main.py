#!/usr/bin/env python
import json
import ssl

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import traceback
from biomio.protocol.data_stores.condition_data_store import ConditionDataStore
from biomio.protocol.probes.probe_plugin_manager import ProbePluginManager
from biomio.protocol.rpc.plugins.pgp_extension_plugin.pgp_extension_jobs import generate_pgp_keys_job

from biomio.protocol.settings import settings
from biomio.protocol.engine import BiomioProtocol
from biomio.protocol.connectionhandler import ConnectionTimeoutHandler
from biomio.protocol.rpc.bioauthflow import BioauthFlow

import logging
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
        request_body = json.loads(self.request.body)
        ConditionDataStore.instance().store_data(user_id=request_body.get('user_id'),
                                                 condition=request_body.get('condition'),
                                                 auth_types=request_body.get('auth_types'))


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
            (r'/set_condition', SetUserCondition)
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
