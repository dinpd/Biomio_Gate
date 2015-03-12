from os import urandom
import time
from worker_jobs import *
from worker_processor import run_worker_job
from hashlib import sha1

RANDOM_STRING = sha1(urandom(64)).hexdigest()

USER_ID = '%s_user_id' % RANDOM_STRING
USER_NAME = 'test_USER_name'
APP_ID = '%s_test_app_id' % RANDOM_STRING
APP_PUBLIC_KEY = 'Test APP Public Key'
EMAIL = '%s@email.com' % RANDOM_STRING
PASS_PHRASE = 'testabcd'
PUBLIC_PGP_KEY = 'Test public pgp key'

if __name__ == '__main__':
    run_worker_job(create_user_job, user_id=USER_ID, name=USER_NAME)
    time.sleep(10)
    run_worker_job(create_app_job, app_id=APP_ID, app_public_key=APP_PUBLIC_KEY, user_id=USER_ID)
    run_worker_job(create_user_email, email=EMAIL, pass_phrase=PASS_PHRASE, public_pgp_key=PUBLIC_PGP_KEY,
                   user_id=USER_ID)
    time.sleep(10)
    run_worker_job(delete_app_job, app_id=APP_ID)
    time.sleep(5)
    run_worker_job(update_redis_job)