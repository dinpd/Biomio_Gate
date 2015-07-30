import json
import logging
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT

logger = logging.getLogger(__name__)


class PolicyActions(BaseActions):

    _FIELD_RESOURCE_TYPE = 'rType'
    _FIELD_SAMPLES_NUM = 'samples'

    def __init__(self, callback):
        self._callback = callback

    @rule_action(params={"required_resources_dict": FIELD_TEXT})
    def return_verification_resources(self, required_resources_dict):
        required_resources_list = []
        try:
            required_resources_list = json.loads(required_resources_dict)
        except Exception as e:
            logging.exception("Was not able to generate the list of required resources.")
            logging.exception(e)
        self._callback(required_resources_list)
