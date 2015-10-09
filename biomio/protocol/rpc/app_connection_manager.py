from threading import Lock
from biomio.protocol.data_stores.app_connection_store import AppConnectionStore
from biomio.protocol.data_stores.application_data_store import ApplicationDataStore

__author__ = 'alexchmykhalo'


class AppConnectionManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._app_connection_store = AppConnectionStore.instance()

    @classmethod
    def instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = AppConnectionManager()
        return cls._instance

    @staticmethod
    def get_connected_apps(app_id, callback, probe_device=False):
        """
        Generates list of connected app id for the given app.
        :param app_id: Application id for which get connected apps.
        :return: List of connected app ids.
        """

        if probe_device:
            ApplicationDataStore.instance().get_extension_ids_by_probe_id(probe_id=app_id, callback=callback)
        else:
            ApplicationDataStore.instance().get_probe_ids_by_user_email(email=app_id, callback=callback)

    def add_active_app(self, current_app_id, app_id_to_add):
        self._app_connection_store.add_active_app(current_app_id=current_app_id, app_id_to_add=app_id_to_add)

    def remove_active_app(self, current_app_id, app_id_to_remove):
        self._app_connection_store.remove_active_app(current_app_id=current_app_id, app_id_to_remove=app_id_to_remove)

    def get_active_apps(self, current_app_id):
        return self._app_connection_store.get_active_apps(current_app_id=current_app_id)

    def delete_active_apps_list(self, current_app_id):
        self._app_connection_store.delete_active_apps_list(current_app_id=current_app_id)

    def mark_app_active(self, app_id, probe_device=False):
        if probe_device:
            self._app_connection_store.add_active_probe_device(probe_id=app_id)
        else:
            self._app_connection_store.add_active_client_connection(client_app_id=app_id)

    def mark_app_off(self, app_id, probe_device=False):
        if probe_device:
            self._app_connection_store.remove_active_probe_device(probe_id=app_id)
        else:
            self._app_connection_store.remove_active_client_connection(client_app_id=app_id)

    def get_on_apps(self, probe_device=False):
        if probe_device:
            return self._app_connection_store.get_active_client_connections()
        return self._app_connection_store.get_active_probe_devices()
