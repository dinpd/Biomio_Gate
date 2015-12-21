from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from interface_helper import result_training_helper, ind_final_helper


FINAL_TRAINING_PROCESS_CLASS_NAME = "FinalTrainingProcess"

def job(callback_code, **kwargs):
    FinalTrainingProcess.job(callback_code, **kwargs)


class FinalTrainingProcess(AlgorithmProcessInterface):
    def __init__(self, callback):
        AlgorithmProcessInterface.__init__(self)
        self._classname = FINAL_TRAINING_PROCESS_CLASS_NAME
        self.external_callback(callback)

    def handler(self, result):
        raise NotImplementedError

    @staticmethod
    def job(callback_code, **kwargs):
        FinalTrainingProcess._job_logger_info(FINAL_TRAINING_PROCESS_CLASS_NAME, **kwargs)
        # data = kwargs["data"]
        sources = dict()
        for k in kwargs['clusters_list']:
            sources[k] = kwargs[k]
        res_record = {
            'status': "update",
            'algoID': kwargs['algoID'],
            'userID': kwargs['userID'],
            'database': sources
        }
        result = {
            'algo_result': res_record,
            'temp_image_path': kwargs['general_data']['data_path'],
            'probe_id': kwargs['general_data']['probe_id'],
            'try_type': kwargs['general_data']['try_type'],
            'ai_code': kwargs['general_data']['ai_code']
        }
        logger.info('Status::The database updated.')
        result_training_helper(callback_code=callback_code, final_func=ind_final_helper, **result)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run_external(worker, job, kwargs_list_for_results_gatherer, **kwargs)
