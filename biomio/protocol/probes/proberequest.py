import logging
from biomio.protocol.probes.policy_engine.policy_engine_manager import PolicyEngineManager

logger = logging.getLogger(__name__)


class ProbeRequest:
    """
    Class ProbeRequest is responsible for checking and counting probes and samples for each probe.
    """

    def __init__(self, probe_condition):
        self.probe_list = []
        self.sample_count_by_probe_type = {}
        self.sample_data_by_probe_type = {}

        self.current_probe = None
        self.current_sample = None

        self._probe_condition = probe_condition

    def clear(self):
        self.probe_list = []
        self.sample_count_by_probe_type = {}
        self.sample_data_by_probe_type = {}

        self.current_probe = None
        self.current_sample = None

    def add_probe(self, probe_type, samples):
        """
        Add new probe to count.
        :param probe_type: Probe type string (as defined in scheme 'face-photo', 'fp-scan', etc).
        :param samples: List of samples of he given type.
        """
        if probe_type not in self.probe_list:
            self.probe_list.append(probe_type)
            self.sample_count_by_probe_type[probe_type] = samples
        else:
            logger.error('Could not add probe - probe already exists.')

    def has_pending_probes(self, current_probe_id):
        if self.probe_list:
            if self._probe_condition == PolicyEngineManager.CONDITION_ANY:
                probe_type = self.probe_list[int(current_probe_id)]
                return len(self.sample_data_by_probe_type.get(probe_type, [])) != self.sample_count_by_probe_type.get(
                    probe_type, 0)
            for probe_type in self.probe_list:
                if len(self.sample_data_by_probe_type.get(probe_type, [])) != self.sample_count_by_probe_type.get(
                        probe_type, 0):
                    return True
        return False

    def add_next_sample(self, probe_id, samples_list):
        try:
            # Get probe type by index (id)
            probe_type = self.probe_list[int(probe_id)]

            # Check sample number(id) is in bounds
            samples_count = self.sample_count_by_probe_type.get(probe_type, 0)
            if samples_count > len(self.sample_data_by_probe_type.get(probe_type, [])):
                if not self.sample_data_by_probe_type.has_key(str(probe_type)):
                    # First sample for given probe - create list for samples
                    self.sample_data_by_probe_type[probe_type] = samples_list
                else:
                    # Append sample to list for given probe
                    self.sample_data_by_probe_type[probe_type].extend(samples_list)

                # Return true if sample successfully added
                return True
        except Exception as e:
            pass

        return False

    def get_samples_by_probe_type(self):
        return self.sample_data_by_probe_type
