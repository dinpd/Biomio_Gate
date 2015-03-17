from __future__ import absolute_import
from redis import StrictRedis
import ast
import re
import tornado.gen
from os import urandom
from hashlib import sha1
from tornadoredis import Client
from biomio.constants import USER_DATA_PREFIX, APP_DATA_PREFIX, EMAIL_DATA_PREFIX, SESSION_DATA_PREFIX
from biomio.workers_processor.worker_processor import run_worker_job
from biomio.protocol.settings import settings


class RedisStore:
    _instance = None

    def __init__(self):
        self._redis = StrictRedis(host=settings.redis_host, port=settings.redis_port)
        self._redis_client = Client(host=settings.redis_host, port=settings.redis_port)
        self._RESULT_CALLBACKS = {}

        import biomio.protocol.storage.storage_jobs as sj

        self._MYSQL_STORAGE_JOBS = {
            USER_DATA_PREFIX % 'get': sj.get_app_job,
            USER_DATA_PREFIX % 'create': sj.create_user_job,
            USER_DATA_PREFIX % 'update': sj.update_user_job,
            USER_DATA_PREFIX % 'delete': sj.delete_user_job,

            APP_DATA_PREFIX % 'get': sj.get_app_job,
            APP_DATA_PREFIX % 'create': sj.create_app_job,
            APP_DATA_PREFIX % 'update': sj.update_app_job,
            APP_DATA_PREFIX % 'delete': sj.delete_app_job,

            EMAIL_DATA_PREFIX % 'get': sj.get_user_email,
            EMAIL_DATA_PREFIX % 'create': sj.create_user_email,
            EMAIL_DATA_PREFIX % 'update': sj.update_email_job,
            EMAIL_DATA_PREFIX % 'delete': sj.delete_user_email,

            SESSION_DATA_PREFIX % 'get': sj.get_session_job,
            SESSION_DATA_PREFIX % 'create': sj.create_session_job,
            SESSION_DATA_PREFIX % 'update': sj.update_session_job,
            SESSION_DATA_PREFIX % 'delete': sj.delete_session_job
        }
        self._listen()

    @tornado.gen.engine
    def _listen(self):
        self._redis_client.connect()
        yield tornado.gen.Task(self._redis_client.psubscribe, "__keyspace*:mysql_store:*")
        self._redis_client.listen(self._on_redis_message)

    def _on_redis_message(self, msg):
        if msg.kind == 'pmessage':
            if msg.body == 'set':
                worker_result_key = re.search('.*:(mysql_store:.*)', msg.channel).group(1)
                result_key = self._redis.get(name=worker_result_key)
                if result_key:
                    result_key = ast.literal_eval(result_key)
                    if 'redis_key' in result_key:
                        result = self._redis.get(name=result_key.get('redis_key'))
                        if result:
                            self._redis.delete(worker_result_key)
                            callback_key = worker_result_key.split(':')[-1]
                            callback = self._RESULT_CALLBACKS.get(callback_key)
                            if callback:
                                del self._RESULT_CALLBACKS[callback_key]
                                callback(result)

    def _store_data_dict(self, key, data_prefix, store_mysql, ex=None, **kwargs):
        current_data = self._redis.get(key)

        if not current_data:
            run_job_key = data_prefix % 'create'
            current_data = {}
        else:
            run_job_key = data_prefix % 'update'
            current_data = ast.literal_eval(current_data)

        self._store_data(key, current_data, ex=ex, **kwargs)

        run_job = self._MYSQL_STORAGE_JOBS.get(run_job_key)
        if store_mysql:
            if run_job is None:
                raise Exception('No job specified for specified data parameters.')
            run_worker_job(run_job, **kwargs)

    def _delete_data(self, key, data_prefix, job_kwargs):
        self._redis.delete(key)
        run_job = self._MYSQL_STORAGE_JOBS.get(data_prefix % 'delete')
        if run_job is None:
            raise Exception('No job specified for specified data parameters.')
        run_worker_job(run_job, **job_kwargs)

    def _get_data(self, key, data_prefix, job_kwargs, callback):
        result = self._redis.get(name=key)
        if result is None:
            run_job = self._MYSQL_STORAGE_JOBS.get(data_prefix % 'get', None)
            if run_job is None:
                callback(dict(error='No job for specified data parameters.'))
            else:
                callback_code = sha1(urandom(32)).hexdigest()
                self._RESULT_CALLBACKS.update({callback_code: callback})
                run_worker_job(run_job, callback_code=callback_code, **job_kwargs)
        else:
            callback(result)

    def _store_data(self, key, current_data, ex, **kwargs):
        for (k, v) in kwargs.iteritems():
            current_data[k] = v
        self._redis.set(name=key, value=current_data, ex=ex)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = RedisStore()
        return cls._instance

    def delete_custom_data(self, key):
        self._redis.delete(key)

    def store_job_result(self, key, **kwargs):
        self._store_data(key, current_data={}, ex=None, **kwargs)