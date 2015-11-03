from threading import Lock
from biomio.constants import REDIS_DEVICE_INFORMATION_KEY, DEVICE_INFORMATION_TABLE_CLASS_NAME
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class DeviceInformationStore(BaseDataStore):
    _instance = None
    _lock = Lock()
    _table_class_name = DEVICE_INFORMATION_TABLE_CLASS_NAME

    DEVICE_TOKEN_ATTR = 'device_token'
    PUSH_TOKEN_ATTR = 'push_token'

    _KEYS_TO_DELETE = [REDIS_DEVICE_INFORMATION_KEY]

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = DeviceInformationStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(app_id):
        return REDIS_DEVICE_INFORMATION_KEY % app_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, app_id, callback):
        self._get_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name, object_id=app_id,
                           callback=callback, to_dict=True)

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, app_id, **kwargs):
        if self.DEVICE_TOKEN_ATTR not in kwargs:
            kwargs.update({self.DEVICE_TOKEN_ATTR: app_id})
        self._store_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name,
                             object_id=app_id, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, app_id):
        self._delete_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name, object_id=app_id)

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, app_ids, callback):
        self._select_data_by_ids(table_class_name=self._table_class_name, object_ids=app_ids, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, app_id, **kwargs):
        self._update_lru_data(key=self.get_data_key(app_id), table_class_name=self._table_class_name, object_id=app_id,
                              **kwargs)

    def get_keys_to_delete(self):
        return self._KEYS_TO_DELETE
