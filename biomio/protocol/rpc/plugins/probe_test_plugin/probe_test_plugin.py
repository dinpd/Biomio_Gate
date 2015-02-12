
from yapsy.IPlugin import IPlugin
from biomio.protocol.rpc.rpcutils import rpc_call, rpc_call_with_auth


class ProbeTestPlugin(IPlugin):
    @rpc_call
    def test_func(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def test_func_auth(self, val1, val2):
        return {"result": "some value"}