import logging
from yapsy.IPlugin import IPlugin
from biomio.protocol.rpc.rpcutils import rpc_call_with_auth

logger = logging.getLogger(__name__)


class AuthClientPlugin(IPlugin):

    @rpc_call_with_auth
    def process_auth(self, auth_code):
        logger.info('Authentication was successful.')
        # TODO: POST auth code to AI here.
        return dict(resut=True)
