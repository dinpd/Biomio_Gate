from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from rq import Connection, Queue
from rq_gevent_worker import GeventWorker
from redis import Redis
from logger import worker_logger

if __name__ == '__main__':
    # Tell rq what Redis connection to use
    with Connection():
        q = Queue(connection=Redis())
        gevent_worker = GeventWorker(q)
        gevent_worker.log = worker_logger
        gevent_worker.work()

