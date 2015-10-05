from threading import Lock
from datetime import datetime
from redis import Redis
from rq_scheduler import Scheduler
from biomio.protocol.settings import settings
from biomio.worker.scheduled_jobs import update_redis_job


class SchedulerInterface:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._scheduler = Scheduler(connection=Redis(host=settings.redis_host, port=settings.redis_port), interval=5)

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = SchedulerInterface()
            return cls._instance

    def get_scheduler_instance(self):
        return self._scheduler

    def schedule_required_jobs(self):
        self._scheduler.schedule(
            scheduled_time=datetime.utcnow(),
            func=update_redis_job,
            interval=5,
        )
