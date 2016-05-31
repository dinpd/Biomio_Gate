from biomio.constants import REDIS_UPDATE_TRAINING_KEY, TRAINING_SUCCESS_STATUS, TRAINING_SUCCESS_MESSAGE, \
    TRAINING_STARTED_STATUS, TRAINING_STARTED_MESSAGE
from biomio.algorithms.plugins_tools import store_test_photo_helper, ai_response_sender, get_algo_db, save_images
from biomio.protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from biomio.algorithms.flows.base import AlgorithmFlow
from biomio.algorithms.logger import logger
import tempfile


FINAL_TRAINING_STAGE = 'final_training_sg'


class InitialTrainingStage(AlgorithmFlow):
    def __init__(self):
        AlgorithmFlow.__init__(self)

    def apply(self, data):
        """

        :param data: dictionary = {
                'images': training image set,
                'probe_id': prove identifier,
                'settings': general settings dictionary,
                'callback_code': code of callback function,
                'try_type': type of try request,
                'ai_code': AI response code,
                'temp_data_dir': Path to the temporary storage
            }
        :return:
        """
        images = data['images']
        settings = data['settings']
        ai_code = data['ai_code']
        probe_id = data['probe_id']
        try_type = data['try_type']
        temp_data_dir = data['temp_data_dir']
        logger.info('Running training for user - %s, with given parameters - %s' % (settings.get('userID'),
                                                                                    settings))
        ai_response_type = dict()
        try:
            logger.info('Telling AI that we are starting training with code - %s' % ai_code)
            ai_response_type.update({'status': TRAINING_STARTED_STATUS, 'message': TRAINING_STARTED_MESSAGE})
            ai_response_sender(ai_code, ai_response_type)
        except Exception as e:
            # TODO: Write Error handler
            logger.error('Failed to build rest request to AI - %s' % str(e))
            logger.exception(e)
        ai_response_type.update({'status': TRAINING_SUCCESS_STATUS, 'message': TRAINING_SUCCESS_MESSAGE})
        result = False
        if AlgorithmsDataStore.instance().exists(key=REDIS_UPDATE_TRAINING_KEY % probe_id):
            settings.update({'database': get_algo_db(probe_id=probe_id)})
            AlgorithmsDataStore.instance().delete_data(key=REDIS_UPDATE_TRAINING_KEY % probe_id)
        temp_image_path = tempfile.mkdtemp(dir=temp_data_dir)
        try:
            image_paths = save_images(images, temp_image_path)

            # Store photos for test purposes
            store_test_photo_helper(temp_data_dir, image_paths)

            settings.update({'data': image_paths})
            settings.update({'general_data': {'data_path': temp_image_path, 'ai_code': ai_code,
                                              'try_type': try_type, 'probe_id': probe_id}})
            return settings
        except Exception as error:
            end_data = data.copy()
            del end_data['images']
            del end_data['settings']
            end_data.update({'temp_image_path': temp_image_path, 'error': error,
                             'result': result, 'ai_response_type': ai_response_type})
            return self._stages.get(FINAL_TRAINING_STAGE).apply(end_data)
