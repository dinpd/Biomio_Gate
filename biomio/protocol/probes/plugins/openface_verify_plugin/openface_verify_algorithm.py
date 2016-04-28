from statictics_writer import append_verify_result_format, print_verify_result_output
from algoflows_defs import OPENFACE_DATA_REPRESENTATION, OPENFACE_SD_ESTIMATE
from biomio.algorithms.flows.flow import AlgorithmFlow
from biomio.algorithms.logger import logger
import os


class OpenFaceVerificationFlowAlgorithm(AlgorithmFlow):
    """
    Input:
    {
        'database': database based on the training data
        {
            'data': list of training data
            {
                'rep': representation array
            }
            'threshold': threshold for database
        }
        'data': test data
        {
            'rep': representation array
        }
    }
    Output:
    {
        'result': bool value (True or False)
    }
    """

    def __init__(self):
        AlgorithmFlow.__init__(self)

    def apply(self, data):
        logger.debug("===================================")
        logger.debug("OpenFaceVerificationFlowAlgorithm::apply")
        logger.debug(data)
        logger.debug("===================================")
        if data is None:
            # TODO: Write Error handler
            return {'result': False}
        database = data.get('database')
        path = data.get('data')
        if data.get('backup_image_path', None) is not None:
            path = os.path.join(data.get('backup_image_path'), os.path.basename(path))
        tdata = self._stages.get(OPENFACE_DATA_REPRESENTATION).apply({'path': path})
        if tdata is None or len(tdata.get('rep', [])) <= 0:
            return {'result': False}
        dist = self._stages.get(OPENFACE_SD_ESTIMATE).apply({'data': tdata, 'database': database})
        result = {'result': dist['result'] < database.get('threshold', 0.0)}
        ##############################################################################################
        #                                   Statistics Data Stream
        ##############################################################################################
        stat_data = data.get('metadata', {}).copy()
        stat_data.update({'threshold': database.get('threshold', 0.0), 'status': dist['result'],
                          'result': result['result'], 'data_path': data.get('backup_image_path', "")})
        append_verify_result_format(stat_data)
        print_verify_result_output()
        ##############################################################################################
        return result
