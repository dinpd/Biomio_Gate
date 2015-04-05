#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import traceback

from biomio.protocol.settings import settings
from biomio.protocol.engine import BiomioProtocol
from biomio.protocol.connectionhandler import ConnectionTimeoutHandler
from biomio.protocol.rpc.bioauthflow import BioauthFlow

import logging
logger = logging.getLogger(__name__)

ssl_options = {
        "certfile": "server.crt",
        "keyfile": "server.key"
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
            logger.exception(msg='Error during next message processing: %s' % ''.join(traceback.format_exception(*info)))
        else:
            logger.debug(msg='--- Message processed successfully')

    def on_close(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)
        self.biomio_protocol.connection_closed()

    def stop_connection_timer(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)

    def start_connection_timer(self):
        ConnectionTimeoutHandler.instance().start_connection_timer(connection=self, timeout_callback=self.on_connection_timeout)

    def on_connection_timeout(self):
        logger.warning('Connection timeout')
        self.biomio_protocol.close_connection(status_message='Connection timeout')

    def check_connected(self):
        return bool(self.ws_connection)


class InitialProbeRestHandler(tornado.web.RequestHandler):
    def get(self):
        status_url = "https://{host}:{port}/training_status".format(host=settings.host, port=settings.port)
        BioauthFlow.start_training(app_id='test_app_id')
        self.write('<html><head><title>BIOMIO: Initial Probes</title></head><body>'
                   'Please, use BIOMIO probe application to input initial probes.'
                   'See status here:  <a href="{url}">{url}</a>'
                   '</body></html>'.format(url=status_url))


class InitialProbeStatusRestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Processing...')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler),
            (r'/training', InitialProbeRestHandler),
            (r'/training_status', InitialProbeStatusRestHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

def run_tornado():
    app = Application()
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    logger.info('Running tornado server...')
    server.listen(settings.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    # Run tornado application
    run_tornado()
