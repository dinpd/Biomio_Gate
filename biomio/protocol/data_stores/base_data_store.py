import abc
import ast
import logging
from threading import Lock

from biomio.constants import REDIS_JOB_RESULT_KEY
from biomio.protocol.storage.redis_storage import RedisStorage

logger = logging.getLogger(__name__)


class BaseDataStore:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._lru_redis = RedisStorage.lru_instance()
        self._persistence_redis = RedisStorage.persistence_instance()

        from biomio.worker.worker_interface import WorkerInterface
        self._worker = WorkerInterface.instance()

    @classmethod
    @abc.abstractmethod
    def instance(cls):
        """
            Returns current BaseDataStore instance.
            If it doesn't exist creates new one.

        :return: BaseDataStore instance.
        """
        with cls._lock:
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
    def update_data(self, object_id, **kwargs):
        """
            Updates data in redis
        :param object_id: The ID of the object that must be updated
        :param kwargs: Values to update
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
            self._run_storage_job(self._worker.CREATE_JOB, table_class_name=table_class_name, object_id=object_id,
                                  **kwargs)
        else:
            self._run_storage_job(self._worker.UPDATE_JOB, table_class_name=table_class_name, object_id=object_id,
                                  **kwargs)

    def _update_lru_data(self, key, table_class_name, object_id, ex=None, **kwargs):
        """
            Internal method which updates data in redis and after that updates data in MySQL
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object that must be updated in MySQL.
        :param ex: boolean optional parameter, redis data expiration, default = None.
        :param kwargs: Key/Value parameters that must be stored in redis and after in MySQL.
        """
        self._lru_redis.store_data(key=key, ex=ex, **kwargs)
        self._run_storage_job(self._worker.UPDATE_JOB, table_class_name=table_class_name, object_id=object_id, **kwargs)

    def _get_lru_data(self, key, table_class_name, object_id, callback, to_dict=False):
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
            self._run_storage_job(self._worker.GET_JOB, callback, table_class_name=table_class_name,
                                  object_id=object_id, to_dict=to_dict)

    def _delete_lru_data(self, key, table_class_name, object_id):
        """
            Internal method which deletes data from LRU Redis and after that runs worker job to delete it
            from MySQL.
        :param key: str Generated Redis Key.
        :param table_class_name: str Pony MySQL Entity class name.
        :param object_id: str ID of the object to delete data from MySQL.
        """
        self._lru_redis.delete_data(key)
        self._run_storage_job(self._worker.DELETE_JOB, table_class_name=table_class_name, object_id=object_id)

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
        result = self._persistence_redis.get_data(key)
        if result is not None:
            try:
                result = ast.literal_eval(result)
            except ValueError as e:
                logger.exception(e)
                result = None
        return result

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
        :param kwargs: iput parameters for job.
        """
        self._worker.run_job(job_to_run=job_to_run, callback=callback,
                             kwargs_list_for_results_gatherer=kwargs_list_for_results_gatherer, **kwargs)

    def _get_app_ids_by_app_id(self, table_class_name, object_id, callback, probes=False):
        if probes:
            self._run_storage_job(self._worker.SELECT_PROBES_BY_EXTENSION_JOB, callback,
                                  table_class_name=table_class_name, user_id=object_id)
        else:
            self._run_storage_job(self._worker.SELECT_EXTENSIONS_BY_PROBE_JOB, callback,
                                  table_class_name=table_class_name, probe_id=object_id)

    def _append_value_to_list(self, key, value, to_head=False):
        """
            Persistence Redis instance
            internal method to append specified value into list by given key.
        :param key: of the stored list
        :param value: to add
        :param to_head: whether to add value into the head of the list (by default it is appended to tail)
        """
        self._persistence_redis.append_value_to_list(key=key, value=value, append_to_head=to_head)

    def _remove_value_from_list(self, key, value):
        """
            Persistence instance
            Internal method to remove given value from the list by given key.
        :param key: of the stored list
        :param value: to remove
        """
        self._persistence_redis.remove_value_from_list(key=key, value=value)

    def _get_stored_list(self, key):
        """
            Persistence redis instance
            internal method to return stored list by given key.
        :param key: of the stored list
        :return: list
        """
        return self._persistence_redis.get_stored_list(key=key)

    def _delete_stored_list(self, key):
        """
            Persistence Redis instance
            Internal method to delete stored list by given key.
        :param key: of the stored list
        """
        self._persistence_redis.delete_data(key=key)
