from __future__ import absolute_import
import base64
import shutil
import tempfile
import cPickle
import os
import binascii

from biomio.constants import REDIS_PROBE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY, REDIS_PARTIAL_RESULTS_KEY, \
    TRAINING_DATA_TABLE_CLASS_NAME, REDIS_JOB_RESULTS_ERROR, REDIS_VERIFICATION_RETIES_COUNT_KEY
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.probes.plugins.face_verify_plugin.algorithms.algorithms_interface import AlgorithmsInterface
from biomio.algorithms.plugins_tools import store_test_photo_helper
from biomio.protocol.storage.redis_storage import RedisStorage
from logger import worker_logger

ALGO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'algorithms')


def verification_job(image, probe_id, settings, callback_code):
    """
        Runs verification for user with given image
    :param image: to run verification for
    :param probe_id: app_id
    :param settings: settings with values for algoId and userID
    :param callback_code: code of the callback which should be executed after job is finished.
    """
    worker_logger.info('Running verification for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                           settings))
    if RedisStorage.persistence_instance().exists(key=REDIS_JOB_RESULTS_ERROR % callback_code):
        worker_logger.info('Job interrupted because of job_results_error key existence.')
        return
    result = False
    database = _get_algo_db(probe_id=probe_id)
    settings.update({'database': database})
    settings.update({'action': 'verification'})
    temp_image_path = tempfile.mkdtemp(dir=ALGO_ROOT)
    error = None
    try:
        fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
        os.close(fd)
        photo_data = binascii.a2b_base64(str(image))
        with open(temp_image, 'wb') as f:
            f.write(photo_data)
        settings.update({'data': temp_image})

        # Store photos for test purposes
        store_test_photo_helper(ALGO_ROOT, [temp_image])

        algo_result = AlgorithmsInterface.verification(**settings)
        if algo_result.get('status', '') == "result":
            # record = dictionary:
            # key          value
            #      'status'     "result"
            #      'result'     bool value: True is verification successfully, otherwise False
            #      'userID'     Unique user identifier
            #
            # Need save to redis
            result = algo_result.get('result', False)
        elif algo_result.get('status', '') == "data_request":
            # record = dictionary:
            # key          value
            #      'status'     "data_request"
            #      'userID'     Unique user identifier
            #      'algoID'     Unique algorithm identifier
            #
            # Need save to redis as data request (for this we can use this dictionary)
            pass
        elif algo_result.get('status', '') == "error":
            worker_logger.exception('Error during verification - %s, %s, %s' % (algo_result.get('status'),
                                                                                algo_result.get('type'),
                                                                                algo_result.get('details')))
            if 'Internal algorithm' in algo_result.get('type', ''):
                error = algo_result.get('details', {}).get('message', '')
            # record = dictionary:
            # key          value
            #      'status'     "error"
            #      'type'       Type of error
            #      'userID'     Unique user identifier
            #      'algoID'     Unique algorithm identifier
            #      'details'    Error details dictionary
            #
            # Algorithm can have three types of errors:
            #       "Algorithm settings are empty"
            #        in this case fields 'userID', 'algoID', 'details' are empty
            #       "Invalid algorithm settings"
            #        in this case 'details' dictionary has following structure:
            #               key         value
            #               'params'    Parameters key ('data')
            #               'message'   Error message (for example "File <path> doesn't exists")
            #       "Internal algorithm error"
            # Need save to redis
            pass
    except Exception as e:
        worker_logger.exception(e)
    finally:
        if error is not None or RedisStorage.persistence_instance().exists(
                key=REDIS_JOB_RESULTS_ERROR % callback_code):
            if not RedisStorage.persistence_instance().exists(key=REDIS_JOB_RESULTS_ERROR % callback_code):
                result = dict(verified=False, error=error)
                RedisStorage.persistence_instance().store_data(key=REDIS_JOB_RESULTS_ERROR % callback_code,
                                                               ex=300, result=result)
                store_verification_results(result=result, callback_code=callback_code, probe_id=probe_id)
            if error is not None:
                worker_logger.info('Job was finished with internal algorithm error %s ' % error)
            else:
                worker_logger.info('Job was not stored because of job_results_error key existence.')
        else:
            RedisStorage.persistence_instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                                     value=result)
            results_counter = RedisStorage.persistence_instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                                      callback_code)
            if results_counter <= 0:
                gathered_results = RedisStorage.persistence_instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                                       callback_code)
                worker_logger.debug('All gathered results for verification job - %s' % gathered_results)
                if results_counter < 0:
                    worker_logger.exception('Results count is less than 0, check worker jobs consistency!')
                    result = dict(verified=False)
                else:
                    true_count = float(gathered_results.count('True'))
                    result = dict(verified=((true_count / len(gathered_results)) * 100) >= 50)
                store_verification_results(result=result, callback_code=callback_code, probe_id=probe_id)
        shutil.rmtree(temp_image_path)
    worker_logger.info('Verification finished for user - %s, with result - %s' % (settings.get('userID'), result))


def store_verification_results(result, callback_code, probe_id):
    if 'error' in result:
        retries_count = RedisStorage.persistence_instance().decrement_int_value(
            REDIS_VERIFICATION_RETIES_COUNT_KEY % probe_id)
        if retries_count == 0:
            RedisStorage.persistence_instance().delete_data(key=REDIS_VERIFICATION_RETIES_COUNT_KEY % probe_id)
            worker_logger.debug('Max number of verification attempts reached...')
            del result['error']
            result.update({'max_retries': True})
    else:
        RedisStorage.persistence_instance().delete_data(key=REDIS_VERIFICATION_RETIES_COUNT_KEY % probe_id)
    RedisStorage.persistence_instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % callback_code)
    RedisStorage.persistence_instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
    RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)


def _get_algo_db(probe_id):
    database = MySQLDataStoreInterface.get_object(table_name=TRAINING_DATA_TABLE_CLASS_NAME, object_id=probe_id)
    return cPickle.loads(base64.b64decode(database.data)) if database is not None else {}
