from __future__ import absolute_import
import importlib
import logging
from apns import APNs, Payload
from biomio.protocol.settings import APNS_PRODUCTION_PEM, APNS_DEV_PEM, settings


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
                payload = Payload(alert=message, sound='default', badge=0 if clear else None)

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
