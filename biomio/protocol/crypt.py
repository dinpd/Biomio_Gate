
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

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
    def check_digest(key, digest, data):
        hash = SHA256.new(data).digest()
        public_key = RSA.importKey(externKey=key)
        return public_key.verify(hash, digest)
