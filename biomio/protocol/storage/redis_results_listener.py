from __future__ import absolute_import
import ast
import logging
from tornadoredis import Client
from biomio.constants import REDIS_JOB_RESULT_KEY, REDIS_DO_NOT_STORE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY
from biomio.protocol.settings import settings
from biomio.protocol.storage.redis_storage import RedisStorage
from os import urandom
from hashlib import sha1
import tornado.gen
import re

logger = logging.getLogger(__name__)


class RedisResultsListener():
    _instance = None

    def __init__(self):
        self._redis_client = Client(host=settings.redis_host, port=settings.redis_port)
        self._result_callbacks = {}
        self._lru_redis = RedisStorage.lru_instance()
        self._persistence_redis = RedisStorage.persistence_instance()
        self._listen()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = RedisResultsListener()
        return cls._instance

    def subscribe_callback(self, callback):
        """
            Puts specified callback into _result_callbacks dict, so after result is received
            it will be executed.
        :param callback: function that must be executed after result is received.
        :return: callback_code that identifies specified callback.
        """
        callback_code = sha1(urandom(32)).hexdigest()
        self._result_callbacks.update({callback_code: callback})
        return callback_code

    def unsubscribe_callback(self, callback_code):
        """
            Deletes callback from _result_callbacks by specified callback_code.
        :param callback_code:
        """
        del self._result_callbacks[callback_code]

    def activate_results_gatherer(self, results_count):
        """
            Stores int results count into redis
        :param results_count: int number of results that must be received before running callback.
        :returns results_code: randomly generated string.
        """
        results_code = sha1(urandom(32)).hexdigest()
        self._persistence_redis.store_counter_value(REDIS_RESULTS_COUNTER_KEY % results_code, results_count)
        return results_code

    @tornado.gen.engine
    def _listen(self):
        """
            Subscribes to Redis Channel changes and initializes changes listener.

        """
        self._redis_client.connect()
        yield tornado.gen.Task(self._redis_client.psubscribe, "__keyspace*:%s" % (REDIS_JOB_RESULT_KEY % ('*', '*')))
        self._redis_client.listen(self._on_redis_message)

    def _on_redis_message(self, msg):
        """
            Parses redis change message and processes the result.
        :param msg: Redis changes message.
        """
        if msg.kind == 'pmessage':
            if msg.body == 'set':

                job_result_key = re.search('.*:(%s)' % (REDIS_JOB_RESULT_KEY % ('.*', '.*')), msg.channel).group(1)
                callback_code = re.search('.*:%s' % (REDIS_JOB_RESULT_KEY % ('(.*):.*', '.*')), msg.channel).group(1)
                redis_result_key = re.search('.*:%s' % (REDIS_JOB_RESULT_KEY % ('.*', '(.*:.*)')), msg.channel).group(1)

                result = self._persistence_redis.get_data(job_result_key)
                try:
                    result = ast.literal_eval(result) if result is not None else {}
                except ValueError as e:
                    logger.exception(msg=str(e))
                    result = {}
                logger.debug('Received result from MySQL - %s' % result)

                if redis_result_key != REDIS_DO_NOT_STORE_RESULT_KEY % callback_code:
                    self._lru_redis.store_data(redis_result_key, **result)
                    logger.debug('Saved result into LRU Redis instance.')

                callback = self._result_callbacks.get(callback_code)

                try:
                    logger.debug('Running callback with result - %s' % result)
                    logger.debug('Callback - %s' % callback)
                    callback(result)
                except Exception as e:
                    logger.warning(msg=str(e))
                finally:
                    self._persistence_redis.delete_data(job_result_key)
                    self.unsubscribe_callback(callback_code)