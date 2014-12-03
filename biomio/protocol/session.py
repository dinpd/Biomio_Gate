from os import urandom
from hashlib import sha1

import logging
logger = logging.getLogger(__name__)


class Session:
    """ The session class is abstraction for session in Biomio protocol.

        Session will expire after some time. Client should send message with the given refresh token during the
         session TTL period, otherwise session and connection will be closed. Refresh token is unique for every session
         and generated once per session. After session being refreshed, new session token is generated.

    Attributes:
        refresh_token (str): Session refresh token.
        session_token (str): Session token.
        close_callback (callback): Will be called when session expired.
        is_open (bool): True inf session valid; False otherwise.
    """
    def __init__(self):
        self.refresh_token = Session.generate_token()
        self.session_token = Session.generate_token()
        self.close_callback = None
        self.is_open = True

    def close(self):
        """ Should be called when session is expired.
        """
        self.is_open = False
        if self.close_callback:
            self.close_callback()

    @staticmethod
    def generate_token():
        """Generates unique 128-byte token"""
        return sha1(urandom(128)).hexdigest()

    def refresh(self):
        """Refreshes session. As a result new session token being generated"""
        self.session_token = Session.generate_token()
