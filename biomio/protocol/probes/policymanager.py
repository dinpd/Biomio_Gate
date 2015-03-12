from biomio.protocol.probes.policies.fixedorderpolicy import FixedOrderPolicy
import os

class PolicyManager:
    @staticmethod
    def get_policy_for_user(user_id):
        # Get policy config
        config_str = PolicyManager._policy_config_for_user(user_id=user_id)
        return FixedOrderPolicy(config_str=config_str)

    @staticmethod
    def _policy_config_for_user(user_id):
        currdir =os.path.dirname(os.path.abspath(__file__))
        config_file = open('%s/policies/default_fixedorderpolicy.conf' % currdir, 'r')
        config_str = config_file.read()
        return config_str
