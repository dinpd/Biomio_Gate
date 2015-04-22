from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.protocol.settings import settings

import ast

import logging
logger = logging.getLogger(__name__)


class AuthStateStorage:
    _instance = None

    def __init__(self):
        self._persistence_redis = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = AuthStateStorage()

        return cls._instance

    def get_probe_data(self, id, key=None):
        data = self._persistence_redis.get_data(key=id)
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)

        if key:
            data = data.get(key, None)

        return data

    def store_probe_data(self, id, ttl=None, **kwargs):
        self._persistence_redis.store_data(key=id, ex=ttl, **kwargs)

    def remove_probe_data(self, id):
        self._persistence_redis.delete_data(id)

    def move_connected_app_data(self, src_key, dst_key, ttl=None):
        self._persistence_redis.move_data(src_key=src_key, dst_key=dst_key, ex=ttl)


