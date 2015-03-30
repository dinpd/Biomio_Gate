import os
import random
import shutil
import string
import tempfile
import gnupg
from yapsy.IPlugin import IPlugin
from biomio.protocol.data_stores.email_data_store import EmailDataStore

from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call, get_user_id_by_fingerprint, get_data_helper


class ExtensionPlugin(IPlugin):
    @rpc_call
    def test_func(self, val1, val2):
        pass

    @rpc_call_with_auth
    def test_func_with_auth(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def get_pass_phrase(self, app_id, email):
        email = self.parse_email_data(email)
        user_id = get_user_id_by_fingerprint(fingerprint=app_id)
        if user_id is None:
            raise Exception('User not found for given fingerprint - %s.' % app_id)
        email_store_instance = EmailDataStore.instance()
        email_data = get_data_helper(email_store_instance, object_id=email)
        if email_data is not None:
            result = {'pass_phrase': email_data.get(EmailDataStore.PASS_PHRASE_ATTR)}
            if email_data.get(EmailDataStore.PRIVATE_PGP_KEY_ATTR) is not None:
                result.update({'private_pgp_key': email_data.get(EmailDataStore.PRIVATE_PGP_KEY_ATTR)})
                update_keywords = {EmailDataStore.PRIVATE_PGP_KEY_ATTR: None}
                email_store_instance.store_data(email, **update_keywords)
            return result
        public_pgp_key, private_pgp_key, pass_phrase = self.generate_pgp_key_pair(email)
        if public_pgp_key is None or private_pgp_key is None:
            raise Exception('PGP keys where not generated for email - %s' % email)
        store_keywords = {EmailDataStore.PASS_PHRASE_ATTR: pass_phrase,
                          EmailDataStore.PUBLIC_PGP_KEY_ATTR: public_pgp_key, EmailDataStore.USER_ATTR: user_id}
        email_store_instance.store_data(email, **store_keywords)
        return {'pass_phrase': pass_phrase, 'private_pgp_key': private_pgp_key}

    @rpc_call
    def get_users_public_pgp_keys(self, emails):
        emails = self.parse_email_data(emails).split(',')
        emails_store_instance = EmailDataStore.instance()
        public_pgp_keys = []
        for email in emails:
            email_data = get_data_helper(emails_store_instance, object_id=email)
            if email_data is not None:
                public_pgp_keys.append(email_data.get(EmailDataStore.PUBLIC_PGP_KEY_ATTR))
            else:
                # TODO: Implement functionality that will send REST request to adm backend.
                pass
        return {'public_pgp_keys': ','.join(public_pgp_keys)}

    @staticmethod
    def generate_pgp_key_pair(email):
        pass_phrase = ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
        home = tempfile.mkdtemp()
        fd, keyring = tempfile.mkstemp(dir=home)
        ascii_armored_public_key = None
        ascii_armored_private_key = None
        os.close(fd)
        if os.environ.get('USERNAME', None) is None:
            os.environ['USERNAME'] = email.split('@')[0]
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
        return ascii_armored_public_key, ascii_armored_private_key, pass_phrase

    @staticmethod
    def parse_email_data(emails):
        for rep in ['<', '>']:
            emails = emails.replace(rep, '')
        return emails