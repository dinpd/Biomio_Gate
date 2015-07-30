from business_rules.variables import BaseVariables, boolean_rule_variable, select_rule_variable, string_rule_variable


class DeviceResources(BaseVariables):

    def __init__(self, probe_device_resources):
        self.probe_device_resources = probe_device_resources

    @boolean_rule_variable
    def has_fp_scanner(self):
        return self.probe_device_resources.fp_scanner_available

    @boolean_rule_variable
    def has_front_photo_cam(self):
        return self.probe_device_resources.front_photo_cam_available

    @boolean_rule_variable
    def has_back_photo_cam(self):
        return self.probe_device_resources.back_photo_cam_available

    @boolean_rule_variable
    def has_mic(self):
        return self.probe_device_resources.mic_avaialble

    @select_rule_variable
    def front_cam_available_resolutions(self):
        return self.probe_device_resources.front_cam_resolutions

    @select_rule_variable
    def back_cam_available_resolutions(self):
        return self.probe_device_resources.back_cam_resolutions

    @string_rule_variable
    def os_version(self):
        return self.probe_device_resources.os_version

    @string_rule_variable
    def model_type(self):
        return self.probe_device_resources.model_type
