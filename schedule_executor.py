from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from rq_scheduler import Scheduler
from redis import Redis
from biomio.protocol.settings import settings

scheduler = Scheduler(connection=Redis(host=settings.redis_host, port=settings.redis_port), interval=10)

if __name__ == '__main__':
    scheduler.run()
