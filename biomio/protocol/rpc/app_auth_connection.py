from genericpath import exists
from biomio.protocol.rpc.app_connection_listener import AppConnectionListener
from biomio.protocol.rpc.app_connection_manager import AppConnectionManager
from biomio.protocol.storage.auth_state_storage import AuthStateStorage
from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)


class AppAuthConnection:
    """
    AppAuthConnection class is responsible for connection between probe and extension during the auth.
    """
    def __init__(self, app_id, app_type):
        self._app_key = None
        self._app_id = app_id
        self._app_type = app_type
        self._listener = AppConnectionListener(app_id=app_id, app_type=app_type)
        self.extension_keys = []
        self._app_auth_data_callback = None

    def is_probe_owner(self):
        """
        Checks if probe connection is owner of this object.
        :return: Returns True if probe is owner; returns False otherwise.
        """
        return self._app_type.lower().startswith('probe')

    def is_extension_owner(self):
        """
        Checks if extension connection is owner of this object.
        :return: Returns True if extension is owner; returns False otherwise.
        """
        return self._app_type.lower().startswith('extension')

    def _set_keys_for_connected_app(self, on_behalf_of=None):
        connected_apps = AppConnectionManager.instance().get_active_apps(self._app_id)
        if len(connected_apps):
            existing_connected_app_apps = AppConnectionManager.instance().get_active_apps(connected_apps[0])
            for connected_app in existing_connected_app_apps:
                AppConnectionManager.instance().remove_active_app(connected_app, connected_apps[0])
            AppConnectionManager.instance().add_active_app(connected_apps[0], self._app_id)
            if self.is_probe_owner():
                new_app_key = self._listener.auth_key(extension_id=connected_apps[0], probe_id=self._app_id)
            else:
                new_app_key = self._listener.auth_key(extension_id=self._app_id, probe_id=connected_apps[0])
            if self._app_key is None or self._app_key != new_app_key:
                self.remove_extension_keys_that_are_not_connected()
                self._app_key = new_app_key
                self.extension_keys = []
            self.extension_keys = [self._app_key]
            self.store_data(state='auth_wait')
        else:
            app_id = self._app_id if on_behalf_of is None else on_behalf_of
            AppConnectionManager.get_connected_apps(app_id=app_id, device=self.is_probe_owner(),
                                                    callback=self._get_keys_for_connected_apps_callback())

    def _get_keys_for_connected_apps_callback(self):
        def _set_keys_for_connected_app_callback(app_ids):
            app_ids = app_ids.get('result') if app_ids else []
            for app_id in app_ids:
                AppConnectionManager.instance().add_active_app(app_id, self._app_id)
        return _set_keys_for_connected_app_callback

    def set_app_connected(self, app_auth_data_callback):
        """
        Links application to auth status key.
        :param app_auth_data_callback: Callback will be called when auth data is available.
        """
        # Start listen to auth data changes
        if self._app_auth_data_callback is None:
            self._app_auth_data_callback = app_auth_data_callback
            self._listener.subscribe(callback=self._on_connection_data)
        if self.is_probe_owner():
            self._set_keys_for_connected_app()
            app_key_pattern = AppConnectionListener.app_key_pattern(app_id=self._app_id, app_type=self._app_type)
            existing_keys = AuthStateStorage.instance().get_matching_keys(pattern=app_key_pattern)
            if len(existing_keys) and 'code_' in existing_keys[0]:
                self._app_key = existing_keys[0]
            if self._app_key in existing_keys:
                existing_keys.remove(self._app_key)
            AuthStateStorage.instance().remove_keys(keys=existing_keys)
            self.remove_extension_keys_that_are_not_connected()

    def remove_extension_keys_that_are_not_connected(self):
        if self._app_key:
            extension_id = AppConnectionListener.extension_id(redis_auth_key=self._app_key)
            pattern = AppConnectionListener.app_key_pattern(app_id=extension_id, app_type='extension')
            keys_to_remove = AuthStateStorage.instance().get_matching_keys(pattern)
            if self._app_key in keys_to_remove:
                keys_to_remove.remove(self._app_key)
            AuthStateStorage.instance().remove_keys(keys=keys_to_remove)

    def set_app_disconnected(self, on_behalf_of=None):
        """
        Unsubscribes app from auth status key changes.
        """
        self._remove_disconnected_app_keys(on_behalf_of)
        self._listener.unsubscribe()

    def start_auth(self, on_behalf_of):
        if self.is_extension_owner():
            self._set_keys_for_connected_app(on_behalf_of=on_behalf_of)

    def end_auth(self):
        self._remove_disconnected_app_keys(clear_related_keys=False)
        self.remove_extension_keys_that_are_not_connected()
        key_to_remove = self._app_key
        self._app_key = None
        AuthStateStorage.instance().remove_probe_data(key_to_remove)

    def store_data(self, **kwargs):
        """
        Stores custom auth status data.
        :param kwargs: Auth data keys/values.
        """
        keys_to_set = []

        if self._app_key is None and self.is_extension_owner():
            keys_to_set = self.extension_keys
        elif self._app_key is not None:
            keys_to_set.append(self._app_key)

        if keys_to_set:
            for app_key in keys_to_set:
                AuthStateStorage.instance().store_probe_data(id=app_key, ttl=settings.bioauth_timeout, **kwargs)
        else:
            logger.error(msg='No keys to store data for app %s' % self._app_id)

    def get_data(self, key=None):
        """
        Gets custom auth status data.
        :param key: Data key that should be retrieved. If None - dictionary containing all data will be retrieved.
        :return: Auth state data.
        """
        result = None

        if self._app_key is not None:
            result = AuthStateStorage.instance().get_probe_data(id=self._app_key, key=key)

        return result

    def _redis_key(self, other_id):
        return self._listener.auth_key(
            extension_id=self._app_id if self.is_extension_owner() else other_id,
            probe_id=self._app_id if self.is_probe_owner() else other_id
        )

    def _remove_disconnected_app_keys(self, on_behalf_of=None, clear_related_keys=True):
        app_id = self._app_id if on_behalf_of is None else on_behalf_of
        self.clear_related_keys = clear_related_keys
        AppConnectionManager.get_connected_apps(app_id=app_id, device=self.is_probe_owner(),
                                                callback=self._get_disconnect_apps_callback())

    def _get_disconnect_apps_callback(self):
        def _disconnect_apps(app_ids):
            if self.clear_related_keys:
                app_ids = app_ids.get('result') if app_ids is not None else []
                logger.debug('App ids to remove connections for: %s' % app_ids)
                for app_id in app_ids:
                    AppConnectionManager.instance().remove_active_app(app_id, self._app_id)
            if self.is_probe_owner():
                AppConnectionManager.instance().delete_active_apps_list(self._app_id)
            if self.is_probe_owner() and self._app_key:
                self.remove_extension_keys_that_are_not_connected()
        return _disconnect_apps

    def _on_connection_data(self, connected_extension_id, connected_probe_id):
        """
        Callback that should be called when application got changes in subscribed namespace.
        :param connected_extension_id: Connected extension id.
        :param connected_probe_id: Connected probe id.
        """
        key = self._listener.auth_key(extension_id=connected_extension_id, probe_id=connected_probe_id)
        if self._app_key is None or self._app_key != key:
            if AuthStateStorage.instance().probe_data_exists(id=key):
                self._app_key = key
                if self.is_probe_owner():
                    self._remove_disconnected_app_keys(clear_related_keys=False)
                # else:
                #     self.extension_keys = []

        data = AuthStateStorage.instance().get_probe_data(id=self._app_key)
        if data:
            self._app_auth_data_callback(data)
