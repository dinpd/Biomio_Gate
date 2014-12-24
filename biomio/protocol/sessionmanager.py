from time import time
from weakref import WeakValueDictionary
import logging

import tornado.ioloop

from biomio.protocol.session import Session
from biomio.protocol.settings import settings
from biomio.protocol.storage.redisstore import RedisStore
from biomio.utils.timeoutqueue import TimeoutQueue

logger = logging.getLogger(__name__)


class SessionManager:
    """ The SessionManager singleton handles all sessions and tracks sessions lifetime. Also handles session related data (e.g. protocol state).
    """
    _instance = None

    def __init__(self):
        self._sessions = TimeoutQueue()
        self._sessions_by_token = WeakValueDictionary()
        self._timeout_handle = None
        self.interval = 1  # timeout to check for expired sessions
        self._redis_session_store = RedisStore.instance()

    @classmethod
    def instance(cls):
        """ Returns singleton instance for this class.
        :return: SessionManager instance.
        """
        if not cls._instance:
            cls._instance = SessionManager()

        return cls._instance

    def adjust(self, ts):
        """ Helper method to adjust session timestamp using check interval.
        :param ts:
        """
        return ts - ts % self.interval

    def run_timer(self):
        """ Start timer to check for expired sessions after some interval.
        """
        self._timeout_handle = tornado.ioloop.IOLoop.instance().call_later(callback=self._on_check_expired_sessions, delay=self.interval)

    def _enqueue_session(self, session):
        """ Add session to session tieout queue and start session check timer if necessary.
        :param session: Session instance.
        """
        ts = time()
        ts += settings.session_ttl
        ts = self.adjust(ts)

        if not self._sessions.has_ts(ts):
            self._sessions.create_timeout(ts)

        self._sessions.append(ts, session)
        self._sessions_by_token[session.refresh_token] = session

    def _dequeue_session(self, session):
        """ Remove session from session timeout queue.
        :param session: Session instance.
        """
        self._sessions.remove(item=session)
        if session.session_token in self._sessions_by_token:
            del self._sessions_by_token[session.refresh_token]

    def create_session(self, close_callback=None):
        """ Creates an new session and starts tracking its lifetime.
        :param close_callback: Function or method to call when session expires.
        :return: Session instance.
        """
        session = Session()
        session.close_callback = close_callback

        should_run_timer = not bool(self._sessions)
        self._enqueue_session(session)
        logger.debug('Created session %s', session.refresh_token)

        if should_run_timer:
            self.run_timer()

        return session

    def restore_session(self, token):
        """ Restores session after involuntary disconnection.
        :param token: Session refresh token string.
        :return: Session instance if restored; None otherwise.
        """
        session = self._sessions_by_token.get(token, None)

        if not session and self._redis_session_store.has_session(refresh_token=token):
            session = Session()
            session.refresh_token = token
            self._enqueue_session(session=session)
            self._redis_session_store.refresh_session()

        return session

    def get_protocol_state(self, token):
        """ Returns current protocol state for session.
        :param token: Session refresj token string.
        :return: Protocol state name string if session is alive and state stored; None otherwise.
        """
        return self._redis_session_store.get_session_data(refresh_token=token, key='state')

    def set_protocol_state(self, token, current_state):
        """ Store protocol state information for session. Used to save protocol state during client disconnection period.
        :note Protocol state information will be erased when session expires.
        :param token: Session refresh token string.
        :param current_state: Current state name string.
        """
        session = self._sessions_by_token.get(token, None)
        refresh_token = session.refresh_token
        self._redis_session_store.store_session_data(refresh_token=refresh_token, state=current_state, ttl=settings.session_ttl)

    def refresh_session(self, session):
        """ Refreshes given session. Make session life longer by session TTL value. Also session get a new session token.
        :param session: Session instance.
        """
        logger.debug('Refreshing session %s...' % session.refresh_token)
        self._dequeue_session(session)
        session.refresh()
        logger.debug('New session token: %s' % session.session_token)
        self._enqueue_session(session)

    def close_session(self, session):
        """ Closes given session.
        :param session: Session instance.
        """
        logger.debug('Closing session %s' % session.refresh_token)
        self._dequeue_session(session)
        if not self._sessions and self._timeout_handle:
            tornado.ioloop.IOLoop.instance().remove_timeout(timeout=self._timeout_handle)

    def _on_check_expired_sessions(self):
        """ Called to check if any expire sessions exists.
        """
        expires_sessions = self._sessions.take_expired(ts=time())
        for session in expires_sessions:
            logger.debug(msg='Session expired - closing: %s' % session.refresh_token)
            session.close()
        self.run_timer()