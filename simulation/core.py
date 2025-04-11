import numpy as np
import random
from agents.broadcaster import StreamerConfig
from agents.viewer import ViewerConfig
from platform.recommendation import recommend_streamers

from platform.policy_engine import apply_intervention

from simulation.metrics import gini


# from platform.policy_engine import apply_intervention
# from platform.recommendation import recommend_streamers

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
        streamers = {}
        initial_qualities = np.random.normal(0.5, 0.2, self.n_streamers)
        initial_qualities = np.clip(initial_qualities, 0.1, 0.9)

        high_count = int(self.n_streamers * self.config['initial_audience_distribution']['high'])
        medium_count = int(self.n_streamers * self.config['initial_audience_distribution']['medium'])
        low_count = self.n_streamers - high_count - medium_count

        for i in range(high_count):
            streamers[i] = StreamerConfig(
                initial_quality=initial_qualities[i],
                current_quality=initial_qualities[i],
                cost_coefficient=random.uniform(0.1, 0.3),
                revenue_share=self.config['base_revenue_share'],
                exposure_boost=1.0,
                followers=100  # 高初始人气组
            )
        for i in range(high_count, high_count + medium_count):
            streamers[i] = StreamerConfig(
                initial_quality=initial_qualities[i],
                current_quality=initial_qualities[i],
                cost_coefficient=random.uniform(0.1, 0.3),
                revenue_share=self.config['base_revenue_share'],
                exposure_boost=1.0,
                followers=50  # 中初始人气组
            )
        for i in range(high_count + medium_count, self.n_streamers):
            streamers[i] = StreamerConfig(
                initial_quality=initial_qualities[i],
                current_quality=initial_qualities[i],
                cost_coefficient=random.uniform(0.1, 0.3),
                revenue_share=self.config['base_revenue_share'],
                exposure_boost=1.0,
                followers=10  # 低初始人气组
            )
        return streamers

    def _initialize_viewers(self) -> dict:
        viewers = {}
        high_count = int(self.n_viewers * self.config['viewer_interaction_groups']['high'])
        low_count = self.n_viewers - high_count

        for i in range(high_count):
            viewers[i] = ViewerConfig(
                interaction_willingness=random.uniform(0.6, 0.8),
                price_sensitivity=random.uniform(0.3, 0.5),
                quality_sensitivity=random.uniform(0.6, 0.8),
                network_effect_sensitivity=random.uniform(0.2, 0.4),
                preferred_content_type=random.randint(0, 2),
                loyalty=random.uniform(0.5, 0.7)
            )
        for i in range(high_count, self.n_viewers):
            viewers[i] = ViewerConfig(
                interaction_willingness=random.uniform(0.2, 0.4),
                price_sensitivity=random.uniform(0.5, 0.7),
                quality_sensitivity=random.uniform(0.4, 0.6),
                network_effect_sensitivity=random.uniform(0.1, 0.2),
                preferred_content_type=random.randint(0, 2),
                loyalty=random.uniform(0.3, 0.5)
            )
        return viewers

    def run_experiment(self,
                       intervention_round: int = None,
                       intervention_type=None,
                       experiment_phase: int = 1):
        for round_num in range(self.n_rounds):
            if round_num == intervention_round:
                self.current_phase = experiment_phase

            if self.current_phase == 2:
                if intervention_type == "high_tax":
                    self._apply_high_tax()
                elif intervention_type == "beta_boost":
                    self._apply_beta_boost()
                elif intervention_type == "revenue_boost":
                    self._apply_revenue_boost()
            elif self.current_phase == 3:
                self._apply_combined_interventions()

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

            self._calculate_revenues(round_num)
            self._update_streamer_quality(round_num)
            self._record_metrics(round_num)

    def _apply_high_tax(self):
        top_streamers = np.argsort(self.viewer_distribution[self.current_round - 1])[-3:]
        for streamer_id in top_streamers:
            self.streamers[streamer_id].revenue_share = min(
                self.streamers[streamer_id].revenue_share + 0.2, 0.6
            )

    def _apply_beta_boost(self):
        bottom_streamers = np.argsort(self.viewer_distribution[self.current_round - 1])[:5]
        for streamer_id in bottom_streamers:
            self.streamers[streamer_id].exposure_boost = 2.0
            self.streamers[streamer_id].revenue_share *= 0.8

    def _apply_revenue_boost(self):
        bottom_streamers = np.argsort(self.viewer_distribution[self.current_round - 1])[:5]
        for streamer_id in bottom_streamers:
            self.streamers[streamer_id].revenue_share *= 0.8

    def _apply_combined_interventions(self):
        self._apply_high_tax()
        self._apply_beta_boost()
        self._apply_revenue_boost()

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

    def _record_metrics(self, round_num):
        for streamer_id in range(self.n_streamers):
            viewers = self.viewer_distribution[round_num, streamer_id]
            self.metrics['viewers_per_streamer'][round_num, streamer_id] = viewers
            self.metrics['total_viewers'][round_num] += viewers
            self.metrics['total_reward'][round_num] += self.streamer_revenues[round_num, streamer_id]
            self.metrics['platform_revenue'][round_num] += self.platform_revenue[round_num]
            self.metrics['activity'][round_num, streamer_id] = self._calculate_activity(streamer_id, round_num)

    def _calculate_activity(self, streamer_id, round_num):
        # 假设活跃度根据观众互动次数和观看时长计算
        # 这里简单模拟，实际可根据具体需求调整
        return self.viewer_distribution[round_num, streamer_id] * 0.1 + self.viewer_satisfaction[round_num].sum() * 0.01

    def calculate_metrics(self):
        final_distribution = self.viewer_distribution[-1]
        gini_coefficient = gini(final_distribution)
        hhi_index = self._calculate_hhi(final_distribution)
        top_10_share = np.sort(final_distribution)[-int(0.1 * self.n_streamers):].sum() / final_distribution.sum()

        consumer_surplus = self._calculate_consumer_surplus()
        producer_surplus = self._calculate_producer_surplus()
        platform_profit = self.platform_revenue.sum()

        social_welfare = consumer_surplus + producer_surplus + platform_profit

        return {
            'gini_coefficient': gini_coefficient,
            'hhi_index': hhi_index,
            'top_10_share': top_10_share,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': producer_surplus,
            'platform_profit': platform_profit,
            'social_welfare': social_welfare
        }

    def _calculate_hhi(self, distribution):
        shares = distribution / distribution.sum()
        return np.sum(shares ** 2)

    def _calculate_consumer_surplus(self):
        # 简单假设消费者剩余根据观众满意度和观看时长计算
        # 实际可根据问卷或更复杂模型调整
        return self.viewer_satisfaction.sum() * 0.1 + self.viewer_distribution.sum() * 0.01

    def _calculate_producer_surplus(self):
        return self.streamer_revenues.sum() - self._calculate_production_costs()

    def _calculate_production_costs(self):
        # 假设生产成本根据主播质量提升投入计算
        # 实际可根据主播投入时间或资源点数调整
        costs = []
        for streamer in self.streamers.values():
            cost = (streamer.current_quality - streamer.initial_quality) * streamer.cost_coefficient * 1000
            costs.append(cost)
        return np.sum(costs)