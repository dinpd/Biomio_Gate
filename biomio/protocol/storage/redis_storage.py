import ast
from threading import Lock
from redis.client import StrictRedis
from biomio.constants import REDIS_CONFIG_MAX_MEMORY_OPTION_KEY, REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY, \
    REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY
from biomio.protocol.settings import settings


class RedisStorage:
    _lru_instance = None
    _persistence_instance = None
    _ihr_instance = None
    _lock = Lock()

    def __init__(self, lru_instance=True, ihr_instance=False, ihr_number=-1):
        if ihr_instance:
            self._ihr_instance = StrictRedis(host=settings.redis_host, port=settings.redis_ihr_port[ihr_number])
        elif lru_instance:
            self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_lru_port)
            self._configure_redis_instance()
        else:
            self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)

        move_script = """
            local value = redis.call('GET', KEYS[1])
            redis.call('SET', KEYS[2], value)
            redis.call('DEL', KEYS[1])
        """
        self.move_script = self._redis.register_script(move_script)

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
        with cls._lock:
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
        with cls._lock:
            if cls._persistence_instance is None:
                cls._persistence_instance = RedisStorage(lru_instance=False)
        return cls._persistence_instance

    @classmethod
    def ihr_instance(cls, number):
        """
            Returns current RedisStorage instance for identification hash.
            If it doesn't exist creates new one.
        :return: RedisStorage identification hash instance.
        """
        with cls._lock:
            if cls._ihr_instance is None:
                cls._ihr_instance = RedisStorage(ihr_instance=True, ihr_number=number)
        return cls._ihr_instance

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

    def decrement_int_value(self, key):
        """
            Decrements counter value under given key.
        :param key: counter key.
        :return: int decremented counter value.
        """
        return self._redis.decr(name=key)

    def store_counter_value(self, key, counter):
        """
            Stores int counter value into redis under given key.
        :param key: string counter key
        :param counter: int counter value
        """
        self._redis.set(name=key, value=counter)

    def append_value_to_list(self, key, value, append_to_head=False):
        """
            Appends value to the tail of the list which is under specified key.
            If list doesn't exists it should create new one.
        :param key: str key to store value.
        :param value: value that should be appended to the list.
        :return: int length of the list.
        """
        if append_to_head:
            return self._redis.lpush(key, value)
        return self._redis.rpush(key, value)

    def remove_value_from_list(self, key, value):
        """
            Removes all elements that are equal to value from the list stored at the given key
        :param key: stored list key
        :param value: to delete from the list
        :return: int number of removed elements
        """
        return self._redis.lrem(name=key, count=0, value=value)

    def get_stored_list(self, key):
        """
            Returns list which is placed under specified key.
        :param key: str key to get list for.
        :return: list of elements
        """
        return self._redis.lrange(name=key, start=0, end=-1)

    def move_data(self, src_key, dst_key, ex=None):
        """
        Moves data from source to destination key.
        :param src_key:
        :param dst_key:
        :param ex:
        :return:
        """
        self.move_script(keys=[src_key, dst_key])

    def exists(self, key):
        """
        Checks if existing Redis key exists.
        :param key: Redis data key.
        :return: True if key exists; False otherwise.
        """
        return self._redis.exists(key)

    def remove_keys(self, keys):
        """
        Removes all given keys from redis. Executing as an atomic operation.
        :param keys: List of keys to remove.
        """
        pipeline = self._redis.pipeline()

        for key in keys:
            pipeline.delete(key)

        pipeline.execute()

    def find_keys(self, pattern):
        """
        Returns list of keys matching pattern.
        :param pattern: Pattern for key search.
        :return: List of keys matching.
        """
        return self._redis.keys(pattern=pattern)
