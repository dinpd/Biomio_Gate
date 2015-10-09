from business_rules.operators import SelectMultipleType, NumericType
from business_rules.variables import BaseVariables, rule_variable


class PolicyVariables(BaseVariables):
    def __init__(self, policy_data):
        self._policy_data = policy_data

    @rule_variable(SelectMultipleType, cache_result=False)
    def available_device_resources(self):
        return self._policy_data.get('available_device_resources', [])

    @rule_variable(NumericType, cache_result=False)
    def max_attempts(self):
        return self._policy_data.get('max_attempts', 0)

    @rule_variable(NumericType, cache_result=False)
    def max_authentication_time(self):
        return self._policy_data.get('max_authentication_time', 0)

    @rule_variable(NumericType, cache_result=False)
    def max_re_auth_time(self):
        return self._policy_data.get('max_re_auth_time', 0)

    @rule_variable(NumericType, cache_result=False)
    def max_cer(self):
        return self._policy_data.get('max_cer', 0)
