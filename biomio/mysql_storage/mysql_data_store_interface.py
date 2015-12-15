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
    def select_data(table_name, module_name=TABLES_MODULE, **kwargs):
        """
            Gets all data for specified table.
        :param module_name: string name of the module
        :param table_name: string name of the table
        :param values: list of values (arguments) that are required to get.
        :return: dict(key=obj_id, value=dict(key=arg, value=val))

        """
        return MySQLDataStore.instance().select_data(module_name=module_name, table_name=table_name, **kwargs)

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
    def get_object(table_name, object_id, return_dict=False, module_name=TABLES_MODULE, custom_search_attr=None,
                   **additional_query_params):
        """
            Returns single object for given table_name
        :param module_name: string name of the module
        :param table_name: string name of the class (table)
        :param object_id: unique ID to get the object
        :param return_dict: indicates whether to dictionary
        :return: Specified table_name class instance.

        """
        return MySQLDataStore.instance().get_object(module_name=module_name, table_name=table_name, object_id=object_id,
                                                    return_dict=return_dict, custom_search_attr=custom_search_attr,
                                                    **additional_query_params)

    @staticmethod
    def select_data_by_ids(table_name, object_ids, module_name=TABLES_MODULE, flat_result=False):
        """
            Selects data from given table with filter:
            obj.<unique_id> in [object_ids]
        :param module_name: string name of the module
        :param object_ids: list of unique object ids to select data for
        :param table_name: string name of the class (table)
        :param flat_result: bool, indicates whether it is required to return simple list of results
        :return: dict with unique object id as key and object dict as value OR list with all results dicts
        """
        return MySQLDataStore.instance().select_data_by_ids(module_name=module_name, table_name=table_name,
                                                            object_ids=object_ids, flat_result=flat_result)

    @staticmethod
    def get_applications_by_user_id_and_type(table_name, user_id, app_type, module_name=TABLES_MODULE):
        """
            Gets Applications ids by given user_id and application type
        :param table_name: string name of the class (table)
        :param user_id: user_id to get applications for.
        :param app_type: Type of the applications to get.
        :param module_name: string name of the module
        :return:
        """
        return MySQLDataStore.instance().get_applications_by_user_id_and_type(module_name=module_name,
                                                                              table_name=table_name, user_id=user_id,
                                                                              app_type=app_type)

    @staticmethod
    def create_multiple_records(table_name, values, update=False, module_name=TABLES_MODULE):
        """
            Creates/Updates multiple records with one query.
        :param table_name: string name of the class (table)
        :param values: tuple of tuples with values to insert/update into the table. (e.g. ((1, 'a'), (2, 'b')) )
        :param update: bool, indicates whether it is required to update existing values.
        :param module_name: string name of the module
        """
        MySQLDataStore.instance().create_multiple_records(module_name=module_name, table_name=table_name,
                                                          values=values, update=update)

    @staticmethod
    def delete_multiple_data(table_name, object_ids, module_name=TABLES_MODULE):
        """
            Deletes specified records from the specified table.
        :param module_name: string name of the module
        :param table_name: string name of the class (table)
        :param object_ids: list of IDs of the objects(records) to delete.
        """
        MySQLDataStore.instance().delete_multiple_data(module_name=module_name, table_name=table_name,
                                                       object_ids=object_ids)
