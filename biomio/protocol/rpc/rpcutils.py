from functools import wraps
import tornado.gen
import inspect
import tornado.gen
import greenado
import traceback
from biomio.protocol.data_stores.application_data_store import ApplicationDataStore

from biomio.protocol.rpc import bioauthflow

import logging

logger = logging.getLogger(__name__)

# Arguments that are implicitly passed to every RPC routine.
# If rpc routine does not takes explicitly one or all of this arguments,
# it will be excluded from argument list before call. Method should be decorated
# with @rpc_call or @rpc_call_with_auth decorators for that.
CALLBACK_ARG = 'callback'
USER_ID_ARG = 'user_id'
WAIT_CALLBACK_ARG = 'wait_callback'
BIOAUTH_FLOW_INSTANCE_ARG = 'bioauth_flow'
APP_ID_ATG = 'app_id'


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

    implicit_params_list = [USER_ID_ARG, CALLBACK_ARG, WAIT_CALLBACK_ARG, BIOAUTH_FLOW_INSTANCE_ARG, APP_ID_ATG]
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
            logger.exception(msg="RPC call processing error: %s" % str(e))

    return wraps(rpc_func)(_decorator)


def get_verification_started_callback(callback):
    def verification_started_callback_func():
        callback(result={"msg": 'Verification in progress...'}, status='inprogress')
    return verification_started_callback_func

def _is_biometric_data_valid(callable_func, callable_args, callable_kwargs):
    """
    Provides biometric authentication to support @rpc_call_with_auth
    :param callable_func: RPC routine
    :param callable_args: List of arguments of RPC routine.
    :param callable_kwargs: List of named arguments of RPC routine.
    """
    user_id = callable_kwargs.get(USER_ID_ARG, None)
    app_id = callable_kwargs.get(APP_ID_ATG, None)
    wait_callback = callable_kwargs.get(WAIT_CALLBACK_ARG, None)
    callback = callable_kwargs.get(CALLBACK_ARG, None)
    bioauth_flow = callable_kwargs.get(BIOAUTH_FLOW_INSTANCE_ARG, None)
    
    if app_id is not None and bioauth_flow is not None and bioauth_flow.app_type == 'extension':
        assign_user_to_extension(ApplicationDataStore.instance(), app_id=app_id, email=user_id)
    
    # Send RPC message with inprogress state
    try:
        wait_callback()
    except Exception as e:
        logger.exception(msg="RPC call with auth error - could not send rpc inprogress status: %s" % str(e))
        callback(result={"error": "Internal server error"}, status='fail')

    try:
        if not bioauth_flow.is_current_state(state=bioauthflow.STATE_AUTH_READY):
            if not bioauth_flow.is_current_state(state=bioauthflow.STATE_AUTH_TRAINING_STARTED):
                bioauth_flow.reset()
            else:
                error_msg = 'Training is in progress. Please, wait one minute and try again.'
                logger.exception(msg="RPC call with auth processing canceled: %s" % error_msg)
                callback(result={"error": error_msg}, status='fail')
                return

        future = tornado.gen.Task(bioauth_flow.request_auth, get_verification_started_callback(callback=callback),
                                  user_id)
        greenado.gyield(future)

        # TODO: check for current auth state
        # if bioauth_flow.is_current_state(state=bioauthflow.STATE_AUTH_READY):
        # yield tornado.gen.Task(bioauth_flow.request_auth)
        # else:
        #     error = "RPC ERROR: authentication already in progress"
        #     logger.error(msg=error)
        #     callback(result={"error": error}, status='fail')
        #     return

    except Exception as e:
        logger.exception(msg="Bioauth flow error: %s" % str(e))
        callback(result={"error": 'Server internal error'}, status='fail')
        return

    try:
        if bioauth_flow.is_current_state(bioauthflow.STATE_AUTH_SUCCEED):
            kwargs = _check_rpc_arguments(callable_func=callable_func, current_kwargs=callable_kwargs)
            tornado.ioloop.IOLoop.current().add_future(run_callback(callable_func, callable_args, kwargs),
                                                       callback=create_rpc_final_callback(rpc_result_callback=callback))
        else:
            if bioauth_flow.is_current_state(bioauthflow.STATE_AUTH_FAILED):
                error_msg = 'Biometric authentication failed.'
            elif bioauth_flow.is_current_state(bioauthflow.STATE_AUTH_TIMEOUT):
                error_msg = 'Biometric authentication timeout.'
            elif bioauth_flow.is_current_state(bioauthflow.STATE_AUTH_CANCELED):
                error_msg = 'Biometric authentication canceled.'
            else:
                error_msg = 'Biometric auth internal error'
            callback(result={"error": error_msg}, status='fail')
    except Exception as e:
        # TODO: handle exception
        callback(result={"error": 'Server internal error'}, status='fail')
        logger.exception(msg="RPC call with auth processing error: %s" % str(e))


def create_rpc_final_callback(rpc_result_callback):
    def message_processed(future):
        callback = rpc_result_callback
        if future.exception():
            info = future.exc_info()
            logger.exception(msg='Error during next message processing: %s' % ''.join(traceback.format_exception(*info)))
            error_msg = 'Exception raised from RPC method'
            callback(result={"error": error_msg}, status='fail')
        else:
            result = future.result()
            callback(result=result, status='complete')
            logger.debug(msg='--- RPC call processed successfully')
    return message_processed

@greenado.groutine
def run_callback(callback, callable_args, kwargs):
    return callback(*callable_args, **kwargs)


def rpc_call_with_auth(rpc_func):
    """
    Every RPC routine that require biometric authentication should be decorated with @rpc_call_with_auth decorator.
    """

    def _decorator(*args, **kwargs):
        _is_biometric_data_valid(callable_func=rpc_func, callable_args=args, callable_kwargs=kwargs)

    return wraps(rpc_func)(_decorator)


@greenado.generator
def get_store_data(data_store_instance, object_id, key=None):
    """
    Takes data using DataStore class instance synchronously.
    :param data_store_instance: instance of the required DataStore.
    :param object_id: Id of the object to get.
    :param key: Data key to retrieve. If this field is None - returns all data in dictionary.
                This field is None by default.
    :return: Result of get_data() operation.
    """
    value = None
    try:
        result = yield tornado.gen.Task(data_store_instance.get_data, str(object_id))
        if key is not None and result is not None:
            value = result.get(key)
        else:
            value = result

    except Exception as e:
        logger.exception(e)

    raise tornado.gen.Return(value)


@greenado.generator
def select_store_data(data_store_instance, object_ids):
    result = None
    try:
        result = yield tornado.gen.Task(data_store_instance.select_data_by_ids, object_ids)
    except Exception as e:
        logger.exception(e)
    raise tornado.gen.Return(result)


@greenado.generator
def verify_emails_ai(data_store_instance, emails):
    result = None
    try:
        result = yield  tornado.gen.Task(data_store_instance.update_emails_pgp_keys, emails)
    except Exception as e:
        logger.exception(e)
    raise tornado.gen.Return(result)

def assign_user_to_extension(data_store_instance, app_id, email):
    email = parse_email_data(email)
    data_store_instance.assign_user_to_extension(app_id=app_id, email=email)

def parse_email_data(emails):
    for rep in ['<', '>']:
        emails = emails.replace(rep, '')
    return emails
