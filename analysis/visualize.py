import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def plot_heatmap(matrix: np.ndarray, title: str):
    """观众分布热力图"""
    plt.figure(figsize=(10, 6))
    sns.heatmap(matrix.T, cmap="YlGnBu")
    plt.title(title)
    plt.xlabel("Round")
    plt.ylabel("Streamer ID")
    plt.tight_layout()
    plt.savefig(f"results/{title.replace(' ', '_')}.png")
    plt.close()


def plot_revenue_trends(platform_rev: list, streamer_rev: list):
    """收益趋势对比图"""
    plt.plot(platform_rev, label='Platform Revenue')
    plt.plot(streamer_rev, label='Total Streamer Revenue')
    plt.legend()
    plt.savefig("results/revenue_trends.png")
    plt.close()
