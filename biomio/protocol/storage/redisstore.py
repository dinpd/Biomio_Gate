from __future__ import absolute_import
import ast
import logging

from redis import StrictRedis

from biomio.protocol.settings import settings


logger = logging.getLogger(__name__)


class RedisStore:
    _instance = None

    def __init__(self):
        self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)

    def _store_data_dict(self, key, ex=None, **kwargs):
        current_data = self._redis.get(key)

        if not current_data:
            current_data = {}
        else:
            current_data = ast.literal_eval(current_data)

        self._store_data(key, current_data, ex=ex, **kwargs)

    def _delete_data(self, key):
        self._redis.delete(key)

    def _get_data(self, key):
        return self._redis.get(name=key)

    def _store_data(self, key, current_data, ex, **kwargs):
        for (k, v) in kwargs.iteritems():
            current_data[k] = v
        self._redis.set(name=key, value=current_data, ex=ex)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = RedisStore()
            cls._RESULT_CALLBACKS = {}
        return cls._instance

    def delete_custom_data(self, key):
        logger.debug('Deleting from redis key - %s' % key)
        self._redis.delete(key)