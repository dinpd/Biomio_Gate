from biomio.protocol.storage.probe_results_storage import ProbeResultsStorage
from biomio.protocol.rpc.app_connection_listener import AppConnectionListener

import logging
logger = logging.getLogger(__name__)

from biomio.protocol.storage.redis_storage import RedisStorage

class ProbeResultsStorage:
    _instance = None

    def __init__(self):
        self._persistence_redis = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ProbeResultsStorage()

        return cls._instance

    def get_probe_data(self, id, key):
        data = self._persistence_redis.get_data(key=id)
        return data.get(key, None)

    def store_probe_data(self, id, ttl=None, **kwargs):
        self._persistence_redis.store_data(key=id, ex=ttl, **kwargs)

    def remove_probe_data(self, id):
        self._persistence_redis.delete_data(id)


class AppAuthConnection():
    def __init__(self, app_id, app_type):
        self._app_key = None
        self._app_id = app_id
        self._app_type = app_type
        self._listener = AppConnectionListener(app_id=app_id, app_type=app_type)

    def link_app(self, app_auth_data_callback):
        self._listener.subscribe(callback=app_auth_data_callback)

    def unlink_app(self):
        self._listener.unsubscribe()

    def _initialize_auth_key(self):
        if self._app_type == 'extension':
            self._app_key = self._listener._auth_key(extension_id=self._app_id)
            # ProbeResultsStorage.instance().get_probe_data(id=)


