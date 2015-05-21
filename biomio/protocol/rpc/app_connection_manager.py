from biomio.protocol.data_stores.application_data_store import ApplicationDataStore

__author__ = 'alexchmykhalo'


class AppConnectionManager():
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = AppConnectionManager()

        return cls._instance

    def get_connected_apps(self, app_id, callback, extension=False):
        """
        Generates list of connected app id for the given app.
        :param app_id: Application id for which get connected apps.
        :return: List of connected app ids.
        """

        if extension:
            ApplicationDataStore.instance().get_probe_ids_by_user_email(email=app_id, callback=callback)
        else:
            ApplicationDataStore.instance().get_extension_ids_by_probe_id(probe_id=app_id, callback=callback)
