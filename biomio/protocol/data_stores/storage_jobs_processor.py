
from datetime import datetime
from rq import Queue, use_connection
from redis import Redis
from rq_scheduler import Scheduler
from logger import worker_logger


use_connection()
q = Queue(connection=Redis())

scheduler = Scheduler(connection=Redis(), interval=10)


def run_storage_job(job_to_run, **kwargs):
    """
        Put job in worker's queue.
    :param job_to_run:
    :param kwargs:
    """
    worker_logger.info('Running job - %s' % str(job_to_run))
    q.enqueue(job_to_run, **kwargs)


def schedule_job(job_to_schedule, interval, repeat=None, start_time=datetime.utcnow(), **kwargs):
    """
        Schedules job for periodic execution.
    :param job_to_schedule: Function to be queued
    :param interval: Time before the function is called again, in seconds
    :param repeat: Repeat this number of times (None means repeat forever)
    :param start_time: Time for first execution, in UTC timezone
    :param kwargs: Keyword arguments passed into function when executed
    """
    scheduler.schedule(
        scheduled_time=start_time,
        func=job_to_schedule,
        kwargs=kwargs,
        interval=interval,
        repeat=repeat
    )