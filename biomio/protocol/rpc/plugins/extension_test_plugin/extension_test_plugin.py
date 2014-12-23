from yapsy.IPlugin import IPlugin

from biomio.protocol.rpc.rpcutils import biometric_auth

class ExtensionTestPlugin(IPlugin):

    def test_func(self, val1, val2):
        print "Test Func Call"
        return {"result": "some value"}

    @biometric_auth
    def test_funch_with_auth(self):
        return {"result": "some value"}
