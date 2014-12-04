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


from biomio.utils.timeoutqueue import TimeoutQueue
from weakref import WeakKeyDictionary
from time import time


class ConnectionTimeoutHandler:
    _instance = None

    @classmethod
    def instance(cls):
        """ Returns singleton instance for this class.
        :return: ConnectionTimeoutHandler instance.
        """
        if not cls._instance:
            cls._instance = ConnectionTimeoutHandler()
        return cls._instance

    def __init__(self):
        self._connections_queue = TimeoutQueue()
        self._callback_by_connection = WeakKeyDictionary()
        self._timeout_handle = None
        self._connection_checking_interval = 1

    def adjust(self, ts):
        """ Helper method to adjust connection timestamp using check interval.
        :param ts: Connection timestamp
        """
        return ts - ts % self._connection_checking_interval

    def _run_timer(self):
        """ Start timer to check for expired connections after some interval.
        """
        self._timeout_handle = tornado.ioloop.IOLoop.instance().call_later(callback=self._on_check_expired_connections,
                                                                           delay=self._connection_checking_interval)

    def start_connection_timer(self, connection, timeout_callback):
        """ Add connection to connection timeout queue and start connection check timer if necessary.
        :param connection: connection object.
        """
        queue_was_empty = not bool(self._connections_queue)

        ts = time()
        ts += settings.connection_timeout
        ts = self.adjust(ts)

        if not self._connections_queue.has_ts(ts):
            self._connections_queue.create_timeout(ts)

        logger.debug('Creating timer for connection %d' % id(connection))
        self._connections_queue.append(ts, connection)
        self._callback_by_connection[connection] = timeout_callback
        if queue_was_empty:
            self._run_timer()

    def stop_connection_timer(self, connection):
        """ Remove connection object from connection timeout queue.
        :param connection: connection object.
        """
        logger.debug('Removing timer for connection %d' % id(connection))
        self._connections_queue.remove(item=connection)

    def _on_check_expired_connections(self):
        """ Called to check if any expired connections exists.
        """
        expired_connections = self._connections_queue.take_expired(ts=time())
        for connection in expired_connections:
            logger.debug(msg='Connection timeout - closing: %s' % connection)
            callback = self._callback_by_connection[connection]
            if callback:
                callback()
        self._run_timer()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = {}
    timeouts = {}

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
        # timeout_handle = self.timeouts.get(self, None)
        # if timeout_handle:
        #     logger.debug('Removing timer for connection %d' % id(self))
        #     tornado.ioloop.IOLoop.instance().remove_timeout(timeout=timeout_handle)
        #     del self.timeouts[self]

    def start_connection_timer(self):
        # if self.timeouts.get(self, None):
        #     logger.debug('Removing old timer for connection %d' % id(self))
        #     self.stop_connection_timer()
        # logger.debug('Creating timer for connection %d' % id(self))
        # timeout_handle = tornado.ioloop.IOLoop.instance().call_later(delay=settings.connection_timeout, callback=self.on_connection_timeout)
        # self.timeouts[self] = timeout_handle
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


if __name__ == '__main__':

    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.DEBUG
    )

    # Run tornado application
    run_tornado()
