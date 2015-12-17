from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from algo_hash_redis_store import AlgorithmsHashRedisStackStore
from biomio.algorithms.datastructs import get_data_structure
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY

UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME = "UpdateDataStructureProcess"

def job(callback_code, **kwargs):
    UpdateDataStructureProcess.job(callback_code, **kwargs)


class UpdateDataStructureProcess(AlgorithmProcessInterface):
    def __init__(self, callback):
        AlgorithmProcessInterface.__init__(self)
        self.external_callback(callback)
        self._classname = UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME
        self._count = 0

    def _internal_handler(self, result):
        logger.debug(result)
        self._count -= 1
        if self._count == 0:
            self._callback(result)

    def handler(self, result):
        self._handler_logger_info(result)
        if result is not None:
            buckets = result['data']
            redis_store = result['store']
            AlgorithmsHashRedisStackStore.instance(redis_store).store_vectors(buckets, result['uuid'],
                                                                              self._internal_handler)

    @staticmethod
    def job(callback_code, **kwargs):
        UpdateDataStructureProcess._job_logger_info(UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME, **kwargs)
        redis_store = kwargs['database']
        database_store = get_data_structure(kwargs['settings']['database_type'])(kwargs['settings']['settings'])
        buckets = database_store.hash_vectors(kwargs['template'], kwargs['uuid'])
        record = {'data': buckets,
                  'store': redis_store,
                  'uuid': kwargs['uuid'],
                  'data_settings': kwargs['data_settings']
                  }
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._count += 1
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
