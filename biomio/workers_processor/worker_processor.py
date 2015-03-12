from rq import Queue, use_connection
from redis import Redis


use_connection()
q = Queue(connection=Redis())


def run_worker_job(job_to_run, **kwargs):
    print 'Running job - %s' % str(job_to_run)
    print kwargs
    q.enqueue(job_to_run, **kwargs)
