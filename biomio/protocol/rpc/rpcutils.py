from functools import wraps
import tornado.gen
import inspect

from biomio.protocol.storage.proberesultsstore import ProbeResultsStore
from biomio.protocol.settings import settings

import logging
logger = logging.getLogger(__name__)

# Arguments that are implicitly passed to every RPC routine.
# If rpc routine does not takes explicitly one or all of this arguments,
# it will be excluded from argument list before call. Method should be decorated
# with @rpc_call or @rpc_call_with_auth decorators for that.
CALLBACK_ARG = 'callback'
USER_ID_ARG = 'user_id'
WAIT_CALLBACK_ARG = 'wait_callback'


def _check_rpc_arguments(callable_func, current_kwargs):
    """
    Internal helper method to check if all argument should be passed
    to RPC routine.

    Some arguments (like user_id, wait_callback ...) are implicitly passed
    to every RPC routine. If rpc routine does not takes explicitly one or
    all of this arguments, this function exclude them from argument list before call.
    :param callable_func: RPC routine
    :param current_kwargs: Named arguments that are passed to RPC routine.
    :return: Resulting arguments list.
    """
    result_kwargs = {}

    def _get_required_args(callable_func):
        args, varargs, varkw, defaults = inspect.getargspec(callable_func)
        if defaults:
            args = args[:-len(defaults)]
        return args

    required_args = _get_required_args(callable_func)

    implicit_params_list = [USER_ID_ARG, CALLBACK_ARG, WAIT_CALLBACK_ARG]
    for k, v in current_kwargs.iteritems():
        if k in implicit_params_list and k not in required_args:
            continue
        else:
            result_kwargs[k] = v

    return result_kwargs


def rpc_call(rpc_func):
    """
    Every RPC routine (that do not require biometric authentication) should be decorated with @rpc_call decorator.
    """
    def _decorator(*args, **kwargs):
        callable_kwargs = _check_rpc_arguments(callable_func=rpc_func, current_kwargs=kwargs)
        result = rpc_func(*args, **callable_kwargs)
        status = 'complete'

        # Send call results
        try:
            callback = kwargs.get(CALLBACK_ARG, None)
            callback(result=result, status=status)
        except Exception as e:
            logger.debug(msg="RPC call processing error: %s" % str(e))

    return wraps(rpc_func)(_decorator)


@tornado.gen.engine
def _is_biometric_data_valid(callable_func, callable_args, callable_kwargs):
    """
    Provides biometric authentication to support @rpc_call_with_auth
    :param callable_func: RPC routine
    :param callable_args: List of arguments of RPC routine.
    :param callable_kwargs: List of named arguments of RPC routine.
    """
    user_id = callable_kwargs.get(USER_ID_ARG, None)
    wait_callback = callable_kwargs.get(WAIT_CALLBACK_ARG, None)
    callback = callable_kwargs.get(CALLBACK_ARG, None)

    # Send RPC message with inprogress state
    try:
        wait_callback()
    except Exception as e:
        logger.debug(msg="RPC call with auth error - could not send rpc inprogress status: %s" % str(e))
        callback(result={"error": str(e)}, status='fail')

    # Check if there is already connection that waiting for biometric auth
    if ProbeResultsStore.instance().has_probe_results(user_id=user_id):
        is_already_waiting = ProbeResultsStore.instance().get_probe_data(user_id=user_id, key='waiting_auth')
        if not is_already_waiting:
            # Remove existing key, create new
            ProbeResultsStore.instance().remove_probe_data(user_id)
            ProbeResultsStore.instance().store_probe_data(user_id=user_id, ttl=settings.bioauth_timeout, waiting_auth=True)
        else:
            # Another connection is waiting on auth - do nothing, just subscribe later
            pass
    else:
        # There is no key for probe results - create and wait for auth
        ProbeResultsStore.instance().store_probe_data(user_id=user_id, ttl=settings.bioauth_timeout, waiting_auth=True)

    # Create redis key - that will trigger probe try message
    yield tornado.gen.Task(ProbeResultsStore.instance().subscribe_to_data, user_id, 'auth')

    error_msg = None
    user_authenticated = None

    # Check if key does not expire
    if ProbeResultsStore.instance().has_probe_results(user_id=user_id):
        # Not expired, get probe results
        user_authenticated = ProbeResultsStore.instance().get_probe_data(user_id=user_id, key='auth')
        if not user_authenticated:
            error_msg = 'Biometric authentication failed.'
    else:
        error_msg = 'Biometric auth timeout'

    try:
        if user_authenticated:
            kwargs = _check_rpc_arguments(callable_func=callable_func, current_kwargs=callable_kwargs)
            result = callable_func(*callable_args, **kwargs)
            callback(result=result, status='complete')
        else:
            callback(result={"error": error_msg}, status='fail')
    except Exception as e:
        logger.debug(msg="RPC call with auth processing error: %s" % str(e))


def rpc_call_with_auth(rpc_func):
    """
    Every RPC routine that require biometric authentication should be decorated with @rpc_call_with_auth decorator.
    """
    def _decorator(*args, **kwargs):
        _is_biometric_data_valid(callable_func=rpc_func, callable_args=args, callable_kwargs=kwargs)

    return wraps(rpc_func)(_decorator)
