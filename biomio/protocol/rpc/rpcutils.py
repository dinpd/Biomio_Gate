from functools import wraps
import tornado.gen

from biomio.protocol.storage.redissubscriber import RedisSubscriber

@tornado.gen.engine
def _is_biometric_data_valid(callable_func, callable_args, callable_kwargs):
    user_id = "userid"
    # RedisProbeSubscriber.instance().subscribe(user_id)
    print 'waiting for redis...'
    yield tornado.gen.Task(RedisSubscriber.instance().subscribe, user_id)
    print 'results form redis...'
    callable_func(*callable_args, **callable_kwargs)


def biometric_auth(verify_func):
    def _decorator(*args, **kwargs):
        _is_biometric_data_valid(callable_func=verify_func, callable_args=args, callable_kwargs=kwargs)
    return wraps(verify_func)(_decorator)