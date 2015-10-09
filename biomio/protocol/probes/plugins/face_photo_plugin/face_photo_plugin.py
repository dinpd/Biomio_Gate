import biomio.protocol.probes.plugins.base_probe_plugin as base_probe_plugin
from biomio.protocol.probes.plugins.face_photo_plugin.face_photo_jobs import training_job, verification_job
from biomio.utils.biomio_decorators import inherit_docstring_from


class FacePhotoPlugin(base_probe_plugin.BaseProbePlugin):
    _settings = dict(algoID="001022", userID="0000000000000")

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def set_plugin_config(self, config_values):
        self._settings.update({'algoID': config_values.get('algo_id', "001022")})

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def run_training(self, data, callback=None):
        self._callback = callback
        self._data_validator(data)
        normalized_images = [str(image) for image in data.get('samples')]
        del data['samples']
        data.update({'images': normalized_images, 'settings': self._settings})
        self._process_probe(training_job, **data)

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def run_verification(self, data, callback=None):
        self._callback = callback
        self._data_validator(data)
        data.update({'settings': self._settings})
        kwargs_list_for_results_gatherer = []
        for image in data.get('samples'):
            kwargs_list_for_results_gatherer.append({'image': str(image)})
        del data['samples']
        self._process_probe(verification_job,
                            kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer, **data)

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def check_resources(self, resources, plugin_auth_config, training=False):
        plugin_auth_resources = plugin_auth_config.get(self._AUTH_CONFIG_RESOURCES_ATTR, {})

        plugin_r_type = plugin_auth_resources.get(self._AUTH_CONFIG_R_TYPE_ATTR, '')
        device_resource_properties = resources.get(plugin_r_type)

        if device_resource_properties is not None:
            resolutions = plugin_auth_resources.get(self._AUTH_CONFIG_RESOLUTIONS_ATTR, [])
            for resolution in resolutions:
                if resolution in device_resource_properties:
                    resource = {self._AUTH_CONFIG_R_TYPE_ATTR: plugin_r_type,
                                self._AUTH_CONFIG_PROPERTIES_ATTR: resolution}
                    samples = plugin_auth_resources.get(self._AUTH_CONFIG_SAMPLES_ATTR, {})
                    if training:
                        samples = samples.get('training', 5)
                    else:
                        samples = samples.get('verification', 1)
                    return dict(resource=resource, samples=samples)
        return None

    @staticmethod
    def _data_validator(data):
        if 'probe_id' not in data:
            raise ValueError('probe_id is missing.')
        if 'samples' not in data:
            raise ValueError('Samples list is missing.')

    @staticmethod
    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def _generate_ai_rest_urls(data):
        pass
