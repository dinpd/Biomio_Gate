from rq import Queue, use_connection
from redis import Redis
from biomio.protocol.redisstore import RedisStore

from biomio.workers_processor.worker_jobs import *


use_connection()
q = Queue(connection=RedisStore.instance().get_redis_session())


def run_worker_job(job_to_run, **kwargs):
    print 'Running job - %s' % str(job_to_run)
    print kwargs
    q.enqueue(job_to_run, **kwargs)
