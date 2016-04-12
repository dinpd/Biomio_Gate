import ast
from datetime import datetime
from biomio.protocol.data_stores.email_data_store import EmailDataStore
import biomio.protocol.rpc.plugins.base_rpc_plugin as base_rpc_plugin
from biomio.protocol.data_stores.pgp_keys_data_store import PgpKeysDataStore
from biomio.protocol.rpc.plugins.pgp_extension_plugin.pgp_extension_jobs import assign_user_to_application_job, \
    verify_email_job, generate_pgp_keys_job

from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call, get_store_data, select_store_data, \
    parse_email_data, run_sync_job
import logging
from biomio.utils.biomio_decorators import inherit_docstring_from

logger = logging.getLogger(__name__)


class ExtensionPlugin(base_rpc_plugin.BaseRpcPlugin):
    pgp_data_store = PgpKeysDataStore.instance()
    email_data_store = EmailDataStore.instance()

    @inherit_docstring_from(base_rpc_plugin.BaseRpcPlugin)
    def identify_user(self, on_behalf_of):
        email = parse_email_data(on_behalf_of)
        email_data = get_store_data(self.email_data_store, object_id=email)
        if email_data is None:
            return None
        return email_data.get(self.email_data_store.USER_ID_ATTR)

    @inherit_docstring_from(base_rpc_plugin.BaseRpcPlugin)
    def assign_user_to_application(self, app_id, user_id):
        self._process_job(assign_user_to_application_job, app_id=app_id, user_id=user_id)

    @rpc_call_with_auth
    def get_pass_phrase(self, email, user_id):
        email = parse_email_data(email)
        pgp_data = get_store_data(self.pgp_data_store, object_id=email)
        if pgp_data is None:
            primary_email = get_store_data(self.email_data_store, object_id=user_id,
                                           specific_method='get_primary_email')
            pgp_data = get_store_data(self.pgp_data_store,
                                      object_id=primary_email.get(self.email_data_store.EMAIL_ATTR))
        if pgp_data is None or len(pgp_data) == 0 or 'error' in pgp_data:
            raise Exception('Sorry but your email is not activated in your BioMio account.')
        result = {'pass_phrase': pgp_data.get(PgpKeysDataStore.PASS_PHRASE_ATTR)}
        if pgp_data.get(PgpKeysDataStore.PRIVATE_PGP_KEY_ATTR) is not None:
            result.update({'private_pgp_key': pgp_data.get(PgpKeysDataStore.PRIVATE_PGP_KEY_ATTR)})
            update_keywords = {PgpKeysDataStore.PRIVATE_PGP_KEY_ATTR: None}
            self.pgp_data_store.store_data(email, **update_keywords)
        return result

    @rpc_call
    def get_users_public_pgp_keys(self, on_behalf_of, sender, emails):
        if on_behalf_of != sender:
            sender_data = get_store_data(self.email_data_store, object_id=sender)
            if sender_data is None or 'error' in sender_data:
                base_account_data = get_store_data(self.email_data_store, object_id=on_behalf_of)
                record_kwargs = {
                    self.email_data_store.USER_ID_ATTR: int(base_account_data.get(self.email_data_store.USER_ID_ATTR)),
                    'extention': True,
                    'verified': True
                }
                self.email_data_store.store_data(email=sender, **record_kwargs)
        emails = parse_email_data(emails).split(',')
        public_pgp_keys = []
        pgp_emails_data = select_store_data(self.pgp_data_store, emails)
        emails_with_errors = []
        if pgp_emails_data is not None:
            for key in pgp_emails_data.keys():
                pgp_data = pgp_emails_data.get(key)
                emails.remove(key)
                public_pgp_keys.append(pgp_data.get(PgpKeysDataStore.PUBLIC_PGP_KEY_ATTR))
        if len(emails):
            primary_emails = []
            users_by_emails = select_store_data(self.email_data_store, emails)
            if users_by_emails is not None:
                for user_email in users_by_emails.keys():
                    primary_email = get_store_data(self.email_data_store, specific_method='get_primary_email',
                                                   object_id=users_by_emails.get(user_email).get(
                                                       self.email_data_store.USER_ID_ATTR))
                    emails.remove(user_email)
                    primary_emails.append(primary_email.get(self.email_data_store.EMAIL_ATTR))
            if len(primary_emails):
                pgp_emails_data = select_store_data(self.pgp_data_store, primary_emails)
                for key in pgp_emails_data.keys():
                    pgp_data = pgp_emails_data.get(key)
                    public_pgp_keys.append(pgp_data.get(PgpKeysDataStore.PUBLIC_PGP_KEY_ATTR))
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
                                public_pgp_keys.append(email_data.get(PgpKeysDataStore.PUBLIC_PGP_KEY_ATTR))
                        except ValueError as e:
                            logger.exception(e)
                else:
                    logger.debug("No results from emails verification, emails - %s" % emails)
        if len(emails_with_errors):
            emails_with_errors = ',,,'.join(str(x) for x in emails_with_errors)
            return {'public_pgp_keys': ','.join(public_pgp_keys), 'emails_with_errors': emails_with_errors}
        return {'public_pgp_keys': ','.join(public_pgp_keys)}

    def generate_pgp_keys(self, email, is_primary=False):
        if not is_primary:
            email_data = get_store_data(self.email_data_store, object_id=email)
            if email_data is not None and not email_data.get(self.email_data_store.PRIMARY_ATTR):
                primary_email = get_store_data(self.email_data_store,
                                               object_id=email_data.get(self.email_data_store.USER_ID_ATTR),
                                               specific_method='get_primary_email')
                email = primary_email.get(self.email_data_store.EMAIL_ATTR)
        self._process_job(generate_pgp_keys_job, email=email)
