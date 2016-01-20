from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY, REDIS_PARTIAL_RESULTS_KEY, REDIS_RESULTS_COUNTER_KEY
from biomio.algorithms.recognition.processes.messages import create_result_message, create_error_message
from biomio.protocol.probes.plugins.face_identification_plugin.algo_hash_redis_store import \
    AlgorithmsHashRedisStackStore
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.recognition.processes.defs import INTERNAL_TRAINING_ERROR
from biomio.protocol.data_stores.provider_user_store import ProviderUserStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.algorithms.datastructs import get_data_structure
from biomio.algorithms.tools import load_json, save_json
from defs import HASH_SETTINGS_FILE
import os

LOAD_IDENTIFICATION_HASH_PROCESS_CLASS_NAME = "LoadIdentificationHashProcess"

def job(callback_code, **kwargs):
    LoadIdentificationHashProcess.job(callback_code, **kwargs)


class LoadIdentificationHashProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = LOAD_IDENTIFICATION_HASH_PROCESS_CLASS_NAME
        self._ident_estimate_process = AlgorithmProcessInterface()

    def set_identification_estimate_process(self, process):
        self._ident_estimate_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        if result is not None:
            self._ident_estimate_process.run(self._worker, **result['data'])

    @staticmethod
    def job(callback_code, **kwargs):
        LoadIdentificationHashProcess._job_logger_info(LOAD_IDENTIFICATION_HASH_PROCESS_CLASS_NAME, **kwargs)
        record = LoadIdentificationHashProcess.process(**kwargs)
        AlgorithmsDataStore.instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                            value=record)
        results_counter = AlgorithmsDataStore.instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                             callback_code)
        if results_counter <= 0:
            gathered_results = AlgorithmsDataStore.instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                              callback_code)
            if results_counter < 0:
                result = create_error_message(INTERNAL_TRAINING_ERROR, "jobs_counter", "Number of jobs is incorrect.")
            else:
                result = create_result_message({'results': gathered_results}, 'estimation')
            AlgorithmsDataStore.instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % callback_code)
            AlgorithmsDataStore.instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
            AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                            record_dict=result, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        LoadIdentificationHashProcess._process_logger_info(LOAD_IDENTIFICATION_HASH_PROCESS_CLASS_NAME, **kwargs)
        """

        :param kwargs:
        :return: dict
            "cluster_size": length of cluster of the test image,
            "cluster_id": cluster ID,
            "candidates_size": number of found candidates,
            "candidates_score": dict
                <key>: <value>, where <key> - ID of database,
                                      <value> - number of candidates for this database
        """
        cluster = kwargs['cluster']
        db = {
            "cluster_size": len(cluster),
            "cluster_id": kwargs["cluster_id"],
            "candidates_size": 0,
            "candidates_score": {}
        }
        redis_store = kwargs['database']
        user_ids = ProviderUserStore.instance().get_data(kwargs['providerID'])
        settings = kwargs['hash_settings']['settings']
        settings_path = os.path.join(kwargs['hash_settings']['hash_config_path'],
                                     HASH_SETTINGS_FILE % kwargs['cluster_id'])
        if os.path.exists(settings_path):
            settings = load_json(settings_path)
        else:
            settings['projection_name'] += str(kwargs['cluster_id'])
        database_store = get_data_structure(
            kwargs['hash_settings']['database_type'])(settings,
                                                      storage=AlgorithmsHashRedisStackStore.instance(redis_store))
        hash_keys = database_store.hash_list()
        AlgorithmsHashRedisStackStore.instance(redis_store).load_data(user_ids=user_ids, include_only_from=hash_keys)
        if not os.path.exists(settings_path):
            if not os.path.exists(kwargs['hash_settings']['hash_config_path']):
                os.mkdir(kwargs['hash_settings']['hash_config_path'])
            save_json(settings_path, database_store.get_config())
        for desc in cluster:
            buckets = database_store.neighbours(desc)
            db["candidates_size"] += len(buckets)
            for item in buckets:
                lcount = db["candidates_score"].get(item[1], 0)
                lcount += 1
                db["candidates_score"][item[1]] = lcount
        return db

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
