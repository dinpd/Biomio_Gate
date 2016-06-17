from __future__ import absolute_import
import ast
import re
from threading import Lock

from biomio.protocol.storage.redis_subscriber import RedisSubscriber
from os import urandom
from hashlib import sha1

from redis.client import StrictRedis

from rq import Queue

# from tornadoredis import Client
# import tornado.gen

from biomio.constants import REDIS_JOB_RESULT_KEY, REDIS_DO_NOT_STORE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY, \
    REDIS_PROBE_RESULT_KEY
from biomio.protocol.settings import settings
from biomio.protocol.storage.redis_storage import RedisStorage
from logger import worker_logger


class WorkerInterface:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._queue = Queue(connection=StrictRedis(host=settings.redis_host, port=settings.redis_port))
        self._subscribed_callbacks = dict()
        # self._redis_client = Client(host=settings.redis_host, port=settings.redis_port)
        # self._redis_probes_client = Client(host=settings.redis_host, port=settings.redis_port)
        self._lru_redis = RedisStorage.lru_instance()
        self._persistence_redis = RedisStorage.persistence_instance()

        self._redis_subscriber = RedisSubscriber.instance()

        import biomio.worker.storage_jobs as sj
        import biomio.worker.engine_jobs as ej

        self.CREATE_JOB = sj.create_record_job
        self.GET_JOB = sj.get_record_job
        self.SELECT_JOB = sj.select_records_by_ids_job
        self.UPDATE_JOB = sj.update_record_job
        self.DELETE_JOB = sj.delete_record_job
        self.SELECT_PROBES_BY_EXTENSION_JOB = ej.get_probe_ids_by_user_email
        self.SELECT_EXTENSIONS_BY_PROBE_JOB = ej.get_extension_ids_by_probe_id
        self.VERIFY_REGISTRATION_JOB = ej.verify_registration_job

        self._listen_for_results()
        self._listen_for_probe_results()

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

    def run_job(self, job_to_run, callback=None, kwargs_list_for_results_gatherer=None, **kwargs):
        """
            Adds job to worker's queue so it will be picked up by worker.
        :param job_to_run: Job that will be placed inside queue
        :param callback: optional callback function that will be executed after job is finished.
        :param kwargs_list_for_results_gatherer: List of kwargs dicts that will be given to each job one by one.
        :param kwargs: Arguments to run the job with.
        """
        worker_logger.info('Running job - %s' % job_to_run)
        if callback is not None:
            callback_code = sha1(urandom(32)).hexdigest()
            self._subscribed_callbacks.update({callback_code: callback})
            kwargs.update({'callback_code': callback_code})
            if kwargs_list_for_results_gatherer is not None and len(kwargs_list_for_results_gatherer) > 0:
                self._persistence_redis.store_counter_value(REDIS_RESULTS_COUNTER_KEY % callback_code,
                                                            len(kwargs_list_for_results_gatherer))
                self._run_job_with_results_gatherer(job_to_run, kwargs_list_for_results_gatherer, **kwargs)
                return
        self._queue.enqueue(job_to_run, **kwargs)

    def _run_job_with_results_gatherer(self, job_to_run, kwargs_list_for_results_gatherer, **kwargs):
        """
            Adds multiple jobs into queue with the same callback_code. We will run the corresponding
            callback with gather results only after all jos are done.
        :param job_to_run:
        :param kwargs_list_for_results_gatherer: List of kwargs dicts that will be given to each job one by one.
        :param kwargs: Parameters that must be given to each job.
        """
        for kwarg in kwargs_list_for_results_gatherer:
            kwargs.update(kwarg)
            self._queue.enqueue(job_to_run, **kwargs)

#    @tornado.gen.engine
    def _listen_for_results(self):
        """
            Initializes redis changes listener for given key pattern.

        """
        self._redis_subscriber.subscribe(channel_key=REDIS_JOB_RESULT_KEY % ('*', '*'), callback=self._process_results)
        # self._redis_client.connect()
        # yield tornado.gen.Task(self._redis_client.psubscribe, "__keyspace*:%s" % (REDIS_JOB_RESULT_KEY % ('*', '*')))
        # self._redis_client.listen(self._process_results)

#    @tornado.gen.engine
    def _listen_for_probe_results(self):
        """
            Initializes redis changes listener for given key pattern.

        """
        self._redis_subscriber.subscribe(channel_key=REDIS_PROBE_RESULT_KEY % '*', callback=self._process_probe_results)
        # self._redis_probes_client.connect()
        # yield tornado.gen.Task(self._redis_probes_client.psubscribe, "__keyspace*:%s" % (REDIS_PROBE_RESULT_KEY % '*'))
        # self._redis_probes_client.listen(self._process_probe_results)

    def _process_results(self, message):
        """
            Parses redis changes message and processes the result.
        :param message: Redis changes message.
        """
        if message.kind == 'pmessage':
            if message.body == 'set':

                job_result_key = re.search('.*:(%s)' % (REDIS_JOB_RESULT_KEY % ('.*', '.*')), message.channel).group(1)
                callback_code = re.search('.*:%s' % (REDIS_JOB_RESULT_KEY % ('(.*):.*', '.*')), message.channel).group(
                    1)
                redis_result_key = re.search('.*:%s' % (REDIS_JOB_RESULT_KEY % ('.*', '(.*:.*)')),
                                             message.channel).group(1)

                callback, result = self._parse_result_get_callback(result_key=job_result_key,
                                                                   callback_code=callback_code)

                if redis_result_key != REDIS_DO_NOT_STORE_RESULT_KEY % callback_code:
                    self._lru_redis.store_data(redis_result_key, **result)
                    worker_logger.debug('Saved result into LRU Redis instance.')

                self._run_results_callback(result=result, result_key=job_result_key, callback=callback,
                                           callback_code=callback_code)

    def _process_probe_results(self, message):
        """
            Parses redis change message and processes the result.
        :param message: Redis changes message.
        """
        if message.kind == 'pmessage':
            if message.body == 'set':
                job_result_key = re.search('.*:(%s)' % (REDIS_PROBE_RESULT_KEY % '.*'), message.channel).group(1)
                callback_code = re.search('.*:%s' % (REDIS_PROBE_RESULT_KEY % '(.*)'), message.channel).group(1)

                callback, result = self._parse_result_get_callback(result_key=job_result_key, algo_result=True,
                                                                   callback_code=callback_code)
                self._run_results_callback(result=result, result_key=job_result_key, callback=callback,
                                           callback_code=callback_code)

    def _parse_result_get_callback(self, result_key, callback_code, algo_result=False):
        result = self._persistence_redis.get_data(result_key)
        worker_logger.debug('Raw result - %s' % result)
        try:
            result = ast.literal_eval(result) if result is not None else {}
        except ValueError as e:
            worker_logger.exception(msg=str(e))
            result = {}
        if algo_result:
            result = result.get('result', False)
        worker_logger.debug('Result dictionary - %s' % result)

        callback = self._subscribed_callbacks.get(callback_code)
        return callback, result

    def _run_results_callback(self, result, result_key, callback, callback_code):
        try:
            worker_logger.debug('Running callback with result - %s' % result)
            worker_logger.debug('Callback - %s' % callback)
            callback(result)
        except Exception as e:
            worker_logger.warning(msg=str(e))
        finally:
            self._persistence_redis.delete_data(result_key)
            try:
                del self._subscribed_callbacks[callback_code]
            except KeyError as e:
                worker_logger.warning(e)

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
