from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from biomio.algorithms.recognition.processes.defs import ERROR_FORMAT, INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR
from biomio.algorithms.datastructs import get_data_structure
from biomio.protocol.probes.plugins.face_identification_plugin.algo_hash_redis_store import \
    AlgorithmsHashRedisStackStore

UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME = "UpdateDataStructureProcess"

def job(callback_code, **kwargs):
    UpdateDataStructureProcess.job(callback_code, **kwargs)


class UpdateDataStructureProcess(AlgorithmProcessInterface):
    def __init__(self):
        AlgorithmProcessInterface.__init__(self)
        self._classname = UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME

    def handler(self, result):
        pass

    @staticmethod
    def job(callback_code, **kwargs):
        UpdateDataStructureProcess._job_logger_info(UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME, **kwargs)
        database_store = get_data_structure(kwargs['settings']['database_type'])
        database_store.init_structure(kwargs['settings']['settings'],
                                      AlgorithmsHashRedisStackStore(kwargs['database']))
        kwargs['database'] = database_store
        engines = UpdateDataStructureProcess.process(**kwargs)
        if len(engines) > 0:
            pass
        else:
            logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, UNKNOWN_ERROR))

    @staticmethod
    def process(**kwargs):
        UpdateDataStructureProcess._process_logger_info(UPDATE_DATA_STRUCTURE_PROCESS_CLASS_NAME, **kwargs)
        data_struct = kwargs.get("database", None)
        settings = kwargs["settings"]
        print settings
        print data_struct
        if data_struct is None:
            data_struct = get_data_structure(settings.get("database_type"))(settings.get("settings", {}))
        print data_struct
        db = kwargs.get("template", [])
        if len(db) > 0:
            cluster_id = kwargs.get("cluster_id", -1)
            if cluster_id >= 0:
                cluster = db[cluster_id]
            else:
                cluster = db
            for desc in cluster:
                data_struct.store_vector(desc, kwargs.get("uuid"))
        return data_struct

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
