
from time import time, strftime, gmtime
import tornado.ioloop
from weakref import WeakValueDictionary

from biomio.protocol.session import Session
from biomio.protocol.settings import settings
from biomio.protocol.redisstore import RedisStore
from biomio.utils.timeoutqueue import TimeoutQueue

import logging
logger = logging.getLogger(__name__)


class SessionManager:
    _instance = None

    def __init__(self):
        self._sessions = TimeoutQueue()
        self._sessions_by_token = WeakValueDictionary()
        self._timeout_handle = None
        self.interval = 1  # seconds
        self._redis_session_store = RedisStore.instance()

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

    def _enqueue_session(self, session):
        ts = self.ts()
        ts += settings.session_ttl
        ts = self.adjust(ts)

        if not self._sessions.has_ts(ts):
            self._sessions.create_timeout(ts)

        self._sessions.append(ts, session)
        self._sessions_by_token[session.refresh_token] = session

    def _dequeue_session(self, session):
        self._sessions.remove(item=session)
        if session.session_token in self._sessions_by_token:
            del self._sessions_by_token[session.refresh_token]

    def create_session(self, close_callback=None):
        session = Session()
        session.close_callback = close_callback

        self._redis_session_store.store_session_data(refresh_token=session.refresh_token)
        self._enqueue_session(session)
        logger.debug('Created session %s', session.refresh_token)

        # print strftime('%H:%M:%S', gmtime(time()))
        # print strftime('%H:%M:%S', gmtime(ts))

        self.run_timer()

        return session

    def restore_session(self, token):
        session = self._sessions_by_token.get(token, None)

        if not session and self._redis_session_store.has_session(refresh_token=token):
            session = Session()
            session.refresh_token = token
            self._enqueue_session(session=session)

        return session

    def get_protocol_state(self, token):
        return self._redis_session_store.get_session_data(refresh_token=token, key='state')

    def set_protocol_state(self, token, current_state):
        session = self._sessions_by_token.get(token, None)
        refresh_token = session.refresh_token
        self._redis_session_store.store_session_data(refresh_token=refresh_token, state=current_state)

    def refresh_session(self, session):
        logger.debug('Refreshing session %s...' % session.refresh_token)
        self._dequeue_session(session)
        session.refresh()
        logger.debug('New session token: %s' % session.session_token)
        self._enqueue_session(session)

    def close_session(self, session):
        logger.debug('Closing session %s' % session.refresh_token)
        self._dequeue_session(session)
        if not self._sessions and self._timeout_handle:
            tornado.ioloop.IOLoop.instance().remove_timeout(timeout=self._timeout_handle)

    def on_check_expired_sessions(self):
        # logger.debug('Checking for expired sessions ...')
        expires_sessions = self._sessions.take_expired(ts=self.ts())
        for session in expires_sessions:
            logger.debug(msg='Session expired - closing: %s' % session.refresh_token)
            session.close()
            self._redis_session_store.remove_session_data(session.refresh_token)
        self.run_timer()