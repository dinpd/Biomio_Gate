from __future__ import absolute_import
import ast
import re
from threading import Lock
from os import urandom
from hashlib import sha1
from redis import Redis
from rq import Queue
from tornadoredis import Client
from biomio.constants import REDIS_JOB_RESULT_KEY, REDIS_DO_NOT_STORE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY
from biomio.protocol.settings import settings
from biomio.protocol.storage.redis_storage import RedisStorage
from logger import worker_logger
import tornado.gen


class WorkerInterface:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._queue = Queue(connection=Redis())
        self._subscribed_callbacks = dict()
        self._redis_client = Client(host=settings.redis_host, port=settings.redis_port)
        self._lru_redis = RedisStorage.lru_instance()
        self._persistence_redis = RedisStorage.persistence_instance()

        import biomio.worker.algo_jobs as aj
        import biomio.worker.storage_jobs as sj

        self.TRAINING_JOB = aj.training_job
        self.VERIFICATION_JOB = aj.verification_job
        self.CREATE_JOB = sj.create_record_job
        self.GET_JOB = sj.get_record_job
        self.SELECT_JOB = sj.select_records_by_ids_job
        self.UPDATE_JOB = sj.update_record_job
        self.DELETE_JOB = sj.delete_record_job
        self.SELECT_PROBES_BY_EXTENSION_JOB = sj.get_probe_ids_by_user_email
        self.SELECT_EXTENSIONS_BY_PROBE_JOB = sj.get_extension_ids_by_probe_id
        self.GENERATE_PGP_KEYS_JOB = sj.generate_pgp_keys_job
        self.VERIFY_EMAIL_JOB = sj.verify_email_job
        self.VERIFY_REGISTRATION_JOB = sj.verify_registration_job
        self.ASSIGN_USER_TO_EXTENSION_JOB = sj.assign_user_to_extension_job

        self._listen_for_results()

    @classmethod
    def instance(cls):
        """
            Synchronized method which creates (if required) and returns
            current instance of WorkerInterface
        :return: WorkerInterface instance.
        """
        with cls._lock:
            if cls._instance is None:
                worker_logger.info('Initializing worker processor.')
                cls._instance = WorkerInterface()
        return cls._instance

    def run_job(self, job_to_run, callback=None, results_count=0, **kwargs):
        """
            Adds to worker queue so it will be picked up by worker.
        :param job_to_run: Job that will be placed inside queue
        :param callback: optional callback function that will be executed after job is finished.
        :param results_count: optional value that is used in case we need to run same job more than once and
                                in the end it is required to collect all results and run given callback.
        :param kwargs: Arguments to run the job with.
        """
        if callback is not None:
            callback_code = sha1(urandom(32)).hexdigest()
            self._subscribed_callbacks.update({callback_code: callback})
            kwargs.update({'callback_code': callback_code})
            if results_count > 0:
                self._persistence_redis.store_counter_value(REDIS_RESULTS_COUNTER_KEY % callback_code, results_count)
        worker_logger.info('Running job - %s' % job_to_run)
        self._queue.enqueue(job_to_run, **kwargs)

    @tornado.gen.engine
    def _listen_for_results(self):
        """
            Initializes redis changes listener for given key pattern.

        """
        self._redis_client.connect()
        yield tornado.gen.Task(self._redis_client.psubscribe, "__keyspace*:%s" % (REDIS_JOB_RESULT_KEY % ('*', '*')))
        self._redis_client.listen(self._process_results)

    def _process_results(self, msg):
        """
            Parses redis changes message and processes the result.
        :param msg: Redis changes message.
        """
        if msg.kind == 'pmessage':
            if msg.body == 'set':

                job_result_key = re.search('.*:(%s)' % (REDIS_JOB_RESULT_KEY % ('.*', '.*')), msg.channel).group(1)
                callback_code = re.search('.*:%s' % (REDIS_JOB_RESULT_KEY % ('(.*):.*', '.*')), msg.channel).group(1)
                redis_result_key = re.search('.*:%s' % (REDIS_JOB_RESULT_KEY % ('.*', '(.*:.*)')), msg.channel).group(1)

                result = self._persistence_redis.get_data(job_result_key)
                try:
                    result = ast.literal_eval(result) if result is not None else {}
                except ValueError as e:
                    worker_logger.exception(msg=str(e))
                    result = {}
                worker_logger.debug('Received result from MySQL - %s' % result)

                if redis_result_key != REDIS_DO_NOT_STORE_RESULT_KEY % callback_code:
                    self._lru_redis.store_data(redis_result_key, **result)
                    worker_logger.debug('Saved result into LRU Redis instance.')

                callback = self._subscribed_callbacks.get(callback_code)

                try:
                    worker_logger.debug('Running callback with result - %s' % result)
                    worker_logger.debug('Callback - %s' % callback)
                    callback(result)
                except Exception as e:
                    worker_logger.warning(msg=str(e))
                finally:
                    self._persistence_redis.delete_data(job_result_key)
                    del self._subscribed_callbacks[callback_code]

    def queue_jobs_count(self):
        """
            Returns number of jobs that are currently inside the worker's queue

        :return: int number of queue jobs.
        """
        return self._queue.count

    def get_all_jobs_from_queue(self):
        """
            Returns list of jobs that are currently inside the worker's queue

        :return: list of queue jobs.
        """
        return self._queue.get_jobs()

    def clear_queue(self):
        """
            Clears worker's queue. It deletes everything that is inside the queue.

        """
        self._queue.empty()
