from biomio.algorithms.recognition.processes.handling import save_temp_data, load_temp_data
from biomio.algorithms.recognition.processes.defs import STATUS_RESULT, STATUS_ERROR
from biomio.algorithms.datastructs import wNearPyHash, DEFAULT_NEAR_PY_HASH_SETTINGS
from biomio.algorithms.recognition.processes.messages import create_result_message
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from defs import get_plugin_dir

INIT_IDENTIFICATION_UPDATE_PROCESS_CLASS_NAME = "InitIdentificationUpdateProcess"

def job(callback_code, **kwargs):
    InitIdentificationUpdateProcess.job(callback_code, **kwargs)


class InitIdentificationUpdateProcess(AlgorithmProcessInterface):
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = INIT_IDENTIFICATION_UPDATE_PROCESS_CLASS_NAME
        self.db_settings = DEFAULT_NEAR_PY_HASH_SETTINGS
        self._update_data_process = AlgorithmProcessInterface()

    def set_update_data_hash_process(self, process):
        self._update_data_process = process

    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
            {
                'status': 'result',
                'data':
                {
                    'data_file': data file path
                },
                'type': 'update_hash'
            }
        """
        self._handler_logger_info(result)
        if result is not None:
            if result['status'] == STATUS_ERROR:
                pass
            elif result['status'] == STATUS_RESULT:
                data = load_temp_data(result['data']['data_file'], remove=True)
                database = data['database']
                del data['database']
                for inx, cluster in database.iteritems():
                    settings = {
                        "database": 0,
                        "cluster_id": inx,
                        "template": cluster,
                        "uuid": data['userID'],
                        "data_settings": data.copy(),
                        "hash_settings": {
                            "database_type": wNearPyHash.type(),
                            "settings":  self.db_settings,
                            "hash_config_path": get_plugin_dir("settings")
                        }
                    }
                    self._update_data_process.run(worker=self._worker, **settings)

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for preparing data to update the identification hash.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'algoID': algorithm identifier string,
                'userID': user identifier string,
                'general_data':
                {
                    'ai_code': AI code string,
                    'data_path': image data path,
                    'probe_id': probe identifier string,
                    'try_type': try type string
                },
                'temp_data_path': temporary data path,
                'ended': matching ending status,
                'clusters_list': list of optional keys,
                <optional key>: descriptor list,
                <optional key>: descriptor list,
                ...
                <optional key>: descriptor list
            }
        """
        InitIdentificationUpdateProcess._job_logger_info(INIT_IDENTIFICATION_UPDATE_PROCESS_CLASS_NAME, **kwargs)
        record = InitIdentificationUpdateProcess.process(**kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        InitIdentificationUpdateProcess._process_logger_info(INIT_IDENTIFICATION_UPDATE_PROCESS_CLASS_NAME, **kwargs)
        sources = dict()
        for k in kwargs['clusters_list']:
            sources[k] = kwargs[k]
        result = {
            'database': sources,
            'algoID': kwargs['algoID'],
            'userID': kwargs['userID'],
            'temp_image_path': kwargs['general_data']['data_path'],
            'probe_id': kwargs['general_data']['probe_id'],
            'try_type': kwargs['general_data']['try_type'],
            'ai_code': kwargs['general_data']['ai_code']
        }
        temp_data_path = kwargs['temp_data_path']
        iden_process_data = save_temp_data(result, temp_data_path)
        return create_result_message({'data_file': iden_process_data}, 'update_hash')

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
