import time
from biomio.mysql_storage.mysql_data_entities import pny, database
from biomio.protocol.settings import settings

if settings.logging == 'DEBUG':
    pny.sql_debug(True)


class MySQLDataStore():
    _instance = None
    _locked = False

    def __init__(self):
        self.database = database
        self.database.bind('mysql', host=settings.mysql_host, user=settings.mysql_user, passwd=settings.mysql_pass,
                           db=settings.mysql_db_name)
        self.database.generate_mapping(create_tables=True)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            if cls._locked:
                time.sleep(1)
                return cls.instance()
            cls._locked = True
            cls._instance = MySQLDataStore()
            cls._locked = False
        return cls._instance

    @pny.db_session
    def insert_data(self, module_name, table_name, **kwargs):
        table_class_ = self.get_table_class(module_name, table_name)
        table_class_.create_record(**kwargs)

    @pny.db_session
    def select_data(self, module_name, table_name, **kwargs):
        table_class_ = self.get_table_class(module_name, table_name)
        if 'order_by' in kwargs:
            result = pny.select(r for r in table_class_).order_by('r.%s' % kwargs.get('order_by'))
        else:
            result = pny.select(r for r in table_class_)
        return [res.to_dict() for res in result]

    @pny.db_session
    def get_object(self, module_name, table_name, object_id, return_dict):
        table_class = self.get_table_class(module_name, table_name)
        search_query = {table_class.get_unique_search_attribute(): object_id}
        result = table_class.get(**search_query)
        if return_dict and result is not None:
            return result.to_dict(with_collections=True)
        return result

    @pny.db_session
    def update_data(self, module_name, table_name, update_object_pk, **kwargs):
        table_class = self.get_table_class(module_name, table_name)
        table_class.update_record(record_id=update_object_pk, **kwargs)

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

    @pny.db_session
    def select_data_by_ids(self, module_name, table_name, object_ids):
        table_class = self.get_table_class(module_name, table_name)
        objects = table_class.select_by_sql("SELECT * FROM %s WHERE %s IN %s" %
                                            (table_class.get_table_name(),
                                             table_class.get_unique_search_attribute(),
                                             "('%s')" % "','".join(object_ids)))
        result = {}
        for obj in objects:
            result.update({getattr(obj, obj.get_unique_search_attribute()): obj.to_dict()})
        return result

    @pny.db_session
    def get_applications_by_user_id_and_type(self, module_name, table_name, user_id, app_type):
        table_class = self.get_table_class(module_name=module_name, table_name=table_name)
        objects = pny.select(app.app_id for app in table_class if user_id in app.users and app.app_type == app_type)[:]
        return objects

    @pny.db_session
    def self_join_applications(self, module_name, table_name, app_id, app_type):
        table_class = self.get_table_class(module_name=module_name, table_name=table_name)

    @staticmethod
    def get_table_class(module_name, table_name):
        module = __import__(module_name, globals())
        return getattr(module, table_name)