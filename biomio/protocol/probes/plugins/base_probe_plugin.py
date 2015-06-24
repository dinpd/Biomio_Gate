from yapsy.IPlugin import IPlugin


class BaseProbePlugin(IPlugin):

    def __init__(self, callback=None):
        self.callback = callback
        super(BaseProbePlugin, self).__init__()

    def apply_policy(self, resources):
        pass

    def _process_probe(self, data):
        raise NotImplementedError

    def run(self, data):
        result = self._process_probe(data)
        if self.callback is not None:
            self.callback(result)
