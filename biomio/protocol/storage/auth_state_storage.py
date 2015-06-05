from biomio.protocol.storage.redis_storage import RedisStorage

import ast

import logging
logger = logging.getLogger(__name__)


class AuthStateStorage:
    """
    The AuthStateStorage class is responsible for storing current authentication state related information.
    """
    _instance = None

    def __init__(self):
        self._persistence_redis = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        """
        Creates if necessary and returns AuthStateStorage singleton instance.
        :return: AuthStateStorage singleton instance.
        """
        if not cls._instance:
            cls._instance = AuthStateStorage()

        return cls._instance

    def get_probe_data(self, id, key=None):
        """
        Gets custom auth state data.
        :param id: Auth state key id.
        :param key: Data key that should be retrieved. If None - dictionary containing all data will be retrieved.
        :return: Auth state data.
        """
        data = self._persistence_redis.get_data(key=id)
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)

        if key:
            data = data.get(key, None)

        return data

    def store_probe_data(self, id, ttl=None, **kwargs):
        """
        Stores custom auth state data.
        :param id: Auth state key id.
        :param ttl: Auth state key expiry timeout.
        :param kwargs: Custom data to store.
        """
        self._persistence_redis.store_data(key=id, ex=ttl, **kwargs)

    def remove_probe_data(self, key):
        """
        Removes custom auth state data.
        :param id: Auth state key id.
        """
        self._persistence_redis.delete_data(key=key)

    def probe_data_exists(self, id):
        """
        Checks if existing Redis key exists.
        :param id: Auth state key id.
        :return: True if key exists; False otherwise.
        """
        return self._persistence_redis.exists(key=id)

    def move_connected_app_data(self, src_key, dst_key, ttl=None):
        """
        Moves auth data from source key to destination. Source ky will be removed after moving.
        Moving performed as one atomic operation.
        :param src_key: Source key containing data.
        :param dst_key: Destination key where data should be moved.
        :param ttl: Auth state key expiry timeout.
        """
        self._persistence_redis.move_data(src_key=src_key, dst_key=dst_key, ex=ttl)

    def remove_keys(self, keys):
        self._persistence_redis.remove_keys(keys=keys)

    def get_matching_keys(self, pattern):
        return self._persistence_redis.find_keys(pattern=pattern)
