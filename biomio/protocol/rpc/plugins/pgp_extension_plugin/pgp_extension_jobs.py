import requests
from requests.exceptions import HTTPError
from biomio.constants import REST_CREATE_EMAIL_KEYS, REDIS_PARTIAL_RESULTS_KEY, REDIS_RESULTS_COUNTER_KEY, \
    REDIS_DO_NOT_STORE_RESULT_KEY, EMAILS_TABLE_CLASS_NAME, APPS_TABLE_CLASS_NAME, REDIS_EMAILS_KEY
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.protocol.settings import settings
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.utils.gnugpg_generator import generate_pgp_key_pair
from logger import worker_logger


def verify_email_job(email, callback_code):
    worker_logger.info('Started email verification, for email - %s' % email)
    result = dict(email=email)
    try:
        check_email_url = settings.ai_rest_url % (REST_CREATE_EMAIL_KEYS % email)
        response = requests.post(check_email_url)
        try:
            response.raise_for_status()
        except HTTPError as e:
            worker_logger.exception(e)
            if response.reason == 'not gmail':
                result.update({'error': 'Is not Gmail E-mail address.'})
            elif response.reason == 'not email':
                result.update({'error': 'Not valid E-mail format.'})
            else:
                result.update({'error': response.reason})
        if 'error' not in result:
            result = generate_email_pgp_keys(email, EMAILS_TABLE_CLASS_NAME, result)
    except Exception as e:
        worker_logger.exception(e)
        result.update({'error': 'Sorry but we were not able to generate PGP keys for email %s' % email})
    finally:
        RedisStorage.persistence_instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                                 value=result)
        results_counter = RedisStorage.persistence_instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                                  callback_code)
        if results_counter <= 0:
            gathered_results = RedisStorage.persistence_instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                                   callback_code)
            worker_logger.debug('All gathered results for generate_pgp_keys job - %s' % gathered_results)
            if results_counter < 0:
                worker_logger.exception('Results count is less than 0, check the worker consistency!')
            result = dict(result=gathered_results)
            BaseDataStore.instance().delete_custom_persistence_redis_data(key=REDIS_RESULTS_COUNTER_KEY % callback_code)
            BaseDataStore.instance().delete_custom_persistence_redis_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
            BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                      record_dict=result, callback_code=callback_code)
        worker_logger.info('Finished email verification, for email - %s' % email)


def generate_pgp_keys_job(email):
    worker_logger.info('Started email PGP keys generation, email - %s' % email)
    # TODO: Temp solution, use lru cleaner scheduled method.
    BaseDataStore.instance().delete_custom_lru_redis_data(REDIS_EMAILS_KEY % email)

    generate_email_pgp_keys(email=email, table_class_name=EMAILS_TABLE_CLASS_NAME)
    worker_logger.info('Finished email PGP keys generation, email - %s' % email)


def generate_email_pgp_keys(email, table_class_name, result=None):
    public_pgp_key, private_pgp_key, pass_phrase = generate_pgp_key_pair(email=email)
    if public_pgp_key is not None:
        MySQLDataStoreInterface.update_data(table_name=table_class_name, object_id=email,
                                            pass_phrase=pass_phrase,
                                            public_pgp_key=public_pgp_key, private_pgp_key=private_pgp_key)
        key, value = "public_pgp_key", public_pgp_key
    else:
        worker_logger.exception('Something went wrong, check logs, pgp keys were not generated for email - %s' %
                                email)
        key, value = 'error', 'PGP keys were not generated.'
    if result is not None:
        result.update({key: value})
        return result


def assign_user_to_extension_job(app_id, email):
    worker_logger.info('Checking if user with email %s is assigned to application %s' % (email, app_id))
    email_data = MySQLDataStoreInterface.get_object(table_name=EMAILS_TABLE_CLASS_NAME, object_id=email,
                                                    return_dict=True)
    if email_data is not None:
        extension = MySQLDataStoreInterface.get_object(table_name=APPS_TABLE_CLASS_NAME, object_id=app_id,
                                                       return_dict=True)
        email_user = email_data.get('user')
        extension_users = extension.get('users')
        if email_user in extension_users:
            worker_logger.info('User with email %s is assigned to application %s' % (email, app_id))
        else:
            extension_users.append(email_user)

            from biomio.protocol.data_stores.application_data_store import ApplicationDataStore

            ApplicationDataStore.instance().update_data(app_id=app_id, users=extension_users)
            worker_logger.info('Assigned user with email %s to application %s' % (email, app_id))
    else:
        worker_logger.info('Email %s is not registered' % email)
