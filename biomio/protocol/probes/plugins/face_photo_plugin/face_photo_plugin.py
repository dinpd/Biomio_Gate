import biomio.protocol.probes.plugins.base_probe_plugin as base_probe_plugin
from biomio.utils.biomio_decorators import inherit_docstring_from
from biomio.worker.worker_interface import WorkerInterface


class FacePhotoPlugin(base_probe_plugin.BaseProbePlugin):

    _settings = dict(algoID="001002", userID="0000000000000")

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def run_training(self, data, callback=None):
        self._callback = callback
        self._data_validator(data)
        normalized_images = [str(image) for image in data.get('samples')]
        del data['samples']
        data.update({'images': normalized_images, 'settings': self._settings})
        self._process_probe(WorkerInterface.instance().TRAINING_JOB, **data)

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def run_verification(self, data, callback=None):
        self._callback = callback
        self._data_validator(data)
        data.update({'settings': self._settings})
        kwargs_list_for_results_gatherer = []
        for image in data.get('samples'):
            kwargs_list_for_results_gatherer.append({'image': str(image)})
        del data['samples']
        self._process_probe(WorkerInterface.instance().VERIFICATION_JOB,
                            kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer, **data)

    @inherit_docstring_from(base_probe_plugin.BaseProbePlugin)
    def apply_policy(self, resources):
        # TODO: run policy evaluation on resources.
        return resources

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
