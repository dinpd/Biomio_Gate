from __future__ import absolute_import
from logger import worker_logger
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.utils.utils import import_module_class
from biomio.constants import REDIS_CHANGES_CLASS_NAME, MODULES_CLASSES_BY_TABLE_NAMES


def update_redis_job():
    worker_logger.info('Doing REDIS UPDATE job')
    results = MySQLDataStoreInterface.select_data(REDIS_CHANGES_CLASS_NAME, order_by='change_time',
                                                  clear_after_select=True)
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
