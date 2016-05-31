from biomio.algorithms.logger import logger
from statictics_writer import append_error_handle_format, print_error_handle_output

def error_handler(message):
    logger.debug(message.get('message', None))
    append_error_handle_format(message)
    print_error_handle_output()

