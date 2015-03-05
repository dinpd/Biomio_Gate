
from biomio.third_party.fysom import Fysom, FysomError
from biomio.protocol.storage.proberesultsstore import ProbeResultsStore
from biomio.protocol.settings import settings
import tornado.gen

import logging
logger = logging.getLogger(__name__)

STATE_AUTH_READY = 'auth_ready'
STATE_AUTH_WAIT = 'auth_wait'
STATE_AUTH_STARTED = 'auth_started'
STATE_AUTH_FINISHED = 'auth_finished'

# Authentication result statuses
AUTH_NONE = 'none'
AUTH_IN_PROGRESS = 'inprogress'
AUTH_SUCCEED = 'succeed'
AUTH_FAILED = 'failed'
AUTH_TIMEOUT = 'timeout'
AUTH_INTERNAL_ERROR = 'error'

# Event callbacks
def on_reset(e):
    ProbeResultsStore.instance().remove_probe_data(e.bioauth_flow.user_id)
    return STATE_AUTH_READY


def on_request(e):
    return STATE_AUTH_WAIT


def on_start(e):
    return STATE_AUTH_STARTED


def on_probe_available(e):
    return STATE_AUTH_FINISHED


def on_got_results(e):
    return STATE_AUTH_READY


def on_state_changed(e):
    flow = e.bioauth_flow

    next_state = ProbeResultsStore.instance().get_probe_data(user_id=flow.user_id, key=_PROBESTORE_STATE_KEY)
    if next_state is None:
        next_state = STATE_AUTH_FINISHED

    return next_state

# State callbacks


def on_auth_wait(e):
    flow = e.bioauth_flow
    flow.status = AUTH_IN_PROGRESS

    # TODO: remove
    # Create redis key - that will trigger probe try message
    ProbeResultsStore.instance().store_probe_data(user_id=flow.user_id, ttl=settings.bioauth_timeout, waiting_auth=True)

    # Subscribe callback to changes
    ProbeResultsStore.instance().subscribe_to_data(user_id=flow.user_id, data_key='auth', callback=flow.rpc_callback)

    error_msg = None
    user_authenticated = None

    # Check if key does not expire
    if ProbeResultsStore.instance().has_probe_results(user_id=flow.user_id):
        # Not expired, get probe results
        user_authenticated = ProbeResultsStore.instance().get_probe_data(user_id=flow.user_id, key='auth')

    _store_state(e)


def on_auth_finished(e):
    pass

auth_states = {
    'initial': STATE_AUTH_READY,
    'events': [
        {
            'name': 'reset',
            'src': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_STARTED, STATE_AUTH_FINISHED],
            'dst': [STATE_AUTH_READY],
            'decision': on_reset
        },
        {
            'name': 'request',
            'src': STATE_AUTH_READY,
            'dst': STATE_AUTH_WAIT,
            'decision': on_request
        },
        {
            'name': 'start',
            'src': STATE_AUTH_WAIT,
            'dst': STATE_AUTH_STARTED,
            'decision': on_start
        },
        {
            'name': 'probe_available',
            'src': STATE_AUTH_STARTED,
            'dst': [STATE_AUTH_FINISHED],
            'decision': on_probe_available
        },
        {
            'name': 'got_results',
            'src': STATE_AUTH_STARTED,
            'dst': [STATE_AUTH_FINISHED],
            'decision': on_got_results
        },
        {
            'name': 'state_changed',
            'src': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_STARTED, STATE_AUTH_FINISHED],
            'dst': [STATE_AUTH_READY, STATE_AUTH_WAIT, STATE_AUTH_STARTED, STATE_AUTH_FINISHED],
            'decision': on_state_changed
        }
    ],
    'callbacks': {
        'onauth_wait': on_auth_wait,
        'onauth_finished': on_auth_finished,
    }
}

_PROBESTORE_STATE_KEY = 'state'

# Helper Methods


def _store_state(e):
    # TODO: check if we need to set ttl again
    data = {_PROBESTORE_STATE_KEY: e.fsm.current}
    ProbeResultsStore.instance().store_probe_data(user_id=e.flow.user_id, ttl=None, **data)


class BioauthFlow:
    def __init__(self, user_id, app_id, auth_wait_callback=None):
        self.user_id = user_id
        self.app_id = app_id
        self.rpc_callback = None
        self.auth_wait_callback = None
        self.status = None

        self._state_machine_instance = Fysom(auth_states)
        self._restore_state()

        ProbeResultsStore.instance().subscribe(user_id=user_id, callback=self._change_state_callback())
        self._state_machine_instance.onchangestate = self._state_machine_logger_callback()

    # def _print_change_state(self):
    #     logger.debug('BIOMETRIC AUTH [%s, %s]: %s -> %s' % (self.user_id, self.app_id, self.))

    def _state_machine_logger_callback(self):
        def _state_machine_logger(e):
            flow = self
            logger.debug('BIOMETRIC AUTH [%s, %s]: %s -> %s' % (flow.user_id, flow.app_id, e.src, e.dst))

        return _state_machine_logger

    def _change_state_callback(self):

        def _state_changed(*args, **kwargs):
            flow = self
            if not flow is None:
                flow._state_machine_instance.state_changed(bioauth_flow=self)
            else:
                # TODO: remove debug output
                logger.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        return _state_changed

    def _restore_state(self):
        """
        Restores BioauthFlow object state by probe results key by given user id.
        """
        if ProbeResultsStore.instance().has_probe_results(user_id=self.user_id):
            state = ProbeResultsStore.instance().get_probe_data(user_id=self.user_id, key=_PROBESTORE_STATE_KEY)
            # TODO: re-subscribe on restore probably needed
            if state:
                logger.debug("Restoring state for bioauth flow: %s, %s" % (self.user_id, self.app_id))
                self._state_machine_instance.current = state
                logger.debug("Current state: %s" % state)

    def reset(self):
        self._state_machine_instance.reset(bioauth_flow=self)

    @tornado.gen.engine
    def request_auth(self, callback):
        """
        Should be called for extension to request biometric authentication from probe.
        """
        self.rpc_callback = callback # Store callback to call later in STATE_AUTH_FINISHED state
        self._state_machine_instance.request(bioauth_flow=self)

    def auth_started(self):
        self._state_machine_instance.start(bioauth_flow=self)

    def set_auth_results(self, result):
        self._state_machine_instance.got_results(bioauth_flow=self, result=result)

    def is_current_state(self, state):
        return self._state_machine_instance.current == state
