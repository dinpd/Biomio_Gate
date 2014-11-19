from os import urandom
from hashlib import sha1

from biomio.protocol.settings import settings

class Session:
    def __init__(self):
        self.refresh_token = Session.generate_token()
        self.session_token = Session.generate_token()
        self.ttl = settings.session_ttl

    @staticmethod
    def generate_token():
        return sha1(urandom(128)).hexdigest()