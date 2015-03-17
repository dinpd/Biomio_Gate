from __future__ import absolute_import
from biomio.constants import APP_DATA_PREFIX, REDIS_APPLICATION_KEY
from biomio.protocol.storage.redisstore import RedisStore


class ApplicationDataStore(RedisStore):
    _instance = None
    _data_prefix = APP_DATA_PREFIX

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ApplicationDataStore()
        return cls._instance

    @staticmethod
    def get_app_redis_key(app_id):
        return REDIS_APPLICATION_KEY % app_id

    def get_app_data(self, app_id, callback):
        self._get_data(self.get_app_redis_key(app_id), self._data_prefix, {'app_id': app_id}, callback)

    def store_app_data(self, app_id, store_mysql=True, **kwargs):
        self._store_data_dict(self.get_app_redis_key(app_id), self._data_prefix, store_mysql=store_mysql, **kwargs)

    def delete_app_data(self, app_id):
        self._delete_data(self.get_app_redis_key(app_id), self._data_prefix, {'app_id': app_id})
