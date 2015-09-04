import logging
from yapsy.IPlugin import IPlugin
from biomio.protocol.rpc.rpcutils import rpc_call_with_auth

logger = logging.getLogger(__name__)


class AuthClientPlugin(IPlugin):

    @rpc_call_with_auth
    def process_auth(self):
        logger.info('Authentication was successful.')
        return dict(resut=True)
