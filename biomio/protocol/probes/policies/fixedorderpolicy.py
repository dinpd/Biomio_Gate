
from biomio.protocol.probes.ipolicy import IPolicy
from ast import literal_eval

import logging
logger = logging.getLogger(__name__)

def create_resource_item(type_str, samples):
    return {'rType': type_str, 'samples': samples}

class FixedOrderPolicy(IPolicy):
    def __init__(self):
        self.resource_items_ordered_dict = {}

    def get_resources_list_for_try(self, available_resources):
        """
        Reimplemented from IPolicy.get_resources_list_for_try().
        """
        resource_item_list = []
        for resource_item_type, samples in self.resource_items_ordered_dict.iteritems():
            if resource_item_type in available_resources:
                resource_item_list.append(create_resource_item(type_str=resource_item_type, samples=samples))

        return resource_item_list

    def set_config(self, config_string):
        """
        Reimplemented from IPolicy.set_config().
        """
        try:
            self.resource_items_ordered_dict = literal_eval(config_string)
        except ValueError:
            logging.error(msg="Cannot read config for FixedOrderPolicy")