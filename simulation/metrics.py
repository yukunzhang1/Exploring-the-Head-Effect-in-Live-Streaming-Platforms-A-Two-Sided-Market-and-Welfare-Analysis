import numpy as np


def gini(x):
    """
    计算数组 x 的 Gini 系数。
    参数：
        x: 一个可转为 numpy 数组的一维非负数数组。
    返回：
        Gini 系数，一个介于 0 和 1 之间的浮点数。
    """
    x = np.array(x).flatten()
    if np.amin(x) < 0:
        x = x - np.amin(x)
    x = x + 1e-10  # 避免除零
    x = np.sort(x)
    n = x.shape[0]
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * x)) / (n * np.sum(x))


def calculate_metrics(viewer_distribution, viewer_satisfaction, quality_history):
    """计算评估指标"""
    final_distribution = viewer_distribution[-1]

    # 基础指标
    gini_coefficient = gini(final_distribution)
    top_3_share = np.sort(final_distribution)[-3:].sum() / final_distribution.sum()

    # 流动性指标
    viewer_changes = np.diff(viewer_distribution, axis=0)
    mobility = np.mean(np.abs(viewer_changes))

    # 长尾指标
    tail_share = np.sort(final_distribution)[:-3].sum() / final_distribution.sum()

    # 观众满意度
    avg_satisfaction = np.mean(viewer_satisfaction[-1])

    # 质量提升
    quality_improvement = np.mean(quality_history[-1] - quality_history[0])

    return {
        'gini_coefficient': gini_coefficient,
        'top_3_share': top_3_share,
        'viewer_mobility': mobility,
        'tail_share': tail_share,
        'avg_satisfaction': avg_satisfaction,
        'quality_improvement': quality_improvement
    }
