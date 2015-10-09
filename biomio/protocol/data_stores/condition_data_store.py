from threading import Lock
from biomio.constants import REDIS_USER_CONDITION_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class ConditionDataStore(BaseDataStore):
    _instance = None
    _lock = Lock()

    CONDITION_ATTR = 'condition'
    AUTH_TYPES_ATTR = 'auth_types'

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = ConditionDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(user_id):
        return REDIS_USER_CONDITION_KEY % user_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, user_id, callback=None):
        return self._get_persistence_data(key=self.get_data_key(user_id=user_id))

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, user_id, **kwargs):
        self._store_persistence_data(key=self.get_data_key(user_id=user_id), **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, user_id, **kwargs):
        self._store_persistence_data(key=self.get_data_key(user_id=user_id), **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, user_id):
        self.delete_custom_persistence_redis_data(key=self.get_data_key(user_id=user_id))

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, user_ids, callback=None):
        pass


