import logging
from rq import Queue, use_connection
from redis import Redis

logger = logging.getLogger(__name__)

use_connection()
q = Queue(connection=Redis())


def run_storage_job(job_to_run, **kwargs):
    logger.info('Running job - %s' % str(job_to_run))
    logger.info(kwargs)
    q.enqueue(job_to_run, **kwargs)
