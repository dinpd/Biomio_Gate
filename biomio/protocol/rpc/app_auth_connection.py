from biomio.constants import PROBE_APP_TYPE_PREFIX
from biomio.protocol.data_stores.device_information_store import DeviceInformationStore
from biomio.protocol.rpc.app_connection_listener import AppConnectionListener
from biomio.protocol.rpc.app_connection_manager import AppConnectionManager
from biomio.protocol.storage.auth_state_storage import AuthStateStorage
from biomio.protocol.settings import settings

import logging
from biomio.utils.utils import push_notification_callback

logger = logging.getLogger(__name__)


class AppAuthConnection:
    """
    AppAuthConnection class is responsible for connection between probe and extension during the auth.
    """

    def __init__(self, app_id, app_type):
        self._app_key = None
        self._app_id = app_id
        self._app_type = app_type
        self._connection_listener = AppConnectionListener(app_id=app_id, app_type=app_type)
        self._connection_manager = AppConnectionManager.instance()
        self.extension_keys = []
        self._app_auth_data_callback = None
        self._on_behalf_of = None
        self._push_notifications_callback = push_notification_callback(
            'Please open the app to proceed with Verification.')
        self._push_notifications_clear_callback = push_notification_callback('', clear=True)

    def is_probe_owner(self):
        """
        Checks if probe connection is owner of this object.
        :return: Returns True if probe is owner; returns False otherwise.
        """
        return self._app_type.lower().startswith(PROBE_APP_TYPE_PREFIX)

    def _set_keys_for_connected_app(self):
        if 'code_' in self._app_id:
            app_id = self._app_id
        else:
            app_id_parts = self._app_id.split('_')
            app_id = app_id_parts[0]
            self._on_behalf_of = app_id_parts[1] if len(app_id_parts) > 1 else None

        connected_apps = self._connection_manager.get_active_apps(app_id)
        if len(connected_apps) and self.is_probe_owner():
            # Looking for already connected extensions that are waiting for authentication.
            existing_connected_app_apps = self._connection_manager.get_active_apps(connected_apps[0].split('_')[0])
            for connected_app in existing_connected_app_apps:
                DeviceInformationStore.instance().get_data(app_id=connected_app,
                                                           callback=self._push_notifications_clear_callback)
                self._connection_manager.remove_active_app(connected_app, connected_apps[0])
            self._connection_manager.add_active_app(connected_apps[0].split('_')[0], self._app_id)
            new_app_key = self._connection_listener.auth_key(extension_id=connected_apps[0], probe_id=self._app_id)
            if self._app_key is None or self._app_key != new_app_key:
                self.remove_extension_keys_that_are_not_connected()
                self._app_key = new_app_key
                self.extension_keys = []
            self.extension_keys = [self._app_key]
            self.store_data(state='auth_wait')
        else:
            app_id = app_id if self._on_behalf_of is None else self._on_behalf_of
            AppConnectionManager.get_connected_apps(app_id=app_id, probe_device=self.is_probe_owner(),
                                                    callback=self._get_keys_for_connected_apps_callback())

    def _get_keys_for_connected_apps_callback(self):

        def _set_keys_for_connected_app_callback(app_ids):
            # App arrived first so we tell all its related probes/extensions that it is available for them
            app_ids = app_ids.get('result') if app_ids else []
            if not self.is_probe_owner():
                # Check if there are any connected probe devices for incoming extension
                act_app_id = self._app_id.split('_')[0]
                connected_probes = self._connection_manager.get_active_apps(act_app_id)
                if not len(connected_probes):
                    # Maybe device was connected before client app was registered
                    connected_probes = self._connection_manager.get_on_apps(probe_device=self.is_probe_owner())
                if len(connected_probes):
                    # Getting only probe devices that belong to current user.
                    matching_connections = list(set(connected_probes).intersection(set(app_ids)))
                    if len(matching_connections):
                        new_app_key = self._connection_listener.auth_key(extension_id=self._app_id,
                                                                         probe_id=matching_connections[0])
                        if self._app_key is None or self._app_key != new_app_key:
                            self.remove_extension_keys_that_are_not_connected()
                            self._app_key = new_app_key
                            self.extension_keys = []
                        self.extension_keys = [self._app_key]
                        self.store_data(state='auth_wait')
                        return
            for app_id in app_ids:
                if not self.is_probe_owner():
                    DeviceInformationStore.instance().get_data(app_id=app_id,
                                                               callback=self._push_notifications_callback)
                self._connection_manager.add_active_app(app_id, self._app_id)

        return _set_keys_for_connected_app_callback

    def set_app_connected(self, app_auth_data_callback):
        """
        Links application to auth status key.
        :param app_auth_data_callback: Callback will be called when auth data is available.
        """
        # Start listen to auth data changes
        if self._app_auth_data_callback is None:
            self._connection_manager.mark_app_active(app_id=self._app_id, probe_device=self.is_probe_owner())
            self._app_auth_data_callback = app_auth_data_callback
            self._connection_listener.subscribe(callback=self._on_connection_data)
        if self.is_probe_owner():
            self._set_keys_for_connected_app()
            app_key_pattern = self._connection_listener.app_key_pattern(app_id=self._app_id, app_type=self._app_type)
            existing_keys = AuthStateStorage.instance().get_matching_keys(pattern=app_key_pattern)
            if len(existing_keys) and 'code_' in existing_keys[0]:
                self._app_key = existing_keys[0]
            if self._app_key in existing_keys:
                existing_keys.remove(self._app_key)
            AuthStateStorage.instance().remove_keys(keys=existing_keys)
            self.remove_extension_keys_that_are_not_connected()

    def remove_extension_keys_that_are_not_connected(self):
        if self._app_key:
            extension_id = self._connection_listener.extension_id(redis_auth_key=self._app_key)
            pattern = self._connection_listener.app_key_pattern(app_id=extension_id, app_type='extension')
            keys_to_remove = AuthStateStorage.instance().get_matching_keys(pattern)
            if self._app_key in keys_to_remove:
                keys_to_remove.remove(self._app_key)
            AuthStateStorage.instance().remove_keys(keys=keys_to_remove)

    def set_app_disconnected(self):
        """
        Unsubscribes app from auth status key changes.
        """
        self._connection_manager.mark_app_off(app_id=self._app_id, probe_device=self.is_probe_owner())
        self._remove_disconnected_app_keys()
        self._connection_listener.unsubscribe()

    def start_auth(self):
        if not self.is_probe_owner():
            self._set_keys_for_connected_app()

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

        if self._app_key is None and not self.is_probe_owner():
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

    def _remove_disconnected_app_keys(self, clear_related_keys=True):
        app_id = self._app_id if self._on_behalf_of is None else self._on_behalf_of
        self.clear_related_keys = clear_related_keys
        AppConnectionManager.get_connected_apps(app_id=app_id, probe_device=self.is_probe_owner(),
                                                callback=self._get_disconnect_apps_callback())

    def get_client_id(self):
        if self._app_key is not None:
            return self._connection_listener.extension_id(self._app_key)
        return None

    def _get_disconnect_apps_callback(self):
        def _disconnect_apps(app_ids):
            if self.clear_related_keys:
                app_ids = app_ids.get('result') if app_ids is not None else []
                logger.debug('App ids to remove connections for: %s' % app_ids)
                for app_id in app_ids:
                    if not self.is_probe_owner():
                        DeviceInformationStore.instance().get_data(app_id=app_id,
                                                                   callback=self._push_notifications_clear_callback)
                    self._connection_manager.remove_active_app(app_id, self._app_id)
            if self.is_probe_owner():
                self._connection_manager.delete_active_apps_list(self._app_id)
            if self.is_probe_owner() and self._app_key:
                self.remove_extension_keys_that_are_not_connected()

        return _disconnect_apps

    def _on_connection_data(self, connected_extension_id, connected_probe_id):
        """
        Callback that should be called when application got changes in subscribed namespace.
        :param connected_extension_id: Connected extension id.
        :param connected_probe_id: Connected probe id.
        """
        key = self._connection_listener.auth_key(extension_id=connected_extension_id, probe_id=connected_probe_id)
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
