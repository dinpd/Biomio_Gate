from rq import Queue, use_connection
from redis import Redis
from worker_jobs import *

q = None


def run_job():
    print 'Start SAVE'
    q.enqueue(save_data_job)
    print 'End SAVE'
    print 'START GET'
    q.enqueue(get_data_job)
    print 'End GET'
    print 'Start UPDATE Job'
    q.enqueue(update_data_job)
    print 'END UPDATE'
    print 'START GET'
    q.enqueue(get_data_job)
    print 'End GET'


if __name__ == '__main__':
    use_connection()
    q = Queue(connection=Redis())
    run_job()