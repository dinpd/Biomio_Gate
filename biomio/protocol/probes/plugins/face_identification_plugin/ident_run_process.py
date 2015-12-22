from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from biomio.algorithms.datastructs import wNearPyHash


IDENTIFICATION_RUN_PROCESS_CLASS_NAME = "IdentificationRunProcess"

def job(callback_code, **kwargs):
    IdentificationRunProcess.job(callback_code, **kwargs)


class IdentificationRunProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = IDENTIFICATION_RUN_PROCESS_CLASS_NAME
        self._identification_process = AlgorithmProcessInterface()

    def set_identification_process(self, process):
        self._identification_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        data = result["data"]
        test_size = 0
        settings = {
            "settings": {
                "database_type": wNearPyHash.type(),
                "settings": {}
            }
        }
        jobs_list = []
        for inx, cluster in enumerate(data):
            test_size += len(cluster)
            jobs_list.append({
                "cluster": cluster,
                "database": inx,
                "cluster_id": inx
            })
        self._identification_process.run(self._worker, kwargs_list_for_results_gatherer=jobs_list, **settings)

    @staticmethod
    def job(callback_code, **kwargs):
        IdentificationRunProcess._job_logger_info(IDENTIFICATION_RUN_PROCESS_CLASS_NAME, **kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=kwargs, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
