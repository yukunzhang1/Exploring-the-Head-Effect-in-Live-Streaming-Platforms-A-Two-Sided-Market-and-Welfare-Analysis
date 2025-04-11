# agents/broadcaster.py
from dataclasses import dataclass

import numpy as np


@dataclass
class Broadcaster:
    current_quality: float
    cost_coefficient: float
    revenue_share: float
    exposure_boost: float = 1.0
    followers: int = 0

    def update_quality(self, revenue: float):
        investment = revenue * 0.1
        quality_delta = (investment / (1000 * self.cost_coefficient)) - 0.05
        self.current_quality = np.clip(self.current_quality + quality_delta, 0.1, 1.0)