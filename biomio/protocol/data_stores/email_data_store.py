from threading import Lock
from biomio.constants import EMAILS_TABLE_CLASS_NAME, REDIS_EMAILS_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class EmailDataStore(BaseDataStore):
    _instance = None
    _lock = Lock()
    _table_class_name = EMAILS_TABLE_CLASS_NAME

    USER_ID_ATTR = 'profileId'
    EMAIL_ATTR = 'email'
    PRIMARY_ATTR = 'primary'

    _KEYS_TO_DELETE = [REDIS_EMAILS_KEY]

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = EmailDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(email):
        return REDIS_EMAILS_KEY % email

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, email, callback):
        self._get_lru_data(key=self.get_data_key(email=email), table_class_name=self._table_class_name,
                           object_id=email, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, email, **kwargs):
        pass

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, email):
        pass

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, email, **kwargs):
        if 'email' not in kwargs:
            kwargs.update({'email': email})
        self._store_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name, object_id=email,
                             **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, emails, callback):
        self._select_data_by_ids(table_class_name=self._table_class_name, object_ids=emails, callback=callback)

    def get_keys_to_delete(self):
        return self._KEYS_TO_DELETE

    def get_primary_email(self, user_id, callback):
        self._get_lru_data(key=self.get_data_key(email=user_id), table_class_name=self._table_class_name,
                           object_id=user_id, callback=callback, custom_search_attr=self.USER_ID_ATTR,
                           additional_query_params=dict(primary=True))
