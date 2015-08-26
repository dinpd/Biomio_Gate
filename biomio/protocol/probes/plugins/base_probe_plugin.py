import abc
from yapsy.IPlugin import IPlugin
from biomio.worker.worker_interface import WorkerInterface


class BaseProbePlugin(IPlugin):

    _AUTH_CONFIG_RESOURCES_ATTR = 'resources'
    _AUTH_CONFIG_CER_ATTR = 'cer'
    _AUTH_CONFIG_SAMPLES_ATTR = 'samples'
    _AUTH_CONFIG_PROPERTIES_ATTR = 'rProperties'
    _AUTH_CONFIG_R_TYPE_ATTR = 'rType'
    _AUTH_CONFIG_RESOLUTIONS_ATTR = 'resolutions'

    def __init__(self):
        self._callback = None
        self._worker = WorkerInterface.instance()
        super(BaseProbePlugin, self).__init__()

    @abc.abstractmethod
    def check_resources(self, resources, plugin_auth_config, **kwargs):
        """
            Will check if device resource are valid for plugin.
        :param resources: dict with probe(device) resources
        :param plugin_auth_config: dict with plugin auth config
        :returns updated resources dict based on policy results.
        """
        return resources

    def _process_probe(self, algo_job, **kwargs):
        self._worker.run_job(algo_job, callback=self._probe_callback, **kwargs)

    @abc.abstractmethod
    def run_verification(self, data, callback=None):
        """
            Will asynchronously process the required verification algorithm job with given input data.
        :param data:
        """
        pass

    def _probe_callback(self, result):
        if self._callback is not None:
            self._callback(result)

    @abc.abstractmethod
    def run_training(self, data, callback=None):
        """
            Will asynchronously process the required training algorithm job with given input data.
        :param data:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def _generate_ai_rest_urls(data):
        """
            Private method that must generate AI REST API URLs that are required to send during/before/after
            verification/training process.
        :param data: dict() with values that are required to build the URL.
        """
        pass
