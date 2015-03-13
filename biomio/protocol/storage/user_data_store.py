from biomio.workers_processor.worker_jobs import get_user_job
from biomio.workers_processor.worker_processor import run_worker_job
from redisstore import RedisStore


class UserDataStore(RedisStore):
    _instance = None

    def __init__(self):
        RedisStore.__init__(self)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserDataStore()
        return cls._instance

    def store_user_data(self, key, data):
        self._redis.set(name=key, value=data)

    def get_user_data(self, user_id, callback, *args):
        user_data = self._redis.get(name=user_id)
        if user_data is None:
            run_worker_job(get_user_job, user_id=user_id)
        else:
            callback(user_data=user_data, *args)

