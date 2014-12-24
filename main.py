#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen

from biomio.protocol.engine import BiomioProtocol
from biomio.protocol.settings import settings
from biomio.protocol.connectionhandler import ConnectionTimeoutHandler

import logging
logger = logging.getLogger(__name__)

ssl_options = {
        "certfile": "server.crt",
        "keyfile": "server.key"
}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = {}
    timeouts = {}

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
        self.biomio_protocol.process_next(message_string)

    def on_close(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)
        self.biomio_protocol.connection_closed()

    def stop_connection_timer(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)

    def start_connection_timer(self):
        ConnectionTimeoutHandler.instance().start_connection_timer(connection=self, timeout_callback=self.on_connection_timeout)

    def on_connection_timeout(self):
        logger.debug('Connection timeout')
        self.biomio_protocol.close_connection(status_message='Connection timeout')


    def check_connected(self):
        return bool(self.ws_connection)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]

        tornado.web.Application.__init__(self, handlers)

def run_tornado():
    app = Application()
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    logger.info('Running tornado server...')
    server.listen(settings.port)
    tornado.ioloop.IOLoop.instance().start()


from biomio.protocol.rpc.rpcutils import _is_biometric_data_valid

if __name__ == '__main__':

    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.DEBUG
    )



    # Run tornado application
    run_tornado()
