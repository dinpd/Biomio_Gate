import logging
import requests
from requests.exceptions import HTTPError
from biomio.protocol.data_stores.email_data_store import EmailDataStore

import biomio.protocol.rpc.plugins.base_rpc_plugin as base_rpc_plugin
from biomio.constants import REST_BIOAUTH_LOGIN
from biomio.protocol.rpc.plugins.pgp_extension_plugin.pgp_extension_jobs import assign_user_to_application_job
from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call, get_store_data, parse_email_data
from biomio.protocol.settings import settings
from biomio.utils.biomio_decorators import inherit_docstring_from

logger = logging.getLogger(__name__)


class AuthClientPlugin(base_rpc_plugin.BaseRpcPlugin):

    client_auth_data_store = EmailDataStore.instance()

    @inherit_docstring_from(base_rpc_plugin.BaseRpcPlugin)
    def identify_user(self, on_behalf_of):
        email = parse_email_data(on_behalf_of)
        email_data = get_store_data(self.client_auth_data_store, object_id=email)
        return email_data.get(self.client_auth_data_store.USER_ID_ATTR) if email_data is not None else None

    @inherit_docstring_from(base_rpc_plugin.BaseRpcPlugin)
    def assign_user_to_application(self, app_id, user_id):
        self._process_job(assign_user_to_application_job, app_id=app_id, user_id=user_id)

    @rpc_call_with_auth
    def process_auth(self, email, auth_code):
        logger.info('Authentication was successful.')
        logger.debug('Received email with auth_code - %s - %s' % (email, auth_code))
        if auth_code != 'NO_REST':
            bioauth_login_url = settings.ai_rest_url % (REST_BIOAUTH_LOGIN % (auth_code, email))
            response = requests.post(bioauth_login_url)
            try:
                response.raise_for_status()
                logger.info('AI was successfully notified about successful bio auth result.')
            except HTTPError as e:
                logger.error('Request to AI was unsuccessful.')
                logger.exception(e)
        return dict(resut=True)

    @rpc_call
    def check_user_exists(self, client_key):
        logger.info('Checking if user with key - %s, exists.' % client_key)
        email_data = get_store_data(self.client_auth_data_store, object_id=client_key)
        if email_data is None or len(email_data) == 0 or 'error' in email_data:
            return dict(exists=False)
        # TODO: Implement method that will check user existence in DB by his client key.
        return dict(exists=True, email=client_key)
