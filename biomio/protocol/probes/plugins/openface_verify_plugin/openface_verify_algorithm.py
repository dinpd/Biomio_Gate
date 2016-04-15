from algoflows_defs import OPENFACE_DATA_REPRESENTATION, OPENFACE_SD_ESTIMATE
from biomio.algorithms.flows.flow import AlgorithmFlow
from biomio.algorithms.logger import logger
from statictics_writer import append_verify_result_format, print_output


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
            return data
        database = data.get('database')
        tdata = self._stages.get(OPENFACE_DATA_REPRESENTATION).apply({'path': data.get('data')})
        dist = self._stages.get(OPENFACE_SD_ESTIMATE).apply({'data': tdata, 'database': database})
        result = {'result': dist['result'] < database.get('threshold', 0.0)}
        ##############################################################################################
        #                                   Statistics Data Stream
        ##############################################################################################
        stat_data = data.get('metadata', {}).copy()
        stat_data.update({'threshold': database.get('threshold', 0.0), 'status': dist['result'],
                          'result': result['result']})
        append_verify_result_format(stat_data)
        print_output()
        ##############################################################################################
        return result
