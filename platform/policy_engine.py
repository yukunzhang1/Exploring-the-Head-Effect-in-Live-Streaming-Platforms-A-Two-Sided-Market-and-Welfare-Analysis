from typing import List

import numpy as np


class PolicyEngine:
    @staticmethod
    def apply_high_tax(streamers: List[Broadcaster], top_percent: float = 0.1):
        """对头部主播征收阶梯税"""
        revenues = [s.revenue for s in streamers]
        threshold = np.quantile(revenues, 1 - top_percent)

        for s in streamers:
            if s.revenue > threshold:
                tax_rate = 0.25 + 0.1 * (s.revenue - threshold) / threshold
                s.revenue_share = min(s.revenue_share + tax_rate, 0.6)

    @staticmethod
    def boost_small_streamers(streamers: List[Broadcaster], bottom_percent: float = 0.3):
        """扶持尾部主播"""
        viewers = [s.viewers for s in streamers]
        cutoff = np.quantile(viewers, bottom_percent)

        for s in streamers:
            if s.viewers <= cutoff:
                s.exposure_boost = 2.0
                s.revenue_share *= 0.8