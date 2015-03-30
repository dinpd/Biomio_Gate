from __future__ import absolute_import
from biomio.constants import REDIS_APPLICATION_KEY, APPS_TABLE_CLASS_NAME
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class ApplicationDataStore(BaseDataStore):
    _instance = None
    _table_class_name = APPS_TABLE_CLASS_NAME

    # Names of attributes of the corresponding Entity class.
    APP_ID_ATTR = 'app_id'
    APP_TYPE_ATTR = 'app_type'
    PUBLIC_KEY_ATTR = 'public_key'
    USER_ATTR = 'user'

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        if cls._instance is None:
            cls._instance = ApplicationDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(app_id):
        return REDIS_APPLICATION_KEY % app_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, app_id, callback):
        self._get_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name, object_id=app_id,
                           callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, app_id, **kwargs):
        if self.APP_ID_ATTR not in kwargs:
            kwargs.update({self.APP_ID_ATTR: app_id})
        self._store_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name,
                             object_id=app_id, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, app_id):
        self._delete_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name, object_id=app_id)
