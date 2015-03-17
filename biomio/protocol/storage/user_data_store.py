from biomio.constants import REDIS_USER_KEY, USER_DATA_PREFIX
from redisstore import RedisStore


class UserDataStore(RedisStore):
    _instance = None
    _data_prefix = USER_DATA_PREFIX

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserDataStore()
        return cls._instance

    @staticmethod
    def get_user_redis_key(user_id):
        return REDIS_USER_KEY % user_id

    def get_user_data(self, user_id, callback):
        self._get_data(self.get_user_redis_key(user_id), self._data_prefix, {'user_id': user_id}, callback)

    def delete_user_data(self, user_id):
        self._delete_data(self.get_user_redis_key(user_id), self._data_prefix, {'user_id': user_id})

    def store_user_data(self, user_id, store_mysql=True, **kwargs):
        self._store_data_dict(self.get_user_redis_key(user_id), self._data_prefix, store_mysql=store_mysql, **kwargs)