from algoflows_defs import OPENFACE_DATA_REPRESENTATION
from biomio.algorithms.flows.flow import AlgorithmFlow


class OpenFaceTrainingFlowAlgorithm(AlgorithmFlow):
    """
    Input:
    {
        'images': list of image paths
        'threshold': default threshold for database
        'database': [optional] trained database
        {
            'data': list of training data
            {
                'rep': representation array
            }
            threshold: threshold for database
        }
    }
    Output:
    {
        'data': list of training data
        {
            'rep': representation array
        }
        threshold: threshold for database
    }
    """
    def __init__(self):
        AlgorithmFlow.__init__(self)

    def apply(self, data):
        if data is None:
            # TODO: Write Error handler
            return data

        db = {
            'data': [],
            'threshold': data['threshold']
        } if data.get('database', None) is None else data.get('database')
        for img in data['images']:
            res = self._stages.get(OPENFACE_DATA_REPRESENTATION).apply({'path': img})
            db['data'].append(res)
        return db
