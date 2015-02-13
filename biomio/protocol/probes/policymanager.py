from biomio.protocol.probes.ipolicy import IPolicy
from biomio.protocol.probes.policies.fixedorderpolicy import FixedOrderPolicy


class PolicyManager:

    @staticmethod
    def get_policy_for_user(self, user_id):

        policy = FixedOrderPolicy()

        config_file = open('biomio/protocol/policies/default_fixedorderpolicy.conf', 'r')
        config_str = config_file.read()
        policy.set_config(config_str=config_str)

        return policy
