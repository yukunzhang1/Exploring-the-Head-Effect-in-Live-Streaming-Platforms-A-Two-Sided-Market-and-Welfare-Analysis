from typing import List


class LiveStreamSimulator:
    def __init__(self, config: dict):
        self.n_rounds = config['n_rounds']
        self.streamers = self._init_streamers(config)
        self.viewers = self._init_viewers(config)
        self.metrics = SimulationMetrics()

    def run(self, policies: List[callable] = []):
        for round in range(self.n_rounds):
            self._apply_policies(round, policies)
            self._simulate_viewer_choices(round)
            self._update_streamers(round)
            self.metrics.record(round, self.streamers, self.viewers)

    def _apply_policies(self, round: int, policies: List[callable]):
        if round >= config['intervention_start']:
            for policy in policies:
                policy(self.streamers)