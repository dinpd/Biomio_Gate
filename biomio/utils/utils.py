from __future__ import absolute_import
from apns import APNs, Payload
from django.utils import importlib
from biomio.protocol.settings import APNS_PRODUCTION_PEM, APNS_DEV_PEM


def send_push_notification(device_token, message, use_sandbox=False):
    """
        Sends push notification to device by specified token and with specified message
    :param device_token: Apple device notification token.
    :param message: str message to send to device.
    :param use_sandbox: indicates whether to use sandbox mode.
    """
    if use_sandbox:
        cert_file = APNS_DEV_PEM
    else:
        cert_file = APNS_PRODUCTION_PEM

    apns = APNs(use_sandbox=use_sandbox, cert_file=cert_file)
    payload = Payload(alert=message, sound='default', badge=1)

    apns.gateway_server.send_notification(token_hex=device_token, payload=payload)


def import_module_class(module, class_name):
    """
        Imports specified class from given module
    :param module: absolute path to module
    :param class_name: name of the class to import
    :return:
    """
    module = importlib.import_module(module)
    return getattr(module, class_name, None)