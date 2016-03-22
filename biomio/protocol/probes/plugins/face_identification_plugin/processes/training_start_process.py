from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
from interface_helper import pre_training_helper


TRAINING_START_PROCESS_CLASS_NAME = "TrainingStartProcess"

def job(callback_code, **kwargs):
    TrainingStartProcess.job(callback_code, **kwargs)


class TrainingStartProcess(AlgorithmProcessInterface):
    def __init__(self, callback):
        AlgorithmProcessInterface.__init__(self)
        self._classname = TRAINING_START_PROCESS_CLASS_NAME
        self._main_training_process = AlgorithmProcessInterface()
        self.external_callback(callback)

    def set_main_training_process(self, process):
        """
          Sets main training process instance. This process instance
        called by handler for run this process.

        :param process: AlgorithmProcessInterface-based instance
        """
        self._main_training_process = process

    def handler(self, result):
        """
        Callback function for corresponding job function.

        :param result: data result dictionary:
            {
                'algoID': algorithm identifier string,
                'general_data':
                {
                    'ai_code': AI code string,
                    'data_path': image data path,
                    'try_type': try type string,
                    'probe_id': probe identifier string
                },
                'providerID': provider identifier string,
                'userID': user identifier string,
                'data': image paths list
            }
        """
        self._handler_logger_info(result)
        if result.keys().__contains__('error'):
            self._callback(result)
        else:
            self._main_training_process.process(**result)

    @staticmethod
    def job(callback_code, **kwargs):
        """
        Job function for preparing data to training.

        :param callback_code: callback function identifier
        :param kwargs: settings dictionary:
            {
                'images': image byte arrays list,
                'ai_code': AI code string,
                'try_type': try type string,
                'probe_id': probe identifier string,
                'settings':
                {
                    'providerID': provider identifier string,
                    'algoID': algorithm identifier string,
                    'userID': user identifier string
                }
            }
        """
        TrainingStartProcess._job_logger_info(TRAINING_START_PROCESS_CLASS_NAME, **kwargs)
        settings = pre_training_helper(callback_code=callback_code, **kwargs)
        if settings is not None:
            AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                            record_dict=settings, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)
