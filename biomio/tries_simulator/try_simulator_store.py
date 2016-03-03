import ast
from threading import Lock
from biomio.mysql_storage.mysql_data_store import MySQLDataStore
from biomio.protocol.storage.redis_storage import RedisStorage


class TrySimulatorStore:
    _instance = None
    _lock = Lock()

    USER_INFO_KEY = 'user_info:%s'
    AUTH_STATUS_KEY = 'simulator_auth_status_key:%s'
    DEVICE_ALGO_TYPE_KEY = 'device_algo_auth_type:%s'

    def __init__(self):
        self._persistence_store = RedisStorage.persistence_instance()

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = TrySimulatorStore()
        return cls._instance

    @staticmethod
    def generate_key(key_prefix, identifier):
        return key_prefix % identifier

    def store_data(self, key, identifier, **kwargs):
        self._persistence_store.store_data(key=self.generate_key(key, identifier), **kwargs)

    def get_data(self, key, identifier):
        redis_data = self._persistence_store.get_data(key=self.generate_key(key, identifier))
        return ast.literal_eval(redis_data) if redis_data is not None else {}

    @staticmethod
    def get_providers_list(identifier):
        return MySQLDataStore.instance().get_providers_by_device(app_id=identifier)

    def get_auth_status(self, identifier):
        auth_status = self.get_data(key=self.AUTH_STATUS_KEY, identifier=identifier)
        return ast.literal_eval(auth_status) if auth_status is not None else {}

    def get_user_info(self, user_id):
        user_data = self.get_data(key=self.USER_INFO_KEY, identifier=user_id)
        if user_data is not None:
            return ast.literal_eval(user_data)
        user_data = MySQLDataStore.get_object(module_name='mysql_data_entities', table_name='Email',
                                              object_id=user_id, return_dict=True,
                                              custom_search_attr='profileId', primary=True)
        if user_data is not None:
            self.store_data(key=self.USER_INFO_KEY, identifier=user_id, ex=86400, **user_data)
        return user_data
