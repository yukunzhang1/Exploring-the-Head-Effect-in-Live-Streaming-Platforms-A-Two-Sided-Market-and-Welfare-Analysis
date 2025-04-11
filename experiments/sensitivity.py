import pandas as pd
import numpy as np
from simulation.core import LiveStreamingPlatform
from analysis.visualize import plot_results
from simulation.metrics import calculate_metrics
import argparse

def sensitivity_analysis(param, param_range, steps):
    """敏感性分析"""
    param_values = np.linspace(param_range[0], param_range[1], steps)
    results = {}
    for value in param_values:
        print(f"Testing {param}={value}")
        if param == 'network_effect_beta':
            platform = LiveStreamingPlatform(network_effect_beta=value)
        elif param == 'base_revenue_share':
            platform = LiveStreamingPlatform(base_revenue_share=value)
        else:
            raise ValueError(f"Unsupported parameter: {param}")
        platform.run_experiment()
        results[value] = calculate_metrics(
            platform.viewer_distribution,
            platform.viewer_satisfaction,
            platform.quality_history
        )
        plot_results(
            platform.viewer_distribution,
            platform.platform_revenue,
            platform.streamer_revenues,
            platform.quality_history,
            platform.viewer_satisfaction
        )

        # 保存结果
        import numpy as np
        np.save(f'results/sensitivity_{param}_{value}/viewer_distribution.npy', platform.viewer_distribution)
        np.save(f'results/sensitivity_{param}_{value}/platform_revenue.npy', platform.platform_revenue)
        np.save(f'results/sensitivity_{param}_{value}/streamer_revenues.npy', platform.streamer_revenues)
        np.save(f'results/sensitivity_{param}_{value}/quality_history.npy', platform.quality_history)
        np.save(f'results/sensitivity_{param}_{value}/viewer_satisfaction.npy', platform.viewer_satisfaction)

    return pd.DataFrame(results).T

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sensitivity analysis')
    parser.add_argument('--param', type=str, required=True, help='Parameter to vary')
    parser.add_argument('--range', type=float, nargs=2, required=True, help='Range of parameter values')
    parser.add_argument('--steps', type=int, required=True, help='Number of steps in the range')
    args = parser.parse_args()

    print("\nRunning sensitivity analysis...")
    results_sensitivity = sensitivity_analysis(args.param, args.range, args.steps)
    print("\nSensitivity analysis results:")
    print(results_sensitivity)