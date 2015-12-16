from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY

TRANSFER_DATA_PROCESS_CLASS_NAME = "TransferDataProcess"

def job(callback_code, **kwargs):
    TransferDataProcess.job(callback_code, **kwargs)


class TransferDataProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = TRANSFER_DATA_PROCESS_CLASS_NAME
        self._processes = []

    def add_transfer_process(self, process):
        self._processes.append(process)

    def handler(self, result):
        if result is not None:
            for process in self._processes:
                process.run(worker=self._worker, **result)

    @staticmethod
    def job(callback_code, **kwargs):
        TransferDataProcess._job_logger_info(TRANSFER_DATA_PROCESS_CLASS_NAME, **kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=kwargs, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
