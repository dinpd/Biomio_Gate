
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
        super(FixedOrderPolicy, self).__init__(config_str=config_str)
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

        return resource_item_list

    def _set_config(self, config_string):
        """
        Reimplemented from IPolicy._set_config().
        """
        try:
            self.resource_items_ordered_dict = literal_eval(config_string)
        except ValueError:
            logging.error(msg="Cannot read config for FixedOrderPolicy")