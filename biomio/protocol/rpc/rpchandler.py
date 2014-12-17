__author__ = 'alexchmykhalo'

from biomio.protocol.rpc.rpcpluginmanager import RpcPluginManager

import logging
logger = logging.getLogger(__name__)

class RpcHandler:

    def __init__(self):
        pass

    def process_rpc_call(self, call, namespace, data):
        logger.debug('Processing RPC call %s/%s, with parameters: %s' % (namespace, call, data))
        rpc_obj = RpcPluginManager.instance().get_rpc_object(namespace=namespace)

        if hasattr(rpc_obj, call):
            rpc_call = getattr(rpc_obj, call)
            if rpc_call:
                rpc_call(**data)


    def get_available_calls(self, namespace):
        pass

    def get_available_namespaces(self):
        pass