from __future__ import absolute_import
from threading import Lock
from biomio.constants import (REDIS_DO_NOT_STORE_RESULT_KEY, REDIS_JOB_RESULT_KEY)
from biomio.protocol.storage.redis_storage import RedisStorage
import ast
import logging

logger = logging.getLogger(__name__)

class AlgorithmsDataStore:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._persistence_redis = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = AlgorithmsDataStore()
        return cls._instance

    def exists(self, key):
        """
        Checks if existing persistence Redis key exists.
        :param key: Redis data key.
        :return: True if key exists; False otherwise.
        """
        return self._persistence_redis.exists(key)

    def get_data(self, key):
        """
            Returns data dictionary from persistence redis by specified key.
        :param key: To get data for for.
        :return: dict - with required data in it.
        """
        result = self._persistence_redis.get_data(key)
        if result is not None:
            try:
                result = ast.literal_eval(result)
            except ValueError as e:
                logger.exception(e)
                result = None
        return result

    def store_data(self, key, ex=None, **kwargs):
        """
            Stores data into redis.
        :param key: Key that must be used to store the data.
        :param ex: Data Expiration value, default - None
        :param kwargs: values that will be stored into Redis like a dictionary.
        :return: True/False - indicates whether record was created, False if record was updated.
        """
        self._persistence_redis.store_data(key=key, ex=ex, **kwargs)

    def delete_data(self, key):
        """
            Deletes data only from persistence redis instance for given redis key.
        :param key: Generated redis key.
        """
        self._persistence_redis.delete_data(key)

    def store_job_result(self, record_key, record_dict, callback_code):
        """
            Stores job result data into redis with generated JOB_RESULT key.
        :param record_key: Redis key of the current record object.
        :param record_dict: dict data from the current record.
        :param callback_code: Code of the callback that must be executed after we got result.
        """
        job_result_key = REDIS_JOB_RESULT_KEY % (callback_code, record_key)
        self._persistence_redis.store_data(key=job_result_key, **record_dict)

    def decrement_int_value(self, key):
        """
            Decrements counter value under given key.
        :param key: counter key.
        :return: int decremented counter value.
        """
        return self._persistence_redis.decrement_int_value(key)

    def store_counter_value(self, key, counter):
        """
            Stores int counter value into redis under given key.
        :param key: string counter key
        :param counter: int counter value
        """
        self._persistence_redis.store_counter_value(key, counter)

    def append_value_to_list(self, key, value, append_to_head=False):
        """
            Appends value to the tail of the list which is under specified key.
            If list doesn't exists it should create new one.
        :param key: str key to store value.
        :param value: value that should be appended to the list.
        :return: int length of the list.
        """
        return self._persistence_redis.append_value_to_list(key, value, append_to_head)

    def remove_value_from_list(self, key, value):
        """
            Removes all elements that are equal to value from the list stored at the given key
        :param key: stored list key
        :param value: to delete from the list
        :return: int number of removed elements
        """
        return self._persistence_redis.remove_value_from_list(key, value)

    def get_stored_list(self, key):
        """
            Returns list which is placed under specified key.
        :param key: str key to get list for.
        :return: list of elements
        """
        return self._persistence_redis.get_stored_list(key)
