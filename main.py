#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen

from biomio.protocol.engine import BiomioProtocol
from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)

ssl_options = {
        "certfile": "server.crt",
        "keyfile": "server.key"
}

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = {}
    timeouts = {}

    def open(self):
        biomio_protocol = BiomioProtocol(
            close_callback=self.close,
            send_callback=self.write_message,
            start_connection_timer_callback=self.start_connection_timer,
            stop_connection_timer_callback=self.stop_connection_timer,
            check_connected_callback=self.check_connected
        )
        self.connections[self] = biomio_protocol
        self.start_connection_timer()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def on_message(self, message_string):
        biomio_protocol = self.connections.get(self, None)
        if biomio_protocol:
            yield tornado.gen.Task(biomio_protocol.process_next, message_string)

    def on_close(self):
        # Remove protocol instance from connection dictionary
        self.stop_connection_timer()
        biomio_protocol = self.connections[self]
        biomio_protocol.connection_closed()
        if biomio_protocol:
            del self.connections[self]

    def stop_connection_timer(self):
        timeout_handle = self.timeouts.get(self, None)
        if timeout_handle:
            logger.debug('Removing timer for connection %d' % id(self))
            tornado.ioloop.IOLoop.instance().remove_timeout(timeout=timeout_handle)
            del self.timeouts[self]

    def start_connection_timer(self):
        if self.timeouts.get(self, None):
            logger.debug('Removing old timer for connection %d' % id(self))
            self.stop_connection_timer()
        logger.debug('Creating timer for connection %d' % id(self))
        timeout_handle = tornado.ioloop.IOLoop.instance().call_later(delay=settings.connection_timeout, callback=self.on_connection_timeout)
        self.timeouts[self] = timeout_handle

    def on_connection_timeout(self):
        logger.debug('Connection timeout')
        biomio_protocol = self.connections.get(self, None)
        if biomio_protocol:
            biomio_protocol.close_connection(status_message='Connection timeout')

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


if __name__ == '__main__':

    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.DEBUG
    )

    # Run tornado application
    run_tornado()