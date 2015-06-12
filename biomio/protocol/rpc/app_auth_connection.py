from genericpath import exists
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

    def _find_connected_extension(self, callback):
        """
        Finds if any extension is connected to server.
        :return: Connected extension id.
        """

        if self._app_id and self.is_probe_owner():
            AppConnectionManager.instance().get_connected_apps(self._app_id, callback=callback)

    def _set_keys_for_connected_probes(self, extension_id, on_behalf_of):
        self.extension_id = extension_id
        AppConnectionManager.instance().get_connected_apps(app_id=on_behalf_of, extension=True,
                                                           callback=self.get_set_keys_for_connected_probes_callback())

    def get_set_keys_for_connected_probes_callback(self):
        def _set_keys_for_connected_probes_callback(probes_list):
            probes_list = probes_list.get('result') if probes_list is not None else []
            for probe_id in probes_list:
                key = self._listener.auth_key(extension_id=self.extension_id, probe_id=probe_id)
                self.extension_keys.append(key)
            if self.extension_keys:
                #TODO: refactor
                self.store_data(state='auth_wait')
        return _set_keys_for_connected_probes_callback

    def set_app_connected(self, app_auth_data_callback):
        """
        Links application to auth status key.
        :param app_auth_data_callback: Callback will be called when auth data is available.
        """
        # Start listen to auth data changes
        self._app_auth_data_callback = app_auth_data_callback
        self._listener.subscribe(callback=self._on_connection_data)
        if self.is_probe_owner():
            app_key_pattern = AppConnectionListener.app_key_pattern(app_id=self._app_id, app_type=self._app_type)
            existing_keys = AuthStateStorage.instance().get_matching_keys(pattern=app_key_pattern)
            if existing_keys:
                self._app_key = existing_keys[0]
            self.remove_extension_keys_that_are_not_connected()

    def remove_extension_keys_that_are_not_connected(self):
        extension_id = AppConnectionListener.extension_id(redis_auth_key=self._app_key)
        pattern = AppConnectionListener.app_key_pattern(app_id=extension_id, app_type='extension')
        keys_to_remove = AuthStateStorage.instance().get_matching_keys(pattern)
        if self._app_key in keys_to_remove:
            keys_to_remove.remove(self._app_key)
        AuthStateStorage.instance().remove_keys(keys=keys_to_remove)

    def set_app_disconnected(self):
        """
        Unsubscribes app from auth status key changes.
        """
        self._listener.unsubscribe()

    def start_auth(self, on_behalf_of):
        if self.is_extension_owner():
            self._set_keys_for_connected_probes(extension_id=self._app_id, on_behalf_of=on_behalf_of)

    def end_auth(self):
        AuthStateStorage.instance().remove_probe_data(self._app_key)
        self._app_key = None

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
        key = self._listener.auth_key(extension_id=connected_extension_id, probe_id=connected_probe_id)
        if self._app_key is None or self._app_key != key:
            if AuthStateStorage.instance().probe_data_exists(id=key):
                if self.is_probe_owner():
                    self.remove_extension_keys_that_are_not_connected()
                else:
                    self.extension_keys = []

        data = AuthStateStorage.instance().get_probe_data(id=self._app_key)
        if data:
            self._app_auth_data_callback(data)


