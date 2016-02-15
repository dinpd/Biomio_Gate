from biomio.algorithms.recognition.processes.defs import IDENTIFICATION_DATA_TRAINING_KEY
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
import uuid


IDENTIFICATION_PREPARE_PROCESS_CLASS_NAME = "IdentificationPrepareProcess"

def job(callback_code, **kwargs):
    IdentificationPrepareProcess.job(callback_code, **kwargs)


class IdentificationPrepareProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = IDENTIFICATION_PREPARE_PROCESS_CLASS_NAME
        self._load_users_process = AlgorithmProcessInterface()

    def set_load_users_process(self, process):
        self._load_users_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        self._load_users_process.run(self._worker, **result)

    @staticmethod
    def job(callback_code, **kwargs):
        IdentificationPrepareProcess._job_logger_info(IDENTIFICATION_PREPARE_PROCESS_CLASS_NAME, **kwargs)
        data_redis_key = IDENTIFICATION_DATA_TRAINING_KEY % (str(uuid.uuid4()), kwargs['providerID'])
        AlgorithmsDataStore.instance().store_data(data_redis_key, **kwargs)
        settings = {'providerID': kwargs['providerID'], 'data_redis_key': data_redis_key}
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=settings, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
