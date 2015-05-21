from __future__ import absolute_import
from biomio.constants import REDIS_APP_AUTH_KEY, REDIS_APPLICATION_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class AppAuthStore(BaseDataStore):
    """
    The AppAuthStore class handles authentication result data in persistence Redis.
    """
    _instance = None

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        if cls._instance is None:
            cls._instance = AppAuthStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(object_id):
        return REDIS_APPLICATION_KEY % object_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, app_id, callback=None):
        self._get_persistence_data(self.get_data_key(app_id))

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, app_id, ttl=None, **kwargs):
        self._store_persistence_data(self.get_data_key(app_id), ex=ttl, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, app_id):
        self.delete_custom_persistence_redis_data(self.get_data_key(app_id))

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, app_id, ttl=None, **kwargs):
        self._store_persistence_data(key=self.get_data_key(app_id), ex=ttl, **kwargs)
