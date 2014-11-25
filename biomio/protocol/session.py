from os import urandom
from hashlib import sha1

from biomio.protocol.settings import settings
import tornado

import tornadoredis

import logging
logger = logging.getLogger(__name__)

import time

class Session:
    def __init__(self, _close_callback=None):
        self.refresh_token = Session.generate_token()
        self.session_token = Session.generate_token()
        self.ttl = settings.session_ttl
        self.redis = tornadoredis.Client(host=settings.redis_host, port=settings.redis_port)
        self._start_session()
        self._close_callback = _close_callback
        self.is_open = True

    def redis_session_name(self):
        return 'token:%s' % self.session_token

    def _start_session(self):
        default_data = {
            'state': None
        }
        self.redis.set(key=self.redis_session_name(), value=default_data)

    def close(self):
        self.is_open = False
        if self._close_callback:
            self._close_callback()

    @staticmethod
    def generate_token():
        return sha1(urandom(128)).hexdigest()