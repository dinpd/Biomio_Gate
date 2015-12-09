from biomio.algorithms.interfaces import AlgorithmProcessInterface, logger
from interface_helper import final_helper


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

    def job(self, callback_code, **kwargs):
        data = kwargs["data"]
        sources = dict()
        for k in data['clusters_list']:
            sources[k] = data[k]
        res_record = {
            'status': "update",
            'algoID': data['algoID'],
            'userID': data['userID'],
            'database': sources
        }
        logger.info('Status::The database updated.')
        final_helper(callback_code=callback_code, **res_record)

    @staticmethod
    def process(**kwargs):
        raise NotImplementedError

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run_external(worker, job, kwargs_list_for_results_gatherer, **kwargs)
