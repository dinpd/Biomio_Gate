from biomio.constants import MYSQL_IDENTIFICATION_HASH_DATA_TABLE_NAME, IDEN_USER_HASH_TABLE_NAME
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.worker.worker_interface import WorkerInterface
from threading import Lock

REDIS_IDENTIFICATION_BUCKET_KEY = 'identification_hash:%s:%s'
HASH_BUCKET_KEY_FORMAT = "bucket_key:%s:%s"

class AlgorithmsHashRedisStackStore:
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

    def store_vectors(self, hash_data_list, data, callback):
        user_hash_data = []
        hash_keys_data = {}
        for hash_name, hash_buckets in hash_data_list:
            for key, value in hash_buckets:
                bucket_key = HASH_BUCKET_KEY_FORMAT % (hash_name, key)
                user_hash_data.append((data, bucket_key))
                values = hash_keys_data.get(bucket_key, [])
                values.append((value, data))
                hash_keys_data[bucket_key] = values
        # TODO: Database store data

    def get_bucket(self, hash_name, bucket_key):
        bucket_key = HASH_BUCKET_KEY_FORMAT % (hash_name, bucket_key)
        return self._ihr_redis.get_data(bucket_key)

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
