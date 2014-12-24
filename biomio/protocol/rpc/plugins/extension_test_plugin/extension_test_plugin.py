from yapsy.IPlugin import IPlugin

from biomio.protocol.rpc.rpcutils import biometric_auth

import tornado.gen
import time

class ExtensionTestPlugin(IPlugin):

    def test_func(self, val1, val2, callback):
        callback({"result": "some value"})

    @biometric_auth
    def test_funch_with_auth(self, val1, val2, callback):
        print "Done!"
        callback({"result": "some value"})
        # return {"result": "some value"}
