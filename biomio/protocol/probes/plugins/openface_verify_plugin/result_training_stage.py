from biomio.constants import TRAINING_RETRY_STATUS, TRAINING_RETRY_MESSAGE, TRAINING_SUCCESS_STATUS, \
    TRAINING_SUCCESS_MESSAGE, TRAINING_FAILED_STATUS, TRAINING_FAILED_MESSAGE
from biomio.algorithms.plugins_tools import store_training_db
from biomio.algorithms.flows.base import AlgorithmFlow
from algoflows_defs import FINAL_TRAINING_STAGE
from biomio.algorithms.logger import logger


class ResultTrainingStage(AlgorithmFlow):
    def __init__(self):
        AlgorithmFlow.__init__(self)
        
    def apply(self, data):
        """

        :param data: dictionary = {
                'algo_result': result dictionary,
                'callback_code': code of callback function,
                 'probe_id': probe identifier,
                 'temp_image_path': path to the temporary image storage,
                 'try_type': type of try,
                 'ai_code': AI response code
            }
        :return:
        """
        algo_result = data['algo_result']
        probe_id = data['probe_id']
        temp_image_path = data['temp_image_path']
        callback_code = data['callback_code']
        try_type = data['try_type']
        ai_code = data['ai_code']

        ai_response_type = dict()
        ai_response_type.update({'status': TRAINING_SUCCESS_STATUS, 'message': TRAINING_SUCCESS_MESSAGE})
        result = False
        error = None
        try:
            if isinstance(algo_result, dict) and algo_result.get('status', '') == "update":
                # record = dictionary:
                # key          value
                #      'status'     "update"
                #      'userID'     Unique user identificator
                #      'algoID'     Unique algorithm identificator
                #      'database'   BLOB data of user, with userID, for verification algorithm algoID
                #
                # Need update record in algorithms database or create record for user userID and algorithm
                # algoID if it doesn't exists
                database = algo_result.get('database', None)
                if database is not None:
                    store_training_db(database, probe_id)
                    result = True
                    ai_response_type.update({'status': TRAINING_SUCCESS_STATUS, 'message': TRAINING_SUCCESS_MESSAGE})
            elif isinstance(algo_result, list):
                for algo_result_item in algo_result:
                    if algo_result_item.get('status', '') == "error":
                        logger.exception('Error during education - %s, %s, %s' % (algo_result_item.get('status'),
                                                                                  algo_result_item.get('type'),
                                                                                  algo_result_item.get('details')))
                        if 'Internal Training Error' in algo_result_item.get('type', ''):
                            error = algo_result_item.get('details', {}).get('message', '')
                            ai_response_type.update({'status': TRAINING_RETRY_STATUS,
                                                     'message': TRAINING_RETRY_MESSAGE})
                        else:
                            ai_response_type.update({'status': 'error'})

                    elif algo_result_item.get('status', '') == 'update':
                        database = algo_result_item.get('database', None)
                        if database is not None:
                            store_training_db(database, probe_id)
                            result = True
                            ai_response_type.update({'status': TRAINING_SUCCESS_STATUS,
                                                     'message': TRAINING_SUCCESS_MESSAGE})
                # record = dictionary:
                # key          value
                #      'status'     "error"
                #      'type'       Type of error
                #      'userID'     Unique user identificator
                #      'algoID'     Unique algorithm identificator
                #      'details'    Error details dictionary
                #
                # Algorithm can have three types of errors:
                #       "Algorithm settings are empty"
                #        in this case fields 'userID', 'algoID', 'details' are empty
                #       "Invalid algorithm settings"
                #        in this case 'details' dictionary has following structure:
                #               key         value
                #               'params'    Parameters key ('data')
                #               'message'   Error message (for example "File <path> doesn't exists")
                #       "Internal algorithm error"
                # Need save to redis
                pass
            elif algo_result.get('status', '') == "error":
                logger.exception('Error during education - %s, %s, %s' % (algo_result.get('status'),
                                                                          algo_result.get('type'),
                                                                          algo_result.get('details')))
                if 'Internal Training Error' in algo_result.get('type', ''):
                    error = algo_result.get('details', {}).get('message', '')
                    ai_response_type.update({'status': TRAINING_RETRY_STATUS, 'message': TRAINING_RETRY_MESSAGE})
                else:
                    ai_response_type.update({'status': 'error'})
                    ai_response_type.update({'status': TRAINING_FAILED_STATUS, 'message': TRAINING_FAILED_MESSAGE})
                # record = dictionary:
                # key          value
                #      'status'     "error"
                #      'type'       Type of error
                #      'userID'     Unique user identificator
                #      'algoID'     Unique algorithm identificator
                #      'details'    Error details dictionary
                #
                # Algorithm can have three types of errors:
                #       "Algorithm settings are empty"
                #        in this case fields 'userID', 'algoID', 'details' are empty
                #       "Invalid algorithm settings"
                #        in this case 'details' dictionary has following structure:
                #               key         value
                #               'params'    Parameters key ('data')
                #               'message'   Error message (for example "File <path> doesn't exists")
                #       "Internal algorithm error"
                # Need save to redis
                pass
        except Exception as e:
            logger.exception(e)
        finally:
            self._stages[FINAL_TRAINING_STAGE].apply({'temp_image_path': temp_image_path, 'probe_id': probe_id,
                                                      'error': error, 'callback_code': callback_code, 'result': result,
                                                      'ai_response_type': ai_response_type, 'try_type': try_type,
                                                      'ai_code': ai_code})
