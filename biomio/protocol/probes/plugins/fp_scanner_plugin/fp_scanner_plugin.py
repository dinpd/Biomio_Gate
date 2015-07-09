import biomio.protocol.probes.plugins.base_probe_plugin as base_probe_plugin
from biomio.utils.biomio_decorators import inherit_docstring_from


class FpScannerPlugin(base_probe_plugin.BaseProbePlugin):

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def run_training(self, data, callback=None):
        # No training is required for finger prints.
        pass

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def run_verification(self, data, callback=None):
        self._callback = callback
        result = False
        for sample in data.get('samples', []):
            result = result or str(sample).lower() == 'true'
        self._probe_callback({'verified': result})

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def apply_policy(self, resources):
        # TODO: run policy evaluation on resources.
        return resources

    @staticmethod
    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def _generate_ai_rest_urls(data):
        pass
