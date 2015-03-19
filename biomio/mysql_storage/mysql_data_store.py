import logging

from biomio.mysql_storage.mysql_data_entities import pny, database
from biomio.protocol.settings import settings

logger = logging.getLogger(__name__)

if settings.logging == 'DEBUG':
    pny.sql_debug(True)


class MySQLDataStore():
    _instance = None

    def __init__(self):
        self.database = database
        self.database.bind('mysql', host=settings.mysql_host, user=settings.mysql_user, passwd=settings.mysql_pass,
                           db=settings.mysql_db_name)
        self.database.generate_mapping(create_tables=True)
        logger.debug('Connection opened.')

    def __del__(self):
        logger.debug('Connection closed.')
        self.database.disconnect()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = MySQLDataStore()
        return cls._instance

    @pny.db_session
    def insert_data(self, module_name, table_name, **kwargs):
        table_class_ = self.get_table_class(module_name, table_name)
        table_class_.create_record(**kwargs)
        logger.debug('Data saved.')
        logger.debug(kwargs)

    @pny.db_session
    def select_data(self, module_name, table_name):
        table_class_ = self.get_table_class(module_name, table_name)
        result = pny.select(r for r in table_class_)
        return [res.to_dict() for res in result]

    @pny.db_session
    def get_object(self, module_name, table_name, object_id):
        table_class = self.get_table_class(module_name, table_name)
        search_query = {table_class.get_unique_search_attribute(): object_id}
        return table_class.get(**search_query)

    @pny.db_session
    def update_data(self, module_name, table_name, update_object_pk, **kwargs):
        table_class = self.get_table_class(module_name, table_name)
        search_query = {table_class.get_unique_search_attribute(): update_object_pk}
        update_object = table_class.get(**search_query)
        if update_object is not None:
            for (k, v) in kwargs.iteritems():
                setattr(update_object, k, v)

    @pny.db_session
    def update_data_set(self, module_name, update_table_name, update_object_pk, add_table_name, add_object_pk,
                        set_attr):
        update_table_class = self.get_table_class(module_name, update_table_name)
        add_table_class = self.get_table_class(module_name, add_table_name)
        search_query = {update_table_class.get_unique_search_attribute(): update_object_pk}
        update_object = update_table_class.get(**search_query)
        if update_object:
            kwargs = {add_table_class.get_unique_search_attribute(): add_object_pk}
            add_object = add_table_class.get(**kwargs)
            if add_object:
                update_set = getattr(update_object, set_attr)
                update_set.add(add_object)
                setattr(update_object, set_attr, update_set)

    @pny.db_session
    def delete_data(self, module_name, table_name, delete_object_pk):
        table_class = self.get_table_class(module_name, table_name)
        search_query = {table_class.get_unique_search_attribute(): delete_object_pk}
        delete_object = table_class.get(**search_query)
        if delete_object is not None:
            delete_object.delete()

    @staticmethod
    def get_table_class(module_name, table_name):
        module = __import__(module_name, globals())
        return getattr(module, table_name)

