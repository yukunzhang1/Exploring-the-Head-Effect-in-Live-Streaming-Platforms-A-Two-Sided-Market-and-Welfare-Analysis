import numpy as np
import random
from agents.broadcaster import StreamerConfig
from agents.viewer import ViewerConfig
from platform.policy_engine import apply_intervention
from platform.recommendation import recommend_streamers

class LiveStreamingPlatform:
    def __init__(
            self,
            n_streamers: int = 15,
            n_viewers: int = 1000,
            n_rounds: int = 50,
            base_revenue_share: float = 0.2,
            network_effect_beta: float = 0.15,
            quality_decay_rate: float = 0.01,
            random_effect_scale: float = 0.2
    ):
        self.n_streamers = n_streamers
        self.n_viewers = n_viewers
        self.n_rounds = n_rounds
        self.base_revenue_share = base_revenue_share
        self.network_effect_beta = network_effect_beta
        self.quality_decay_rate = quality_decay_rate
        self.random_effect_scale = random_effect_scale

        # 初始化数据结构
        self.streamers = self._initialize_streamers()
        self.viewers = self._initialize_viewers()

        # 记录数据
        self.viewer_distribution = np.zeros((n_rounds, n_streamers))
        self.streamer_revenues = np.zeros((n_rounds, n_streamers))
        self.platform_revenue = np.zeros(n_rounds)
        self.quality_history = np.zeros((n_rounds, n_streamers))
        self.viewer_satisfaction = np.zeros((n_rounds, n_viewers))

    def _initialize_streamers(self) -> dict:
        """初始化主播属性，使用正态分布生成初始质量"""
        streamers = {}
        initial_qualities = np.random.normal(0.5, 0.2, self.n_streamers)
        initial_qualities = np.clip(initial_qualities, 0.1, 0.9)

        for i in range(self.n_streamers):
            streamers[i] = StreamerConfig(
                initial_quality=initial_qualities[i],
                current_quality=initial_qualities[i],
                cost_coefficient=random.uniform(0.1, 0.3),
                revenue_share=self.base_revenue_share,
                exposure_boost=1.0,
                followers=0
            )
        return streamers

    def _initialize_viewers(self) -> dict:
        """初始化观众属性，增加更多个性化特征"""
        viewers = {}
        for i in range(self.n_viewers):
            viewers[i] = ViewerConfig(
                interaction_willingness=random.uniform(0.2, 0.8),
                price_sensitivity=random.uniform(0.3, 0.7),
                quality_sensitivity=random.uniform(0.4, 0.8),
                network_effect_sensitivity=random.uniform(0.1, 0.4),
                preferred_content_type=random.randint(0, 2),
                loyalty=random.uniform(0.3, 0.7)
            )
        return viewers

    def run_experiment(self,
                       intervention_round: int = None,
                       intervention_type=None):
        """运行实验"""
        for round_num in range(self.n_rounds):
            # 实施干预
            if intervention_round and round_num >= intervention_round:
                apply_intervention(self.streamers, self.viewer_distribution, round_num, intervention_type)

            # 观众选择
            viewer_choices, self.viewer_satisfaction[round_num] = recommend_streamers(
                self.viewers,
                self.streamers,
                self.viewer_distribution,
                round_num,
                self.quality_decay_rate,
                self.network_effect_beta,
                self.random_effect_scale
            )
            self.viewer_distribution[round_num] = viewer_choices

            # 计算收益
            self._calculate_revenues(round_num)

            # 更新主播质量
            self._update_streamer_quality(round_num)

    def _calculate_revenues(self, round_num: int):
        """计算收益，考虑观众数量和质量"""
        for streamer_id in range(self.n_streamers):
            viewers = self.viewer_distribution[round_num, streamer_id]
            base_revenue = viewers * 10  # 基础收益

            # 质量奖励
            quality_bonus = self.streamers[streamer_id].current_quality * viewers * 2

            total_revenue = base_revenue + quality_bonus

            # 计算平台和主播收益
            platform_share = total_revenue * self.streamers[streamer_id].revenue_share
            streamer_share = total_revenue - platform_share

            self.streamer_revenues[round_num, streamer_id] = streamer_share
            self.platform_revenue[round_num] += platform_share

    def _update_streamer_quality(self, round_num: int):
        """更新主播质量"""
        for streamer_id in range(self.n_streamers):
            revenue = self.streamer_revenues[round_num, streamer_id]
            viewers = self.viewer_distribution[round_num, streamer_id]
            new_quality = self.streamers[streamer_id].update_quality(revenue, viewers)
            self.quality_history[round_num, streamer_id] = new_quality