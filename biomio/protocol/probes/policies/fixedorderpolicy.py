
from biomio.protocol.probes.ipolicy import IPolicy
from ast import literal_eval

import logging
logger = logging.getLogger(__name__)


FIELD_RESOURCE_TYPE = 'rType'
FIELD_SAMPLES_NUM = 'samples'


def create_resource_item(type_str, samples):
    return {FIELD_RESOURCE_TYPE: type_str, FIELD_SAMPLES_NUM: samples}


class FixedOrderPolicy(IPolicy):
    def __init__(self, config_str):
        self._set_config(config_str)
        self.resource_items_ordered_dict = {}

    def get_resources_list_for_try(self, available_resources):
        """
        Reimplemented from IPolicy.get_resources_list_for_try().
        """
        resource_item_list = []
        for resource_item_type, props in self.resource_items_ordered_dict.iteritems():
            res_type = props.get(FIELD_RESOURCE_TYPE, None)
            if res_type in available_resources:
                samples_num = props.get(FIELD_SAMPLES_NUM, None)
                resource_item_list.append(create_resource_item(type_str=resource_item_type, samples=samples_num))
        #TODO: fixme
        from biomio.protocol.settings import settings
        resource_item_list.append(create_resource_item(settings.policy_try_type, 1))

        return resource_item_list

    def get_resources_list_for_training(self, available_resources):
        resource_item_list = []
        resource_item_list.append(create_resource_item('face-photo', 5))
        return resource_item_list

    def _set_config(self, config_string):
        """
        Reimplemented from IPolicy._set_config().
        """
        try:
            self.resource_items_ordered_dict = literal_eval(config_string)
        except ValueError:
            logging.error(msg="Cannot read config for FixedOrderPolicy")