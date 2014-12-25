import re
from tornadoredis import Client
from biomio.protocol.settings import settings
import tornado.gen

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
        self.args_by_key = {}
        self.kwargs_by_key = {}
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.redis.connect()
        yield tornado.gen.Task(self.redis.psubscribe, "__keyspace*:probe:*")
        self.redis.listen(self.on_redis_message)

    @tornado.gen.engine
    def subscribe(self, user_id, callback=None):
        key = RedisSubscriber._redis_probe_key(user_id=user_id)
        self.callback_by_key[key] = callback

    @staticmethod
    def _redis_probe_key(user_id):
        probe_key = 'probe:%s' % user_id
        return probe_key

    def on_redis_message(self, msg):
        if msg.kind == 'pmessage':
            if msg.body == 'set' or msg.body == 'expired':
                probe_key = re.search('.*:(probe:.*)', msg.channel).group(1)
                callback = self.callback_by_key.get(probe_key, None)
                if callback:
                    callback()