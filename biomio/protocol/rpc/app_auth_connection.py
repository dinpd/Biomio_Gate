from biomio.protocol.rpc.app_connection_listener import AppConnectionListener
from biomio.protocol.rpc.app_connection_manager import AppConnectionManager
from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)

from biomio.protocol.storage.redis_storage import RedisStorage
import ast


class ProbeResultsStorage:
    _instance = None

    def __init__(self):
        self._persistence_redis = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ProbeResultsStorage()

        return cls._instance

    def get_probe_data(self, id, key=None):
        data = self._persistence_redis.get_data(key=id)
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)

        if key:
            data = data.get(key, None)

        return data

    def store_probe_data(self, id, ttl=None, **kwargs):
        self._persistence_redis.store_data(key=id, ex=ttl, **kwargs)

    def remove_probe_data(self, id):
        self._persistence_redis.delete_data(id)

    def move_connected_app_data(self, src_key, dst_key, ttl=None):
        self._persistence_redis.move_data(src_key=src_key, dst_key=dst_key, ex=ttl)


class AppAuthConnection():
    """
    AppAuthConnection class is responsible for connection between probe and extension during the auth.
    """
    def __init__(self, app_id, app_type):
        self._app_key = None
        self._app_id = app_id
        self._app_type = app_type
        self._listener = AppConnectionListener(app_id=app_id, app_type=app_type)
        self._buffered_data = {}
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
            for app_id in connected_apps:
                data = ProbeResultsStorage.instance().get_probe_data(id=self._listener.auth_key(extension_id=app_id))
                print data
                if data:
                    extension_id = app_id
                    break

        return extension_id

    def link_app(self, app_auth_data_callback):
        """
        Links application.
        :param app_auth_data_callback: Callback will be called when auth data is available.
        """
        # Start listen to auth data changes
        self._app_auth_data_callback = app_auth_data_callback
        self._listener.subscribe(callback=self._on_connection_data)

        # Create temporary key - includes only extension app id
        if self.is_extension_owner():
            self._app_key = self._listener.auth_key(extension_id=self._app_id)

        # In a case of probe - move extension key if any
        if self.is_probe_owner():
            extension_id = self._find_connected_extension()
            if extension_id:
                self._app_key = self._listener.auth_key(extension_id=extension_id, probe_id=self._app_id)
                extension_tmp_key = self._listener.auth_key(extension_id=extension_id)
                ProbeResultsStorage.instance().move_connected_app_data(src_key=extension_tmp_key, dst_key=self._app_key)

        self._sync_buffered_data()

    def unlink_app(self):
        self._listener.unsubscribe()

    def _initialize_auth_key(self):
        if self.is_probe_owner():
            self._app_key = self._listener.auth_key(extension_id=self._app_id)
            # ProbeResultsStorage.instance().get_probe_data(id=)

    def store_data(self, **kwargs):
        if self._app_key is not None:
            ProbeResultsStorage.instance().store_probe_data(id=self._app_key, ttl=settings.bioauth_timeout, **kwargs)
        else:
            self._buffered_data.update(**kwargs)

    def _sync_buffered_data(self):
        if self._app_id and self._buffered_data:
            self.store_data(**self._buffered_data)

    def get_data(self, key=None):
        result = None

        if self._app_key is not None:
            return ProbeResultsStorage.instance().get_probe_data(id=self._app_key, key=key)
        else:
            result = self._buffered_data

            if key is not None:
                result = result.get(key, None)

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
        if connected_probe_id not in self._app_key and self.is_extension_owner():
            self._app_key = self._listener.auth_key(extension_id=connected_extension_id, probe_id=connected_probe_id)

        data = ProbeResultsStorage.instance().get_probe_data(id=self._app_key)
        if data:
            self._app_auth_data_callback(data)


