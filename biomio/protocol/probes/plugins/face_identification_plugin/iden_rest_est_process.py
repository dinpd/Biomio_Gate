from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.interfaces import AlgorithmProcessInterface
from biomio.constants import REDIS_DO_NOT_STORE_RESULT_KEY
import ast

IDENTIFICATION_RE_PROCESS_CLASS_NAME = "IdentificationREProcess"

def job(callback_code, **kwargs):
    IdentificationREProcess.job(callback_code, **kwargs)


class IdentificationREProcess(AlgorithmProcessInterface):
    """
        Identification Results Estimation Process
    """
    def __init__(self, worker):
        AlgorithmProcessInterface.__init__(self, worker=worker)
        self._classname = IDENTIFICATION_RE_PROCESS_CLASS_NAME
        self._final_identification_process = AlgorithmProcessInterface()

    def set_final_identification_process(self, process):
        self._final_identification_process = process

    def handler(self, result):
        self._handler_logger_info(result)
        if result is not None:
            self._final_identification_process.run(self._worker, **result)

    @staticmethod
    def job(callback_code, **kwargs):
        IdentificationREProcess._job_logger_info(IDENTIFICATION_RE_PROCESS_CLASS_NAME, **kwargs)
        record = IdentificationREProcess.process(**kwargs)
        AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                        record_dict=record, callback_code=callback_code)

    @staticmethod
    def process(**kwargs):
        IdentificationREProcess._process_logger_info(IDENTIFICATION_RE_PROCESS_CLASS_NAME, **kwargs)
        """

        :param kwargs: dict
            "results": list of dicts
                "cluster_size": length of cluster of the test image,
                "cluster_id": cluster ID,
                "candidates_size": number of found candidates,
                "candidates_score": dict
                    <key>: <value>, where <key> - ID of database,
                                          <value> - number of candidates for this database
            "test_size": numbers of descriptors in test dataset
        :return:
        """
        results = [ast.literal_eval(val) for val in kwargs["results"]]
        if len(results) > 0:
            db_score = {}
            gsum = 0
            test_size = 0
            for result in results:
                test_size += result['cluster_size']
            for result in results:
                res_score = result.get("candidates_score", {})
                gsum += result.get("candidates_size", 0)
                score_cost = 1#result.get("cluster_size", 0) / (1.0 * test_size)
                for key, value in res_score.iteritems():
                    lcount = db_score.get(key, 0)
                    lcount += score_cost * value
                    db_score[key] = lcount
            return {'candidates_count': gsum,
                    'candidates_score': db_score}

    def run(self, worker, kwargs_list_for_results_gatherer=None, **kwargs):
        self._run(worker, job, kwargs_list_for_results_gatherer, **kwargs)