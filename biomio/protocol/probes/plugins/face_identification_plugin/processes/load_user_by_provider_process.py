from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.protocol.data_stores.provider_user_store import ProviderUserStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface

LOAD_USERS_BY_PROVIDER_PROCESS_CLASS_NAME = "LoadUsersByProviderProcess"

def job(callback_code, **kwargs):
    LoadUsersByProviderProcess.job(callback_code, **kwargs)


class LoadUsersByProviderProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = LOAD_USERS_BY_PROVIDER_PROCESS_CLASS_NAME
        self._ident_run_process = AlgorithmProcessInterface()
        self._data_redis_key = None

    def set_identification_run_process(self, process):
        self._ident_run_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        if result is not None:
            ident_data = AlgorithmsDataStore.instance().get_data(self._data_redis_key)
            AlgorithmsDataStore.instance().delete_data(self._data_redis_key)
            ident_data.update({'users': result})
            self._ident_run_process.run(self._worker, **ident_data)

    @staticmethod
    def job(callback_code, **kwargs):
        raise NotImplementedError

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._data_redis_key = kwargs['data_redis_key']
        ProviderUserStore.instance().get_data(kwargs['providerID'], callback=self.handler)
