import abc
from yapsy.IPlugin import IPlugin
from biomio.worker.worker_interface import WorkerInterface


class BaseProbePlugin(IPlugin):

    def __init__(self):
        self._callback = None
        self._worker = WorkerInterface.instance()
        super(BaseProbePlugin, self).__init__()

    @abc.abstractmethod
    def apply_policy(self, resources):
        """
            Will apply policy on given probe (device) resources
        :param resources: dict with probe(device) resources
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
