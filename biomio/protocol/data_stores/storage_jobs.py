from __future__ import absolute_import

from biomio.constants import REDIS_CHANGES_CLASS_NAME, REDIS_DO_NOT_STORE_RESULT_KEY
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore
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
                                                                                               object_id, kwargs))
    try:
        MySQLDataStoreInterface.update_data(table_name=table_class_name, object_id=object_id, **kwargs)
        worker_logger.info('Updated record for table class - %s, with object_id - %s, with data - %s' % (table_class_name,
                                                                                                  object_id, kwargs))
    except Exception as e:
        worker_logger.exception(msg=str(e))


def get_record_job(table_class_name, object_id, callback_code):
    worker_logger.info('Getting record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    try:
        record = MySQLDataStoreInterface.get_object(table_name=table_class_name, object_id=object_id)
        worker_logger.info('Got record for table class - %s, with object_id - %s' % (table_class_name, object_id))
        worker_logger.debug('Data: %s' % record.to_dict())
        BaseDataStore.instance().store_job_result(record_key=record.get_redis_key(),
                                                  record_dict=record.to_dict(),
                                                  callback_code=callback_code)
    except Exception as e:
        worker_logger.exception(msg=str(e))


def select_records_by_ids_job(table_class_name, object_ids, callback_code):
    worker_logger.info('Getting records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
    try:
        records = MySQLDataStoreInterface.select_data_by_ids(table_name=table_class_name, object_ids=object_ids)
        worker_logger.info('Got records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
        worker_logger.debug('Data: %s' % records)
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=records, callback_code=callback_code)
    except Exception as e:
        worker_logger.exception(msg=str(e))


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