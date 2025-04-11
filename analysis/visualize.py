import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def plot_results(viewer_distribution, platform_revenue, streamer_revenues, quality_history, viewer_satisfaction):
    """绘制结果图表"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    # 观众分布热力图
    sns.heatmap(viewer_distribution.T, ax=ax1)
    ax1.set_title('Viewer Distribution Over Time')
    ax1.set_xlabel('Round')
    ax1.set_ylabel('Streamer ID')

    # 收益曲线
    ax2.plot(platform_revenue, label='Platform Revenue')
    ax2.plot(streamer_revenues.sum(axis=1), label='Total Streamer Revenue')
    ax2.set_title('Revenue Over Time')
    ax2.set_xlabel('Round')
    ax2.set_ylabel('Revenue')
    ax2.legend()

    # 质量变化
    ax3.plot(quality_history)
    ax3.set_title('Streamer Quality Over Time')
    ax3.set_xlabel('Round')
    ax3.set_ylabel('Quality')

    # 观众满意度
    ax4.plot(np.mean(viewer_satisfaction, axis=1))
    ax4.set_title('Average Viewer Satisfaction')
    ax4.set_xlabel('Round')
    ax4.set_ylabel('Satisfaction')

    plt.tight_layout()
    plt.show()
