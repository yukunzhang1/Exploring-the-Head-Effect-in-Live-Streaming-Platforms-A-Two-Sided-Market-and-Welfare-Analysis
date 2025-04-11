from dataclasses import dataclass
import random

import numpy as np


@dataclass
class ViewerConfig:
    interaction_willingness: float  # 互动意愿
    price_sensitivity: float  # 价格敏感度
    quality_sensitivity: float  # 质量敏感度
    network_effect_sensitivity: float  # 网络效应敏感度
    preferred_content_type: int  # 内容偏好
    loyalty: float  # 观众忠诚度

    def calculate_utility(self, streamer, current_viewers, round_num, quality_decay_rate, network_effect_beta, random_effect_scale):
        """计算观众效用函数，增加时间衰减和随机因素"""
        # 时间衰减因子
        time_decay = np.exp(-quality_decay_rate * round_num)

        # 计算各组件效用
        quality_utility = self.quality_sensitivity * streamer.current_quality
        network_utility = (self.network_effect_sensitivity *
                           network_effect_beta *
                           np.log1p(current_viewers) *
                           time_decay)
        price_cost = self.price_sensitivity * streamer.revenue_share

        # 随机扰动
        random_factor = np.random.normal(0, random_effect_scale)

        # 忠诚度影响
        loyalty_bonus = 0
        if round_num > 0 and current_viewers > 0:
            loyalty_bonus = self.loyalty * 0.2

        return quality_utility + network_utility - price_cost + random_factor + loyalty_bonus