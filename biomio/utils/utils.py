from __future__ import absolute_import
import importlib
import logging
from apns import APNs, Payload
from biomio.constants import REDIS_JOB_RESULT_KEY
from biomio.protocol.settings import APNS_PRODUCTION_PEM, APNS_DEV_PEM, settings
from biomio.protocol.storage.redis_storage import RedisStorage

logger = logging.getLogger(__name__)


def push_notification_callback(message, clear=False):
    """

    :param message: str message to send to device.
    :param clear: specifies whether it is required to clear the notifications on device,
    """

    def send_push_notification(data):
        """
            Sends push notification to device by specified token and with specified message
        :param data: dictionary with Apple device notification token.
        """
        push_token = data.get('push_token')
        try:
            logger.info('Sending push notification to app - %s' % data.get('device_token'))
            if push_token is not None and len(push_token) > 0:
                if settings.dev_mode:
                    cert_file = APNS_DEV_PEM
                else:
                    cert_file = APNS_PRODUCTION_PEM

                apns = APNs(use_sandbox=settings.dev_mode, cert_file=cert_file)
                payload = Payload(alert=message, sound='default' if not clear else None, badge=0 if clear else 1)

                apns.gateway_server.send_notification(token_hex=push_token, payload=payload)
                logger.info('Notification sent')
        except Exception as e:
            logger.exception(e)

    return send_push_notification


def import_module_class(module, class_name):
    """
        Imports specified class from given module
    :param module: absolute path to module
    :param class_name: name of the class to import
    :return:
    """
    module = importlib.import_module(module)
    return getattr(module, class_name, None)


def store_job_result(record_key, record_dict, callback_code):
    """
        Stores job result data into redis with generated JOB_RESULT key.
    :param record_key: Redis key of the current record object.
    :param record_dict: dict data from the current record.
    :param callback_code: Code of the callback that must be executed after we got result.
    """
    _persistence_redis = RedisStorage.persistence_instance()
    job_result_key = REDIS_JOB_RESULT_KEY % (callback_code, record_key)
    _persistence_redis.store_data(key=job_result_key, **record_dict)


def delete_custom_redis_data(key, lru=False):
    """
        Deletes data only from persistence redis instance for given redis key.
    :param key: Generated redis key.
    """
    if lru:
        _persistence_redis = RedisStorage.lru_instance()
    else:
        _persistence_redis = RedisStorage.persistence_instance()
    _persistence_redis.delete_data(key)
