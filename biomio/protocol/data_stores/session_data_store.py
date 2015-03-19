from __future__ import absolute_import
from biomio.constants import REDIS_SESSION_KEY, SESSION_TABLE_CLASS_NAME
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class SessionDataStore(BaseDataStore):
    _instance = None
    _table_class_name = SESSION_TABLE_CLASS_NAME

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        if cls._instance is None:
            cls._instance = SessionDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(object_id):
        return REDIS_SESSION_KEY % object_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, refresh_token, callback):
        self._get_data(self.get_data_key(refresh_token), self._table_class_name, refresh_token, callback)

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, refresh_token, **kwargs):
        if 'refresh_token' not in kwargs:
            kwargs.update({'refresh_token': refresh_token})
        ttl = None
        if 'ttl' in kwargs:
            ttl = kwargs.get('ttl')
        self._store_data(self.get_data_key(refresh_token), self._table_class_name, refresh_token, ex=ttl, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, refresh_token):
        self._delete_data(self.get_data_key(refresh_token), self._table_class_name, refresh_token)