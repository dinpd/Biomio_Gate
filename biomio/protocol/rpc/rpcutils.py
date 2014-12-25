from functools import wraps
import tornado.gen

from biomio.protocol.storage.redissubscriber import RedisSubscriber
from biomio.protocol.storage.proberesultsstore import ProbeResultsStore
from biomio.protocol.settings import settings


def _callback_arg(callable_kwargs):
    return callable_kwargs.get('callback', None)


@tornado.gen.engine
def _is_biometric_data_valid(callable_func, callable_args, callable_kwargs):
    user_id = "userid"
    ProbeResultsStore.instance().store_probe_data(user_id=user_id, ttl=settings.bioauth_timeout, auth=False)
    yield tornado.gen.Task(RedisSubscriber.instance().subscribe, user_id)

    status = None
    user_authenticated = None

    if ProbeResultsStore.instance().has_probe_results(user_id=user_id):
        # Not expired, get probe results
        user_authenticated = ProbeResultsStore.instance().get_probe_data(user_id=user_id, key='auth')
        if not user_authenticated:
            status = 'Biometric authentication failed.'
    else:
        status = 'Biometric auth timeout'

    if user_authenticated:
        callable_func(*callable_args, **callable_kwargs)
    else:
        callback = _callback_arg(callable_kwargs)
        callback({"status": status})
        pass


def biometric_auth(verify_func):
    def _decorator(*args, **kwargs):
        _is_biometric_data_valid(callable_func=verify_func, callable_args=args, callable_kwargs=kwargs)

    return wraps(verify_func)(_decorator)