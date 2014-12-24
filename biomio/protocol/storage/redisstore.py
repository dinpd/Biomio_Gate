from redis import StrictRedis
import ast

from biomio.protocol.settings import settings

class RedisStore:
    _instance = None

    def __init__(self):
        self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)

    def _store_data_dict(self, key, ex=None, **kwargs):
        current_data = self._redis.get(key)

        if not current_data:
            current_data = {}
        else:
            current_data = ast.literal_eval(current_data)

        for (k, v) in kwargs.iteritems():
            current_data[k] = v

        self._redis.set(name=key, value=current_data, ex=ex)
