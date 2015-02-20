from biomio.protocol.probes.policies.fixedorderpolicy import FixedOrderPolicy

class PolicyManager:
    @staticmethod
    def get_policy_for_user(self, user_id):
        # Get policy config
        config_str = self._policy_config_for_user(user_id=user_id)
        return FixedOrderPolicy(config_str=config_str)

    @staticmethod
    def _policy_config_for_user(self, user_id):
        config_file = open('biomio/protocol/policies/default_fixedorderpolicy.conf', 'r')
        config_str = config_file.read()
        return config_str
