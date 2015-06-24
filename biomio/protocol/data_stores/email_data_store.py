from biomio.constants import EMAILS_TABLE_CLASS_NAME, REDIS_EMAILS_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.worker.storage_jobs import verify_email_job, generate_pgp_keys_job
from biomio.utils.biomio_decorators import inherit_docstring_from


class EmailDataStore(BaseDataStore):
    _instance = None
    _table_class_name = EMAILS_TABLE_CLASS_NAME

    # Names of attributes of the corresponding Entity class.
    PASS_PHRASE_ATTR = 'pass_phrase'
    PUBLIC_PGP_KEY_ATTR = 'public_pgp_key'
    PRIVATE_PGP_KEY_ATTR = 'private_pgp_key'
    USER_ATTR = 'user'

    _KEYS_TO_DELETE = [REDIS_EMAILS_KEY]

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

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, emails, callback):
        self._select_data_by_ids(table_class_name=self._table_class_name, object_ids=emails, callback=callback)

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, email, **kwargs):
        self._update_lru_data(key=self.get_data_key(email), table_class_name=self._table_class_name, object_id=email,
                              **kwargs)

    def update_emails_pgp_keys(self, emails, callback):
        """
            Runs job to create new user with given email and generate pgp keys for him.
        :param emails: list of emails to create users for.
        :param callback: function that must be executed after all jobs are completed.
        """
        callback_code = self._subscribe_redis_callback(callback=callback)
        result_code = self._activate_results_gatherer(len(emails))
        for email in emails:
            self._run_storage_job(verify_email_job, table_class_name=self._table_class_name, email=email,
                                  callback_code=callback_code, result_code=result_code)

    def generate_pgp_keys_by_ai_request(self, email):
        """
            Generates PGP keys for email received from AI
        :param email: to generate PGP key pair for.
        """
        self._run_storage_job(generate_pgp_keys_job, table_class_name=self._table_class_name, email=email)

    def get_keys_to_delete(self):
        return self._KEYS_TO_DELETE
