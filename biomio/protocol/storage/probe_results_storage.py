from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.protocol.settings import settings

import ast
import re
from tornadoredis import Client
import tornado.gen

import logging
logger = logging.getLogger(__name__)


class ProbeResultsStorage():
    _instance = None

    def __init__(self):
        #TODO: listen to right instance of redis
        self.redis = Client(host=settings.redis_host, port=settings.redis_port)
        self._persistence_redis = RedisStorage.persistence_instance()
        self.callback_by_key = {}
        self.data_key_by_callback = {}
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.redis.connect()
        yield tornado.gen.Task(self.redis.psubscribe, "__keyspace*:probe:*")
        self.redis.listen(self.on_redis_message)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ProbeResultsStorage()

        return cls._instance

    @staticmethod
    def redis_probe_key(user_id):
        # TODO: removed for test purposes - should be fixed when userId handling in probe, extension and server
        # will be implemented
        # probe_key = 'probe:%s' % user_id
        probe_key = 'probe:id'
        return probe_key

    # def has_probe_results(self, user_id):
    #     return self._redis.exists(name=self.redis_probe_key(user_id=user_id))


    def get_probe_data(self, user_id, key):
        data = self._persistence_redis.get_data(key=self.redis_probe_key(user_id=user_id))
        if not data:
            data = {}
        else:
            data = ast.literal_eval(data)
        return data.get(key, None)

    def store_probe_data(self, user_id, ttl=None, **kwargs):
        key = self.redis_probe_key(user_id=user_id)
        self._persistence_redis.store_data(key=key, ex=ttl, **kwargs)

    def remove_probe_data(self, user_id):
        key = self.redis_probe_key(user_id=user_id)
        self._persistence_redis.delete_data(key)

    def subscribe_to_data(self, user_id, data_key, callback):
        self.data_key_by_callback[callback] = data_key
        self.subscribe(user_id, callback)

    def subscribe(self, user_id, callback):
        #TODO: added for test purposes - remove later
        user_id = 'id'
        key = self.redis_probe_key(user_id=user_id)
        subscribers = self.callback_by_key.get(key, [])
        if not subscribers or callback not in subscribers:
            subscribers.append(callback)
            self.callback_by_key[key] = subscribers

    def unsubscribe_all(self, user_id):
        user_id = 'id'
        probe_key = self.redis_probe_key(user_id)
        subscribers = self.callback_by_key.get(probe_key, [])
        for callback in subscribers:
            self.unsubscribe(user_id=user_id, callback=callback)

    def unsubscribe(self, user_id, callback):
        user_id = 'id'
        key = self.redis_probe_key(user_id=user_id)
        subscribers = self.callback_by_key.get(key, [])
        if subscribers and callback in subscribers:
            subscribers.remove(callback)
            self.callback_by_key[key] = subscribers
            if callback in self.data_key_by_callback:
                del self.data_key_by_callback[callback]

    def on_redis_message(self, msg):
        if msg.kind == 'pmessage':
            if msg.body == 'set' or msg.body == 'expired' or msg.body == 'del':
                probe_key = re.search('.*:(probe:.*)', msg.channel).group(1)
                # user_id = re.search('.*:probe:(.*)', msg.channel).group(1)
                subscribers = self.callback_by_key.get(probe_key, [])

                data = self._persistence_redis.get_data(probe_key)
                if msg.body == 'expired' and data:
                    return

                logger.debug("GOT SUBSCRIBED MESSAGE: %s" % (str(msg)))
                for callback in subscribers:
                    data_key = self.data_key_by_callback.get(callback, None)
                    if not data_key or (data_key and data.get(data_key, None)):
                        try:
                            logger.debug("CALLED: %s" % str(callback))
                            callback()
                            logger.debug("DONE")
                        except Exception as e:
                            logger.exception(msg=str(e))
