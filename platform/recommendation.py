import numpy as np


def recommend_streamers(viewers, streamers, viewer_distribution, round_num, quality_decay_rate, network_effect_beta,
                        random_effect_scale):
    """观众选择主播"""
    n_streamers = len(streamers)
    n_viewers = len(viewers)
    viewer_choices = np.zeros(n_streamers)
    viewer_satisfaction = np.zeros(n_viewers)

    for viewer_id in range(n_viewers):
        utilities = [
            viewers[viewer_id].calculate_utility(
                streamers[streamer_id],
                viewer_distribution[round_num - 1, streamer_id] if round_num > 0 else 0,
                round_num,
                quality_decay_rate,
                network_effect_beta,
                random_effect_scale
            )
            for streamer_id in range(n_streamers)
        ]

        # 考虑曝光提升
        utilities = np.array(utilities) * np.array([s.exposure_boost for s in streamers.values()])

        chosen_streamer = np.argmax(utilities)
        viewer_choices[chosen_streamer] += 1

        # 记录观众满意度
        viewer_satisfaction[viewer_id] = max(utilities)

    return viewer_choices, viewer_satisfaction
