import pandas as pd
import numpy as np
from simulation.core import LiveStreamingPlatform
from analysis.visualize import plot_results
from simulation.metrics import calculate_metrics
import argparse


def sensitivity_analysis(param, param_range, steps, experiment_phase=1):
    """敏感性分析"""
    param_values = np.linspace(param_range[0], param_range[1], steps)
    results = {}
    for value in param_values:
        print(f"Testing {param}={value} in experiment phase {experiment_phase}")
        config = {
            'n_streamers': 15,
            'n_viewers': 1000,
            'n_rounds': 50,
            'base_revenue_share': 0.2,
            'network_effect_beta': 0.15,
            'quality_decay_rate': 0.01,
            'random_effect_scale': 0.2,
            'initial_audience_distribution': {
                'high': 0.1,
               'medium': 0.3,
                'low': 0.6
            },
            'viewer_interaction_groups': {
                'high': 0.3,
                'low': 0.7
            },
            'tax_rates': [0, 0.2, 0.4],
            'exposure_betas': [1.0, 1.5, 2.0],
           'reward_thresholds': [10, 20, 30]
        }
        if param == 'network_effect_beta':
            config['network_effect_beta'] = value
        elif param == 'base_revenue_share':
            config['base_revenue_share'] = value
        # 新增参数的处理逻辑
        elif param == 'tax_rates':
            config['tax_rates'] = [value]
        elif param == 'exposure_betas':
            config['exposure_betas'] = [value]
        elif param =='reward_thresholds':
            config['reward_thresholds'] = [value]
        else:
            raise ValueError(f"Unsupported parameter: {param}")

        platform = LiveStreamingPlatform(**config)
        platform.run_experiment(experiment_phase=experiment_phase)
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
    parser.add_argument('--phase', type=int, default=1, help='Experiment phase for sensitivity analysis')
    args = parser.parse_args()

    print("\nRunning sensitivity analysis...")
    results_sensitivity = sensitivity_analysis(args.param, args.range, args.steps, args.phase)
    print("\nSensitivity analysis results:")
    print(results_sensitivity)