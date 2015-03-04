
from biomio.third_party.fysom import Fysom, FysomError
from biomio.protocol.storage.proberesultsstore import ProbeResultsStore

import logging
logger = logging.getLogger(__name__)

STATE_AUTH_READY = 'auth_ready'
STATE_AUTH_WAIT = 'auth_wait'
STATE_AUTH_STARTED = 'auth_started'
STATE_AUTH_SUCCESS = 'auth_success'
STATE_AUTH_FAIL = 'auth_fail'

def on_reset(e):
    pass

def on_request(e):
    pass

def on_start(e):
    pass

def on_got_results(e):
    pass

auth_states = {
    'initial': STATE_AUTH_READY,
    'events': [
        {
            'name': 'reset',
            'src': [STATE_AUTH_FAIL, STATE_AUTH_SUCCESS],
            'dst': [STATE_AUTH_READY, STATE_AUTH_SUCCESS, STATE_AUTH_FAIL],
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
            'name': 'got_results',
            'src': STATE_AUTH_STARTED,
            'dst': [STATE_AUTH_FAIL, STATE_AUTH_SUCCESS],
            'decision': on_got_results
        }
    ]#,
    # 'callbacks': {
    #     'onchangestate': print_state_change
    # }
}

_PROBESTORE_KEY_STATE = 'state'

class BioauthFlow:
    def __init__(self, user_id, app_id):
        self.user_id = user_id
        self.app_id = app_id

        self._state_machine_instance = Fysom(auth_states)
        self._restore_state()
        # self._state_machine_instance.onchangestate = self._print_change_state

    # def _print_change_state(self):
    #     logger.debug('BIOMETRIC AUTH [%s, %s]: %s -> %s' % (self.user_id, self.app_id, self.))

    def _restore_state(self):
        """
        Restores BioauthFlow object state by probe results key by given user id.
        """
        if ProbeResultsStore.instance().has_probe_results(user_id=self.user_id):
            state = ProbeResultsStore.instance().get_probe_data(user_id=self.user_id, key=_PROBESTORE_KEY_STATE)
            if state:
                logger.debug("Restoring state for bioauth flow: %s, %s" % (self.user_id, self.app_id))
                self._state_machine_instance.current = state
                logger.debug("Current state: %s" % state)

    def reset(self):
        self._state_machine_instance.reset(bioauth_flow=self)

    def request_auth(self):
        self._state_machine_instance.requet(bioauth_flow=self)

    def auth_started(self):
        self._state_machine_instance.start(bioauth_flow=self)

    def set_auth_results(self, result):
        self._state_machine_instance.got_results(bioauth_flow=self, result=result)

    def is_current_state(self, state):
        pass