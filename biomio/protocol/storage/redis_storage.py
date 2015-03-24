import ast
from redis.client import StrictRedis
from biomio.constants import REDIS_CONFIG_MAX_MEMORY_OPTION_KEY, REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY, \
    REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY
from biomio.protocol.settings import settings


class RedisStorage():
    _lru_instance = None
    _persistence_instance = None

    def __init__(self, lru_instance=True):
        if lru_instance:
            self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)
            self._configure_redis_instance()
        else:
            self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)

    def _configure_redis_instance(self):
        self._redis.config_set(REDIS_CONFIG_MAX_MEMORY_OPTION_KEY, settings.redis_max_memory)
        self._redis.config_set(REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY, settings.redis_eviction_policy)
        self._redis.config_set(REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY, settings.redis_max_memory_samples)

    @classmethod
    def lru_instance(cls):
        """
            Returns current RedisStorage LRU instance. If it doesn't exist creates new one.

        :return: RedisStorage LRU instance.
        """
        if cls._lru_instance is None:
            cls._lru_instance = RedisStorage()
        return cls._lru_instance

    @classmethod
    def persistence_instance(cls):
        """
            Returns current RedisStorage persistence (without Eviction) instance.
            If it doesn't exist creates new one.
        :return: RedisStorage persistence instance.
        """
        if cls._persistence_instance is None:
            cls._persistence_instance = RedisStorage(lru_instance=False)
        return cls._persistence_instance

    def store_data(self, key, ex=None, **kwargs):
        """
            Stores data into redis.
        :param key: Key that must be used to store the data.
        :param ex: Data Expiration value, default - None
        :param kwargs: values that will be stored into Redis like a dictionary.
        :return: True/False - indicates whether record was created, False if record was updated.
        """
        existing_data = self.get_data(key)
        created = True
        if existing_data is None:
            existing_data = {}
        else:
            created = False
            existing_data = ast.literal_eval(existing_data)

        for (k, v) in kwargs.iteritems():
            existing_data[k] = v

        self._redis.set(name=key, value=existing_data, ex=ex)
        return created

    def get_data(self, key):
        """
            Returns data dictionary from redis by specified key.
        :param key: To get data for for.
        :return: dict - with required data in it.
        """
        return self._redis.get(name=key)

    def delete_data(self, key):
        """
            Deletes data from redis for specified key.
        :param key: To delete data for.
        """
        self._redis.delete(key)