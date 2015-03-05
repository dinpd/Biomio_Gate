import inspect
from mysql_entities import *
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
    def insert_data(self):
        Test1(name='Test1', value=1)
        Test2(name='Test2', value='abcd')

    @pny.db_session
    def get_data(self, module_name, table_name):
        module = __import__(module_name)
        table_class_ = getattr(module, table_name)
        result = pny.select(r for r in table_class_)
        for res in result:
            res_properties = [i[0] for i in inspect.getmembers(res) if
                              type(i[1]) in [dict, int, str, None, list, unicode] and not i[0].startswith('_') and not
                              i[0].startswith('__')]
            print res_properties
            for res_property in res_properties:
                print res_property + ' = ' + str(getattr(res, res_property))

    def update_data(self):
        pass

    def delete_data(self):
        pass
