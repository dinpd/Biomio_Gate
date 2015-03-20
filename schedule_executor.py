from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from rq_scheduler import Scheduler
from redis import Redis

scheduler = Scheduler(connection=Redis(), interval=10)

if __name__ == '__main__':
    scheduler.run()
