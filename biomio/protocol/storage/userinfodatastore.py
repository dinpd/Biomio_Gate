from biomio.protocol.storage.redisstore import RedisStore
import ast


class UserInfoDataStore(RedisStore):
    _instance = None

    PASS_PHRASE_KEY = 'pass_phrase'
    PUBLIC_PGP_KEY = 'public_pgp_key'

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = UserInfoDataStore()

        return cls._instance

    @classmethod
    def _redis_user_key(cls, user_id):
        return 'user:%s' % user_id

    @classmethod
    def _redis_email_key(cls, email):
        return 'user_email:%s' % email

    def store_user_data(self, user_id, email=None, **kwargs):
        user_key = self._redis_user_key(user_id=user_id)
        self._store_data_dict(key=user_key, **kwargs)
        if email is not None:
            email_key = self._redis_email_key(email=email)
            self._store_data_dict(key=email_key, user_id=user_id)

    def get_user_data_by_id(self, user_id, key=None):
        redis_key = self._redis_user_key(user_id=user_id)
        data = self._redis.get(name=redis_key)
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None) if key is not None else data

    def get_user_id_by_email(self, email):
        redis_key = self._redis_email_key(email=email)
        data = self._redis.get(name=redis_key)
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get('user_id', None)