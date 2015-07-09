from __future__ import absolute_import

from biomio.constants import REDIS_CHANGES_CLASS_NAME, REDIS_DO_NOT_STORE_RESULT_KEY, MODULES_CLASSES_BY_TABLE_NAMES
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.utils import import_module_class

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


def update_redis_job():
    worker_logger.info('Doing REDIS UPDATE job')
    results = MySQLDataStoreInterface.select_data(REDIS_CHANGES_CLASS_NAME, order_by='change_time')
    worker_logger.debug(results)
    for result in results:
        keys_to_delete = get_storage_keys_by_table_name(result.get('table_name'))
        for key_to_delete in keys_to_delete:
            key = key_to_delete % result.get('record_id')
            worker_logger.info('Deleting key - %s' % key)
            BaseDataStore.instance().delete_custom_lru_redis_data(key)
    worker_logger.info('REDIS UPDATE done.')


def get_storage_keys_by_table_name(table_name):
    module_class_name = MODULES_CLASSES_BY_TABLE_NAMES.get(table_name)
    if module_class_name is None:
        worker_logger.info('There is no module and class names specified for given MySQL table name - %s' % table_name)
        return []
    try:
        module_name = module_class_name.get('module_name')
        class_name = module_class_name.get('class_name')
        store = import_module_class(module=module_name,
                                    class_name=class_name)
        if store is None:
            worker_logger.info('Given module - %s, does not contain specified class - %s' % (module_name, class_name))
            return []
        return store.instance().get_keys_to_delete()
    except Exception as e:
        worker_logger.exception(e)
        return []


def test_schedule_job(message):
    worker_logger.info(message)
