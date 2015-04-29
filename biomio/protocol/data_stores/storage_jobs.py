from __future__ import absolute_import

from biomio.constants import REDIS_CHANGES_CLASS_NAME, REDIS_DO_NOT_STORE_RESULT_KEY, REDIS_PARTIAL_RESULTS_KEY, \
    REDIS_RESULTS_COUNTER_KEY, EMAILS_TABLE_CLASS_NAME, USERS_TABLE_CLASS_NAME
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.utils.gnugpg_generator import generate_pgp_key_pair
from logger import worker_logger


def create_record_job(table_class_name, **kwargs):
    worker_logger.info('Creating record for table - %s, with given values - %s' % (table_class_name, kwargs))
    try:
        MySQLDataStoreInterface.create_data(table_name=table_class_name, **kwargs)
        worker_logger.info('Created record for table - %s, with given values - %s' % (table_class_name, kwargs))
    except Exception as e:
        worker_logger.exception(msg=str(e))


def delete_record_job(table_class_name, object_id):
    worker_logger.info('Deleting record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    try:
        MySQLDataStoreInterface.delete_data(table_name=table_class_name, object_id=object_id)
        worker_logger.info('Deleted record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    except Exception as e:
        worker_logger.exception(msg=str(e))


def update_record_job(table_class_name, object_id, **kwargs):
    worker_logger.info('Updating record for table class - %s, with object_id - %s, with data - %s' % (table_class_name,
                                                                                                      object_id,
                                                                                                      kwargs))
    try:
        MySQLDataStoreInterface.update_data(table_name=table_class_name, object_id=object_id, **kwargs)
        worker_logger.info(
            'Updated record for table class - %s, with object_id - %s, with data - %s' % (table_class_name,
                                                                                          object_id, kwargs))
    except Exception as e:
        worker_logger.exception(msg=str(e))


def get_record_job(table_class_name, object_id, callback_code):
    worker_logger.info('Getting record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    try:
        record = MySQLDataStoreInterface.get_object(table_name=table_class_name, object_id=object_id)
        worker_logger.debug('Data: %s' % record.to_dict())
        BaseDataStore.instance().store_job_result(record_key=record.get_redis_key(),
                                                  record_dict=record.to_dict(),
                                                  callback_code=callback_code)
    except Exception as e:
        worker_logger.exception(e)
        result = dict(error=str(e))
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY,
                                                  record_dict=result,
                                                  callback_code=callback_code)
    worker_logger.info('Got record for table class - %s, with object_id - %s' % (table_class_name, object_id))


def select_records_by_ids_job(table_class_name, object_ids, callback_code):
    worker_logger.info('Getting records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
    try:
        records = MySQLDataStoreInterface.select_data_by_ids(table_name=table_class_name, object_ids=object_ids)
        worker_logger.debug('Data: %s' % records)
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=records, callback_code=callback_code)
    except Exception as e:
        worker_logger.exception(e)
        result = dict(error=str(e))
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=result, callback_code=callback_code)
    worker_logger.info('Got records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))


def generate_pgp_keys_job(table_class_name, email, callback_code, result_code):
    worker_logger.info('Started email pgp keys generation, for email - %s' % email)
    result = dict(email=email)
    try:
        # TODO send rest here.
        public_pgp_key, private_pgp_key, pass_phrase = generate_pgp_key_pair(email=email)
        if public_pgp_key is not None:
            result.update({"public_pgp_key": public_pgp_key})
            MySQLDataStoreInterface.update_data(table_name=table_class_name, object_id=email, pass_phrase=pass_phrase,
                                                public_pgp_key=public_pgp_key, private_pgp_key=private_pgp_key)
        else:
            worker_logger.exception('Something went wrong, check logs, pgp keys were not generated for email - %s' %
                                    email)
            result.update({'error': 'Sorry but we were not able to generate PGP keys for user %s' % email})
    except Exception as e:
        worker_logger.exception(e)
        result.update({'error': 'Sorry but we were not able to generate PGP keys for email %s' % email})
    finally:
        RedisStorage.persistence_instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                                 value=result)
        results_counter = RedisStorage.persistence_instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                                  result_code)
        if results_counter <= 0:
            gathered_results = RedisStorage.persistence_instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                                   callback_code)
            worker_logger.debug('All gathered results for generate_pgp_keys job - %s' % gathered_results)
            if results_counter < 0:
                worker_logger.exception('Results count is less than 0, check the worker consistency!')
            result = dict(result=gathered_results)
            BaseDataStore.instance().delete_custom_persistence_redis_data(key=REDIS_RESULTS_COUNTER_KEY % result_code)
            BaseDataStore.instance().delete_custom_persistence_redis_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
            BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                      record_dict=result, callback_code=callback_code)
        worker_logger.info('Finished email pgp keys generation, for email - %s' % email)


def get_probe_ids_by_user_email(table_class_name, email, callback_code):
    worker_logger.info('Getting probe ids by user email - %s' % email)
    result = dict()
    try:
        email_data = MySQLDataStoreInterface.get_object(table_name=EMAILS_TABLE_CLASS_NAME, object_id=email)
        worker_logger.debug('Email Data - %s' % email_data.to_dict())
        worker_logger.debug(email_data.user)
        probe_ids = MySQLDataStoreInterface.get_applications_by_user_id_and_type(table_name=table_class_name,
                                                                                 user_id=email_data.user,
                                                                                 app_type='probe')
        worker_logger.debug('probe IDS - %s' % probe_ids)
        result = dict(result=probe_ids)
    except Exception as e:
        worker_logger.exception(e)
        result = dict(error=str(e))
    finally:
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=result, callback_code=callback_code)
        worker_logger.info('Got probe ids by user email - %s' % email)


def get_extension_ids_by_probe_id(table_class_name, probe_id, callback_code):
    worker_logger.info('Getting extension ids by probe ID - %s' % probe_id)
    result = dict()
    try:
        probe_data = MySQLDataStoreInterface.get_object(table_name=table_class_name, object_id=probe_id,
                                                        return_dict=True)
        worker_logger.debug('Probe data - %s' % probe_data)
        user = MySQLDataStoreInterface.get_object(table_name=USERS_TABLE_CLASS_NAME,
                                                  object_id=probe_data.get('users')[0])
        worker_logger.debug('USer data - %s' % user.to_dict())
        extension_ids = MySQLDataStoreInterface.get_applications_by_user_id_and_type(table_name=table_class_name,
                                                                                     user_id=user,
                                                                                     app_type='extension')
        worker_logger.debug('Extension IDS - %s' % extension_ids)
        result = dict(result=extension_ids)
    except Exception as e:
        worker_logger.exception(e)
        result = dict(error=str(e))
    finally:
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=result, callback_code=callback_code)
        worker_logger.info('Got extension ids by probe ID - %s' % probe_id)


def update_redis_job():
    worker_logger.info('Doing REDIS UPDATE job')
    result = MySQLDataStoreInterface.select_data(REDIS_CHANGES_CLASS_NAME)
    worker_logger.debug(result)
    for redis_keys in result:
        worker_logger.debug('Redis Key', redis_keys.get('redis_key'))
        BaseDataStore.instance().delete_custom_lru_redis_data(redis_keys.get('redis_key'))
    worker_logger.info('REDIS UPDATE done.')


def test_schedule_job(message):
    worker_logger.info(message)