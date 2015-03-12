from biomio.protocol.storage.redisstore import RedisStore
import ast


class SessionStore(RedisStore):
    _instance = None

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = SessionStore()

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
        key = self._redis_session_name(refresh_token=refresh_token)
        self._store_data_dict(key=key, ex=ttl, **kwargs)

    def remove_session_data(self, token):
        self._redis.delete(self._redis_session_name(refresh_token=token))


