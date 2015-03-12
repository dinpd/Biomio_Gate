"""
Interface for Biomio MySQL data management.

Default methods input values:

@:param module_name: String name of the module where table entities are described.
@:param table_name: String name of the class (table) to work with


"""
from data_manager import DataManager


def record_updates(func):
    def func_wrapper(module_name, table_name, object_id, **kwargs):
        table_class = DataManager.instance().get_table_class(module_name=module_name, table_name=table_name)
        redis_key = table_class.get_redis_key(object_id)
        DataManager.instance().insert_data(module_name=module_name, table_name='ChangesTable', redis_key=redis_key)
        return func(module_name, table_name, object_id, **kwargs)

    return func_wrapper


class DataManagerInterface:
    def __init__(self):
        pass

    @staticmethod
    def create_data(module_name, table_name, **kwargs):
        """
            Saves specified data into specified table.
        :param module_name: string name of the module.
        :param table_name: string name of the class (table)
        :param kwargs: col name value pair parameters.

        """
        DataManager.instance().insert_data(module_name=module_name, table_name=table_name, **kwargs)

    @staticmethod
    @record_updates
    def update_data(module_name, table_name, object_id, **kwargs):
        """
            Updates specified object with specified data.
        :param module_name: string name of the module.
        :param table_name: string name of the class (table)
        :param object_id: int ID of the object that must be updated.
        :param kwargs: col name value pair parameters.

        """
        DataManager.instance().update_data(module_name=module_name, table_name=table_name,
                                           update_object_pk=object_id, **kwargs)

    @staticmethod
    def get_data(module_name, table_name, values=None):
        """
            Gets all data for specified table.
        :param module_name: string name of the module
        :param table_name: string name of the table
        :param values: list of values (arguments) that are required to get.
        :return: dict(key=obj_id, value=dict(key=arg, value=val))

        """
        return DataManager.instance().get_data(module_name=module_name, table_name=table_name, values=values)

    @staticmethod
    @record_updates
    def delete_data(module_name, table_name, object_id):
        """
            Deletes specified record from the specified table.
        :param module_name: string name of the module
        :param table_name: string name of the class (table)
        :param object_id: int ID of the object(record) to delete.

        """
        DataManager.instance().delete_data(module_name=module_name, table_name=table_name, delete_object_pk=object_id)

    @staticmethod
    def update_data_set(module_name, update_table_name, update_object_id, add_table_name, add_object_id, set_attr):
        """
            Updates specified update_object Set attribute with specified add_object
        :param module_name:
        :param update_table_name:
        :param update_object_id:
        :param add_table_name:
        :param add_object_id:
        :param set_attr:

        """
        DataManager.instance().update_data_set(module_name=module_name, update_table_name=update_table_name,
                                               update_object_pk=update_object_id, add_table_name=add_table_name,
                                               add_object_pk=add_object_id, set_attr=set_attr)

    @staticmethod
    def get_object(module_name, table_name, object_id):
        """
            Returns single object for given table_name
        :param module_name:
        :param table_name:
        :param object_id:
        :return:
        """
        return DataManager.instance().get_object(module_name=module_name, table_name=table_name, object_id=object_id)