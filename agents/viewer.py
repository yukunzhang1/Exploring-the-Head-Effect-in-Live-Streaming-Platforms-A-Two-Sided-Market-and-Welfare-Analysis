# agents/viewer.py
from dataclasses import dataclass
from random import random

import numpy as np

from agents.broadcaster import Broadcaster


@dataclass
class Viewer:
    interaction_willingness: float
    price_sensitivity: float
    quality_sensitivity: float
    network_effect_sensitivity: float
    preferred_content_type: int
    loyalty: float

    def calculate_utility(self, streamer: Broadcaster, current_viewers: int, round_num: int):
        time_decay = np.exp(-0.01 * round_num)
        return (
            self.quality_sensitivity * streamer.current_quality +
            self.network_effect_sensitivity * 0.15 * np.log1p(current_viewers) * time_decay -
            self.price_sensitivity * streamer.revenue_share +
            random.normalvariate(0, 0.2) +
            (self.loyalty * 0.2 if current_viewers > 0 else 0)
        )