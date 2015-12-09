from threading import Lock
from biomio.constants import PGP_KEYS_DATA_TABLE_CLASS_NAME, REDIS_PGP_DATA_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class PgpKeysDataStore(BaseDataStore):
    _instance = None
    _table_class_name = PGP_KEYS_DATA_TABLE_CLASS_NAME
    _lock = Lock()

    # Names of attributes of the corresponding Entity class.
    PASS_PHRASE_ATTR = 'pass_phrase'
    PUBLIC_PGP_KEY_ATTR = 'public_pgp_key'
    PRIVATE_PGP_KEY_ATTR = 'private_pgp_key'
    USER_ATTR = 'user'

    _KEYS_TO_DELETE = [REDIS_PGP_DATA_KEY]

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = PgpKeysDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(object_id):
        return REDIS_PGP_DATA_KEY % object_id

    def store_data(self, email, **kwargs):
        """
            Stores email data for specified user
        :param email: Email to save, e.g. example@mail.com
        :param kwargs: dictionary with vales, according to entities class:
                        pass_phrase: str pass phrase generated for this email
                        public_pgp_key: str public pgp key
                        private_pgp_key: str private pgp key (optional)
                        user: str user ID related to this email.
        """
        if 'email' not in kwargs:
            kwargs.update({'email': email})
        self._store_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name,
                             object_id=email, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, email):
        self._delete_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name, object_id=email)

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, email, callback, **kwargs):
        self._get_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name,
                           object_id=email, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, emails, callback):
        self._select_data_by_ids(table_class_name=self._table_class_name, object_ids=emails, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, email, **kwargs):
        self._update_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name, object_id=email,
                              **kwargs)

    def get_keys_to_delete(self):
        return self._KEYS_TO_DELETE
