from threading import Lock
from biomio.constants import REDIS_RESOURCES_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class DeviceResourcesDataStore(BaseDataStore):

    _instance = None
    _lock = Lock()

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = DeviceResourcesDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(device_id):
        return REDIS_RESOURCES_KEY % device_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, device_id, callback=None):
        return self._get_persistence_data(key=self.get_data_key(device_id))

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, device_id, **kwargs):
        self._store_persistence_data(key=self.get_data_key(device_id), ex=300, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, device_id):
        self.delete_custom_persistence_redis_data(key=self.get_data_key(device_id))

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, device_ids, callback):
        pass

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, device_id, **kwargs):
        self._store_persistence_data(key=self.get_data_key(device_id), ex=300, **kwargs)
