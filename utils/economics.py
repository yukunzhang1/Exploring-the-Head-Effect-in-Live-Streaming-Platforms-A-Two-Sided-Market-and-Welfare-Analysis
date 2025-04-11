import numpy as np


def calculate_gini(x):
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