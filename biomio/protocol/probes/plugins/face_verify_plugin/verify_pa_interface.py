from biomio.algorithms.interfaces import AlgorithmInterface
from biomio.algorithms.recognition.processes import (MainTrainingProcess, TrainingProcess, DataDetectionProcess,
                                                     RotationDetectionProcess, RotationResultProcess,
                                                     ClusterMatchingProcess)
from biomio.worker.worker_interface import WorkerInterface
from final_training_process import FinalTrainingProcess
from training_start_process import TrainingStartProcess
from defs import TEMP_DATA_PATH


class VerificationPAInterface(AlgorithmInterface):
    def __init__(self):
        self._callback = None

    def _interface_callback(self, result):
        if self._callback is not None:
            self._callback(result)

    def training(self, callback=None, **kwargs):
        self._callback = callback
        worker = WorkerInterface.instance()
        training_start_process = TrainingStartProcess(self._interface_callback)
        main_process = MainTrainingProcess(TEMP_DATA_PATH, worker)
        training_process = TrainingProcess(TEMP_DATA_PATH, worker)
        data_detect_process = DataDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_result_process = RotationResultProcess(TEMP_DATA_PATH, worker)
        cluster_matching_process = ClusterMatchingProcess(worker)
        final_training_process = FinalTrainingProcess(self._interface_callback)

        training_start_process.set_main_training_process(main_process)
        main_process.set_data_training_process(training_process)
        training_process.set_data_detection_process(data_detect_process)
        training_process.set_data_rotation_process(rotation_detect_process)
        rotation_detect_process.set_rotation_result_process(rotation_result_process)
        rotation_result_process.set_data_detection_process(data_detect_process)
        data_detect_process.set_cluster_matching_process(cluster_matching_process)
        data_detect_process.set_final_training_process(final_training_process)
        cluster_matching_process.set_final_training_process(final_training_process)

        training_start_process.run(worker, **kwargs)

    def apply(self, callback=None, **kwargs):
        pass
