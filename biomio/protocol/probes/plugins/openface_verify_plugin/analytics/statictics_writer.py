from biomio.algorithms.analytics.dataformats import VerificationResultFormat, ImageErrorFormat
from biomio.protocol.probes.plugins.openface_verify_plugin.defs import APP_ROOT, os
from biomio.algorithms.analytics.dataformat_stream import DataFormatStream


STATISTICS_FILE_NAME = 'stat.log'
ERROR_FILE_NAME = 'error.log'
STATISTICS_PATH = os.path.join(APP_ROOT, STATISTICS_FILE_NAME)
ERROR_PATH = os.path.join(APP_ROOT, ERROR_FILE_NAME)

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


def append_verify_result_output(dataformat):
    data_stream.addFormat(dataformat)


def print_verify_result_output():
    data_stream.write()


error_stream = DataFormatStream(ERROR_PATH)


def append_error_handle_format(data):
    """

    :param data: {
            'path': image path,
            'message': error message
        }
    """
    error_stream.addFormat(ImageErrorFormat(data))


def append_error_handle_output(dataformat):
    error_stream.addFormat(dataformat)


def print_error_handle_output():
    error_stream.write()


