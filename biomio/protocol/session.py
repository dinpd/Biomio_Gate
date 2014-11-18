from os import urandom
from hashlib import sha1

DEFAULT_SESSION_TTL = 3*60  # 3 minutes

from tornado.options import define, options
define('session_ttl', default=DEFAULT_SESSION_TTL, help='Number of seconds in which session expires.')

class Session:
    def __init__(self):
        self.refresh_token = Session.generate_token()
        self.session_token = Session.generate_token()
        self.ttl = options.session_ttl

    @staticmethod
    def generate_token():
        return sha1(urandom(128)).hexdigest()


