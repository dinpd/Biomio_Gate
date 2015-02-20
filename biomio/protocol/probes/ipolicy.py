

class IPolicy:
    def __init__(self, config_string):
        self._set_config(config_string=config_string)

    def get_resources_list_for_try(self, available_resources):
        """
        Returns list of resources in the correct order, with the corrent number of samples.
        :param available_resources:
        :return:
        """
        raise NotImplementedError

    def _set_config(self, config_string):
        """
        Configures policy based on predefined config.
        :param config_string: String containing configuration for certain policy type.
        """
        raise NotImplementedError