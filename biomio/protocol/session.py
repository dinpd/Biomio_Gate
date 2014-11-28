from os import urandom
from hashlib import sha1

from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)

class Session:
    def __init__(self, _close_callback=None):
        self.refresh_token = Session.generate_token()
        self.session_token = Session.generate_token()
        self.ttl = settings.session_ttl
        self.close_callback = None
        self.is_open = True

    def close(self):
        self.is_open = False
        if self.close_callback:
            self.close_callback()

    @staticmethod
    def generate_token():
        return sha1(urandom(128)).hexdigest()