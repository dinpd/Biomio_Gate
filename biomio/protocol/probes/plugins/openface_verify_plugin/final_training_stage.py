from biomio.constants import REDIS_PROBE_RESULT_KEY, REDIS_UPDATE_TRAINING_KEY, REDiS_TRAINING_RETRIES_COUNT_KEY, \
    TRAINING_MAX_RETRIES_STATUS, TRAINING_MAX_RETRIES_MESSAGE
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.plugins_tools import tell_ai_training_results
from biomio.algorithms.flows.base import AlgorithmFlow
from biomio.algorithms.logger import logger
import shutil


class FinalTrainingStage(AlgorithmFlow):
    def __init__(self):
        AlgorithmFlow.__init__(self)

    def apply(self, data):
        """

        :param data: dictionary = {
                'temp_image_path': path to the temporary image storage,
                'probe_id': probe identifier,
                'error': error message,
                'callback_code': code of callback function,
                'result': status of result
                'ai_response_type': type of AI response,
                'try_type': type of try
                'ai_code': AI response code
            }
        :return:
        """
        temp_image_path = data['temp_image_path']
        error = data['error']
        probe_id = data['probe_id']
        ai_response_type = data['ai_response_type']
        callback_code = data['callback_code']
        result = data['result']
        try_type = data['try_type']
        ai_code = data['ai_code']

        shutil.rmtree(temp_image_path)
        if error is not None:
            retries_count = AlgorithmsDataStore.instance().decrement_int_value(
                REDiS_TRAINING_RETRIES_COUNT_KEY % probe_id)
            if retries_count == 0:
                AlgorithmsDataStore.instance().delete_data(key=REDiS_TRAINING_RETRIES_COUNT_KEY % probe_id)
                logger.debug('Maximum training attempts reached...')
                result = False
                ai_response_type.update({'status': TRAINING_MAX_RETRIES_STATUS,
                                         'message': TRAINING_MAX_RETRIES_MESSAGE})
            else:
                AlgorithmsDataStore.instance().store_data(key=REDIS_UPDATE_TRAINING_KEY % probe_id, error=error)
                result = dict(result=False, error=error)
            AlgorithmsDataStore.instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
            logger.info('Job was finished with internal algorithm error %s ' % error)
        else:
            AlgorithmsDataStore.instance().delete_data(key=REDiS_TRAINING_RETRIES_COUNT_KEY % probe_id)
            AlgorithmsDataStore.instance().store_data(key=REDIS_PROBE_RESULT_KEY % callback_code, result=result)
        tell_ai_training_results(result, ai_response_type, try_type, ai_code)
        return None
