import ast
import biomio.protocol.rpc.plugins.base_rpc_plugin as base_rpc_plugin
from biomio.protocol.data_stores.email_data_store import EmailDataStore
from biomio.protocol.rpc.plugins.pgp_extension_plugin.pgp_extension_jobs import assign_user_to_application_job, \
    verify_email_job

from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call, get_store_data, select_store_data, \
    parse_email_data, run_sync_job
import logging
from biomio.utils.biomio_decorators import inherit_docstring_from

logger = logging.getLogger(__name__)


class ExtensionPlugin(base_rpc_plugin.BaseRpcPlugin):

    email_data_store = EmailDataStore.instance()

    @inherit_docstring_from(base_rpc_plugin.BaseRpcPlugin)
    def identify_user(self, on_behalf_of):
        email = parse_email_data(on_behalf_of)
        email_data = get_store_data(self.email_data_store, object_id=email)
        return email_data.get(self.email_data_store.USER_ATTR) if email_data is not None else None

    @inherit_docstring_from(base_rpc_plugin.BaseRpcPlugin)
    def assign_user_to_application(self, app_id, user_id):
        self._process_job(assign_user_to_application_job, app_id=app_id, user_id=user_id)

    @rpc_call
    def test_func(self, val1, val2):
        pass

    @rpc_call_with_auth
    def test_func_with_auth(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def get_pass_phrase(self, email):
        email = parse_email_data(email)
        email_data = get_store_data(self.email_data_store, object_id=email)
        if email_data is None or len(email_data) == 0 or 'error' in email_data:
            raise Exception('Sorry but your email is not activated in your BioMio account.')
        result = {'pass_phrase': email_data.get(EmailDataStore.PASS_PHRASE_ATTR)}
        if email_data.get(EmailDataStore.PRIVATE_PGP_KEY_ATTR) is not None:
            result.update({'private_pgp_key': email_data.get(EmailDataStore.PRIVATE_PGP_KEY_ATTR)})
            update_keywords = {EmailDataStore.PRIVATE_PGP_KEY_ATTR: None}
            self.email_data_store.store_data(email, **update_keywords)
        return result

    @rpc_call
    def get_users_public_pgp_keys(self, emails):
        emails = parse_email_data(emails).split(',')
        public_pgp_keys = []
        emails_data = select_store_data(self.email_data_store, emails)
        emails_with_errors = []
        if emails_data is not None:
            for key in emails_data.keys():
                email_data = emails_data.get(key)
                emails.remove(key)
                public_pgp_keys.append(email_data.get(EmailDataStore.PUBLIC_PGP_KEY_ATTR))
        if len(emails):
            kwargs_list_for_results_gatherer = []
            for email in emails:
                kwargs_list_for_results_gatherer.append({'email': email})
            new_emails_data = run_sync_job(verify_email_job,
                                           kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer)
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
        if len(emails_with_errors):
            emails_with_errors = ',,,'.join(str(x) for x in emails_with_errors)
            return {'public_pgp_keys': ','.join(public_pgp_keys), 'emails_with_errors': emails_with_errors}
        return {'public_pgp_keys': ','.join(public_pgp_keys)}
