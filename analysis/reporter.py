import argparse
import pandas as pd
from analysis.visualize import plot_results
from simulation.metrics import calculate_metrics
import numpy as np

def generate_report(input_dir, output_dir):
    # 这里简单假设从输入目录读取数据
    # 实际中可能需要根据具体存储格式进行调整
    viewer_distribution = np.load(f'{input_dir}/viewer_distribution.npy')
    platform_revenue = np.load(f'{input_dir}/platform_revenue.npy')
    streamer_revenues = np.load(f'{input_dir}/streamer_revenues.npy')
    quality_history = np.load(f'{input_dir}/quality_history.npy')
    viewer_satisfaction = np.load(f'{input_dir}/viewer_satisfaction.npy')

    # 绘制图表
    plot_results(viewer_distribution, platform_revenue, streamer_revenues, quality_history, viewer_satisfaction)

    # 计算指标
    metrics = calculate_metrics(viewer_distribution, viewer_satisfaction, quality_history)
    metrics_df = pd.DataFrame([metrics])

    # 保存指标到文件
    metrics_df.to_csv(f'{output_dir}/metrics.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate report from simulation results')
    parser.add_argument('--input', type=str, required=True, help='Input directory containing simulation results')
    parser.add_argument('--output', type=str, required=True, help='Output directory for report')
    args = parser.parse_args()

    generate_report(args.input, args.output)