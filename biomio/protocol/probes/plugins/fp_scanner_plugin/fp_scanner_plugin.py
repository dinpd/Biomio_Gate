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
    def check_resources(self, resources, plugin_auth_config, **kwargs):
        plugin_auth_resources = plugin_auth_config.get(self._AUTH_CONFIG_RESOURCES_ATTR, {})

        plugin_r_type = plugin_auth_resources.get(self._AUTH_CONFIG_R_TYPE_ATTR)
        if plugin_r_type is not None and resources.get(plugin_r_type) is not None:
            resource = {self._AUTH_CONFIG_R_TYPE_ATTR: plugin_r_type, self._AUTH_CONFIG_PROPERTIES_ATTR: ''}
            samples = plugin_auth_resources.get(self._AUTH_CONFIG_SAMPLES_ATTR, 1)
            return dict(resource=resource, samples=samples)
        return None

    @staticmethod
    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def _generate_ai_rest_urls(data):
        pass
