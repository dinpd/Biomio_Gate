import ast
from yapsy.IPlugin import IPlugin
from biomio.protocol.data_stores.application_data_store import ApplicationDataStore
from biomio.protocol.data_stores.email_data_store import EmailDataStore

from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call, get_store_data, select_store_data, \
    verify_emails_ai, assign_user_to_extension, parse_email_data
import logging

logger = logging.getLogger(__name__)


class ExtensionPlugin(IPlugin):
    @rpc_call
    def test_func(self, val1, val2):
        pass

    @rpc_call_with_auth
    def test_func_with_auth(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def get_pass_phrase(self, email):
        email = parse_email_data(email)
        email_store_instance = EmailDataStore.instance()
        email_data = get_store_data(email_store_instance, object_id=email)
        if email_data is None or len(email_data) == 0:
            raise Exception('Sorry but your email is not activated in your BioMio account.')
        result = {'pass_phrase': email_data.get(EmailDataStore.PASS_PHRASE_ATTR)}
        if email_data.get(EmailDataStore.PRIVATE_PGP_KEY_ATTR) is not None:
            result.update({'private_pgp_key': email_data.get(EmailDataStore.PRIVATE_PGP_KEY_ATTR)})
            update_keywords = {EmailDataStore.PRIVATE_PGP_KEY_ATTR: None}
            email_store_instance.store_data(email, **update_keywords)
        return result

    @rpc_call
    def get_users_public_pgp_keys(self, user_id, emails, app_id):
        assign_user_to_extension(ApplicationDataStore.instance(), app_id=app_id, email=user_id)
        emails = parse_email_data(emails).split(',')
        emails_store_instance = EmailDataStore.instance()
        public_pgp_keys = []
        emails_data = select_store_data(emails_store_instance, emails)
        emails_with_errors = []
        if emails_data is not None:
            for key in emails_data.keys():
                email_data = emails_data.get(key)
                emails.remove(key)
                public_pgp_keys.append(email_data.get(EmailDataStore.PUBLIC_PGP_KEY_ATTR))
        if len(emails):
            new_emails_data = verify_emails_ai(EmailDataStore.instance(), emails)
            if new_emails_data is not None:
                new_emails_data = new_emails_data.get('result', [])
                for email_data in new_emails_data:
                    try:
                        email_data = ast.literal_eval(email_data)
                        if 'error' in email_data:
                            emails_with_errors.append(email_data)
                        else:
                            public_pgp_keys.append(email_data.get(EmailDataStore.PUBLIC_PGP_KEY_ATTR))
                    except ValueError as e:
                        logger.exception(e)
            else:
                logger.debug("No results from emails verification, emails - %s" % emails)
        return {'public_pgp_keys': ','.join(public_pgp_keys)}

