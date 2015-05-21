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

    def get_connected_apps(self, app_id, extension=False):
        """
        Generates list of connected app id for the given app.
        :param app_id: Application id for which get connected apps.
        :return: List of connected app ids.
        """

        from biomio.protocol.engine import get_app_keys_helper

        apps = get_app_keys_helper(app_id=app_id, extension=extension)
        if apps is not None:
            return apps.get('result', [])
        return []
