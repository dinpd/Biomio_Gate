
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
from binascii import b2a_hex, a2b_hex

class Crypto:

    @staticmethod
    def generate_keypair():
        """
        Generates RSA keypair.
        :return: Tuple with private(first) and public (second) keys.
        """
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        priv_key = key.exportKey()
        pub_key = key.publickey().exportKey()
        return priv_key, pub_key

    @staticmethod
    def create_digest(key, data):
        h = SHA256.new(data).digest()
        private_key = RSA.importKey(externKey=key)
        digest, = private_key.sign(h, '')
        return str(digest)

    @staticmethod
    def check_digest(key, digest, data):
        try:
            h = SHA256.new(data).digest()
            public_key = RSA.importKey(externKey=key)
            result = public_key.verify(h, (long(digest), None))
            return result
        except:
            return False
