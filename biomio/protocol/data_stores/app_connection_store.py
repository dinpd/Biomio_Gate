from __future__ import absolute_import
from threading import Lock
from biomio.constants import REDIS_ACTIVE_DEVICES_KEY
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.biomio_decorators import inherit_docstring_from


class AppConnectionStore(BaseDataStore):
    _instance = None
    _lock = Lock()

    def __init__(self):
        BaseDataStore.__init__(self)

    @classmethod
    @inherit_docstring_from(BaseDataStore)
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = AppConnectionStore()
        return cls._instance

    @staticmethod
    @inherit_docstring_from(BaseDataStore)
    def get_data_key(app_id):
        return REDIS_ACTIVE_DEVICES_KEY % app_id

    @inherit_docstring_from(BaseDataStore)
    def get_data(self, app_id, callback=None):
        self._get_persistence_data(self.get_data_key(app_id))

    @inherit_docstring_from(BaseDataStore)
    def store_data(self, app_id, ttl=None, **kwargs):
        self._store_persistence_data(self.get_data_key(app_id), ex=ttl, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def delete_data(self, app_id):
        self.delete_custom_persistence_redis_data(self.get_data_key(app_id))

    @inherit_docstring_from(BaseDataStore)
    def update_data(self, app_id, ttl=None, **kwargs):
        self._store_persistence_data(self.get_data_key(app_id), ex=ttl, **kwargs)

    @inherit_docstring_from(BaseDataStore)
    def select_data_by_ids(self, object_ids, callback):
        pass

    def add_active_app(self, current_app_id, app_id_to_add):
        """
            Added specified device_id to the list of active (connected) devices of given extension_id
        :param current_app_id: Application to store list for
        :param app_id_to_add: to add to the list of application's active apps
        """
        existing_active_apps = self.get_active_apps(current_app_id)
        if app_id_to_add not in existing_active_apps:
            self._append_value_to_list(key=self.get_data_key(current_app_id), value=app_id_to_add, to_head=True)

    def remove_active_app(self, current_app_id, app_id_to_remove):
        """
            Removes specified app_id_to_remove from given application's active_app_list
        :param current_app_id: Application to remove connection for.
        :param app_id_to_remove: to remove from active app list
        """
        self._remove_value_from_list(key=self.get_data_key(current_app_id), value=app_id_to_remove)

    def get_active_apps(self, current_app_id):
        """
            Gets the list of active (connected) devices from the redis for given extension_id
        :param current_app_id: to get active apps list for.
        :return: list of active devices
        """
        return self._get_stored_list(key=self.get_data_key(current_app_id))

    def delete_active_apps_list(self, current_app_id):
        self._delete_stored_list(key=self.get_data_key(current_app_id))
