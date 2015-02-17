

class IPolicy:
    def __init__(self):
        pass

    def get_resources_list_for_try(self, available_resources):
        """
        Returns list of resources in the correct order, with the correct number of samples.
        :param available_resources: List of available resources.
        :return:
        """
        raise NotImplementedError

    def set_config(self, config_string):
        """
        Configures policy based on predefined config.
        :param config_string: String containing configuration for certain policy type.
        """
        raise NotImplementedError