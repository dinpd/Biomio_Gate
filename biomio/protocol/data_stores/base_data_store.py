import abc
import ast
import logging

from biomio.constants import REDIS_JOB_RESULT_KEY
from biomio.protocol.storage.redis_results_listener import RedisResultsListener
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.protocol.data_stores.storage_jobs_processor import run_storage_job

logger = logging.getLogger(__name__)


class BaseDataStore():
    _instance = None

    def __init__(self):
        self._lru_redis = RedisStorage.lru_instance()
        self._persistence_redis = RedisStorage.persistence_instance()

        import biomio.protocol.data_stores.storage_jobs as sj

        self._GET_JOB = sj.get_record_job
        self._CREATE_JOB = sj.create_record_job
        self._UPDATE_JOB = sj.update_record_job
        self._DELETE_JOB = sj.delete_record_job
        self._SELECT_JOB = sj.select_records_by_ids_job

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
            Save data into redis
        :param object_id: The Id of the object that must be saved.
        :param kwargs: input kwargs. Basically this is a list of fields values
                        that are specified in mysql_data_entities module for each table(db entity)
        """
        pass

    @abc.abstractmethod
    def get_data(self, object_id, callback):
        """
            Get data from MySQL if it doesn't exist in Redis (asynchronously)
            Or directly from Redis if we are using _persistence_redis
        :param object_id: Id of the object that must be received.
        :param callback: callback function that must be executed after data is received.
        """
        pass

    @abc.abstractmethod
    def delete_data(self, object_id):
        """
            Delete data from Redis.
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

    @abc.abstractmethod
    def select_data_by_ids(self, object_ids, callback):
        """
            Selects data from MySQL and filters it with given list of object's ids.
        :param object_ids: list of object ids to get data for.
        :param callback: callback function that must be executed after data is received.
        """
        pass

    def _store_lru_data(self, key, table_class_name, object_id, ex=None, **kwargs):
        """
            Internal method which saves data into LRU Redis and after that runs worker job to save it in MySQL.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object that must be updated (if necessary) in MySQL.
        :param ex: boolean optional parameter, redis data expiration, default = None.
        :param kwargs: Key/Value parameters that must be stored in redis and after in MySQL.
        """
        created = self._lru_redis.store_data(key=key, ex=ex, **kwargs)
        if created:
            run_storage_job(self._CREATE_JOB, table_class_name=table_class_name, **kwargs)
        else:
            run_storage_job(self._UPDATE_JOB, table_class_name=table_class_name, object_id=object_id, **kwargs)

    def _get_lru_data(self, key, table_class_name, object_id, callback):
        """
            Internal method which gets data from LRU Redis. If it exists there then callback is executed with this data.
            If not - we run worker job to get data from MySQL and save it into Redis.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object to get data from MySQL.
        :param callback: function that must be executed after we got data.
        """
        result = self._lru_redis.get_data(key)
        if result is not None:
            try:
                result = ast.literal_eval(result)
            except ValueError as e:
                logger.exception(e)
                result = {}
            callback(result)
        else:
            callback_code = RedisResultsListener.instance().subscribe_callback(callback)
            run_storage_job(self._GET_JOB, table_class_name=table_class_name, object_id=object_id,
                            callback_code=callback_code)

    def _delete_lru_data(self, key, table_class_name, object_id):
        """
            Internal method which deletes data from LRU Redis and after that runs worker job to delete it
            from MySQL.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object to delete data from MySQL.
        """
        self._lru_redis.delete_data(key)
        run_storage_job(self._DELETE_JOB, table_class_name=table_class_name, object_id=object_id)

    def store_job_result(self, record_key, record_dict, callback_code):
        """
            Stores job result data into redis with generated JOB_RESULT key.
        :param record_key: Redis key of the current record object.
        :param record_dict: dict data from the current record.
        :param callback_code: Code of the callback that must be executed after we got result.
        """
        job_result_key = REDIS_JOB_RESULT_KEY % (callback_code, record_key)
        self._persistence_redis.store_data(key=job_result_key, **record_dict)

    def delete_custom_lru_redis_data(self, key):
        """
            Deletes data only from lru redis for given redis key.
        :param key: Generated redis key.
        """
        self._lru_redis.delete_data(key)

    def delete_custom_persistence_redis_data(self, key):
        """
            Deletes data only from persistence redis instance for given redis key.
        :param key: Generated redis key.
        """
        self._persistence_redis.delete_data(key)

    def _store_persistence_data(self, key, ex=None, **kwargs):
        """
            Internal method which stores data into persistence Redis instance.
        :param key: Generated redis key.
        :param ex: optional, expiration time for data.
        :param kwargs: dictionary with data to store.
        """
        self._persistence_redis.store_data(key=key, ex=ex, **kwargs)

    def _get_persistence_data(self, key):
        """
            Internal method which gets data from persistence redis instance by given key.
        :param key: Generated redis key.
        """
        return self._persistence_redis.get_data(key)

    def _select_data_by_ids(self, table_class_name, object_ids, callback):
        """
            Internal methods which selects data from MySQL table by given list of ids.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_ids:  list of object ids to get data for.
        :param callback: function that must be executed after we got data.
        """
        callback_code = RedisResultsListener.instance().subscribe_callback(callback)
        run_storage_job(self._SELECT_JOB, table_class_name=table_class_name, object_ids=object_ids,
                        callback_code=callback_code)