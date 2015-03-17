"""
Interface for Biomio MySQL data management.

Default methods input values:

@:param module_name: String name of the module where table entities are described.
@:param table_name: String name of the class (table) to work with


"""
from biomio.constants import TABLES_MODULE
from biomio.mysql_storage.mysql_data_store import MySQLDataStore


class MySQLDataStoreInterface:
    def __init__(self):
        pass

    @staticmethod
    def create_data(table_name, module_name=TABLES_MODULE, **kwargs):
        """
            Saves specified data into specified table.
        :param module_name: string name of the module.
        :param table_name: string name of the class (table)
        :param kwargs: col name value pair parameters.

        """
        MySQLDataStore.instance().insert_data(module_name=module_name, table_name=table_name, **kwargs)

    @staticmethod
    def update_data(table_name, object_id, module_name=TABLES_MODULE, **kwargs):
        """
            Updates specified object with specified data.
        :param module_name: string name of the module.
        :param table_name: string name of the class (table)
        :param object_id: int ID of the object that must be updated.
        :param kwargs: col name value pair parameters.

        """
        MySQLDataStore.instance().update_data(module_name=module_name, table_name=table_name,
                                              update_object_pk=object_id, **kwargs)

    @staticmethod
    def select_data(table_name, module_name=TABLES_MODULE):
        """
            Gets all data for specified table.
        :param module_name: string name of the module
        :param table_name: string name of the table
        :param values: list of values (arguments) that are required to get.
        :return: dict(key=obj_id, value=dict(key=arg, value=val))

        """
        return MySQLDataStore.instance().select_data(module_name=module_name, table_name=table_name)

    @staticmethod
    def delete_data(table_name, object_id, module_name=TABLES_MODULE):
        """
            Deletes specified record from the specified table.
        :param module_name: string name of the module
        :param table_name: string name of the class (table)
        :param object_id: int ID of the object(record) to delete.

        """
        MySQLDataStore.instance().delete_data(module_name=module_name, table_name=table_name,
                                              delete_object_pk=object_id)

    @staticmethod
    def update_data_set(update_table_name, update_object_id, add_table_name, add_object_id, set_attr,
                        module_name=TABLES_MODULE):
        """
            Updates specified update_object Set attribute with specified add_object
        :param module_name: string name of the module
        :param update_table_name: string name of the class (table) to update
        :param update_object_id: unique ID of the update object
        :param add_table_name: string name of the class (table) to add
        :param add_object_id: unique ID of the add object
        :param set_attr: name of the Set attribute

        """
        MySQLDataStore.instance().update_data_set(module_name=module_name, update_table_name=update_table_name,
                                                  update_object_pk=update_object_id, add_table_name=add_table_name,
                                                  add_object_pk=add_object_id, set_attr=set_attr)

    @staticmethod
    def get_object(table_name, object_id, module_name=TABLES_MODULE):
        """
            Returns single object for given table_name
        :param module_name: string name of the module
        :param table_name: string name of the class (table)
        :param object_id: unique ID to get the object
        :return: Specified table_name class instance.

        """
        return MySQLDataStore.instance().get_object(module_name=module_name, table_name=table_name, object_id=object_id)