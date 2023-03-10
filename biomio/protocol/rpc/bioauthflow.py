import ast
import base64
import json
import requests
from requests.exceptions import HTTPError
from biomio.constants import TRAINING_CANCELED_STATUS, TRAINING_CANCELED_MESSAGE, REST_REGISTER_BIOMETRICS
from biomio.protocol.data_stores.device_information_store import DeviceInformationStore
from biomio.protocol.probes.probe_plugin_manager import ProbePluginManager
from biomio.protocol.rpc.app_connection_listener import AppConnectionListener
from biomio.protocol.storage.redis_storage import RedisStorage
from biomio.third_party.fysom import Fysom, FysomError
from biomio.protocol.storage.auth_state_storage import AuthStateStorage
from biomio.protocol.rpc.app_auth_connection import AppAuthConnection
from biomio.protocol.settings import settings

import tornado.gen

import logging
from biomio.utils.utils import push_notification_callback

logger = logging.getLogger(__name__)

STATE_AUTH_READY = 'auth_ready'

# Auth States
STATE_AUTH_WAIT = 'auth_wait'
STATE_AUTH_VERIFICATION_STARTED = 'auth_verification_started'
STATE_AUTH_SUCCEED = 'auth_succeed'
STATE_AUTH_FAILED = 'auth_failed'
STATE_AUTH_TIMEOUT = 'auth_timeout'
STATE_AUTH_ERROR = 'auth_error'
STATE_AUTH_CANCELED = 'auth_canceled'
STATE_AUTH_MAX_RETRIES = 'max_auth_retries_reached'

# Training states
STATE_AUTH_TRAINING_STARTED = 'auth_training'
STATE_AUTH_TRAINING_INPROGRESS = 'auth_training_inprogress'
STATE_AUTH_TRAINING_DONE = 'auth_training_done'
STATE_AUTH_TRAINING_FAILED = 'auth_training_failed'
STATE_AUTH_RESULTS_AVAILABLE = 'results_available'


# Event callbacks
def on_reset(e):
    return STATE_AUTH_READY


def on_request(e):
    flow = e.bioauth_flow
    current_resources = e.current_resources

    if flow.is_extension_owner():
        flow.auth_connection.start_auth(current_resources=current_resources)

    return STATE_AUTH_WAIT


def on_probe_available(e):
    flow = e.bioauth_flow

    if not e.fsm.current == STATE_AUTH_ERROR:
        if e.max_retries:
            return STATE_AUTH_MAX_RETRIES
        if e.result is not None:
            if e.result:
                return STATE_AUTH_SUCCEED
            else:
                return STATE_AUTH_FAILED
        else:
            return STATE_AUTH_TIMEOUT

    return STATE_AUTH_ERROR


def on_got_results(e):
    return STATE_AUTH_READY


def on_training_results_available(e):
    logger.debug('training results available!')
    return STATE_AUTH_TRAINING_DONE


def on_cancel_auth(e):
    flow = e.bioauth_flow
    logger.warning('BIOMETRIC AUTH [%s, %s]: AUTH CANCELED' % (flow.app_type, flow.app_id))

    return STATE_AUTH_CANCELED


def on_state_changed(e):
    flow = e.bioauth_flow
    connection_data = flow.auth_connection.get_data()
    next_state = None
    provider_id = None
    if connection_data is not None:
        next_state = connection_data.get(_PROBESTORE_STATE_KEY)
        provider_id = connection_data.get('provider_id')

    if provider_id is not None:
        flow._provider_id = provider_id

    if next_state is None:
        if e.fsm.current == STATE_AUTH_WAIT or e.fsm.current == STATE_AUTH_VERIFICATION_STARTED:
            if flow.auth_connection.get_data():
                next_state = STATE_AUTH_ERROR
                logger.debug(
                    'BIOMETRIC AUTH [%s, %s]: AUTH INTERNAL ERROR - state not set' % (flow.app_type, flow.app_id))
            else:
                next_state = STATE_AUTH_TIMEOUT
                logger.debug('BIOMETRIC AUTH [%s, %s]: AUTH TIMEOUT' % (flow.app_type, flow.app_id))
        else:
            next_state = STATE_AUTH_READY

    logger.debug('BIOMETRIC AUTH [%s, %s]: STATE CHANGED - %s' % (flow.app_type, flow.app_id, next_state))
    return next_state


# State callbacks
def on_auth_wait(e):
    flow = e.bioauth_flow

    if flow.is_probe_owner() or flow.is_hybrid_app():
        flow.try_probe_callback(message="Authentication", current_resources=flow.auth_connection._current_resources)


def on_auth_training(e):
    flow = e.bioauth_flow
    if flow.is_probe_owner():
        flow.try_probe_callback(message="Training")


def on_auth_finished(e):
    flow = e.bioauth_flow

    if flow.is_extension_owner() or flow.is_hybrid_app():
        flow.rpc_callback()

    if flow.is_probe_owner():
        if e.fsm.current == STATE_AUTH_CANCELED:
            flow.cancel_auth_callback(bioauth_flow=flow)


def on_auth_verification_started(e):
    flow = e.bioauth_flow

    if flow.is_extension_owner():
        flow._verification_started_callback()
    else:
        RedisStorage.persistence_instance().store_data(key='simulator_auth_status:%s' % flow.app_id,
                                                       result='Auth check in progress....', status='in_progress')


auth_states = {
    'initial': STATE_AUTH_READY,
    'events': [
        {
            'name': 'reset',
            'src': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_CANCELED,
                    STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_MAX_RETRIES,
                    STATE_AUTH_TRAINING_STARTED, STATE_AUTH_TRAINING_DONE, STATE_AUTH_TRAINING_FAILED],
            'dst': [STATE_AUTH_READY],
            'decision': on_reset
        },
        {
            'name': 'request',
            'src': [STATE_AUTH_READY, STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_MAX_RETRIES,
                    STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_CANCELED],
            'dst': [STATE_AUTH_WAIT],
            'decision': on_request
        },
        {
            'name': 'retry',
            'src': [STATE_AUTH_VERIFICATION_STARTED, STATE_AUTH_RESULTS_AVAILABLE],
            'dst': STATE_AUTH_WAIT
        },
        {
            'name': 'verification_started',
            'src': [STATE_AUTH_WAIT],
            'dst': STATE_AUTH_VERIFICATION_STARTED
        },
        {
            'name': 'results_available',
            'src': [STATE_AUTH_VERIFICATION_STARTED],
            'dst': [STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_CANCELED,
                    STATE_AUTH_MAX_RETRIES],
            'decision': on_probe_available
        },
        {
            'name': 'results_accepted',
            'src': [STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_CANCELED,
                    STATE_AUTH_MAX_RETRIES],
            'dst': [STATE_AUTH_READY],
            'decision': on_got_results
        },
        {
            'name': 'training_in_progress',
            'src': [STATE_AUTH_TRAINING_STARTED],
            'dst': STATE_AUTH_TRAINING_INPROGRESS,
        },
        {
            'name': 'training_results_available',
            'src': [STATE_AUTH_TRAINING_INPROGRESS],
            'dst': [STATE_AUTH_TRAINING_DONE, STATE_AUTH_TRAINING_FAILED],
            'decision': on_training_results_available
        },
        {
            'name': 'cancel_auth',
            'src': [STATE_AUTH_WAIT, STATE_AUTH_VERIFICATION_STARTED, STATE_AUTH_TRAINING_STARTED],
            'dst': [STATE_AUTH_CANCELED],
            'decision': on_cancel_auth
        },
        {
            'name': 'state_changed',
            'src': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_VERIFICATION_STARTED, STATE_AUTH_CANCELED,
                    STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_MAX_RETRIES,
                    STATE_AUTH_TRAINING_STARTED, STATE_AUTH_TRAINING_INPROGRESS,
                    STATE_AUTH_TRAINING_DONE, STATE_AUTH_TRAINING_FAILED],
            'dst': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_VERIFICATION_STARTED, STATE_AUTH_CANCELED,
                    STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_MAX_RETRIES,
                    STATE_AUTH_TRAINING_STARTED, STATE_AUTH_TRAINING_INPROGRESS,
                    STATE_AUTH_TRAINING_DONE, STATE_AUTH_TRAINING_FAILED],
            'decision': on_state_changed
        }
    ],
    'callbacks': {
        'onauth_wait': on_auth_wait,
        'onauth_succeed': on_auth_finished,
        'onauth_failed': on_auth_finished,
        'onauth_timeout': on_auth_finished,
        'onauth_error': on_auth_finished,
        'onauth_canceled': on_auth_finished,
        'onauth_max_retries': on_auth_finished,
        'onauth_training': on_auth_training,
        'onauth_verification_started': on_auth_verification_started
    }
}

# TODO: Move to constants
_PROBESTORE_STATE_KEY = 'state'
_PROBESTORE_TRAINING_TYPE_KEY = 'training_type'
_PROBESTORE_AI_CODE_KEY = 'ai_code'
_PROBESTORE_ON_BEHALF_OF_KEY = 'on_behalf_of'


# Helper Methods
def _store_state(e):
    data = {_PROBESTORE_STATE_KEY: e.fsm.current}
    flow = e.bioauth_flow
    flow.auth_connection.store_data(**data)


class BioauthFlow:
    def __init__(self, app_type, app_id, try_probe_callback, cancel_auth_callback, auto_initialize=True, app_user=None):
        self.app_type = app_type
        self.app_id = app_id
        self._app_user = app_user
        self.rpc_callback = None
        self.try_probe_callback = try_probe_callback
        self.cancel_auth_callback = cancel_auth_callback
        self.status = None

        self._state_machine_instance = Fysom(auth_states)
        self._state_machine_instance.onchangestate = self._get_state_machine_logger_callback()
        self._change_state_callback = self._get_change_state_callback()
        self._verification_started_callback = None

        self._resources_list = []
        self._on_behalf_of = None
        self.auth_connection = AppAuthConnection(app_id=app_id, app_type=app_type)
        self._provider_id = None

        if auto_initialize:
            self.initialize()

    def initialize(self):
        logger.debug('BIOMETRIC AUTH OBJECT [%s, %s]: INITIALIZING...' % (self.app_type, self.app_id))
        self.auth_connection.set_app_connected(app_auth_data_callback=self._change_state_callback)
        self._restore_state()

    def shutdown(self):
        logger.debug('BIOMETRIC AUTH OBJECT [%s, %s]: SHUTTING DOWN...' % (self.app_type, self.app_id))
        if self.is_probe_owner() and (self.is_current_state(STATE_AUTH_VERIFICATION_STARTED)):
            RedisStorage.persistence_instance().store_data(key='simulator_auth_status:%s' % self.app_id,
                                                           result='Your device was disconnected...', status='finished')
            logger.debug("BIOMETRIC AUTH OBJECT [%s, %s]: APP DISCONNECTED - CONTINUE PROBE VERIFICATION...")
        else:
            self.cancel_auth()
            self._store_state()
        self.auth_connection.set_app_disconnected()

    def _get_state_machine_logger_callback(self):
        def _state_machine_logger(e):
            flow = self
            logger.debug('BIOMETRIC AUTH [%s, %s]: %s -> %s' % (flow.app_type, flow.app_id, e.src, e.dst))

        return _state_machine_logger

    def _get_change_state_callback(self):

        def _state_changed(*args, **kwargs):
            flow = self
            if flow is not None:
                flow._state_machine_instance.state_changed(bioauth_flow=self)

        return _state_changed

    def _restore_state(self):
        """
        Restores BioauthFlow object state by probe results key by given user id.
        """
        next_state = self.auth_connection.get_data(key=_PROBESTORE_STATE_KEY)

        if next_state in [STATE_AUTH_TRAINING_DONE, STATE_AUTH_CANCELED, STATE_AUTH_SUCCEED, STATE_AUTH_MAX_RETRIES,
                          STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_VERIFICATION_STARTED]:
            # Result of previous auth is still stored in auth key
            self.reset()
        else:
            logger.debug("Restoring state for bioauth flow: %s, %s" % (self.app_type, self.app_id))
            try:
                self._change_state_callback()
                logger.debug("State to restore: %s" % self._state_machine_instance.current)
            except Exception as e:
                logger.exception("Failed to restore state")

    def _store_state(self):
        data = {_PROBESTORE_STATE_KEY: self._state_machine_instance.current}
        self.auth_connection.store_data(**data)

    def reset(self):
        self._state_machine_instance.reset(bioauth_flow=self)
        self._store_state()

    @tornado.gen.engine
    def request_auth(self, verification_started_callback, current_resources=None, callback=None):
        """
        Should be called for extension to request biometric authentication from probe.
        """
        self._verification_started_callback = verification_started_callback  # Store callback to call later before verification started
        self.rpc_callback = callback  # Store callback to call later in STATE_AUTH_FINISHED state
        data_dict = {}
        self.auth_connection.store_data(**data_dict)
        self._state_machine_instance.request(bioauth_flow=self, current_resources=current_resources)
        self._store_state()

    def auth_started(self, resource_list=None):
        self._resources_list = resource_list
        self._store_state()

    def set_probe_results(self, samples_by_probe_type):
        if self.is_current_state(state=STATE_AUTH_TRAINING_STARTED):
            self.set_auth_training_results(samples_by_probe_type=samples_by_probe_type)
        else:
            self.set_next_auth_result(samples_by_probe_type=samples_by_probe_type)

    @tornado.gen.engine
    def set_next_auth_result(self, samples_by_probe_type):
        if not self._resources_list:
            logger.warning(msg='resource item list for probe is empty')
        self._state_machine_instance.verification_started(bioauth_flow=self)
        self._store_state()

        auth_result = True
        max_retries = False
        error = None
        rec_type_data = RedisStorage.persistence_instance().get_data(key='app_rec_type:%s' % self.app_id)
        rec_type_data = {} if rec_type_data is None else ast.literal_eval(rec_type_data)
        for probe_type, samples_list in samples_by_probe_type.iteritems():
            # if self._app_user is not None:
            #     new_probe_type = '%s_%s' % (probe_type, self._app_user)
            #     if new_probe_type in ProbePluginManager.instance().get_available_auth_types():
            #         probe_type = new_probe_type
            data = dict(samples=samples_list, probe_id=self.app_id)
            if rec_type_data.get('rec_type') is not None and probe_type == 'face':
                rec_type = rec_type_data.get('rec_type')
                if rec_type != 'verification':
                    probe_type = 'face_identification'
                    if self._provider_id is not None:
                        data.update({'provider_id': self._provider_id})
            result = yield tornado.gen.Task(
                ProbePluginManager.instance().get_plugin_by_auth_type(probe_type).run_verification, data)
            if isinstance(result, bool):
                verified = result
                error = None
                max_retries = False
            else:
                if isinstance(result, str):
                    auth_result = result
                else:
                    error = result.get('error')
                    verified = result.get('verified', False)
                    max_retries = result.get('max_retries', False)
            if error:
                logger.debug(msg='Some samples could not be processed. Sending "try" message again.')
                self._state_machine_instance.retry(bioauth_flow=self)
                self._store_state()
                break
            else:
                if isinstance(auth_result, str):
                    break
                logger.debug(msg='SET NEXT AUTH RESULT: %s' % verified)
                auth_result = verified and auth_result

        self.set_auth_results(result=auth_result, max_retries=max_retries)
        self._store_state()

    @tornado.gen.engine
    def set_auth_training_results(self, samples_by_probe_type):
        if self._state_machine_instance.current == STATE_AUTH_TRAINING_STARTED:
            self._state_machine_instance.training_in_progress(bioauth_flow=self)
            self._store_state()
            ai_code = self.auth_connection.get_data(key=_PROBESTORE_AI_CODE_KEY)
            training_result = False
            error = None
            rec_type_data = RedisStorage.persistence_instance().get_data(key='app_rec_type:%s' % self.app_id)
            rec_type_data = {} if rec_type_data is None else ast.literal_eval(rec_type_data)
            for probe_type, samples in samples_by_probe_type.iteritems():
                if self._app_user is not None:
                    new_probe_type = '%s_%s' % (probe_type, self._app_user)
                    if new_probe_type in ProbePluginManager.instance().get_available_auth_types():
                        probe_type = new_probe_type
                data = dict(try_type=probe_type, ai_code=ai_code, samples=samples, probe_id=self.app_id)
                if rec_type_data.get('rec_type') is not None and probe_type == 'face':
                    rec_type = rec_type_data.get('rec_type')
                    if rec_type != 'verification':
                        if self._app_user is not None:
                            data.update({'user_id': self._app_user})
                        probe_type = 'face_identification'
                result = yield tornado.gen.Task(
                    ProbePluginManager.instance().get_plugin_by_auth_type(probe_type).run_training, data)
                if not isinstance(result, bool):
                    error = result.get('error')
                    result = result.get('result')
                if not result and error is not None:
                    self.start_training(self.app_id, ai_code)
                    break
                else:
                    training_result = result or training_result

            logger.debug(msg='TRAINING RESULT: %s' % str(training_result))
            if error is None:
                self._state_machine_instance.training_results_available()
                self._store_state()
                self.auth_connection.end_auth()

    def set_auth_results(self, result, max_retries=False):
        # TODO: make method private
        if self.auth_connection.is_probe_owner():
            RedisStorage.persistence_instance().store_data(key='simulator_auth_status:%s' % self.app_id, result=result,
                                                           status='finished')
        self._state_machine_instance.results_available(bioauth_flow=self, result=result, max_retries=max_retries)
        self._store_state()

    def is_current_state(self, state):
        return self._state_machine_instance.current == state

    def is_probe_owner(self):
        return self.auth_connection.is_probe_owner()

    def is_extension_owner(self):
        return not self.auth_connection.is_probe_owner()

    def is_hybrid_app(self):
        return self.auth_connection.is_hybrid_app()

    @classmethod
    def start_training(cls, probe_id, code):
        data = {
            _PROBESTORE_STATE_KEY: STATE_AUTH_TRAINING_STARTED,
            _PROBESTORE_TRAINING_TYPE_KEY: 'face-photo',
            _PROBESTORE_AI_CODE_KEY: code
        }
        app_id = 'biomio_general:auth:%s:%s' % ('code_%s' % code, probe_id)
        DeviceInformationStore.instance().get_data(app_id=probe_id, callback=push_notification_callback(
            'Please open the app to proceed with training'))
        AuthStateStorage.instance().store_probe_data(app_id, ttl=settings.bioauth_timeout, **data)
        logger.debug('Training process started...')

    def cancel_auth(self):
        if self._state_machine_instance.current in [STATE_AUTH_WAIT, STATE_AUTH_TRAINING_STARTED]:
            if self._state_machine_instance.current == STATE_AUTH_TRAINING_STARTED:
                client_id = self.auth_connection.get_client_id()
                if client_id is not None and 'code_' in client_id:
                    self.tell_ai_canceled_training(client_id.split('_')[1])
                self.auth_connection.end_auth()
            self._state_machine_instance.cancel_auth(bioauth_flow=self)
            self._store_state()

    @staticmethod
    def tell_ai_canceled_training(ai_code):
        try:
            ai_response_status = {
                'status': TRAINING_CANCELED_STATUS,
                'message': TRAINING_CANCELED_MESSAGE
            }
            logger.info('Telling AI that training was canceled with code - %s' % ai_code)
            response_type = base64.b64encode(json.dumps(ai_response_status))
            register_biometrics_url = settings.ai_rest_url % (REST_REGISTER_BIOMETRICS % (ai_code, response_type))
            response = requests.post(register_biometrics_url)
            try:
                response.raise_for_status()
                logger.info('AI should now know that training is finished with code - %s and response type - %s' %
                            (ai_code, response_type))
            except HTTPError as e:
                logger.exception(e)
                logger.exception('Failed to tell AI that training is finished, reason - %s' % response.reason)
        except Exception as e:
            logger.error('Failed to build rest request to AI - %s' % str(e))
            logger.exception(e)
