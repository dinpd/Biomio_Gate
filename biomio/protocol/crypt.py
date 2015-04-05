
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from binascii import hexlify, unhexlify
import hashlib

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
        h = SHA.new(data)
        private_key = RSA.importKey(externKey=key)
        signer = PKCS1_v1_5.new(private_key)
        return hexlify(signer.sign(h))

    @staticmethod
    def check_digest(key, digest, data):
        try:
            h = SHA.new(data)
            public_key = RSA.importKey(externKey=key)
            verifier = PKCS1_v1_5.new(public_key)
            result = verifier.verify(h, unhexlify(digest))
            return result
        except:
            return False

    @staticmethod
    def _insert_char_every_n_chars(string, char='\n', every=64):
        return char.join(string[i:i + every] for i in xrange(0, len(string), every))

    @staticmethod
    def get_public_rsa_fingerprint(pub_key):
        """
        Returns the fingerprint of the public portion of an RSA key as a
        32-character string .
        The fingerprint is computed using the MD5 (hex) digest of the DER-encoded
        RSA public key.
        """
        md5digest = hashlib.md5(pub_key).hexdigest()
        return md5digest
