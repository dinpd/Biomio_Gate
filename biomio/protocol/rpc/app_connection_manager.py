from threading import Lock
from biomio.constants import REDIS_ACTIVE_DEVICES_KEY
from biomio.protocol.data_stores.application_data_store import ApplicationDataStore
from biomio.protocol.storage.redis_storage import RedisStorage

__author__ = 'alexchmykhalo'


class AppConnectionManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._persistence_redis = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = AppConnectionManager()
        return cls._instance

    @staticmethod
    def get_connected_apps(app_id, callback, device=False):
        """
        Generates list of connected app id for the given app.
        :param app_id: Application id for which get connected apps.
        :return: List of connected app ids.
        """

        if device:
            ApplicationDataStore.instance().get_extension_ids_by_probe_id(probe_id=app_id, callback=callback)
        else:
            ApplicationDataStore.instance().get_probe_ids_by_user_email(email=app_id, callback=callback)

    def add_active_app(self, current_app_id, app_id_to_add):
        """
            Added specified device_id to the list of active (connected) devices of given extension_id
        :param current_app_id: Application to store list for
        :param app_id_to_add: to add to the list of application's active apps
        """
        existing_active_apps = self.get_active_apps(current_app_id)
        if app_id_to_add not in existing_active_apps:
            self._persistence_redis.append_value_to_list(key=REDIS_ACTIVE_DEVICES_KEY % current_app_id,
                                                         value=app_id_to_add, append_to_head=True)

    def remove_active_app(self, current_app_id, app_id_to_remove):
        """
            Removes specified app_id_to_remove from given application's active_app_list
        :param current_app_id: Application to remove connection for.
        :param app_id_to_remove: to remove from active app list
        """
        self._persistence_redis.remove_value_from_list(key=REDIS_ACTIVE_DEVICES_KEY % current_app_id,
                                                       value=app_id_to_remove)

    def get_active_apps(self, current_app_id):
        """
            Gets the list of active (connected) devices from the redis for given extension_id
        :param current_app_id: to get active apps list for.
        :return: list of active devices
        """
        return self._persistence_redis.get_stored_list(key=REDIS_ACTIVE_DEVICES_KEY % current_app_id)

    def delete_active_apps_list(self, current_app_id):
        self._persistence_redis.delete_data(REDIS_ACTIVE_DEVICES_KEY % current_app_id)
