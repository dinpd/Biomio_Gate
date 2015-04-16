__author__ = 'alexchmykhalo'

class AppConnectionManager():
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = AppConnectionManager()
        return cls._instance

    def _get_connected_ids(self, app_id, app_type):
        return []

    def get_authentication_id(self):
        return "id"