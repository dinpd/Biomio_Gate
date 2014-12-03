from redis import StrictRedis
import ast

from biomio.protocol.settings import settings

class RedisStore:
    _instance = None

    def __init__(self):
        self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = RedisStore()

        return cls._instance

    @classmethod
    def _redis_session_name(cls, refresh_token):
        return 'token:%s' % refresh_token

    def has_session(self, refresh_token):
        return self._redis.exists(name=self._redis_session_name(refresh_token=refresh_token))

    def get_session_data(self, refresh_token, key):
        data = self._redis.get(name=self._redis_session_name(refresh_token=refresh_token))
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None)

    def store_session_data(self, refresh_token, ttl=None, **kwargs):
        current_data = self._redis.get(self._redis_session_name(refresh_token=refresh_token))

        if not current_data:
            current_data = {}
        else:
            current_data = ast.literal_eval(current_data)

        for (k, v) in kwargs.iteritems():
            current_data[k] = v

        self._redis.set(name=self._redis_session_name(refresh_token=refresh_token), value=current_data, ex=ttl)

    def remove_session_data(self, token):
        self._redis.delete(self._redis_session_name(refresh_token=token))
