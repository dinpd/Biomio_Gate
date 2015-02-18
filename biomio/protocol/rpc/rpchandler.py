__author__ = 'alexchmykhalo'

from biomio.protocol.rpc.rpcpluginmanager import RpcPluginManager

import logging
logger = logging.getLogger(__name__)


class RpcHandler:
    def __init__(self):
        pass

    def process_rpc_call(self, user_id, call, namespace, data, wait_callback, callback):
        logger.info('Processing RPC call %s/%s, with parameters: %s' % (namespace, call, data))
        rpc_obj = RpcPluginManager.instance().get_rpc_object(namespace=namespace)

        result = None
        if hasattr(rpc_obj, call):
            rpc_call = getattr(rpc_obj, call)
            if rpc_call:
                result = rpc_call(user_id=user_id, wait_callback=wait_callback, callback=callback, **data)

        return result

    def get_available_calls(self, namespace):
        return []

    def get_available_namespaces(self):
        return RpcPluginManager.instance().get_namespaces_list()