from __future__ import (absolute_import, division, print_function,
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
        gevent_worker = GeventWorker(q)
        gevent_worker.log = worker_logger
        gevent_worker.work()

