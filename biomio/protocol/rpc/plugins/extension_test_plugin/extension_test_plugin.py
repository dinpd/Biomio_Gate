from yapsy.IPlugin import IPlugin

class ExtensionTestPlugin(IPlugin):

    def test_func(self, val1, val2):
        print "Test Func Call"
        return {"result": "some value"}