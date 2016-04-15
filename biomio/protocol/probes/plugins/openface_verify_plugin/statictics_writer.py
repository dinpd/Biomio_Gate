from biomio.algorithms.statistics.dataformats import VerificationResultFormat
from biomio.algorithms.statistics.dataformat_stream import DataFormatStream
from defs import APP_ROOT, os

STATISTICS_FILE_NAME = 'stat.log'
STATISTICS_PATH = os.path.join(APP_ROOT, STATISTICS_FILE_NAME)

data_stream = DataFormatStream(STATISTICS_PATH)


def append_verify_result_format(data):
    """

    :param data: {
            'userID': user identifier,
            'probeID': probe identifier,
            'threshold': threshold coefficient,
            'status': data result,
            'result': algorithm result
        }
    """
    data_stream.addFormat(VerificationResultFormat(data))


def append_output(dataformat):
    data_stream.addFormat(dataformat)


def print_output():
    data_stream.write()

