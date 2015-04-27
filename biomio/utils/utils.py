import os
from apns import APNs, Payload

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

PRODUCTION_CERT_FILE = ''
PRODUCTION_KEY_FILE = ''

SANDBOX_CERT_FILE = ''
SANDBOX_KEY_FILE = ''


def send_push_notification(device_token, message, use_sandbox=False):
    """
        Sends push notification to device by specified token and with specified message
    :param device_token: Apple device notification token.
    :param message: str message to send to device.
    :param use_sandbox: indicates whether to use sandbox mode.
    """
    if use_sandbox:
        cert_file = SANDBOX_CERT_FILE
        key_file = SANDBOX_KEY_FILE
    else:
        cert_file = PRODUCTION_CERT_FILE
        key_file = PRODUCTION_KEY_FILE

    apns = APNs(use_sandbox=use_sandbox, cert_file=cert_file, key_file=key_file)
    payload = Payload(alert=message, sound='default', badge=1)

    apns.gateway_server.send_notification(token_hex=device_token, payload=payload)