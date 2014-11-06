#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

import logging
logger = logging.getLogger(__name__)


from biomio.protocol.engine import BiomioProtocol, logger

CONNECTION_TIMEOUT = 10

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = {}
    timeouts = {}

    def open(self):
        biomio_protocol = BiomioProtocol(close_callback=self.close, send_callback=self.write_message,
            start_connection_timer_callback=self.start_connection_timer, stop_connection_timer_callback=self.stop_connection_timer)
        self.connections[self] = biomio_protocol
        self.start_connection_timer()

    def on_message(self, message_string):
        biomio_protocol = self.connections.get(self, None)
        if biomio_protocol:
            biomio_protocol.process_next(message_string)

    def on_close(self):
        # Remove protocol instance from connection dictionary
        self.stop_connection_timer()
        biomio_protocol = self.connections[self]
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
        timeout_handle = tornado.ioloop.IOLoop.instance().call_later(delay=CONNECTION_TIMEOUT, callback=self.on_connection_timeout)
        self.timeouts[self] = timeout_handle

    def on_connection_timeout(self):
        logger.debug('Connection timeout')
        biomio_protocol = self.connections.get(self, None)
        if biomio_protocol:
            biomio_protocol.close_connection(status_message='Connection timeout')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]

        tornado.web.Application.__init__(self, handlers)


def run_tornado():
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    logger.info('Running tornado server...')
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.DEBUG
    )

    # Run tornado application
    run_tornado()