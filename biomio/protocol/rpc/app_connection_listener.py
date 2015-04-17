import tornado.gen
from tornadoredis import Client
import re

from biomio.constants import REDIS_APP_AUTH_KEY
from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)

GENERAL_SUBSCRIBE_PATTERN = '__keyspace*:{redis_key_pattern}'
EXTENSION_SUBSCRIBE_PATTERN = '{extension_id}:*'
PROBE_SUBSCRIBE_PATTERN = '*:{probe_id}'


class AppConnectionListener():
    # _instance = None

    # @classmethod
    # def instance(cls):
    #     if not cls._instance:
    #         cls._instance = AppConnectionListener()
    #
    #     return cls._instance

    def __init__(self, app_id, app_type):
        self._redis_channel = AppConnectionListener._subscribe_channel(app_id=app_id, app_type=app_type)

        self._callback = None

        self._redis = Client(host=settings.redis_host, port=settings.redis_port)
        self._redis.connect()

        # self._listen()

    # @tornado.gen.engine
    # def _listen(self, key):
    #     self._redis.connect()
    #     redis_key_pattern = '{redis_auth_key}:*'.format(redis_auth_key=REDIS_APP_AUTH_KEY)
    #     yield tornado.gen.Task(self._redis.psubscribe,
    #                            GENERAL_SUBSCRIBE_PATTERN.format(redis_key_pattern=redis_key_pattern))

    @staticmethod
    def _subscribe_channel(app_id, app_type):
        redis_key_pattern = ''

        if app_type == 'extension':
            redis_key_pattern = AppConnectionListener._auth_key(app_id, '*')
        elif app_type == 'probe':
            redis_key_pattern = AppConnectionListener._auth_key('*', app_id)
        else:
            logger.error(msg='Unknown app type')

        print redis_key_pattern
        return GENERAL_SUBSCRIBE_PATTERN.format(redis_key_pattern=redis_key_pattern) if redis_key_pattern else ''

    @staticmethod
    def _auth_key(extension_id, probe_id=None):
        redis_key = '%s:%s' % (extension_id, probe_id) if probe_id is not None else extension_id
        return REDIS_APP_AUTH_KEY % redis_key if redis_key else ''

    @tornado.gen.engine
    def subscribe(self, callback):
        if callback:
            self._callback = callback

            yield tornado.gen.Task(self._redis.psubscribe, self._redis_channel)
            self._redis.listen(self._on_redis_message)
            logger.debug("Subscribed to %s" % self._redis_channel)
        else:
            logger.error("Could not subscribe application")

    @tornado.gen.engine
    def unsubscribe(self):
        if self._redis_channel is not None:
            logger.debug("Unsubscribing from %s" % self._redis_channel)
            yield tornado.gen.Task(self._redis.punsubscribe, self._redis_channel)
        else:
            logger.error(msg='Could not unsubscribe applicaiton')

    def _on_redis_message(self, msg):
        if msg.kind == 'pmessage':
            if msg.body == 'set' or msg.body == 'expired' or msg.body == 'del':
                probe_key = re.search('.*:(%s:.*)' % REDIS_APP_AUTH_KEY, msg.channel).group(1)
                # user_id = re.search('.*:probe:(.*)', msg.channel).group(1)
                # subscribers = self.callback_by_key.get(probe_key, [])

                # data = self._persistence_redis.get_data(probe_key)
                # if msg.body == 'expired' and data:
                #     return

                logger.debug("GOT AUTH MESSAGE FROM SUBSCRIBED APP (%s) : %s" % (self._app_id, str(msg)))

                # for callback in subscribers:
                #     data_key = self.data_key_by_callback.get(callback, None)
                #     if not data_key or (data_key and data.get(data_key, None)):
                #         try:
                #             logger.debug("CALLED: %s" % str(callback))
                #             self._callback()
                #             logger.debug("DONE")
                #         except Exception as e:
                #             logger.exception(msg=str(e))
