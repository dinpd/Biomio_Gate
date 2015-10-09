import logging
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT

logger = logging.getLogger(__name__)


class PolicyActions(BaseActions):
    # _FIELD_RESOURCE_TYPE = 'rType'
    # _FIELD_SAMPLES_NUM = 'samples'

    def __init__(self, callback):
        self._callback = callback

    @rule_action(params={"valid_plugins": FIELD_TEXT})
    def valid_plugins_found(self, valid_plugins):
        logger.debug(valid_plugins)
        self._callback([valid_plugin.strip() for valid_plugin in valid_plugins.split(',')])
