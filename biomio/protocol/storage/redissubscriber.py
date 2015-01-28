import re
from tornadoredis import Client
from biomio.protocol.settings import settings
from biomio.protocol.storage.proberesultsstore import ProbeResultsStore
import tornado.gen
from weakref import WeakValueDictionary

class RedisSubscriber:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = RedisSubscriber()
        return cls._instance

    def __init__(self):
        self.redis = Client(host=settings.redis_host, port=settings.redis_port)
        self.callback_by_key = {}
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.redis.connect()
        yield tornado.gen.Task(self.redis.psubscribe, "__keyspace*:probe:*")
        self.redis.listen(self.on_redis_message)

    @tornado.gen.engine
    def subscribe(self, user_id, callback):
        key = RedisSubscriber._redis_probe_key(user_id=user_id)
        subscribers = self.callback_by_key.get(key, [])
        if not subscribers or callback not in subscribers:
            subscribers.append(callback)
            self.callback_by_key[key] = subscribers
        print key, callback

    def unsubscribe(self, user_id, callback):
        key = RedisSubscriber._redis_probe_key(user_id=user_id)
        subscribers = self.callback_by_key.get(key, [])
        if subscribers and callback in subscribers:
            subscribers.remove(callback)
            self.callback_by_key[key] = subscribers

    @staticmethod
    def _redis_probe_key(user_id):
        return ProbeResultsStore.redis_probe_key(user_id=user_id)
        # # TODO: removed for test purposes - should be fixed when userId handling in probe, extension and server
        # # will be implemented
        # # probe_key = 'probe:%s' % user_id
        # probe_key = 'probe:'
        # return probe_key

    def on_redis_message(self, msg):
        if msg.kind == 'pmessage':
            if msg.body == 'set' or msg.body == 'expired':
                probe_key = re.search('.*:(probe:.*)', msg.channel).group(1)
                subscribers = self.callback_by_key.get(probe_key, None)
                if subscribers:
                    for callback in subscribers:
                        callback()