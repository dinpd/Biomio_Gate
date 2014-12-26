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
        return {"result": "some value"}

    @rpc_call_with_auth
    def test_funch_with_auth(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def get_pass_phrase(self, user_id, email):
        user_pass_phrase = UserInfoDataStore.instance().get_user_data_by_id(user_id=user_id,
                                                                            key=UserInfoDataStore.PASS_PHRASE_KEY)
        if user_pass_phrase is None:
            user_pass_phrase = ''.join(
                random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
            UserInfoDataStore.instance().store_user_data(user_id=user_id, email=email, pass_phrase=user_pass_phrase)
        return {"pass_phrase": user_pass_phrase}

    @rpc_call
    def get_user_public_pgp_key(self, email):
        user_id = UserInfoDataStore.instance().get_user_id_by_email(email=email)
        user_info_redis = UserInfoDataStore.instance()
        if user_id is None:
            # I think this should be done in method which proceeds user registration
            # but for now it is faked here.
            user_id = '%s_fakeID' % email
            random_pass_pharse = ''.join(
                random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
            user_info_redis.store_user_data(user_id=user_id, email=email, pass_phrase=random_pass_pharse)

        user_public_pgp_key = user_info_redis.get_user_data_by_id(user_id=user_id,
                                                                  key=UserInfoDataStore.PUBLIC_PGP_KEY)
        return {'public_key': user_public_pgp_key}

    @rpc_call
    def store_public_pgp_key(self, user_id, public_pgp_key):
        UserInfoDataStore.instance().store_user_data(user_id=user_id, email=None, public_pgp_key=public_pgp_key)
        return  {'result': 'Done'}


# if __name__ == '__main__':
# random_pass_phrase = ''.join(
#         random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
#     home = tempfile.mkdtemp()
#     #os_level, keyring = tempfile.mkstemp(dir=home)
#     print home
#    # print keyring
# #    try:
#     gpg = gnupg.GPG(gnupghome=home, keyring='D:\\temp\\keyring', options=['--no-default-keyring'])
#     #gpg.encoding = 'utf-8'
#     input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, name_comment="Biomio",
#                                    name_email='andriy.lobashchuk@vakoms.com', passphrase=random_pass_phrase)
#     key = gpg.gen_key(input_data)
#     print vars(key)
#     ascii_armored_public_key = gpg.export_keys(key.fingerprint)
#     ascii_armored_private_key = gpg.export_keys(key.fingerprint, True)
#     print ascii_armored_public_key
#     print '---------\n'
#     print ascii_armored_private_key
# #    except Exception, e:
# #        print e
# #    finally:
# #        shutil.rmtree(home)
