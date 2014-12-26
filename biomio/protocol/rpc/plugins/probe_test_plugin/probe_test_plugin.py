
from yapsy.IPlugin import IPlugin

from biomio.protocol.rpc.rpcutils import rpc_call_with_auth, rpc_call
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore


class ProbeTestPlugin(IPlugin):
    @rpc_call
    def test_func(self, val1, val2):
        return {"result": "some value"}

    @rpc_call_with_auth
    def test_funch_with_auth(self, val1, val2):
        return {"result": "some value"}