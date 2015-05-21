from __future__ import absolute_import
from biomio.constants import REDIS_APP_CONNECTION_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class AppConnectionStore(BaseDataStore):
    _instance = None

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        if cls._instance is None:
            cls._instance = AppConnectionStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(app_id):
        return REDIS_APP_CONNECTION_KEY % app_id

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
        self._store_persistence_data(self.get_data_key(app_id), ex=ttl, **kwargs)
