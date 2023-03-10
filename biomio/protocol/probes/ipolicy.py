

class IPolicy:
    def __init__(self, config_string):
        self._set_config(config_string=config_string)

    def get_resources_list_for_try(self, available_resources):
        """
        Returns list of resources in the correct order, with the correct number of samples.
        :param available_resources: List of available resources.
        :return:
        """
        raise NotImplementedError

    def get_resources_list_for_training(self, available_resources):
        raise NotImplementedError

    def _set_config(self, config_string):
        """
        Configures policy based on predefined config.
        :param config_string: String containing configuration for certain policy type.
        """
        raise NotImplementedError