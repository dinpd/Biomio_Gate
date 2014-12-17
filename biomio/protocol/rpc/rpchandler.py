__author__ = 'alexchmykhalo'

import logging
logger = logging.getLogger(__name__)

class RpcHandler:

    def __init__(self):
        pass

    def process_rpc_call(self, call, namespace, data):
        logger.debug('Processing RPC call %s/%s, with parameters: %s' % (namespace, call, data))

    def get_available_calls(self, namespace):
        pass

    def get_available_namespaces(self):
        pass