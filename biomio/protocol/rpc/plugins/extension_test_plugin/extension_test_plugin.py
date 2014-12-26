import random
import string
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
    def generate_pass_phrase(self, user_id, email):
        random_pass_pharse = ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
        UserInfoDataStore.instance().store_user_data(user_id=user_id, email=email, pass_phrase=random_pass_pharse)
        return {"pass_phrase": random_pass_pharse}

    @rpc_call_with_auth
    def get_pass_phrase(self, user_id):
        user_pass_phrase = UserInfoDataStore.instance().get_user_data_by_id(user_id=user_id,
                                                                            key=UserInfoDataStore.PASS_PHRASE_KEY)
        return {"pass_phrase": user_pass_phrase}

    @rpc_call_with_auth
    def get_user_public_pgp_key(self, email):
        user_id = UserInfoDataStore.instance().get_user_id_by_email(email=email)
        if user_id is None:
            # TODO Implement functionality that will create a new user and generate public/private key pair
            pass
        user_public_pgp_key = UserInfoDataStore.instance().get_user_data_by_id(user_id=user_id,
                                                                               key=UserInfoDataStore.PUBLIC_PGP_KEY)
        return {'public_key': user_public_pgp_key}

    @rpc_call_with_auth
    def store_public_pgp_key(self, user_id, public_pgp_key):
        UserInfoDataStore.instance().store_user_data(user_id=user_id, email=None, public_pgp_key=public_pgp_key)
        return {'result': 'Done'}