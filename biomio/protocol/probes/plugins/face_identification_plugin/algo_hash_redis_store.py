from biomio.utils.biomio_decorators import inherit_docstring_from
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.constants import MYSQL_IDENTIFICATION_HASH_DATA_TABLE_NAME, IDEN_USER_HASH_TABLE_NAME
from biomio.worker.worker_interface import WorkerInterface
from nearpy.storage import Storage
from threading import Lock

class AlgorithmsHashRedisStackStore(Storage):
    _instance = None
    _lock = Lock()

    def __init__(self, redis_id):
        self._ihr_redis = RedisStorage.ihr_instance(redis_id)
        self._hash_data_table_name = MYSQL_IDENTIFICATION_HASH_DATA_TABLE_NAME
        self._user_hash_table_name = IDEN_USER_HASH_TABLE_NAME

        self._worker = WorkerInterface.instance()

    @classmethod
    def instance(cls, redis_id):
        with cls._lock:
            if cls._instance is None:
                cls._instance = AlgorithmsHashRedisStackStore(redis_id)
        return cls._instance

    @inherit_docstring_from(Storage)
    def store_vector(self, hash_name, bucket_key, v, data):
        pass

    @inherit_docstring_from(Storage)
    def get_bucket(self, hash_name, bucket_key):
        """
            Internal method which gets data from LRU Redis. If it exists there then callback is executed with this data.
            If not - we run worker job to get data from MySQL and save it into Redis.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object to get data from MySQL.
        :param callback: function that must be executed after we got data.
        """
        result = self._ihr_redis.get_data(key)
        if result is not None:
            try:
                result = ast.literal_eval(result)
            except ValueError as e:
                logger.exception(e)
                result = {}
            callback(result)
        else:
            self._run_storage_job(self._worker.GET_JOB, callback, table_class_name=table_class_name,
                                  object_id=object_id, to_dict=to_dict)

    @inherit_docstring_from(Storage)
    def clean_buckets(self, hash_name):
        pass

    @inherit_docstring_from(Storage)
    def clean_all_buckets(self):
        pass

    @inherit_docstring_from(Storage)
    def store_hash_configuration(self, lshash):
        pass

    @inherit_docstring_from(Storage)
    def load_hash_configuration(self, hash_name):
        pass

    def clean_vectors_by_data(self, hash_name, data, bucket_keys=[]):
        pass

    def clean_all_vectors(self, hash_name, data):
        """
            Removes all records from user_hash and hash_data tables.

        :param hash_name:
        :param data:
        :return:
        """
        pass

    def dump(self):
        pass

    def _select_data_by_ids(self, table_class_name, object_ids, callback):
        """
            Internal methods which selects data from MySQL table by given list of ids.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_ids:  list of object ids to get data for.
        :param callback: function that must be executed after we got data.
        """
        self._run_storage_job(self._worker.SELECT_JOB, callback, table_class_name=table_class_name,
                              object_ids=object_ids)

    def _run_storage_job(self, job_to_run, callback=None, kwargs_list_for_results_gatherer=None, **kwargs):
        """
            Runs given job with specified kwargs.
        :param job_to_run: storage job that we will run using worker.
        :param kwargs: input parameters for job.
        """
        self._worker.run_job(job_to_run=job_to_run, callback=callback,
                             kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer, **kwargs)
