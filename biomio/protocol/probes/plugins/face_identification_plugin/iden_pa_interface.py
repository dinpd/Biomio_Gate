from biomio.algorithms.recognition.processes import (MainTrainingProcess, TrainingProcess, DataDetectionProcess,
                                                     RotationDetectionProcess, RotationResultProcess,
                                                     ClusterMatchingProcess)
from biomio.algorithms.recognition.processes.defs import REDIS_CLUSTER_JOB_ACTION, REDIS_TEMPLATE_RESULT, \
    REDIS_GENERAL_DATA
from biomio.algorithms.recognition.processes.iden_process import IdentificationProcess
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from init_ident_update_process import InitIdentificationUpdateProcess
from update_data_struct_process import UpdateDataStructureProcess
from biomio.algorithms.interfaces import AlgorithmInterface
from biomio.worker.worker_interface import WorkerInterface
from ident_start_process import IdentificationStartProcess
from training_start_process import TrainingStartProcess
from final_training_process import FinalTrainingProcess
from transfer_data_process import TransferDataProcess
from interface_helper import tell_ai_training_results
from biomio.constants import REDIS_PROBE_RESULT_KEY
from defs import TRAINING_FULL, TEMP_DATA_PATH

def result_send_job(callback_code, **kwargs):
    AlgorithmsDataStore.instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=kwargs['result'])
    tell_ai_training_results(kwargs['result'], kwargs['ai_response_type'], kwargs['try_type'], kwargs['ai_code'])

class IdentificationPAInterface(AlgorithmInterface):
    def __init__(self):
        self._callback = None
        self._result_count = 0
        self._store_results = []

    def _interface_callback(self, result):
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

    def training(self, callback=None, **kwargs):
        self._result_count = 0
        self._store_results = []
        mode = kwargs.get("mode", TRAINING_FULL)
        self._callback = callback
        worker = WorkerInterface.instance()
        training_start_process = TrainingStartProcess(self._interface_callback)
        main_process = MainTrainingProcess(TEMP_DATA_PATH, worker)
        training_process = TrainingProcess(TEMP_DATA_PATH, worker)
        data_detect_process = DataDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_result_process = RotationResultProcess(TEMP_DATA_PATH, worker)
        cluster_matching_process = ClusterMatchingProcess(worker)
        transfer_data_process = TransferDataProcess(worker)
        init_ident_process = InitIdentificationUpdateProcess(worker)
        update_data_process = UpdateDataStructureProcess(self._interface_callback)

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
            final_training_process = FinalTrainingProcess(self._interface_callback)
            transfer_data_process.add_transfer_process(final_training_process)
        self._result_count += 1
        transfer_data_process.add_transfer_process(init_ident_process)
        init_ident_process.set_update_data_hash_process(update_data_process)

        training_start_process.run(worker, **kwargs)

    def apply(self, callback=None, **kwargs):
        self._callback = callback
        worker = WorkerInterface.instance()
        training_start_process = TrainingStartProcess(self._interface_callback)
        main_process = MainTrainingProcess(TEMP_DATA_PATH, worker)
        training_process = TrainingProcess(TEMP_DATA_PATH, worker)
        data_detect_process = DataDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_result_process = RotationResultProcess(TEMP_DATA_PATH, worker)
        ident_start_process = IdentificationStartProcess(worker)
        identification_process = IdentificationProcess()

        training_start_process.set_main_training_process(main_process)
        main_process.set_data_training_process(training_process)
        training_process.set_data_detection_process(data_detect_process)
        training_process.set_data_rotation_process(rotation_detect_process)
        rotation_detect_process.set_rotation_result_process(rotation_result_process)
        rotation_result_process.set_data_detection_process(data_detect_process)
        data_detect_process.set_final_training_process(ident_start_process)
        ident_start_process.set_identification_process(identification_process)

        training_start_process.run(worker, **kwargs)
