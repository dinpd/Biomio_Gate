import logging
import os
from biomio.protocol.settings import settings

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
BIOMIO_LOGS_PATH = os.path.join(APP_ROOT, 'biomio', 'logs')

WORKER_LOG_NAME = 'worker.log'
PONY_LOG_NAME = 'mysql_queries.log'

logging.basicConfig(
    format='[%(asctime)s - %(name)s - %(levelname)s] - %(message)s',
    level=settings.logging
)

log_formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')

worker_file_handler = logging.FileHandler(os.path.join(BIOMIO_LOGS_PATH, WORKER_LOG_NAME))
worker_file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

worker_logger = logging.getLogger('worker')
worker_logger.setLevel(settings.logging)
worker_logger.addHandler(worker_file_handler)
worker_logger.addHandler(console_handler)

pony_orm_file_handler = logging.FileHandler(os.path.join(BIOMIO_LOGS_PATH, PONY_LOG_NAME))
pony_orm_file_handler.setFormatter(log_formatter)

pony_orm_logger = logging.getLogger('pony.orm')
pony_orm_logger.setLevel(logging.INFO)
pony_orm_logger.addHandler(pony_orm_file_handler)
pony_orm_logger.addHandler(console_handler)

pony_sql_logger = logging.getLogger('pony.orm.sql')
pony_sql_logger.setLevel(logging.INFO)
pony_sql_logger.addHandler(pony_orm_file_handler)
pony_sql_logger.addHandler(console_handler)