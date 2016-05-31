from biomio.protocol.probes.plugins.face_identification_plugin.processes.interface_helper import pre_training_helper, \
    result_training_helper, final_helper
from biomio.algorithms.openface.openface_simple_dist_estimate import OpenFaceSimpleDistanceEstimation
from biomio.algorithms.openface.openface_data_rep import OpenFaceDataRepresentation
from algoflows_defs import OPENFACE_DATA_REPRESENTATION, OPENFACE_SD_ESTIMATE
from openface_verify_algorithm import OpenFaceVerificationFlowAlgorithm
from openface_training_algorithm import OpenFaceTrainingFlowAlgorithm
from biomio.algorithms.interfaces import AlgorithmInterface
from helper import pre_verification_helper, result_handling
from initial_training_stage import InitialTrainingStage
from final_training_stage import FinalTrainingStage
from analytics.handlers import error_handler
from biomio.algorithms.logger import logger
from defs import OPENFACE_PATH, APP_ROOT
import os


MODEL_DIR = os.path.join(OPENFACE_PATH, "models")
DLIB_MODEL_DIR = os.path.join(MODEL_DIR, "dlib")
OPENFACE_MODEL_DIR = os.path.join(MODEL_DIR, "openface")
DLIB_MODEL_NAME = "shape_predictor_68_face_landmarks.dat"
OPENFACE_MODEL_NAME = 'nn4.small2.v1.t7'
IMAGE_DIMENSION = 96


def training_job(callback_code, **kwargs):
    logger.debug("-----------------------------------")
    logger.debug("OpenFaceVerificationPlugin::training_job")
    logger.debug(kwargs)
    logger.debug("-----------------------------------")
    init_training = InitialTrainingStage()
    init_training.addStage(FinalTrainingStage())
    settings = init_training.apply({'images': kwargs['images'], 'probe_id': kwargs['probe_id'],
                                    'settings': kwargs['settings'], 'callback_code': callback_code,
                                    'try_type': kwargs['try_type'], 'ai_code': kwargs['ai_code'],
                                    'temp_data_dir': APP_ROOT})
    settings.update({'threshold': kwargs['threshold']})
    algo = OpenFaceAlgorithmInterface()
    res = algo.training(callback=None, **settings)
    res_record = {
        'status': "update",
        'userID': settings['userID'],
        'database': res
    }
    result = {
        'algo_result': res_record,
        'temp_image_path': settings['general_data']['data_path'],
        'probe_id': settings['general_data']['probe_id'],
        'try_type': settings['general_data']['try_type'],
        'ai_code': settings['general_data']['ai_code']
    }
    logger.info('Status::The database updated.')
    result_training_helper(callback_code=callback_code, final_func=final_helper, **result)


def verification_job(callback_code, **kwargs):
    logger.debug("-----------------------------------")
    logger.debug("OpenFaceVerificationPlugin::verification_job")
    logger.debug(kwargs)
    logger.debug("-----------------------------------")
    settings = pre_verification_helper(callback_code=callback_code, **kwargs)
    settings.update({'metadata': {'probeID': kwargs['probe_id'], 'userID': kwargs['settings']['userID']}})
    algo = OpenFaceAlgorithmInterface()
    res = algo.apply(callback=None, **settings)
    result_handling(result=res['result'], probe_id=kwargs['probe_id'], temp_image_path=settings['temp_image_path'],
                    settings=kwargs['settings'], callback_code=callback_code)


class OpenFaceAlgorithmInterface(AlgorithmInterface):
    def __init__(self):
        self._callback = None
        self._data_rep = OpenFaceDataRepresentation({
            'dlibFacePredictor': os.path.join(DLIB_MODEL_DIR, DLIB_MODEL_NAME),
            'networkModel': os.path.join(OPENFACE_MODEL_DIR, OPENFACE_MODEL_NAME),
            'imgDim': IMAGE_DIMENSION,
            'error_handler': error_handler
        })
        self._sd_estimate = OpenFaceSimpleDistanceEstimation()

    def _interface_callback(self, result):
        self._callback(result)

    def training(self, callback=None, **kwargs):
        training_algo = OpenFaceTrainingFlowAlgorithm()
        training_algo.addStage(OPENFACE_DATA_REPRESENTATION, self._data_rep)
        return training_algo.apply(kwargs)

    def apply(self, callback=None, **kwargs):
        verify_algo = OpenFaceVerificationFlowAlgorithm()
        verify_algo.addStage(OPENFACE_DATA_REPRESENTATION, self._data_rep)
        verify_algo.addStage(OPENFACE_SD_ESTIMATE, self._sd_estimate)
        return verify_algo.apply(kwargs)
