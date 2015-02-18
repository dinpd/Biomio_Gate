
from biomio.protocol.rpc.rpcpluginmanager import RpcPluginManager

import logging
logger = logging.getLogger(__name__)


class RpcHandler:
    """
    RpcHandler class used to handle BIOMIO protocol RPC commands
    """
    def __init__(self):
        pass

    def process_rpc_call(self, user_id, call, namespace, data, wait_callback, callback):
        """
        Processes RPC call with the given parameters.
        :param user_id: User ID string
        :param call: Name of RPC method.
        :param namespace: Namespace where given method located.
        :param data: Dictionary with RPC call parameters.
        :param wait_callback: Callback, that will be called to notify that additional time for RPC processing is neede
        :param callback: Callback that receives result of RPC call. Should take two parameters: result -
        dictionary containing result of RPC method call. status - Status for RPC responce (inprogress, completed, fail)
        """
        logger.info('Processing RPC call %s/%s, with parameters: %s' % (namespace, call, data))
        rpc_obj = RpcPluginManager.instance().get_rpc_object(namespace=namespace)

        if hasattr(rpc_obj, call):
            rpc_call = getattr(rpc_obj, call)
            if rpc_call:
                rpc_call(user_id=user_id, wait_callback=wait_callback, callback=callback, **data)

    def get_available_calls(self, namespace):
        return []

    def get_available_namespaces(self):
        return RpcPluginManager.instance().get_namespaces_list()