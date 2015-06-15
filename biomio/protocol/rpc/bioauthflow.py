from biomio.constants import get_ai_training_response
from biomio.protocol.data_stores.storage_jobs import register_biometrics_job
from biomio.protocol.data_stores.storage_jobs_processor import run_storage_job
from biomio.third_party.fysom import Fysom, FysomError
from biomio.protocol.storage.auth_state_storage import AuthStateStorage
from biomio.protocol.probes.probeauthbackend import ProbeAuthBackend
from biomio.protocol.rpc.app_auth_connection import AppAuthConnection
from biomio.protocol.settings import settings

import tornado.gen

import logging
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

# Training states
STATE_AUTH_TRAINING_STARTED = 'auth_training'
STATE_AUTH_TRAINING_INPROGRESS = 'auth_training_inprogress'
STATE_AUTH_TRAINING_DONE = 'auth_training_done'
STATE_AUTH_TRAINING_FAILED = 'auth_training_failed'

# Event callbacks
def on_reset(e):
    return STATE_AUTH_READY


def on_request(e):
    flow = e.bioauth_flow

    if flow.is_extension_owner():
        flow.auth_connection.start_auth(on_behalf_of=e.on_behalf_of)

    return STATE_AUTH_WAIT


def on_probe_available(e):
    flow = e.bioauth_flow

    if not e.fsm.current == STATE_AUTH_ERROR:
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
    next_state = flow.auth_connection.get_data(key=_PROBESTORE_STATE_KEY)

    if next_state is None:
        if e.fsm.current == STATE_AUTH_WAIT or e.fsm.current == STATE_AUTH_VERIFICATION_STARTED:
            if flow.auth_connection.get_data():
                next_state = STATE_AUTH_ERROR
                logger.debug('BIOMETRIC AUTH [%s, %s]: AUTH INTERNAL ERROR - state not set' % (flow.app_type, flow.app_id))
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

    if flow.is_probe_owner():
        flow.try_probe_callback(message="Authentication")

def on_auth_training(e):
    flow = e.bioauth_flow
    if flow.is_probe_owner():
        flow.try_probe_callback(message="Training")


def on_auth_finished(e):
    flow = e.bioauth_flow

    if flow.is_extension_owner():
        flow.rpc_callback()

    if flow.is_probe_owner():
        if e.fsm.current == STATE_AUTH_CANCELED:
            flow.cancel_auth_callback()

def on_auth_verification_started(e):
    flow = e.bioauth_flow

    if flow.is_extension_owner():
        flow._verification_started_callback()

auth_states = {
    'initial': STATE_AUTH_READY,
    'events': [
        {
            'name': 'reset',
            'src': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_CANCELED,
                    STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR,
                    STATE_AUTH_TRAINING_STARTED, STATE_AUTH_TRAINING_DONE, STATE_AUTH_TRAINING_FAILED],
            'dst': [STATE_AUTH_READY],
            'decision': on_reset
        },
        {
            'name': 'request',
            'src': [STATE_AUTH_READY, STATE_AUTH_SUCCEED, STATE_AUTH_FAILED,
                    STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_CANCELED],
            'dst': [STATE_AUTH_WAIT],
            'decision': on_request
        },
        {
            'name': 'retry',
            'src': [STATE_AUTH_VERIFICATION_STARTED],
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
            'dst': [STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_CANCELED],
            'decision': on_probe_available
        },
        {
            'name': 'results_accepted',
            'src': [STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR, STATE_AUTH_CANCELED],
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
            'src': [STATE_AUTH_WAIT, STATE_AUTH_VERIFICATION_STARTED],
            'dst': [STATE_AUTH_CANCELED],
            'decision': on_cancel_auth
        },
        {
            'name': 'state_changed',
            'src': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_VERIFICATION_STARTED, STATE_AUTH_CANCELED,
                    STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR,
                    STATE_AUTH_TRAINING_STARTED, STATE_AUTH_TRAINING_INPROGRESS,
                    STATE_AUTH_TRAINING_DONE, STATE_AUTH_TRAINING_FAILED],
            'dst': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_VERIFICATION_STARTED, STATE_AUTH_CANCELED,
                    STATE_AUTH_SUCCEED, STATE_AUTH_FAILED, STATE_AUTH_TIMEOUT, STATE_AUTH_ERROR,
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
    def __init__(self, app_type, app_id, try_probe_callback, cancel_auth_callback, auto_initialize=True):
        self.app_type = app_type
        self.app_id = app_id
        self.rpc_callback = None
        self.try_probe_callback = try_probe_callback
        self.cancel_auth_callback = cancel_auth_callback
        self.status = None

        self._state_machine_instance = Fysom(auth_states)
        self._state_machine_instance.onchangestate = self._get_state_machine_logger_callback()
        self._change_state_callback = self._get_change_state_callback()
        self._verification_started_callback = None

        self._resources_list = []

        self.auth_connection = AppAuthConnection(app_id=app_id, app_type=app_type)

        if auto_initialize:
            self.initialize()

    def initialize(self):
        logger.debug('BIOMETRIC AUTH OBJECT [%s, %s]: INITIALIZING...' % (self.app_type, self.app_id))
        self.auth_connection.set_app_connected(app_auth_data_callback=self._change_state_callback)
        self._restore_state()

    def shutdown(self):
        logger.debug('BIOMETRIC AUTH OBJECT [%s, %s]: SHUTTING DOWN...' % (self.app_type, self.app_id))
        if self.is_probe_owner() and (self.is_current_state(STATE_AUTH_VERIFICATION_STARTED)):
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

        if next_state in [STATE_AUTH_TRAINING_DONE, STATE_AUTH_CANCELED, STATE_AUTH_SUCCEED,
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
    def request_auth(self, verification_started_callback, on_behalf_of, callback):
        """
        Should be called for extension to request biometric authentication from probe.
        """
        self._verification_started_callback = verification_started_callback # Store callback to call later before verification started
        self.rpc_callback = callback # Store callback to call later in STATE_AUTH_FINISHED state
        data_dict = {
            _PROBESTORE_ON_BEHALF_OF_KEY: on_behalf_of
        }
        self.auth_connection.store_data(**data_dict)
        self._state_machine_instance.request(bioauth_flow=self, on_behalf_of=on_behalf_of)
        self._store_state()

    def auth_started(self, resource_list=None):
        self._resources_list = resource_list
        self._store_state()

    @tornado.gen.engine
    def set_next_auth_result(self, samples_by_probe_type):
        if not self._resources_list:
            logger.warning(msg='resource item list for probe is empty')
        self._state_machine_instance.verification_started(bioauth_flow=self)
        self._store_state()

        auth_result = False

        for probe_type, samples_list in samples_by_probe_type.iteritems():
            result = yield tornado.gen.Task(ProbeAuthBackend.instance().probe, probe_type, samples_list, self.app_id, False)
            error = result.get('error')
            verified = result.get('verified')
            if error:
                logger.debug(msg='Some samples could not be processed. Sending "try" message again.')
                self._state_machine_instance.retry(bioauth_flow=auth_result)
                self._store_state()
                break
            else:
                logger.debug(msg='SET NEXT AUTH RESULT: %s' % verified)
                auth_result = verified or auth_result

        self.set_auth_results(result=auth_result)
        self._store_state()

    @tornado.gen.engine
    def set_auth_training_results(self, appId, type, data):
        if self._state_machine_instance.current == STATE_AUTH_TRAINING_STARTED:
            self._state_machine_instance.training_in_progress(bioauth_flow=self)
            self._store_state()
            training_type = self.auth_connection.get_data(key=_PROBESTORE_TRAINING_TYPE_KEY)
            ai_code = self.auth_connection.get_data(key=_PROBESTORE_AI_CODE_KEY)
            if ai_code is not None:
                run_storage_job(register_biometrics_job, code=ai_code, status='in-progress', response_type={})
            result = yield tornado.gen.Task(ProbeAuthBackend.instance().probe, type, data, self.app_id, True)

            key_to_delete = None
            if training_type is not None and ai_code is not None:
                key_to_delete = 'auth:%s:%s' % ('code_%s' % ai_code, self.app_id)
                ai_response = get_ai_training_response(training_type)
                run_storage_job(register_biometrics_job, code=ai_code, status='verified', response_type=ai_response)

            logger.debug(msg='TRAINING RESULT: %s' % str(result))
            self._state_machine_instance.training_results_available()
            self._store_state()
            if key_to_delete is not None:
                AuthStateStorage.instance().remove_probe_data(key=key_to_delete)


    def set_auth_results(self, result):
        #TODO: make method private
        self._state_machine_instance.results_available(bioauth_flow=self, result=result)
        self._store_state()

    def is_current_state(self, state):
        return self._state_machine_instance.current == state

    def is_probe_owner(self):
        return self.auth_connection.is_probe_owner()

    def is_extension_owner(self):
        return self.auth_connection.is_extension_owner()

    @classmethod
    def start_training(cls, probe_id, code):
        data = {
            _PROBESTORE_STATE_KEY: STATE_AUTH_TRAINING_STARTED,
            _PROBESTORE_TRAINING_TYPE_KEY: 'face-photo',
            _PROBESTORE_AI_CODE_KEY: code
        }
        app_id = 'auth:%s:%s' % ('code_%s' % code, probe_id)
        AuthStateStorage.instance().store_probe_data(app_id, ttl=settings.bioauth_timeout, **data)
        logger.debug('Training process started...')

    def cancel_auth(self):
        if self._state_machine_instance.current in [STATE_AUTH_WAIT]:
            self._state_machine_instance.cancel_auth(bioauth_flow=self)
            self._store_state()

