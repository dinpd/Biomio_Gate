import json
import logging
import os
from threading import Lock
from business_rules.engine import run_all
from biomio.protocol.data_stores.condition_data_store import ConditionDataStore
from biomio.protocol.probes.policy_engine.policy_variables import PolicyVariables
from biomio.protocol.probes.policy_engine.policy_actions import PolicyActions
from biomio.protocol.probes.probe_plugin_manager import ProbePluginManager

logger = logging.getLogger(__name__)

MOCKUPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mockups')
FP_SCANNER_AND_FACE_PHOTO_RULE_MOCKUP = os.path.join(MOCKUPS_DIR, 'fp-scanner_&_face-photo.json')
FP_SCANNER_OR_FACE_PHOTO_RULE_MOCKUP = os.path.join(MOCKUPS_DIR, 'fp-scanner_or_face-photo.json')


class PolicyEngineManager:
    _instance = None
    _lock = Lock()

    CONDITION_ANY = 'any'
    CONDITION_ALL = 'all'

    _default_policy = {
        ConditionDataStore.CONDITION_ATTR: CONDITION_ANY
    }

    # TODO: Maybe we should get this values with plugin_manager (via plugin configs?)
    _training_auth_types = ['face']

    def __init__(self):
        self._plugin_manager = ProbePluginManager.instance()
        self._read_rules()

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = PolicyEngineManager()
        return cls._instance

    def _read_rules(self):
        with open(FP_SCANNER_AND_FACE_PHOTO_RULE_MOCKUP, 'r') as f:
            self._fp_scanner_and_face_photo_rule = json.loads(f.read())
        with open(FP_SCANNER_OR_FACE_PHOTO_RULE_MOCKUP, 'r') as f:
            self._fp_scanner_or_face_photo_rule = json.loads(f.read())

    def run_rules(self, policy_variables=None):
        if policy_variables is None:
            policy_variables = dict(
                available_device_resources=["fp-scanner", "photo-cam", "1024x768", "2048x1536"],
                max_attempts=3,
                max_authentication_time=60,  # sec
                max_re_auth_time=30,  # min
                max_cer=1
            )
        run_all(self._fp_scanner_or_face_photo_rule, defined_variables=PolicyVariables(policy_data=policy_variables),
                defined_actions=PolicyActions(callback=None), stop_on_first_trigger=True)

    def generate_try_resources(self, device_resources, user_id, training=False):
        try_resource_items = []
        policy = self._default_policy
        if training:
            auth_types = self._training_auth_types
        else:
            condition_data = ConditionDataStore.instance().get_data(user_id=user_id)
            if condition_data is None:
                logger.warning('No conditions set for user - %s' % user_id)
                auth_types = self._plugin_manager.get_available_auth_types()
            else:
                auth_types = condition_data.get(ConditionDataStore.AUTH_TYPES_ATTR)
                policy.update({ConditionDataStore.CONDITION_ATTR: condition_data.get(ConditionDataStore.CONDITION_ATTR)})
        for auth_type in auth_types:
            if auth_type == 'face_identification':
                continue
            plugin_config = self._plugin_manager.get_plugin_auth_config(auth_type=auth_type)
            r_resource = self._plugin_manager.get_plugin_by_auth_type(auth_type=auth_type).check_resources(
                resources=device_resources, plugin_auth_config=plugin_config, training=training)
            if r_resource is not None:
                r_resource.update({'tType': auth_type})
                try_resource_items.append(r_resource)
        return policy, try_resource_items

    def check_policy_try_wait_conditions(self, try_policy):
        return try_policy.get(ConditionDataStore.CONDITION_ATTR, self.CONDITION_ANY) == self.CONDITION_ANY
