import ast
from redis.client import StrictRedis
from biomio.constants import REDIS_CONFIG_MAX_MEMORY_OPTION_KEY, REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY, \
    REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY
from biomio.protocol.settings import settings


class RedisStorage():
    _instance = None

    def __init__(self):
        self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)
        self._configure_redis_instance()

    def _configure_redis_instance(self):
        self._redis.config_set(REDIS_CONFIG_MAX_MEMORY_OPTION_KEY, settings.redis_max_memory)
        self._redis.config_set(REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY, settings.redis_eviction_policy)
        self._redis.config_set(REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY, settings.redis_max_memory_samples)

    @classmethod
    def instance(cls):
        """
            Returns current RedisStorage instance. If it doesn't exist creates new one.

        :return: RedisStorage instance.
        """
        if cls._instance is None:
            cls._instance = RedisStorage()
        return cls._instance

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