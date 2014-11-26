
from time import time, strftime, gmtime
import tornado.ioloop

from collections import OrderedDict

from biomio.protocol.session import Session
from biomio.protocol.settings import settings

from weakref import WeakValueDictionary

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

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = SessionManager()

        return cls._instance

    @classmethod
    def ts(cls):
        return time()

    def adjust(self, ts):
        return ts - ts % self.interval

    def run_timer(self):
        self._timeout_handle = tornado.ioloop.IOLoop.instance().call_later(callback=self.on_check_expired_sessions, delay=self.interval)

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
        return self._sessions_by_token.get(token, '')

    def get_protocol_state(self, token):
        #TODO: read state from redis
        return 'ready'

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