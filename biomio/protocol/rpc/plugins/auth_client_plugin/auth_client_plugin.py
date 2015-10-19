import logging
import requests
from requests.exceptions import HTTPError

from yapsy.IPlugin import IPlugin
from biomio.constants import REST_BIOAUTH_LOGIN
from biomio.protocol.data_stores.email_data_store import EmailDataStore
from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call, get_store_data
from biomio.protocol.settings import settings

logger = logging.getLogger(__name__)


class AuthClientPlugin(IPlugin):

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
        email_data = get_store_data(EmailDataStore.instance(), object_id=client_key)
        if email_data is None or len(email_data) == 0 or 'error' in email_data:
            return dict(exists=False)
        # TODO: Implement method that will check user existence in DB by his client key.
        return dict(exists=True, email=client_key)
