import pandas as pd
from simulation.core import LiveStreamingPlatform
from analysis.visualize import plot_results
from simulation.metrics import calculate_metrics


def run_comparative_experiments():
    scenarios = {
        'baseline': {
            'intervention_round': None,
            'intervention_type': None,
            'experiment_phase': 1
        },
        'high_tax': {
            'intervention_round': 25,
            'intervention_type': 'high_tax',
            'experiment_phase': 2
        },
        'beta_boost': {
            'intervention_round': 25,
            'intervention_type': 'beta_boost',
            'experiment_phase': 2
        },
        'revenue_boost': {
            'intervention_round': 25,
            'intervention_type': 'revenue_boost',
            'experiment_phase': 2
        },
        'combined': {
            'intervention_round': 25,
            'intervention_type': None,
            'experiment_phase': 3
        }
    }

    results = {}
    for name, params in scenarios.items():
        print(f"Running scenario: {name}")
        platform = LiveStreamingPlatform()
        platform.run_experiment(**params)
        results[name] = platform.calculate_metrics()
        plot_results(
            platform.viewer_distribution,
            platform.platform_revenue,
            platform.streamer_revenues,
            platform.quality_history,
            platform.viewer_satisfaction
        )

        # 保存结果
        import numpy as np
        np.save(f'results/{name}/viewer_distribution.npy', platform.viewer_distribution)
        np.save(f'results/{name}/platform_revenue.npy', platform.platform_revenue)
        np.save(f'results/{name}/streamer_revenues.npy', platform.streamer_revenues)
        np.save(f'results/{name}/quality_history.npy', platform.quality_history)
        np.save(f'results/{name}/viewer_satisfaction.npy', platform.viewer_satisfaction)
        np.save(f'results/{name}/metrics.npy', platform.metrics)

    return pd.DataFrame(results).T


if __name__ == "__main__":
    print("Running comparative experiments...")
    results_comparative = run_comparative_experiments()
    print("\nComparative results:")
    print(results_comparative)
