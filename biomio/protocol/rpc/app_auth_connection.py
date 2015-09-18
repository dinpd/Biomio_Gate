import logging

from biomio.constants import PROBE_APP_TYPE_PREFIX
from biomio.protocol.rpc.app_connection_listener import AppConnectionListener
from biomio.protocol.rpc.app_connection_manager import AppConnectionManager
from biomio.protocol.settings import settings
from biomio.protocol.storage.auth_state_storage import AuthStateStorage

logger = logging.getLogger(__name__)


class AppAuthConnection:
    def __init__(self, app_id, app_type):
        self._app_id = app_id
        self._app_type = app_type
        self._connection_listener = AppConnectionListener(app_id, app_type)
        self._connection_manager = AppConnectionManager.instance()
        self._app_connection_callback = None
        self._on_behalf_of = None
        self._app_key = None

    def _is_probe_device(self):
        return self._app_type.lower().startswith(PROBE_APP_TYPE_PREFIX)

    def _setup_app_connections(self, on_behalf_of=None):
        if on_behalf_of is None or (self._on_behalf_of is not None and self._on_behalf_of == on_behalf_of):
            connected_apps = self._connection_manager.get_active_apps(current_app_id=self._app_id)
            if len(connected_apps):
                connected_app = connected_apps[0]
                existing_connections = self._connection_manager.get_active_apps(current_app_id=connected_app)
                for existing_connection in existing_connections:
                    self._connection_manager.remove_active_app(existing_connection, connected_app)
                for other_connected_app in connected_apps:
                    self._connection_manager.remove_active_app(other_connected_app, self._app_id)
                self._connection_manager.add_active_app(connected_app, self._app_id)
                if self._is_probe_device():
                    new_app_key = self._connection_listener.auth_key(extension_id=connected_apps[0],
                                                                     probe_id=self._app_id)
                else:
                    new_app_key = self._connection_listener.auth_key(extension_id=self._app_id,
                                                                     probe_id=connected_apps[0])
                if self._app_key is None or self._app_key != new_app_key:
                    self._remove_app_keys(with_probe_keys=not self._is_probe_device())
                    self._app_key = new_app_key
                    self._remove_app_keys(with_probe_keys=not self._is_probe_device())
                logger.debug('Setup APP connections app_key - %s' % self._app_key)
                self.store_data(state='auth_wait')
                return
        if on_behalf_of is not None and self._on_behalf_of != on_behalf_of:
            self._on_behalf_of = on_behalf_of
        curr_app_id = self._on_behalf_of if self._on_behalf_of is not None else self._app_id
        self._connection_manager.get_connected_apps(app_id=curr_app_id, probe_device=self._is_probe_device(),
                                                    callback=self._setup_available_apps_callback())

    def _setup_available_apps_callback(self):
        def _setup_available_apps(available_apps):
            available_apps = available_apps.get('result') if available_apps else []
            logger.debug('Activation following apps - %s , for current app - %s' % (available_apps, self._app_id))
            for app_id in available_apps:
                self._connection_manager.add_active_app(app_id, self._app_id)

        return _setup_available_apps

    def _remove_app_keys(self, with_probe_keys=True):
        if self._app_key is not None:
            extension_id = self._connection_listener.extension_id(self._app_key)
            pattern = self._connection_listener.app_key_pattern(app_id=extension_id, app_type='extension')
            existing_app_keys = AuthStateStorage.instance().get_matching_keys(pattern)
            if with_probe_keys:
                probe_id = self._connection_listener.probe_id(self._app_key)
                probe_pattern = self._connection_listener.app_key_pattern(app_id=probe_id, app_type='probe')
                existing_app_keys.extend(AuthStateStorage.instance().get_matching_keys(probe_pattern))
            while self._app_key in existing_app_keys:
                existing_app_keys.remove(self._app_key)
            logger.debug('Removing following app auth keys - %s' % existing_app_keys)
            AuthStateStorage.instance().remove_keys(keys=existing_app_keys)

    def _remove_related_active_apps(self, clear_related_keys=True):
        app_id = self._on_behalf_of if self._on_behalf_of is not None else self._app_id
        self._clear_related_keys = clear_related_keys
        if not clear_related_keys:
            logger.debug('Clearing active apps for probe device - %s' % self._app_id)
            if self._is_probe_device():
                self._connection_manager.delete_active_apps_list(self._app_id)
            if self._is_probe_device() and self._app_key:
                self._remove_app_keys()
        else:
            self._connection_manager.get_connected_apps(app_id=app_id, probe_device=self._is_probe_device(),
                                                        callback=self._remove_related_apps_callback())

    def _remove_related_apps_callback(self):
        def _disconnect_apps(app_ids):
            app_ids = app_ids.get('result') if app_ids is not None else []
            logger.debug('App ids to remove connections for: %s' % app_ids)
            for app_id in app_ids:
                self._connection_manager.remove_active_app(app_id, self._app_id)
            if self._is_probe_device():
                self._connection_manager.delete_active_apps_list(self._app_id)
            if self._is_probe_device() and self._app_key:
                self._remove_app_keys()

        return _disconnect_apps

    def set_app_disconnected(self, on_behalf_of=None):
        """
        Unsubscribes app from auth status key changes.
        """
        self._remove_related_active_apps(on_behalf_of)
        self._connection_listener.unsubscribe()

    def start_auth(self, on_behalf_of):
        if not self._is_probe_device():
            self._setup_app_connections(on_behalf_of=on_behalf_of)

    def end_auth(self):
        self._remove_related_active_apps(clear_related_keys=False)
        self._remove_app_keys()
        key_to_remove = self._app_key
        self._app_key = None
        AuthStateStorage.instance().remove_probe_data(key_to_remove)

    def store_data(self, **kwargs):
        """
        Stores custom auth status data.
        :param kwargs: Auth data keys/values.
        """
        keys_to_set = []

        if self._app_key is not None:
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

    def set_app_connected(self, app_auth_data_callback):
        if self._app_connection_callback is None:
            self._app_connection_callback = app_auth_data_callback
            self._connection_listener.subscribe(callback=self._on_connection_data)
        if self._is_probe_device():
            self._setup_app_connections()
            app_key_pattern = AppConnectionListener.app_key_pattern(app_id=self._app_id, app_type=self._app_type)
            existing_keys = AuthStateStorage.instance().get_matching_keys(pattern=app_key_pattern)
            if len(existing_keys) and 'code_' in existing_keys[0]:
                self._app_key = existing_keys[0]
            logger.debug('Set APP Connected - Probe device app_key - %s' % self._app_key)
            self._remove_app_keys()

    def _on_connection_data(self, connected_extension_id, connected_probe_id):
        """
        Callback that should be called when application got changes in subscribed namespace.
        :param connected_extension_id: Connected extension id.
        :param connected_probe_id: Connected probe id.
        """
        key = self._connection_listener.auth_key(extension_id=connected_extension_id, probe_id=connected_probe_id)
        logger.debug('Received connected apps - %s - %s' % (connected_extension_id, connected_probe_id))
        if self._app_key is None or self._app_key != key:
            if AuthStateStorage.instance().probe_data_exists(id=key):
                self._app_key = key
                if self._is_probe_device():
                    self._remove_related_active_apps(clear_related_keys=False)
                    # else:
                    #     self.extension_keys = []

        data = AuthStateStorage.instance().get_probe_data(id=self._app_key)
        logger.debug('On Connection data: Proceeding probe data - %s' % data)
        if data:
            self._app_connection_callback(data)
