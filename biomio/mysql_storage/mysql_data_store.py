from threading import Lock
from biomio.mysql_storage.mysql_data_entities import pny, database, UserInformation
from biomio.protocol.settings import settings

if settings.logging == 'DEBUG':
    pny.sql_debug(True)


class MySQLDataStore:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.database = database
        self.database.bind('mysql', host=settings.mysql_host, user=settings.mysql_user, passwd=settings.mysql_pass,
                           db=settings.mysql_db_name)
        self.database.generate_mapping(create_tables=True)

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = MySQLDataStore()
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
        result_list = [res.to_dict() for res in result]
        if kwargs.get('clear_after_select', False) and len(result_list) > 0:
            database.execute('DELETE FROM %s' % table_class_.get_table_name())
        return result_list

    @pny.db_session
    def get_object(self, module_name, table_name, object_id, return_dict, custom_search_attr,
                   **additional_query_params):
        table_class = self.get_table_class(module_name, table_name)
        if custom_search_attr is None:
            custom_search_attr = table_class.get_unique_search_attribute()
        search_query = {custom_search_attr: object_id}
        search_query.update(additional_query_params)
        result = table_class.get(**search_query)
        if return_dict and result is not None:
            result_redis_key = result.get_redis_key()
            result = result.to_dict(with_collections=True)
            result.update({'redis_key': result_redis_key})
            return result
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
    def delete_multiple_data(self, module_name, table_name, object_ids):
        table_class = self.get_table_class(module_name, table_name)
        database.execute("DELETE FROM %s WHERE %s IN %s" % (table_class.get_table_name(),
                                                            table_class.get_unique_search_attribute(),
                                                            "('%s')" % "','".join(object_ids)))

    @pny.db_session
    def create_multiple_records(self, module_name, table_name, values, update=False):
        table_class = self.get_table_class(module_name, table_name)
        table_fields = table_class.get_create_update_attr()
        query_values = ','.join(str(value) for value in values)
        create_query = 'INSERT INTO %s (%s) VALUES %s' % (table_class.get_table_name(),
                                                          ','.join(table_fields),
                                                          query_values)
        if update:
            update_query_part = ' ON DUPLICATE KEY UPDATE %s'
            values_set_list = []
            for field in table_fields:
                values_set_list.append('%s=VALUES(%s)' % (field, field))
            create_query += update_query_part % ','.join(values_set_list)
        database.execute(create_query)

    @pny.db_session
    def select_data_by_ids(self, module_name, table_name, object_ids, flat_result=False):
        table_class = self.get_table_class(module_name, table_name)
        objects = table_class.select_by_sql("SELECT * FROM %s WHERE %s IN %s" %
                                            (table_class.get_table_name(),
                                             table_class.get_unique_search_attribute(),
                                             "('%s')" % "','".join(object_ids)))
        result = {}
        if not flat_result:
            for obj in objects:
                result.update({getattr(obj, obj.get_unique_search_attribute()): obj.to_dict()})
        else:
            results = []
            for obj in objects:
                results.append(obj.to_dict())
            result.update({'records': results})
        return result

    @pny.db_session
    def get_applications_by_user_id_and_type(self, module_name, table_name, user_id, app_type):
        table_class = self.get_table_class(module_name=module_name, table_name=table_name)
        if isinstance(user_id, str):
            user_id = UserInformation.get(id=user_id)
        objects = pny.select(app.app_id for app in table_class if user_id in app.users and app.app_type == app_type)[:]
        return objects

    @staticmethod
    def get_table_class(module_name, table_name):
        module = __import__(module_name, globals())
        return getattr(module, table_name)
