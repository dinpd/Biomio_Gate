from __future__ import absolute_import
from threading import Lock
from biomio.constants import REDIS_APPLICATION_KEY, APPS_TABLE_CLASS_NAME, REDIS_DEVICE_INFORMATION_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class ApplicationDataStore(BaseDataStore):
    _instance = None
    _table_class_name = APPS_TABLE_CLASS_NAME
    _lock = Lock()

    # Names of attributes of the corresponding Entity class.
    APP_ID_ATTR = 'app_id'
    APP_TYPE_ATTR = 'app_type'
    PUBLIC_KEY_ATTR = 'public_key'
    USER_ATTR = 'users'

    _KEYS_TO_DELETE = [REDIS_APPLICATION_KEY, REDIS_DEVICE_INFORMATION_KEY]

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
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
                           callback=callback, to_dict=True)

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, app_id, **kwargs):
        if self.APP_ID_ATTR not in kwargs:
            kwargs.update({self.APP_ID_ATTR: app_id})
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

    def get_probe_ids_by_user_email(self, email, callback):
        self._get_app_ids_by_app_id(table_class_name=self._table_class_name, object_id=email, callback=callback,
                                    probes=True)

    def get_extension_ids_by_probe_id(self, probe_id, callback):
        self._get_app_ids_by_app_id(table_class_name=self._table_class_name, object_id=probe_id, callback=callback)

    def get_keys_to_delete(self):
        return self._KEYS_TO_DELETE

    def assign_user_to_extension(self, app_id, email):
        self._run_storage_job(self._worker.ASSIGN_USER_TO_EXTENSION_JOB, table_class_name=self._table_class_name,
                              app_id=app_id, email=email)

    def register_application(self, code, app_type, callback):
        self._run_storage_job(self._worker.VERIFY_REGISTRATION_JOB, callback, code=code, app_type=app_type)
