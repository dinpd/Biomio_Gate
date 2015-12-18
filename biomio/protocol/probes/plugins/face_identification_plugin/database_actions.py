from biomio.algorithms.logger import logger
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface


def select_records_by_ids(table_class_name, object_ids, flat_result=False):
    logger.info('Getting records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
    try:
        records = MySQLDataStoreInterface.select_data_by_ids(table_name=table_class_name,
                                                             object_ids=object_ids,
                                                             flat_result=flat_result)
        logger.debug('Data: %s' % records)
    except Exception as e:
        logger.exception(e)
        records = dict(error=str(e))
    logger.info('Got records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
    return records


def create_records(table_class_name, values, update=False):
    logger.info('Store records for table class - %s, values - %s (with updating - %s)' %
                (table_class_name, values, update))
    try:
        MySQLDataStoreInterface.create_multiple_records(table_name=table_class_name,
                                                        values=values,
                                                        update=update)
        records = dict(status=True)
    except Exception as e:
        logger.exception(e)
        records = dict(error=str(e), status=False)
    logger.info('Stored records for table class - %s, with object_ids - %s (with updating - %s)' %
                (table_class_name, values, update))
    return records


def delete_data(table_class_name, object_ids):
    logger.info('Delete records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
    try:
        MySQLDataStoreInterface.delete_multiple_data(table_name=table_class_name, object_ids=object_ids)
        records = dict(status=True)
    except Exception as e:
        logger.exception(e)
        records = dict(error=str(e), status=False)
    logger.info('Deleted records for table class - %s, with object_ids - %s' % (table_class_name, object_ids))
    return records
