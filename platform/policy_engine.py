from typing import List

import numpy as np

def apply_intervention(streamers, viewer_distribution, round_num, intervention_type):
    """实施干预政策"""
    if isinstance(intervention_type, str):
        intervention_type = [intervention_type]

    for intervention in intervention_type:
        if intervention == "high_tax":
            # 对头部主播提高抽成
            top_streamers = np.argsort(viewer_distribution[round_num - 1])[-3:]
            for streamer_id in top_streamers:
                streamers[streamer_id].revenue_share = min(
                    streamers[streamer_id].revenue_share + 0.2, 0.6
                )

        elif intervention == "boost_small":
            # 扶持小主播
            bottom_streamers = np.argsort(viewer_distribution[round_num - 1])[:5]
            for streamer_id in bottom_streamers:
                streamers[streamer_id].exposure_boost = 2.0
                streamers[streamer_id].revenue_share *= 0.8