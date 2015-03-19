from __future__ import absolute_import
import logging
from biomio.constants import REDIS_CHANGES_CLASS_NAME
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore


logger = logging.getLogger(__name__)


def create_record_job(table_class_name, **kwargs):
    logger.info('Creating record for table - %s, with given values - %s' % (table_class_name, kwargs))
    try:
        MySQLDataStoreInterface.create_data(table_name=table_class_name, **kwargs)
        logger.info('Created record for table - %s, with given values - %s' % (table_class_name, kwargs))
    except Exception as e:
        logger.exception(msg=str(e))


def delete_record_job(table_class_name, object_id):
    logger.info('Deleting record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    try:
        MySQLDataStoreInterface.delete_data(table_name=table_class_name, object_id=object_id)
        logger.info('Deleted record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    except Exception as e:
        logger.exception(msg=str(e))


def update_record_job(table_class_name, object_id, **kwargs):
    logger.info('Updating record for table class - %s, with object_id - %s, with data - %s' % (table_class_name,
                                                                                               object_id, kwargs))
    try:
        MySQLDataStoreInterface.update_data(table_name=table_class_name, object_id=object_id, **kwargs)
        logger.info('Updated record for table class - %s, with object_id - %s, with data - %s' % (table_class_name,
                                                                                                  object_id, kwargs))
    except Exception as e:
        logger.exception(msg=str(e))


def get_record_job(table_class_name, object_id, callback_code):
    logger.info('Getting record for table class - %s, with object_id - %s' % (table_class_name, object_id))
    try:
        record = MySQLDataStoreInterface.get_object(table_name=table_class_name, object_id=object_id)
        logger.info('Got record for table class - %s, with object_id - %s' % (table_class_name, object_id))
        logger.debug('Data: %s' % record.to_dict())
        BaseDataStore.instance().store_job_result(record_key=record.get_redis_key(object_id),
                                                  record_dict=record.to_dict(), callback_code=callback_code)
    except Exception as e:
        logger.exception(msg=str(e))


def update_redis_job():
    logger.info('Doing REDIS UPDATE job')
    result = MySQLDataStoreInterface.select_data(REDIS_CHANGES_CLASS_NAME)
    logger.debug(result)
    for redis_keys in result:
        logger.debug('Redis Key', redis_keys.get('redis_key'))
        BaseDataStore.instance().delete_custom_redis_data(redis_keys.get('redis_key'))
    logger.info('REDIS UPDATE done.')