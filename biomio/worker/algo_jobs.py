from __future__ import absolute_import
import StringIO
import base64
import requests
import shutil
import tempfile
import cPickle
from requests.exceptions import HTTPError
from biomio.constants import REDIS_PROBE_RESULT_KEY, REDIS_RESULTS_COUNTER_KEY, REDIS_PARTIAL_RESULTS_KEY, \
    TRAINING_DATA_TABLE_CLASS_NAME, REDIS_JOB_RESULTS_ERROR, REST_REGISTER_BIOMETRICS, get_ai_training_response
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.algorithms.algorithms_interface import AlgorithmsInterface
from biomio.protocol.settings import settings as biomio_settings
import os
import binascii
import json
from json import dumps
from logger import worker_logger

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALGO_DB_PATH = os.path.join(APP_ROOT, '..', 'algorithms', 'algorithms', 'data')


def load_sources(path):
    if len(path):
        if not os.path.exists(path):
            return dict()
        with open(path, "r") as data_file:
            source = json.load(data_file)
            return source
    return dict()


def verification_job(image, fingerprint, settings, callback_code, result_code):
    """
        Runs verification for user with given image
    :param image: to run verification for
    :param fingerprint: app_id
    :param settings: settings with values for algoId and userID
    :param callback_code: code of the callback which should be executed after job is finished.
    :param result_code: code of the result in case we are running job in parallel.
    """
    worker_logger.info('Running verification for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                           settings))
    if RedisStorage.persistence_instance().exists(key=REDIS_JOB_RESULTS_ERROR % (callback_code, result_code)):
        worker_logger.info('Job interrupted because of job_results_error key existence.')
        return
    result = False
    # database = MySQLDataStoreInterface.get_object(table_name=TRAINING_DATA_TABLE_CLASS_NAME, object_id=fingerprint)
    # if database is not None:
    #     database = cPickle.load(StringIO.StringIO(database.data))
    # else:
    #     database = {}
    settings.update({'database': load_sources(os.path.join(ALGO_DB_PATH, "%s.json" % fingerprint))})
    settings.update({'action': 'verification'})
    temp_image_path = tempfile.mkdtemp(dir=APP_ROOT)
    error = None
    try:
        fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
        os.close(fd)
        photo_data = binascii.a2b_base64(str(image))
        with open(temp_image, 'wb') as f:
            f.write(photo_data)
        settings.update({'data': temp_image})

        # Store photos for test purposes
        store_test_photo_helper([temp_image])

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
                key=REDIS_JOB_RESULTS_ERROR % (callback_code, result_code)):
            result = dict(verified=False, error=error if error is not None else '')
            RedisStorage.persistence_instance().store_data(key=REDIS_JOB_RESULTS_ERROR % (callback_code, result_code),
                                                           ex=300, result=result)
            store_verification_results(result=result, callback_code=callback_code, result_code=result_code)
            if error is not None:
                worker_logger.info('Job was finished with internal algorithm error %s ' % error)
            else:
                worker_logger.info('Job was not stored because of job_results_error key existence.')
        else:
            RedisStorage.persistence_instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                                     value=result)
            results_counter = RedisStorage.persistence_instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                                      result_code)
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
                store_verification_results(result=result, callback_code=callback_code, result_code=result_code)
        shutil.rmtree(temp_image_path)
    worker_logger.info('Verification finished for user - %s, with result - %s' % (settings.get('userID'), result))


def store_verification_results(result, callback_code, result_code):
    RedisStorage.persistence_instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % result_code)
    RedisStorage.persistence_instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
    RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)


def store_test_photo_helper(image_paths):
    import shutil
    import os

    TEST_PHOTO_PATH = os.path.join(APP_ROOT, 'algorithms', 'test_photo')

    if not os.path.exists(TEST_PHOTO_PATH):
        os.makedirs(TEST_PHOTO_PATH)
    else:
        for the_file in os.listdir(TEST_PHOTO_PATH):
            file_path = os.path.join(TEST_PHOTO_PATH, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

    for path in image_paths:
        shutil.copyfile(path, os.path.join(TEST_PHOTO_PATH, os.path.basename(path)))


def training_job(images, fingerprint, settings, callback_code, try_type, ai_code):
    """
        Runs education for given user with given array of images.
    :param images: array of images to run verification on.
    :param fingerprint: current app_id
    :param settings: dictionary which contains information about algoId and userID
    :param callback_code: code of the callback that should be executed after job is finished
    """
    worker_logger.info('Running training for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                       settings))
    ai_response_type = dict()
    try:

        worker_logger.info('Telling AI that we are starting training with code - %s' % ai_code)
        ai_response_type.update({'status': 'in-progress'})
        response_type = base64.b64encode(json.dumps(ai_response_type))
        register_biometrics_url = biomio_settings.ai_rest_url % (REST_REGISTER_BIOMETRICS % (ai_code, response_type))
        response = requests.post(register_biometrics_url)
        try:
            response.raise_for_status()
            worker_logger.info('AI should now that training started with code - %s and response type - %s' %
                               (ai_code, response_type))
        except HTTPError as e:
            worker_logger.exception(e)
            worker_logger.exception('Failed to tell AI that training started, reason - %s' % response.reason)
    except Exception as e:
        worker_logger.error('Failed to build rest request to AI - %s' % str(e))
        worker_logger.exception(e)
    ai_response_type.update({'status': 'verified'})
    result = False
    settings.update({'action': 'education'})
    temp_image_path = tempfile.mkdtemp(dir=APP_ROOT)
    try:
        image_paths = []
        for image in images:
            fd, temp_image = tempfile.mkstemp(dir=temp_image_path)
            os.close(fd)
            photo_data = binascii.a2b_base64(str(image))
            with open(temp_image, 'wb') as f:
                f.write(photo_data)
            image_paths.append(temp_image)

        # Store photos for test purposes
        store_test_photo_helper(image_paths)

        settings.update({'data': image_paths})
        algo_result = AlgorithmsInterface.verification(**settings)
        if algo_result.get('status', '') == "update":
            # record = dictionary:
            # key          value
            #      'status'     "update"
            #      'userID'     Unique user identificator
            #      'algoID'     Unique algorithm identificator
            #      'database'   BLOB data of user, with userID, for verification algorithm algoID
            #
            # Need update record in algorithms database or create record for user userID and algorithm
            # algoID if it doesn't exists
            database_path = os.path.join(ALGO_DB_PATH, "%s.json" % fingerprint)
            database = algo_result.get('database', None)
            if database is not None:
                # data_buffer = cPickle.dumps(database, cPickle.HIGHEST_PROTOCOL)
                # worker_logger.debug(fingerprint)
                # try:
                #     MySQLDataStoreInterface.create_data(table_name=TRAINING_DATA_TABLE_CLASS_NAME, probe_id=fingerprint,
                #                                         data=data_buffer)
                # except Exception as e:
                #     worker_logger.exception(e)
                #     if '1062 Duplicate entry' in str(e):
                #         MySQLDataStoreInterface.update_data(table_name=TRAINING_DATA_TABLE_CLASS_NAME,
                #                                             object_id=fingerprint, data=data_buffer)
                result = True
                with open(database_path, 'wb') as f:
                    f.write(dumps(database))
        elif algo_result.get('status', '') == "error":
            worker_logger.exception('Error during education - %s, %s, %s' % (algo_result.get('status'),
                                                                             algo_result.get('type'),
                                                                             algo_result.get('details')))
            ai_response_type.update({'status': 'error'})
            # record = dictionary:
            # key          value
            #      'status'     "error"
            #      'type'       Type of error
            #      'userID'     Unique user identificator
            #      'algoID'     Unique algorithm identificator
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
        RedisStorage.persistence_instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
        shutil.rmtree(temp_image_path)
        if result:
            ai_response_type.update(get_ai_training_response(try_type))
        try:
            worker_logger.info('Telling AI that training is finished with code - %s and result - %s' %
                               (ai_code, result))
            response_type = base64.b64encode(json.dumps(ai_response_type))
            register_biometrics_url = biomio_settings.ai_rest_url % (REST_REGISTER_BIOMETRICS %
                                                                     (ai_code, response_type))
            response = requests.post(register_biometrics_url)
            try:
                response.raise_for_status()
                worker_logger.info('AI should now that training is finished with code - %s and response type - %s' %
                                   (ai_code, response_type))
            except HTTPError as e:
                worker_logger.exception(e)
                worker_logger.exception('Failed to tell AI that training is finished, reason - %s' % response.reason)
        except Exception as e:
            worker_logger.error('Failed to build rest request to AI - %s' % str(e))
            worker_logger.exception(e)
    worker_logger.info('training finished for user - %s, with result - %s' % (settings.get('userID'), result))
