from biomio.protocol.rpc.app_connection_listener import AppConnectionListener
from biomio.protocol.rpc.app_connection_manager import AppConnectionManager
from biomio.protocol.storage.auth_state_storage import AuthStateStorage
from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)


class AppAuthConnection():
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

        self._initialize_auth_key()

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

    def _find_connected_extension(self):
        """
        Finds if any extension is connected to server.
        :return: Connected extension id.
        """
        extension_id = None

        if self._app_id and self.is_probe_owner():
            connected_apps = AppConnectionManager.instance().get_connected_apps(self._app_id)
            if connected_apps is not None:
                for app_id in connected_apps:
                    data = AuthStateStorage.instance().get_probe_data(id=self._redis_key(other_id=app_id))
                    if data:
                        extension_id = app_id
                        break

        return extension_id

    def _connect_to_extension(self, extension_id):
        probes_list = AppConnectionManager.instance().get_connected_apps(app_id=extension_id)
        for probe_id in probes_list:
            key = self._listener.auth_key(extension_id=extension_id, probe_id=probe_id)
            if probe_id == self._app_id:
                self._app_key = key
            else:
                # TODO: remove key
                pass

    def _set_keys_for_connected_probes(self, extension_id):
        probes_list = AppConnectionManager.instance().get_connected_apps(app_id=extension_id)
        for probe_id in probes_list:
            key = self._listener.auth_key(extension_id=extension_id, probe_id=probe_id)
            self.extension_keys.append(key)

    def set_app_connected(self, app_auth_data_callback):
        """
        Links application to auth status key.
        :param app_auth_data_callback: Callback will be called when auth data is available.
        """
        # Start listen to auth data changes
        self._app_auth_data_callback = app_auth_data_callback
        self._listener.subscribe(callback=self._on_connection_data)

        if self.is_probe_owner():
            # In a case of probe - find connected extension
            extension_id = self._find_connected_extension()
            if extension_id:
                # Extension connected and auth started
                # TODO: remove all other extension keys using Lua script
                self._connect_to_extension(extension_id=extension_id)

    def set_app_disconnected(self):
        """
        Unsubscribes app from auth status key changes.
        """
        self._listener.unsubscribe()

    def start_auth(self, on_behalf_of=None):
        if self.is_extension_owner():
            self._set_keys_for_connected_probes(extension_id=self._app_id)

    def end_auth(self):
        AuthStateStorage.instance().remove_probe_data(self._app_key)
        self._app_key = None

    def _initialize_auth_key(self):
        if self.is_probe_owner():
            self._app_key = self._listener.auth_key(extension_id=self._app_id)

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

    def _on_connection_data(self, connected_extension_id, connected_probe_id):
        """
        Callback that should be called when application got changes in subscribed namespace.
        :param connected_extension_id: Connected extension id.
        :param connected_probe_id: Connected probe id.
        """
        if self._app_key is None:
            key = self._listener.auth_key(extension_id=connected_extension_id, probe_id=connected_probe_id)

            if AuthStateStorage.instance().probe_data_exists(id=key):
                if self.is_probe_owner():
                    self._connect_to_extension(extension_id=connected_extension_id)
                else:
                    self._app_key = key
                    self.extension_keys = []

        data = AuthStateStorage.instance().get_probe_data(id=self._app_key)
        if data:
            self._app_auth_data_callback(data)


