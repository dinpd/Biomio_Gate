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
        return {"result": "some value"}

    @rpc_call_with_auth
    def test_funch_with_auth(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def get_pass_phrase(self, user_id, email):
        email = self.parse_email_data(email)
        user_info_redis = UserInfoDataStore.instance()
        user_data = user_info_redis.get_user_data_by_id(user_id=user_id, key=UserInfoDataStore.USER_DATA_KEY)
        if user_data is None:
            return self.get_pass_phrase_by_email(user_id, email, user_data)
        user_email_data = user_data.get(email, None)
        if user_email_data is not None:
            return {"pass_phrase": user_email_data.get(UserInfoDataStore.PASS_PHRASE_KEY)}
        user_email_data = user_info_redis.get_user_data_by_id(user_id="%s_fakeID" % email,
                                                              key=UserInfoDataStore.USER_DATA_KEY)
        if user_email_data is None:
            return self.get_pass_phrase_by_email(user_id, email, user_data)
        user_email_data = user_email_data.get(email)
        private_pgp_key = user_email_data.get(UserInfoDataStore.PRIVATE_PGP_KEY)
        del user_email_data[UserInfoDataStore.PRIVATE_PGP_KEY]
        user_data.update({email: user_email_data})
        user_info_redis.store_user_data(user_id=user_id, email=email, user_data=user_data)
        user_info_redis.delete_user_data("%s_fakeID" % email)
        return {'private_pgp_key': private_pgp_key,
                'pass_phrase': user_email_data.get(UserInfoDataStore.PASS_PHRASE_KEY)}


    @staticmethod
    def get_pass_phrase_by_email(user_id, email, user_data=None):
        user_info_redis = UserInfoDataStore.instance()
        user_pass_phrase = ExtensionTestPlugin.generate_random_pass_phrase()
        public_pgp_key, private_pgp_key = ExtensionTestPlugin.generate_pgp_key_pair(email, user_pass_phrase)
        if public_pgp_key is not None and private_pgp_key is not None:
            if user_data is not None:
                user_data.update({email: {UserInfoDataStore.PUBLIC_PGP_KEY: public_pgp_key,
                                          UserInfoDataStore.PASS_PHRASE_KEY: user_pass_phrase}})
            else:
                user_data = {email: {UserInfoDataStore.PUBLIC_PGP_KEY: public_pgp_key,
                                     UserInfoDataStore.PASS_PHRASE_KEY: user_pass_phrase}}
            user_info_redis.store_user_data(user_id=user_id, email=email, user_data=user_data)
            return {'private_pgp_key': private_pgp_key, 'pass_phrase': user_pass_phrase}
        return {'error': 'Failed to get public key for given user email.'}

    @rpc_call
    def get_users_public_pgp_keys(self, emails):
        emails = self.parse_email_data(emails).split(',')
        user_info_redis = UserInfoDataStore.instance()
        public_pgp_keys = []
        for email in emails:
            user_id = user_info_redis.get_user_id_by_email(email=email)
            if user_id is None:
                # I think this should be done in method which proceeds user registration
                # but for now it is faked here.
                user_id = '%s_fakeID' % email
                user_pass_phrase = self.generate_random_pass_phrase()
                public_pgp_key, private_pgp_key = self.generate_pgp_key_pair(email, user_pass_phrase)
                if public_pgp_key is not None and private_pgp_key is not None:
                    user_data = {email: {UserInfoDataStore.PUBLIC_PGP_KEY: public_pgp_key,
                                         UserInfoDataStore.PRIVATE_PGP_KEY: private_pgp_key,
                                         UserInfoDataStore.PASS_PHRASE_KEY: user_pass_phrase}}
                    user_info_redis.store_user_data(user_id=user_id, email=email, user_data=user_data)
                    public_pgp_keys.append(public_pgp_key)
            else:
                user_public_pgp_key = user_info_redis.get_user_data_by_id(user_id=user_id,
                                                                          key=UserInfoDataStore.USER_DATA_KEY)\
                    .get(email).get(UserInfoDataStore.PUBLIC_PGP_KEY)
                public_pgp_keys.append(user_public_pgp_key)
        return {'public_pgp_keys': ','.join(public_pgp_keys)}

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
            input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, name_comment="", name_real="BioMio",
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

    @staticmethod
    def parse_email_data(emails):
        for rep in ['<', '>']:
            emails = emails.replace(rep, '')
        return emails