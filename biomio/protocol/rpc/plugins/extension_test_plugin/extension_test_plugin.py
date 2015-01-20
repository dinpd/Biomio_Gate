import os
import random
import shutil
import string
import tempfile
import gnupg
from yapsy.IPlugin import IPlugin

from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore


class ExtensionTestPlugin(IPlugin):
    @rpc_call
    def test_func(self, val1, val2):
        pass

    @rpc_call_with_auth
    def test_func_with_auth(self, val1, val2):
        return {"result": "some value"}

    @rpc_call
    def get_pass_phrase(self, user_id, email):
        user_pass_phrase = UserInfoDataStore.instance().get_user_data_by_id(user_id=user_id,
                                                                            key=UserInfoDataStore.PASS_PHRASE_KEY)
        if user_pass_phrase is None:
            user_pass_phrase = self.generate_random_pass_phrase()
            UserInfoDataStore.instance().store_user_data(user_id=user_id, email=email, pass_phrase=user_pass_phrase)
            public_pgp_key, private_pgp_key = self.generate_pgp_key_pair(email, user_pass_phrase)
            if public_pgp_key is not None and private_pgp_key is not None:
                UserInfoDataStore.instance().store_user_data(user_id=user_id, email=None,
                                                             public_pgp_key=public_pgp_key)
                return {'private_pgp_key': private_pgp_key, 'pass_phrase': user_pass_phrase}
            return {'error': 'Failed to get public key for given user email.'}
        return {"pass_phrase": user_pass_phrase}

    @rpc_call
    def get_user_public_pgp_key(self, email):
        user_id = UserInfoDataStore.instance().get_user_id_by_email(email=email)
        user_info_redis = UserInfoDataStore.instance()
        if user_id is None:
            # I think this should be done in method which proceeds user registration
            # but for now it is faked here.
            user_id = '%s_fakeID' % email
            random_pass_phrase = self.generate_random_pass_phrase()
            user_info_redis.store_user_data(user_id=user_id, email=email, pass_phrase=random_pass_phrase)
            public_pgp_key, private_pgp_key = self.generate_pgp_key_pair(email, random_pass_phrase)
            if public_pgp_key is not None and private_pgp_key is not None:
                UserInfoDataStore.instance().store_user_data(user_id=user_id, email=None,
                                                             public_pgp_key=public_pgp_key)
                UserInfoDataStore.instance().store_user_data(user_id=user_id, email=None,
                                                             private_pgp_key=private_pgp_key)
                return {'public_pgp_key': public_pgp_key}
        else:
            user_public_pgp_key = user_info_redis.get_user_data_by_id(user_id=user_id,
                                                                      key=UserInfoDataStore.PUBLIC_PGP_KEY)
            return {'public_pgp_key': user_public_pgp_key}
        return {'error': 'Failed to get public key for given user email.'}

    @staticmethod
    def generate_pgp_key_pair(email, pass_phrase):
        home = tempfile.mkdtemp()
        fd, keyring = tempfile.mkstemp(dir=home)
        ascii_armored_public_key = None
        ascii_armored_private_key = None
        os.close(fd)
        if os.environ.get('USERNAME', None) is None:
            os.environ['USERNAME'] = 'test'
        try:
            gpg = gnupg.GPG(gnupghome=home, keyring=keyring, options=['--no-default-keyring', '--no-version',
                                                                      '--no-use-agent'])
            input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, name_comment="Biomio",
                                           name_email=email, passphrase=pass_phrase)
            key = gpg.gen_key(input_data)
            ascii_armored_public_key = gpg.export_keys(key.fingerprint)
            ascii_armored_private_key = gpg.export_keys(key.fingerprint, True)
        except Exception, e:
            print e
        finally:
            shutil.rmtree(home)
        return ascii_armored_public_key, ascii_armored_private_key

    @staticmethod
    def generate_random_pass_phrase():
        return ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))