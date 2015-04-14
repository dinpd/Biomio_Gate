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
    def get_data(self, refresh_token, callback=None):
        self._get_persistence_data(self.get_data_key(refresh_token))

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, refresh_token, ttl=None, **kwargs):
        self._store_persistence_data(self.get_data_key(refresh_token), ex=ttl, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, refresh_token):
        self.delete_custom_persistence_redis_data(self.get_data_key(refresh_token))

    def get_application_connections(self, app_id):
        return []

    def check_for_connections(self, app_id):
        return True