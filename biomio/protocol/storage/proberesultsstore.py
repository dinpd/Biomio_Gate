from biomio.protocol.storage.redisstore import RedisStore
import ast


class ProbeResultsStore(RedisStore):
    _instance = None

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = SessionStore()

        return cls._instance

    @staticmethod
    def _redis_probe_key(user_id):
        return 'probe:%s' % user_id

    def has_probe_results(self, user_id):
        return self._redis.exists(name=self._redis_probe_key(user_id=user_id))

    def get_probe_data(self, user_id, key):
        data = self._redis.get(name=self._redis_probe_key(user_id=user_id))
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None)

    def store_probe_data(self, user_id, ttl=None, **kwargs):
        key = self._redis_probe_key(user_id=user_id)
        self._store_data_dict(key=key, ex=ttl, **kwargs)

    def remove_probe_data(self, user_id):
        self._redis.delete(self._redis_probe_key(user_id=user_id))


