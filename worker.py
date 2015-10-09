from __future__ import (absolute_import, division,
                        unicode_literals)
from redis.client import StrictRedis

from rq import Connection, Queue
from rq_gevent_worker import GeventWorker
from biomio.protocol.settings import settings
from logger import worker_logger

if __name__ == '__main__':
    # Tell rq what Redis connection to use
    with Connection(connection=StrictRedis(host=settings.redis_host, port=settings.redis_port)):
        q = Queue(connection=StrictRedis(host=settings.redis_host, port=settings.redis_port))
        waiting_jobs = q.get_jobs()
        for job in waiting_jobs:
            q.remove(job)
        gevent_worker = GeventWorker(q)
        gevent_worker.log = worker_logger
        gevent_worker.work()

