from biomio.constants import EMAILS_TABLE_CLASS_NAME, REDIS_EMAILS_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class EmailDataStore(BaseDataStore):
    _instance = None
    _table_class_name = EMAILS_TABLE_CLASS_NAME

    # Names of attributes of the corresponding Entity class.
    PASS_PHRASE_ATTR = 'pass_phrase'
    PUBLIC_PGP_KEY_ATTR = 'public_pgp_key'
    PRIVATE_PGP_KEY_ATTR = 'private_pgp_key'
    USER_ATTR = 'user'

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        if cls._instance is None:
            cls._instance = EmailDataStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(object_id):
        return REDIS_EMAILS_KEY % object_id

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
    def get_data(self, email, callback):
        self._get_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name,
                           object_id=email, callback=callback)