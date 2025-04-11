from analysis.visualize import plot_heatmap
from platform.policy_engine import PolicyEngine

from simulation.core import LiveStreamSimulator


def run_comparative(config_path: str):
    """运行多场景对比实验"""
    config = load_config(config_path)
    scenarios = {
        'baseline': [],
        'high_tax': [PolicyEngine.apply_high_tax],
        'boost_small': [PolicyEngine.boost_small_streamers],
        'combined': [PolicyEngine.apply_high_tax, PolicyEngine.boost_small_streamers]
    }

    results = {}
    for name, policies in scenarios.items():
        sim = LiveStreamSimulator(config)
        sim.run(policies)
        results[name] = sim.metrics.summary()
        plot_heatmap(sim.viewer_distribution, f'{name} Viewer Distribution')

    return pd.DataFrame(results)