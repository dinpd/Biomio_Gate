__author__ = 'alexchmykhalo'

from setup_default_user_data import probe_app_id, extension_app_id
from biomio.protocol.data_stores.app_connection_store import AppConnectionStore



class AppConnectionManager():
    _instance = None

    def __init__(self):
        self.connections = {}

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = AppConnectionManager()

        return cls._instance

    def get_connected_apps(self, app_id):
        """
        Generates list of connected app id for the given app.
        :param app_id: Application id for which get connected apps.
        :return: List of connected app ids.
        """
        #TODO: temporary hardcoded
        self.connections = {
            extension_app_id: [probe_app_id],
            probe_app_id: [extension_app_id]
        }

        return self.connections.get(app_id, [])