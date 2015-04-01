from __future__ import absolute_import
from biomio.constants import REDIS_USER_KEY, USERS_TABLE_CLASS_NAME
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class UserDataStore(BaseDataStore):
    _instance = None
    _table_class_name = USERS_TABLE_CLASS_NAME

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(object_id):
        return REDIS_USER_KEY % object_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, user_id, callback):
        self._get_lru_data(key=self.get_data_key(user_id), table_class_name=self._table_class_name, object_id=user_id,
                           callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, user_id):
        self._delete_lru_data(key=self.get_data_key(user_id), table_class_name=self._table_class_name,
                              object_id=user_id)

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, user_id, **kwargs):
        self._store_lru_data(key=self.get_data_key(user_id), table_class_name=self._table_class_name,
                             object_id=user_id, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, user_ids, callback):
        self._select_data_by_ids(table_class_name=self._table_class_name, object_ids=user_ids, callback=callback)