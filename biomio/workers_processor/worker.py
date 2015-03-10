from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from rq import Connection, Queue
from rq_gevent_worker import GeventWorker
from redis import Redis

if __name__ == '__main__':
    # Tell rq what Redis connection to use
    with Connection():
        q = Queue(connection=Redis())
        GeventWorker(q).work()

