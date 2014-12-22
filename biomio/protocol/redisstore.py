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

    @classmethod
    def _redis_account_name(cls, account_id):
        return 'acount:%s' % account_id

    @classmethod
    def _redis_application_name(cls, account_id, application_id):
        return '%s:%s' % (cls._redis_account_name(account_id=account_id), application_id)

    def has_session(self, refresh_token):
        return self._redis.exists(name=self._redis_session_name(refresh_token=refresh_token))

    def get_session_data(self, refresh_token, key):
        data = self._redis.get(name=self._redis_session_name(refresh_token=refresh_token))
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None)

    def _store_data_dict(self, key, ex=None, **kwargs):
        current_data = self._redis.get(key)

        if not current_data:
            current_data = {}
        else:
            current_data = ast.literal_eval(current_data)

        for (k, v) in kwargs.iteritems():
            current_data[k] = v

        self._redis.set(name=key, value=current_data, ex=ex)

    def store_session_data(self, refresh_token, ttl=None, **kwargs):
        key = self._redis_session_name(refresh_token=refresh_token)
        self._store_data_dict(key=key, ex=ttl, **kwargs)

    def store_app_data(self, account_id, application_id, **kwargs):
        key = self._redis_application_name(account_id=account_id, application_id=application_id)
        self._store_data_dict(key=key, **kwargs)

    def get_app_data(self, account_id, application_id, key):
        redis_key = self._redis_application_name(account_id=account_id, application_id=application_id)
        data = self._redis.get(name=redis_key)
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None)

    def remove_session_data(self, token):
        self._redis.delete(self._redis_session_name(refresh_token=token))
