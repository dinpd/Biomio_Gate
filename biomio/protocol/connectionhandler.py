
from biomio.utils.timeoutqueue import TimeoutQueue
from biomio.protocol.settings import settings

import tornado.ioloop
from weakref import WeakKeyDictionary
from time import time

import logging
logger = logging.getLogger(__name__)


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
