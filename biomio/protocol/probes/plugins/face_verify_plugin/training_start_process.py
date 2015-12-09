from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from interface_helper import pre_training_helper


def job(callback_code, **kwargs):
    settings = pre_training_helper(callback_code=callback_code, **kwargs)
    if settings is not None:
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=settings, callback_code=callback_code)


class TrainingStartProcess(AlgorithmProcessInterface):
    def __init__(self, callback):
        AlgorithmProcessInterface.__init__(self)
        self._classname = "TrainingStartProcess"
        self._main_training_process = AlgorithmProcessInterface()
        self.external_callback(callback)

    def set_main_training_process(self, process):
        self._main_training_process = process

    def handler(self, **result):
        if result.keys().__contains__('error'):
            self._callback(result)
        else:
            self._main_training_process.process(**result)

    @staticmethod
    def job(callback_code, **kwargs):
        pass

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
