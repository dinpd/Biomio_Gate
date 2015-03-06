import inspect
from mysql_entities import pny, database
from mysql_settings import *


class DataManager():
    _instance = None

    def __init__(self):
        self.database = database
        self.database.bind('mysql', host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                           db=MYSQL_DATABASE_NAME)
        self.database.generate_mapping(create_tables=True)
        print 'Connection opened.'

    def __del__(self):
        print 'Connection closed.'
        self.database.disconnect()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = DataManager()
        return cls._instance

    @pny.db_session
    def insert_data(self, module_name, table_name, **kwargs):
        table_class_ = self.get_table_class(module_name, table_name)
        table_class_(**kwargs)
        print 'Data saved.'

    @pny.db_session
    def get_data(self, module_name, table_name, values=None):
        table_class_ = self.get_table_class(module_name, table_name)
        result = pny.select(r for r in table_class_)
        for res in result:
            if values is None or len(values) == 0:
                res_properties = [i[0] for i in inspect.getmembers(res) if
                                  type(i[1]) in [dict, int, str, None, list, unicode] and not i[0].startswith('_') and not
                                  i[0].startswith('__')]
            else:
                res_properties = values
            result = {}
            for res_property in res_properties:
                print res_property + ' = ' + str(getattr(res, res_property))
                result.update({res_property: getattr(res, res_property)})
            return result


    @pny.db_session
    def update_data(self, module_name, table_name, update_object_pk, **kwargs):
        table_class = self.get_table_class(module_name, table_name)
        update_object = table_class.get(id=update_object_pk)
        if update_object is not None:
            for (k, v) in kwargs.iteritems():
                setattr(update_object, k, v)

    @pny.db_session
    def delete_data(self, module_name, table_name, delete_object_pk):
        table_class = self.get_table_class(module_name, table_name)
        delete_object = table_class.get(id=delete_object_pk)
        if delete_object is not None:
            delete_object.delete()


    @staticmethod
    def get_table_class(module_name, table_name):
        module = __import__(module_name)
        return getattr(module, table_name)