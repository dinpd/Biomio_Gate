from threading import Lock
from biomio.constants import WEB_RESOURCE_TABLE_CLASS_NAME, REDIS_WEB_RESOURCE_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class WebResourcesStore(BaseDataStore):
    _instance = None
    _table_class_name = WEB_RESOURCE_TABLE_CLASS_NAME
    _lock = Lock()

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = WebResourcesStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(resource_id):
        return REDIS_WEB_RESOURCE_KEY % resource_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, resource_id, callback):
        self._get_lru_data(key=self.get_data_key(resource_id), table_class_name=self._table_class_name,
                           object_id=resource_id, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, object_id, **kwargs):
        raise NotImplementedError

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, object_id, **kwargs):
        raise NotImplementedError

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, object_id):
        raise NotImplementedError

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, object_ids, callback):
        raise NotImplementedError
