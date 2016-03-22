from biomio.algorithms.recognition.processes import (MainTrainingProcess, TrainingProcess, DataDetectionProcess,
                                                     RotationDetectionProcess, RotationResultProcess,
                                                     ClusterMatchingProcess)
from biomio.algorithms.recognition.processes.defs import REDIS_CLUSTER_JOB_ACTION, REDIS_TEMPLATE_RESULT, \
    REDIS_GENERAL_DATA
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.processes.transfer_data_process import TransferDataProcess
from processes.init_ident_update_process import InitIdentificationUpdateProcess
from processes.load_user_by_provider_process import LoadUsersByProviderProcess
from processes.load_ident_hash_process import LoadIdentificationHashProcess
from processes.update_data_struct_process import UpdateDataStructureProcess
from processes.ident_prepare_process import IdentificationPrepareProcess
from processes.final_ident_process import FinalIdentificationProcess
from processes.ident_start_process import IdentificationStartProcess
from processes.iden_rest_est_process import IdentificationREProcess
from processes.training_start_process import TrainingStartProcess
from processes.final_training_process import FinalTrainingProcess
from processes.ident_run_process import IdentificationRunProcess
from processes.interface_helper import tell_ai_training_results
from biomio.algorithms.interfaces import AlgorithmInterface
from biomio.worker.worker_interface import WorkerInterface
from biomio.constants import REDIS_PROBE_RESULT_KEY
from defs import TRAINING_FULL, TEMP_DATA_PATH


def result_send_job(callback_code, **kwargs):
    AlgorithmsDataStore.instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=kwargs['result'])
    tell_ai_training_results(kwargs['result'], kwargs['ai_response_type'], kwargs['try_type'], kwargs['ai_code'])

def result_identification_job(callback_code, **kwargs):
    AlgorithmsDataStore.instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=kwargs['result'])

class IdentificationPAInterface(AlgorithmInterface):
    def __init__(self):
        self._callback = None
        self._result_count = 0
        self._store_results = []

    def _interface_training_callback(self, result):
        self._result_count -= 1
        self._store_results.append(result)
        if self._result_count == 0:
            for idx in range(0, 6, 1):
                AlgorithmsDataStore.instance().delete_data(REDIS_CLUSTER_JOB_ACTION % idx)
            AlgorithmsDataStore.instance().delete_data(REDIS_TEMPLATE_RESULT % result['userID'])
            AlgorithmsDataStore.instance().delete_data(REDIS_GENERAL_DATA % result['userID'])
            res = self._store_results[0]
            res['result'] = self._store_results[0]['result'] and self._store_results[1]['result']
            worker = WorkerInterface.instance()
            worker.run_job(result_send_job, callback=self._callback, **res)

    def _interface_apply_callback(self, result):
        worker = WorkerInterface.instance()
        worker.run_job(result_identification_job, callback=self._callback, **result)

    def training(self, callback=None, **kwargs):
        """
          Method for training identification hashes and verification
        database using input images.

        :param callback: callback function object
        :param kwargs: settings dictionary:
            {
                'images': image byte arrays list,
                'ai_code': AI code string,
                'probe_id': probe identifier string,
                'try_type': try type string,
                'settings':
                {
                    'userID': user identifier string,
                    'algoID': algorithm identifier string
                }
            }
        """
        self._result_count = 0
        self._store_results = []
        mode = kwargs.get("mode", TRAINING_FULL)
        self._callback = callback
        worker = WorkerInterface.instance()
        training_start_process = TrainingStartProcess(self._interface_training_callback)
        main_process = MainTrainingProcess(TEMP_DATA_PATH, worker)
        training_process = TrainingProcess(TEMP_DATA_PATH, worker)
        data_detect_process = DataDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_result_process = RotationResultProcess(TEMP_DATA_PATH, worker)
        cluster_matching_process = ClusterMatchingProcess(worker)
        transfer_data_process = TransferDataProcess(worker)
        init_ident_process = InitIdentificationUpdateProcess(worker)
        update_data_process = UpdateDataStructureProcess(self._interface_training_callback)

        training_start_process.set_main_training_process(main_process)
        main_process.set_data_training_process(training_process)
        training_process.set_data_detection_process(data_detect_process)
        training_process.set_data_rotation_process(rotation_detect_process)
        rotation_detect_process.set_rotation_result_process(rotation_result_process)
        rotation_result_process.set_data_detection_process(data_detect_process)
        data_detect_process.set_cluster_matching_process(cluster_matching_process)
        data_detect_process.set_final_training_process(transfer_data_process)
        cluster_matching_process.set_final_training_process(transfer_data_process)
        if mode == TRAINING_FULL:
            self._result_count += 1
            final_training_process = FinalTrainingProcess(self._interface_training_callback)
            transfer_data_process.add_transfer_process(final_training_process)
        self._result_count += 1
        transfer_data_process.add_transfer_process(init_ident_process)
        init_ident_process.set_update_data_hash_process(update_data_process)

        for idx in range(0, 6, 1):
            AlgorithmsDataStore.instance().delete_data(REDIS_CLUSTER_JOB_ACTION % idx)
        AlgorithmsDataStore.instance().delete_data(REDIS_TEMPLATE_RESULT % kwargs['settings']['userID'])
        AlgorithmsDataStore.instance().delete_data(REDIS_GENERAL_DATA % kwargs['settings']['userID'])

        training_start_process.run(worker, **kwargs)

    def apply(self, callback=None, **kwargs):
        self._callback = callback
        worker = WorkerInterface.instance()
        identify_start_process = IdentificationStartProcess(self._interface_apply_callback)
        main_process = MainTrainingProcess(TEMP_DATA_PATH, worker)
        training_process = TrainingProcess(TEMP_DATA_PATH, worker)
        data_detect_process = DataDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_result_process = RotationResultProcess(TEMP_DATA_PATH, worker)
        ident_prepare_process = IdentificationPrepareProcess(worker)
        load_users_process = LoadUsersByProviderProcess(worker)
        ident_run_process = IdentificationRunProcess(worker)
        load_ident_hash_process = LoadIdentificationHashProcess(worker)
        identify_re_process = IdentificationREProcess(worker)
        final_ident_process = FinalIdentificationProcess(self._interface_apply_callback)

        identify_start_process.set_main_training_process(main_process)
        main_process.set_data_training_process(training_process)
        training_process.set_data_detection_process(data_detect_process)
        training_process.set_data_rotation_process(rotation_detect_process)
        rotation_detect_process.set_rotation_result_process(rotation_result_process)
        rotation_result_process.set_data_detection_process(data_detect_process)
        data_detect_process.set_final_training_process(ident_prepare_process)
        ident_prepare_process.set_load_users_process(load_users_process)
        load_users_process.set_identification_run_process(ident_run_process)
        ident_run_process.set_identification_process(load_ident_hash_process)
        load_ident_hash_process.set_identification_estimate_process(identify_re_process)
        identify_re_process.set_final_identification_process(final_ident_process)

        identify_start_process.run(worker, **kwargs)
