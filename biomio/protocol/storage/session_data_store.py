from __future__ import absolute_import
from biomio.constants import REDIS_SESSION_KEY, SESSION_DATA_PREFIX
from biomio.protocol.storage.redisstore import RedisStore


class SessionDataStore(RedisStore):
    _instance = None
    _data_prefix = SESSION_DATA_PREFIX

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = SessionDataStore()
        return cls._instance

    @staticmethod
    def get_session_key(refresh_token):
        return REDIS_SESSION_KEY % refresh_token

    def get_session_data(self, refresh_token, callback):
        self._get_data(self.get_session_key(refresh_token), self._data_prefix, {'refresh_token': refresh_token},
                       callback)


    def store_session_data(self, refresh_token, ttl=None, store_mysql=True, **kwargs):
        kwargs.update({'refresh_token': refresh_token})
        kwargs.update({'ttl': ttl})
        self._store_data_dict(self.get_session_key(refresh_token), self._data_prefix,
                              store_mysql=store_mysql, ex=ttl, **kwargs)

    def delete_session_data(self, refresh_token):
        self._delete_data(self.get_session_key(refresh_token), self._data_prefix, {'refresh_token': refresh_token})