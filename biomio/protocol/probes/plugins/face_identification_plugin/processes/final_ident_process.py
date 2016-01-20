from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY

FINAL_IDENTIFICATION_PROCESS_CLASS_NAME = "FinalIdentificationProcess"

def job(callback_code, **kwargs):
    FinalIdentificationProcess.job(callback_code, **kwargs)


class FinalIdentificationProcess(AlgorithmProcessInterface):
    def __init__(self, callback):
        AlgorithmProcessInterface.__init__(self)
        self._classname = FINAL_IDENTIFICATION_PROCESS_CLASS_NAME
        self.external_callback(callback)

    def handler(self, result):
        raise NotImplementedError

    @staticmethod
    def job(callback_code, **kwargs):
        FinalIdentificationProcess._job_logger_info(FINAL_IDENTIFICATION_PROCESS_CLASS_NAME, **kwargs)
        max_count = 0
        max_key = ""
        for key, count in kwargs['candidates_score'].iteritems():
            if max_count < count:
                max_count = count
                max_key = key
        record = {
            'result': max_key
        }
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run_external(worker, job, kwargs_list_for_results_gatherer, **kwargs)
