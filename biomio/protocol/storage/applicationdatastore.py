from biomio.protocol.storage.redisstore import RedisStore
import ast


class ApplicationDataStore(RedisStore):
    _instance = None

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ApplicationDataStore()

        return cls._instance

    @classmethod
    def _redis_account_name(cls, account_id):
        return 'acount:%s' % account_id

    @classmethod
    def _redis_application_name(cls, account_id, application_id):
        return '%s:%s' % (cls._redis_account_name(account_id=account_id), application_id)

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