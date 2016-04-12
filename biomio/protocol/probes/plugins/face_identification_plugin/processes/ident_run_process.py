from biomio.algorithms.datastructs import wNearPyHash, DEFAULT_NEAR_PY_HASH_SETTINGS
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.recognition.processes.handling import load_temp_data
from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY


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
        data = load_temp_data(result['data_file'], remove=True)
        test_size = 0
        settings = {
            "hash_settings": {
                "database_type": wNearPyHash.type(),
                "settings": DEFAULT_NEAR_PY_HASH_SETTINGS,
                "hash_config_path": data['general_data']['hash_config_path']
            },
            "users": result['users']
        }
        jobs_list = []
        for inx, cluster in data['clusters'].iteritems():
            test_size += len(cluster)
            jobs_list.append({
                "cluster": cluster,
                "database": int(0),
                "cluster_id": int(inx)
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
