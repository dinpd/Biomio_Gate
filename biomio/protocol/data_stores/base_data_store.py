import abc

from biomio.constants import REDIS_JOB_RESULT_KEY
from biomio.protocol.storage.redis_results_listener import RedisResultsListener
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.protocol.data_stores.storage_jobs_processor import run_storage_job


class BaseDataStore():
    _instance = None

    def __init__(self):
        self._redis = RedisStorage.instance()

        import biomio.protocol.data_stores.storage_jobs as sj

        self._GET_JOB = sj.get_record_job
        self._CREATE_JOB = sj.create_record_job
        self._UPDATE_JOB = sj.update_record_job
        self._DELETE_JOB = sj.delete_record_job

    @classmethod
    @abc.abstractmethod
    def instance(cls):
        """
            Returns current BaseDataStore instance.
            If it doesn't exist creates new one.

        :return: BaseDataStore instance.
        """
        if cls._instance is None:
            cls._instance = BaseDataStore()
        return cls._instance

    @abc.abstractmethod
    def store_data(self, object_id, **kwargs):
        """
            Save data into redis and run job to save it in MySQL
        :param object_id: The Id of the object that must be saved.
        :param kwargs: input kwargs.
        """
        pass

    @abc.abstractmethod
    def get_data(self, object_id, callback):
        """
            Get data from MySQL if it doesn't exist in Redis (asynchronously)
        :param object_id: Id of the object that must be received.
        :param callback: callback function that must be executed after data is received.
        """
        pass

    @abc.abstractmethod
    def delete_data(self, object_id):
        """
            Delete data from Redis and after that run job to delete it from MySQL.
        :param object_id ID of the object that must be deleted.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_data_key(object_id):
        """
            Returns Redis key generated with specified object id.
        :param object_id: Is used to generate Redis key.
        :return: str generated redis key.
        """
        return

    def _store_data(self, key, table_class_name, object_id, ex=None, **kwargs):
        """
            Internal method which saves data into Redis and after that runs worker job to save it in MySQL.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object that must be updated (if necessary) in MySQL.
        :param ex: boolean optional parameter, redis data expiration, default = None.
        :param kwargs: Key/Value parameters that must be stored in redis and after in MySQL.
        """
        created = self._redis.store_data(key=key, ex=ex, **kwargs)
        if created:
            run_storage_job(self._CREATE_JOB, table_class_name=table_class_name, **kwargs)
        else:
            run_storage_job(self._UPDATE_JOB, table_class_name=table_class_name, object_id=object_id, **kwargs)

    def _get_data(self, key, table_class_name, object_id, callback):
        """
            Internal method which gets data from Redis. If it exists there then callback is executed with this data.
            If not - we run worker job to get data from MySQL and save it into Redis.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object to get data from MySQL.
        :param callback: function that must be executed after we got data.
        """
        result = self._redis.get_data(key)
        if result is not None:
            callback(result)
        else:
            callback_code = RedisResultsListener.instance().subscribe_callback(callback)
            run_storage_job(self._GET_JOB, table_class_name=table_class_name, object_id=object_id,
                            callback_code=callback_code)

    def _delete_data(self, key, table_class_name, object_id):
        """
            Internal method which deletes data from Redis and after that runs worker job to delete it
            from MySQL.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object to delete data from MySQL.
        """
        self._redis.delete_data(key)
        run_storage_job(self._DELETE_JOB, table_class_name=table_class_name, object_id=object_id)

    def store_job_result(self, record_key, record_dict, callback_code):
        """
            Stores job result data into redis with generated JOB_RESULT key.
        :param record_key: Redis key of the current record object.
        :param record_dict: dict data from the current record.
        :param callback_code: Code of the callback that must be executed after we got result.
        """
        job_result_key = REDIS_JOB_RESULT_KEY % (callback_code, record_key)
        self._redis.store_data(key=job_result_key, **record_dict)

    def delete_custom_redis_data(self, key):
        """
            Deletes data only from redis for given redis key.
        :param key: Generated redis key.
        """
        self._redis.delete_data(key)