import logging
from biomio.protocol.probes.policy_engine.policy_engine_manager import PolicyEngineManager

logger = logging.getLogger(__name__)


class ProbeRequest:
    """
    Class ProbeRequest is responsible for checking and counting probes and samples for each probe.
    """

    def __init__(self, policy):
        self.sample_count_by_probe_type = {}
        self.sample_data_by_probe_type = {}

        self.current_probe = None
        self.current_sample = None

        self._try_policy = policy

    def clear(self):
        self.sample_count_by_probe_type = {}
        self.sample_data_by_probe_type = {}

        self.current_probe = None
        self.current_sample = None

    def add_probe(self, auth_type, samples):
        """
        Add new probe to count.
        :param probe_type: Probe type string (as defined in scheme 'face-photo', 'fp-scan', etc).
        :param samples: List of samples of he given type.
        """
        if auth_type not in self.sample_count_by_probe_type:
            self.sample_count_by_probe_type[auth_type] = samples
        else:
            logger.error('Could not add probe - probe already exists.')

    def has_pending_probes(self, auth_type):
        if PolicyEngineManager.instance().check_policy_try_wait_conditions(self._try_policy):
            return len(self.sample_data_by_probe_type.get(auth_type, [])) != self.sample_count_by_probe_type.get(
                auth_type, 0)
        for auth_type in self.sample_count_by_probe_type.keys():
            if len(self.sample_data_by_probe_type.get(auth_type, [])) != self.sample_count_by_probe_type.get(
                    auth_type, 0):
                return True
        return False

    def add_next_sample(self, auth_type, samples_list):
        try:
            # Check sample number(id) is in bounds
            samples_count = self.sample_count_by_probe_type.get(auth_type, 0)
            if samples_count > len(self.sample_data_by_probe_type.get(auth_type, [])):
                if not self.sample_data_by_probe_type.has_key(auth_type):
                    # First sample for given probe - create list for samples
                    self.sample_data_by_probe_type[auth_type] = samples_list
                else:
                    # Append sample to list for given probe
                    self.sample_data_by_probe_type[auth_type].extend(samples_list)

                # Return true if sample successfully added
                return True
        except Exception as e:
            pass

        return False

    def get_samples_by_probe_type(self):
        return self.sample_data_by_probe_type
