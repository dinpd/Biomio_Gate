from biomio.algorithms.interfaces import AlgorithmInterface
from biomio.algorithms.recognition.processes import (MainTrainingProcess, TrainingProcess, DataDetectionProcess,
                                                     RotationDetectionProcess, RotationResultProcess,
                                                     ClusterMatchingProcess, FinalTrainingProcess)
from biomio.worker.worker_interface import WorkerInterface
from interface_helper import pre_training_helper
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
        main_process = MainTrainingProcess(TEMP_DATA_PATH, worker)
        training_process = TrainingProcess(TEMP_DATA_PATH, worker)
        data_detect_process = DataDetectionProcess(TEMP_DATA_PATH, worker)
        rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH)
        rotation_result_process = RotationResultProcess(TEMP_DATA_PATH, worker)
        cluster_matching_process = ClusterMatchingProcess(worker)
        final_training_process = FinalTrainingProcess(self._interface_callback)

        main_process.set_data_training_process(training_process)
        training_process.set_data_detection_process(data_detect_process)
        training_process.set_data_rotation_process(rotation_detect_process)
        rotation_detect_process.set_rotation_result_process(rotation_result_process)
        rotation_result_process.set_data_detection_process(data_detect_process)
        data_detect_process.set_cluster_matching_process(cluster_matching_process)
        data_detect_process.set_final_training_process(final_training_process)
        cluster_matching_process.set_final_training_process(final_training_process)

        settings = pre_training_helper(**kwargs)
        if settings is not None:
            main_process.process(**settings)

    def apply(self, callback=None, **kwargs):
        pass
