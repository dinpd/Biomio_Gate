from os import urandom
from hashlib import sha1

class Session:
    def __init__(self):
        self.refresh_token = Session.generate_token()
        self.session_token = Session.generate_token()

    @staticmethod
    def generate_token():
        return sha1(urandom(128)).hexdigest()


