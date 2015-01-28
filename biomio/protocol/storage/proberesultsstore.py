from biomio.protocol.storage.redisstore import RedisStore
import ast


class ProbeResultsStore(RedisStore):
    _instance = None

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ProbeResultsStore()

        return cls._instance

    @staticmethod
    def redis_probe_key(user_id):
        # TODO: removed for test purposes - should be fixed when userId handling in probe, extension and server
        # will be implemented
        # probe_key = 'probe:%s' % user_id
        probe_key = 'probe:id'
        return probe_key

    def has_probe_results(self, user_id):
        return self._redis.exists(name=self.redis_probe_key(user_id=user_id))

    def get_probe_data(self, user_id, key):
        data = self._redis.get(name=self.redis_probe_key(user_id=user_id))
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None)

    def store_probe_data(self, user_id, ttl=None, **kwargs):
        key = self.redis_probe_key(user_id=user_id)
        self._store_data_dict(key=key, ex=ttl, **kwargs)

    def remove_probe_data(self, user_id):
        self._redis.delete(self.redis_probe_key(user_id=user_id))


