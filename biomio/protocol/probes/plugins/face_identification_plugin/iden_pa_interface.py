from biomio.algorithms.recognition.processes import MainTrainingProcess, TrainingProcess
from biomio.algorithms.interfaces import AlgorithmInterface
from defs import TRAINING_FULL, TEMP_DATA_PATH

class IdentificationPAInterface(AlgorithmInterface):
    def __init__(self):
        pass

    def training(self, **kwargs):
        mode = kwargs.get("mode", TRAINING_FULL)
        if mode == TRAINING_FULL:
            main_process = MainTrainingProcess(TEMP_DATA_PATH)
            training_process = TrainingProcess(TEMP_DATA_PATH)

            main_process.set_data_training_process(training_process)

            main_process.process(kwargs["data"])
        else:
            pass

    def apply(self, **kwargs):
        pass
