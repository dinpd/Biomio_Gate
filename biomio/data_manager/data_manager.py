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
        table_class_.create_record(**kwargs)
        print 'Data saved.'

    @pny.db_session
    def get_data(self, module_name, table_name, values=None):
        table_class_ = self.get_table_class(module_name, table_name)
        result = pny.select(r for r in table_class_)
        global_result = {}
        for res in result:
            if values is None or len(values) == 0:
                res_properties = [i[0] for i in inspect.getmembers(res) if
                                  type(i[1]) in [dict, int, str, None, list, unicode] and not i[0].startswith('_') and not
                                  i[0].startswith('__')]
            else:
                res_properties = values
            curr_res = {}
            for res_property in res_properties:
                print res_property + ' = ' + str(getattr(res, res_property))
                curr_res.update({res_property: getattr(res, res_property)})
            global_result.update({curr_res.get('id'): curr_res})
        return global_result

    @pny.db_session
    def get_object(self, module_name, table_name, object_id):
        table_class = self.get_table_class(module_name, table_name)
        search_query = table_class.get_unique_search_query(object_id)
        return table_class.get(**search_query)

    @pny.db_session
    def update_data(self, module_name, table_name, update_object_pk, **kwargs):
        table_class = self.get_table_class(module_name, table_name)
        search_query = table_class.get_unique_search_query(update_object_pk)
        update_object = table_class.get(**search_query)
        if update_object is not None:
            for (k, v) in kwargs.iteritems():
                setattr(update_object, k, v)

    @pny.db_session
    def update_data_set(self, module_name, update_table_name, update_object_pk, add_table_name, add_object_pk,
                        set_attr):
        update_table_class = self.get_table_class(module_name, update_table_name)
        add_table_class = self.get_table_class(module_name, add_table_name)
        search_query = update_table_class.get_unique_search_query(update_object_pk)
        update_object = update_table_class.get(**search_query)
        if update_object:
            kwargs = add_table_class.get_unique_search_query(add_object_pk)
            add_object = add_table_class.get(**kwargs)
            if add_object:
                update_set = getattr(update_object, set_attr)
                update_set.add(add_object)
                setattr(update_object, set_attr, update_set)

    @pny.db_session
    def delete_data(self, module_name, table_name, delete_object_pk):
        table_class = self.get_table_class(module_name, table_name)
        search_query = table_class.get_unique_search_query(delete_object_pk)
        delete_object = table_class.get(**search_query)
        if delete_object is not None:
            delete_object.delete()

    @staticmethod
    def get_table_class(module_name, table_name):
        module = __import__(module_name, globals())
        return getattr(module, table_name)
