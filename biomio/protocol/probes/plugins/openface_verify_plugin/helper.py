from biomio.constants import REDIS_PROBE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY, REDIS_PARTIAL_RESULTS_KEY, \
    REDIS_JOB_RESULTS_ERROR, REDIS_VERIFICATION_RETIES_COUNT_KEY
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.algorithms.logger import logger
from biomio.algorithms.plugins_tools import store_test_photo_helper, get_algo_db
import shutil
import tempfile
import os
import binascii


ALGO_ROOT = os.path.dirname(os.path.abspath(__file__))


def pre_verification_helper(image, settings, probe_id, callback_code):
    logger.info('Running verification for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                    settings))
    if RedisStorage.persistence_instance().exists(key=REDIS_JOB_RESULTS_ERROR % callback_code):
        logger.info('Job interrupted because of job_results_error key existence.')
        return
    database = get_algo_db(probe_id=probe_id)
    temp_image_path = tempfile.mkdtemp(dir=ALGO_ROOT)
    try:
        fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
        os.close(fd)
        photo_data = binascii.a2b_base64(str(image))
        with open(temp_image, 'wb') as f:
            f.write(photo_data)

        # Store photos for test purposes
        backup_path = store_test_photo_helper(ALGO_ROOT, [temp_image])

        settings.update({'data': temp_image, 'database': database, 'temp_image_path': temp_image_path,
                         'backup_image_path': backup_path})
        return settings
    except Exception as e:
        logger.exception(e)
        return None


def result_handling(result, probe_id, temp_image_path, settings, callback_code, error=None):
    if error is not None or RedisStorage.persistence_instance().exists(key=REDIS_JOB_RESULTS_ERROR % callback_code):
        if not RedisStorage.persistence_instance().exists(key=REDIS_JOB_RESULTS_ERROR % callback_code):
            result = dict(verified=False, error=error)
            RedisStorage.persistence_instance().store_data(key=REDIS_JOB_RESULTS_ERROR % callback_code,
                                                           ex=300, result=result)
            store_verification_results(result=result, callback_code=callback_code, probe_id=probe_id)
        if error is not None:
            logger.info('Job was finished with internal algorithm error %s ' % error)
        else:
            logger.info('Job was not stored because of job_results_error key existence.')
    else:
        RedisStorage.persistence_instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                                 value=result)
        results_counter = RedisStorage.persistence_instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                                  callback_code)
        if results_counter <= 0:
            gathered_results = RedisStorage.persistence_instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                                   callback_code)
            logger.debug('All gathered results for verification job - %s' % gathered_results)
            if results_counter < 0:
                logger.exception('Results count is less than 0, check worker jobs consistency!')
                result = dict(verified=False)
            else:
                true_count = float(gathered_results.count('True'))
                result = dict(verified=((true_count / len(gathered_results)) * 100) >= 50)
            store_verification_results(result=result, callback_code=callback_code, probe_id=probe_id)
    shutil.rmtree(temp_image_path)
    logger.info('Verification finished for user - %s, with result - %s' % (settings.get('userID'), result))


def store_verification_results(result, callback_code, probe_id):
    if 'error' in result:
        retries_count = RedisStorage.persistence_instance().decrement_int_value(
            REDIS_VERIFICATION_RETIES_COUNT_KEY % probe_id)
        if retries_count == 0:
            RedisStorage.persistence_instance().delete_data(key=REDIS_VERIFICATION_RETIES_COUNT_KEY % probe_id)
            logger.debug('Max number of verification attempts reached...')
            del result['error']
            result.update({'max_retries': True})
    else:
        RedisStorage.persistence_instance().delete_data(key=REDIS_VERIFICATION_RETIES_COUNT_KEY % probe_id)
    RedisStorage.persistence_instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % callback_code)
    RedisStorage.persistence_instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
    RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)

