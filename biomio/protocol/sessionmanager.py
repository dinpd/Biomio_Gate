
from time import time, strftime, gmtime
import tornado.ioloop
import tornado.gen

from collections import OrderedDict

from biomio.protocol.session import Session
from biomio.protocol.settings import settings

from weakref import WeakValueDictionary

import tornadoredis
import ast

import logging
logger = logging.getLogger(__name__)

class TimeoutQueue:
    def __init__(self):
        self.queue = OrderedDict()

    def __nonzero__(self):
        return bool(self.queue)

    def create_timeout(self, ts):
        self.queue[ts] = []

    def has_ts(self, ts):
        return ts in self.queue

    def append(self, ts, item):
        self.queue[ts].append(item)

    def has_expired(self, ts):
        (timestamp, item_list) = self.queue.itervalues().next()
        return timestamp < ts

    def take_expired(self, ts):
        expired = []
        expired_ts = []
        for (t, item_list) in self.queue.iteritems():
            if t <= ts:
                expired.extend(item_list)
                expired_ts.append(t)
            else:
                break

        for t in expired_ts:
            del self.queue[t]

        return expired

    def remove(self, item):
        ts_to_remove = None
        for (t, item_list) in self.queue.iteritems():
            if item in item_list:
                item_list.remove(item)
                if not item_list:
                    ts_to_remove = t
                break
        if ts_to_remove:
            del self.queue[ts_to_remove]

    def iteritems(self):
        return self.queue.iteritems()

    def __str__(self):
        s = ''
        for (t, item_list) in self.queue.iteritems():
            s += '%s  %s\n' % (str(t), str(item_list))
        return s

class SessionManager:
    _instance = None

    def __init__(self):
        self._sessions = TimeoutQueue()
        self._sessions_by_token = WeakValueDictionary()
        self._timeout_handle = None
        self.interval = 1  # seconds
        #TODO: maybe better to use connection pool, and separate connections per operation
        self.redis = tornadoredis.Client(host=settings.redis_host, port=settings.redis_port)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = SessionManager()

        return cls._instance

    def _redis_session_name(self, session_token):
        return 'token:%s' % session_token

    @classmethod
    def ts(cls):
        return time()

    def adjust(self, ts):
        return ts - ts % self.interval

    def run_timer(self):
        self._timeout_handle = tornado.ioloop.IOLoop.instance().call_later(callback=self.on_check_expired_sessions, delay=self.interval)

    @tornado.gen.engine
    def get_session_data(self, refresh_token, key, callback=None):
        data = yield tornado.gen.Task(self.redis.get, self._redis_session_name(session_token=refresh_token))
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        # print 'data: ', data
        # raise tornado.gen.Return(data.get(key, None))
        callback(data.get(key, None))

    @tornado.gen.engine
    def store_session_data(self, refresh_token, **kwargs):
        current_data = yield tornado.gen.Task(self.redis.get, self._redis_session_name(session_token=refresh_token))

        if not current_data:
            current_data = {}
        else:
            current_data = ast.literal_eval(current_data)

        for (k, v) in kwargs.iteritems():
            current_data[k] = v

        yield tornado.gen.Task(self.redis.set, self._redis_session_name(session_token=refresh_token), current_data)

    def remove_session_data(self, token):
        self.redis.delete(key=self._redis_session_name(session_token=token))

    def create_session(self, close_callback=None):
        # print self.sessions
        session = Session()
        session.close_callback = close_callback
        logger.debug('Created session %s', session.refresh_token)

        ts = self.ts()
        ts += settings.session_ttl
        ts = self.adjust(ts)

        if not self._sessions.has_ts(ts):
            self._sessions.create_timeout(ts)

        self._sessions.append(ts, session)
        self._sessions_by_token[session.session_token] = session
        self._sessions_by_token[session.refresh_token] = session

        # print strftime('%H:%M:%S', gmtime(time()))
        # print strftime('%H:%M:%S', gmtime(ts))

        self.run_timer()

        return session

    def get_session(self, token):
        return self._sessions_by_token.get(token, None)

    def get_protocol_state(self, token, callback=None):
        self.get_session_data(refresh_token=token, key='state', callback=callback)

    def set_protocol_state(self, token, current_state):
        session = self._sessions_by_token.get(token, None)
        refresh_token = session.refresh_token
        self.store_session_data(refresh_token=refresh_token, state=current_state)

    def close_session(self, session):
        logger.debug('Closing session %s' % session.refresh_token)
        self._sessions.remove(session)
        if not self._sessions:
            tornado.ioloop.IOLoop.instance().remove_timeout(timeout=self._timeout_handle)

    def on_check_expired_sessions(self):
        # logger.debug('Checking for expired sessions ...')
        expires_sessions = self._sessions.take_expired(ts=self.ts())
        for session in expires_sessions:
            logger.debug(msg='Session expired - closing: %s' % session.refresh_token)
            session.close()

        self.run_timer()