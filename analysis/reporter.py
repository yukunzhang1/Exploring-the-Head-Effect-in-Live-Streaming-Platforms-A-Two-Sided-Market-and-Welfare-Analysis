import argparse
import pandas as pd
from analysis.visualize import plot_results
from simulation.metrics import calculate_metrics
import numpy as np


def generate_report(input_dir, output_dir):
    # 读取数据
    viewer_distribution = np.load(f'{input_dir}/viewer_distribution.npy')
    platform_revenue = np.load(f'{input_dir}/platform_revenue.npy')
    streamer_revenues = np.load(f'{input_dir}/streamer_revenues.npy')
    quality_history = np.load(f'{input_dir}/quality_history.npy')
    viewer_satisfaction = np.load(f'{input_dir}/viewer_satisfaction.npy')

    # 可能存在的其他数据读取，例如新添加的指标相关数据
    # metrics_data = np.load(f'{input_dir}/metrics_data.npy')

    # 绘制图表
    plot_results(viewer_distribution, platform_revenue, streamer_revenues, quality_history, viewer_satisfaction)

    # 计算指标
    metrics = calculate_metrics(viewer_distribution, viewer_satisfaction, quality_history)
    metrics_df = pd.DataFrame([metrics])

    # 保存指标到文件
    metrics_df.to_csv(f'{output_dir}/metrics.csv', index=False)

    # 生成详细的报告文本
    report_text = generate_report_text(metrics)
    with open(f'{output_dir}/report.txt', 'w') as f:
        f.write(report_text)


def generate_report_text(metrics):
    """生成详细的报告文本"""
    report = "实验结果报告\n\n"
    report += f"Gini系数: {metrics['gini_coefficient']}\n"
    report += f"HHI指数: {metrics['hhi_index']}\n"
    report += f"Top 10份额: {metrics['top_10_share']}\n"
    report += f"消费者剩余: {metrics['consumer_surplus']}\n"
    report += f"生产者剩余: {metrics['producer_surplus']}\n"
    report += f"平台利润: {metrics['platform_profit']}\n"
    report += f"社会福利: {metrics['social_welfare']}\n"
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate report from simulation results')
    parser.add_argument('--input', type=str, required=True, help='Input directory containing simulation results')
    parser.add_argument('--output', type=str, required=True, help='Output directory for report')
    args = parser.parse_args()

    generate_report(args.input, args.output)