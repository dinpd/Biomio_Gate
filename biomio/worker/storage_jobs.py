from __future__ import absolute_import

from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore


from logger import worker_logger


def create_record_job(table_class_name, object_id, **kwargs):
    worker_logger.info('Creating record for table - %s, with given values - %s' % (table_class_name, kwargs))
    try:
        MySQLDataStoreInterface.create_data(table_name=table_class_name, **kwargs)
        worker_logger.info('Created record for table - %s, with given values - %s' % (table_class_name, kwargs))
    except Exception as e:
        if '1062 Duplicate entry' in str(e):
            update_record_job(table_class_name=table_class_name, object_id=object_id, **kwargs)
        else:
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


def get_record_job(table_class_name, object_id, callback_code, to_dict=False):
    worker_logger.info('Getting record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    try:
        record = MySQLDataStoreInterface.get_object(table_name=table_class_name, object_id=object_id,
                                                    return_dict=to_dict)
        if not to_dict:
            redis_key = record.get_redis_key()
            record = record.to_dict()
        else:
            redis_key = record.get('redis_key')
            del record['redis_key']
        worker_logger.debug('Data: %s' % record)
        BaseDataStore.instance().store_job_result(record_key=redis_key,
                                                  record_dict=record,
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
