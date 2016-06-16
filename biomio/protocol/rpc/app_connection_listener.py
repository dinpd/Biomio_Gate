# import tornado.gen
from biomio.protocol.storage.redis_subscriber import RedisSubscriber
# from tornadoredis import Client
import re

from biomio.constants import REDIS_APP_AUTH_KEY, GENERAL_SUBSCRIBE_PATTERN, PROBE_APP_TYPE_PREFIX
# from biomio.protocol.settings import settings

import logging

logger = logging.getLogger(__name__)


class AppConnectionListener:
    def __init__(self, app_id, app_type):
        self._redis_channel = self.app_key_pattern(app_id=app_id, app_type=app_type)

        self._callback = None
        self._redis_subscriber = RedisSubscriber.instance()
        # self._redis = Client(host=settings.redis_host, port=settings.redis_port)
        # self._redis.connect()

    @staticmethod
    def app_key_pattern(app_id, app_type):
        if app_type == PROBE_APP_TYPE_PREFIX:
            redis_key_pattern = AppConnectionListener.auth_key('.*', app_id)
        else:
            redis_key_pattern = AppConnectionListener.auth_key(app_id, '.*')

        return redis_key_pattern

    @staticmethod
    def auth_key(extension_id, probe_id=None):
        """
        Return key that used for storing auth data for application. Requires both connected extension and probe ids
        for probe.
        If probe_id is None - temporary key for extension is generated, and should be generated again (with connected
        probe id) when probe will be available.
        :param extension_id: Extension app id string.
        :param probe_id: Probe app id string.
        :return: Auth data key.
        """
        redis_key = '%s:%s' % (extension_id, probe_id) if probe_id is not None else extension_id
        return REDIS_APP_AUTH_KEY % redis_key if redis_key else ''

    def subscribe(self, callback):
        if callback:
            self._callback = callback
            self._redis_subscriber.subscribe(channel_key=self._redis_channel, callback=self._on_redis_message)
            # yield tornado.gen.Task(self._redis.psubscribe, self._redis_channel)
            # self._redis.listen(self._on_redis_message)
            logger.debug("Subscribed to %s" % self._redis_channel)
        else:
            logger.error("Could not subscribe application")

    def unsubscribe(self):
        if self._redis_channel is not None:
            # logger.debug("Unsubscribing from %s" % self._redis_channel)
            self._callback = None
            self._redis_subscriber.unsubscribe(channel_key=self._redis_channel)
            # yield tornado.gen.Task(self._redis.punsubscribe, self._redis_channel)
        else:
            logger.error(msg='Could not unsubscribe applicaiton')

    @staticmethod
    def extension_id(redis_auth_key):
        return re.search(REDIS_APP_AUTH_KEY % '(.*):(.*)', redis_auth_key).group(1)

    @staticmethod
    def probe_id(redis_auth_key):
        return re.search(REDIS_APP_AUTH_KEY % '(.*):(.*)', redis_auth_key).group(2)

    def _on_redis_message(self, message):
        if message.kind == 'pmessage':
            if message.body == 'set' or message.body == 'expired' or message.body == 'del':

                extension_id = self.extension_id(redis_auth_key=message.channel)
                probe_id = self.probe_id(redis_auth_key=message.channel)

                if self._callback:
                    logger.debug("######## GOT AUTH MESSAGE FROM SUBSCRIBED APP : %s" % str(message))
                    try:
                        self._callback(extension_id, probe_id)
                    except Exception as e:
                        logger.warn(str(e))
                        pass
