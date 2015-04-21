__author__ = 'alexchmykhalo'

from setup_default_user_data import probe_app_id, extension_app_id
from biomio.protocol.data_stores.app_connection_store import AppConnectionStore



class AppConnectionManager():
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = AppConnectionManager()

        return cls._instance

    def _create_app_connections(self, app_id, on_behalf_of=None):
        pass

    def add_connections_for_app(self, app_id, on_behalf_of=None):
        """
        Creates a connections for app.
        :param app_id: Application id.
        :param on_behalf_of: In a case of extension app - onBehalfOf key value given during RPC call.
        """
        self._create_app_connections(app_id, on_behalf_of)

    def get_connected_apps(self, app_id):
        """
        Generates list of connected app id for the given app.
        :param app_id: Application id for which get connected apps.
        :return: List of connected app ids.
        """
        #TODO: temporary hardcoded
        CONNECTIONS = {
            extension_app_id: [probe_app_id],
            probe_app_id: [extension_app_id],
        }
        return CONNECTIONS.get(app_id, None)