from threading import Lock
from biomio.constants import POLICY_DATA_TABLE_CLASS_NAME, REDIS_USER_POLICY_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class PolicyDataStore(BaseDataStore):
    _instance = None
    _lock = Lock()
    _table_class_name = POLICY_DATA_TABLE_CLASS_NAME

    _KEYS_TO_DELETE = [REDIS_USER_POLICY_KEY]

    OWNER_ATTR = 'owner'
    NAME_ATTR = 'name'
    BIO_AUTH_ATTR = 'bioAuth'
    MIN_AUTH_ATTR = 'minAuth'
    MAX_AUTH_ATTR = 'maxAuth'
    MATCH_CERTAINTY_ATTR = 'matchCertainty'
    GEO_RESTRICTION_ATTR = 'geoRestriction'
    TIME_RESTRICTION_ATTR = 'timeRestriction'
    DATE_CREATED_ATTR = 'dateCreated'
    DATE_MODIFIED_ATTR = 'dateModified'

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = PolicyDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(owner_id):
        return REDIS_USER_POLICY_KEY % owner_id

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, owner_id, **kwargs):
        if 'owner' not in kwargs:
            kwargs.update({'owner': owner_id})
        self._store_lru_data(key=self.get_data_key(owner_id=owner_id), table_class_name=self._table_class_name,
                             object_id=owner_id, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, owner_id, callback):
        return self._get_lru_data(key=self.get_data_key(owner_id=owner_id), table_class_name=self._table_class_name,
                                  object_id=owner_id, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, owner_id):
        self._delete_lru_data(key=self.get_data_key(owner_id=owner_id), table_class_name=self._table_class_name,
                              object_id=owner_id)

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, owner_id, **kwargs):
        self._update_lru_data(key=self.get_data_key(owner_id=owner_id), table_class_name=self._table_class_name,
                              object_id=owner_id, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, owner_ids, callback):
        return self._select_data_by_ids(table_class_name=self._table_class_name, object_ids=owner_ids,
                                        callback=callback)

    def get_keys_to_delete(self):
        return self._KEYS_TO_DELETE
