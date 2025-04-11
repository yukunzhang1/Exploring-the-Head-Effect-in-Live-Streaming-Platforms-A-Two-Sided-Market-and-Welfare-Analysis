from dataclasses import dataclass
import numpy as np

@dataclass
class StreamerConfig:
    initial_quality: float  # 初始内容质量
    current_quality: float  # 当前质量
    cost_coefficient: float  # 内容质量提升的成本系数
    revenue_share: float  # 平台抽成率
    exposure_boost: float  # 流量提升系数
    followers: int  # 粉丝数量

    def update_quality(self, revenue, viewers):
        """更新主播质量"""
        investment = revenue * 0.1
        quality_delta = (investment / (1000 * self.cost_coefficient)) - 0.05
        self.current_quality += quality_delta
        self.current_quality = np.clip(self.current_quality, 0.1, 1.0)
        return self.current_quality