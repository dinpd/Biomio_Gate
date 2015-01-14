
from yapsy.IPlugin import IPlugin

from biomio.protocol.rpc.rpcutils import rpc_call, set_probe_result


class ProbeTestPlugin(IPlugin):
    @rpc_call
    def test_func(self, val1, val2):
        return {"result": "some value"}

    @rpc_call
    def test_probe_valid(self, user_id):
        set_probe_result(user_id=user_id, auth_successfull=True)
        return {"result": "some value"}

    @rpc_call
    def test_probe_invalid(self, user_id):
        set_probe_result(user_id=user_id, auth_successfull=False)
        return {"result": "some value"}