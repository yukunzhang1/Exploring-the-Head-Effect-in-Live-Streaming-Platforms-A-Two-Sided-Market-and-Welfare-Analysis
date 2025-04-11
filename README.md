# Exploring-the-Head-Effect-in-Live-Streaming-Platforms-A-Two-Sided-Market-and-Welfare-Analysis
Exploring the Head Effect in Live Streaming Platforms: A Two-Sided Market and Welfare Analysis


```TEXT
live-stream-sim/
├── agents/
│   ├── broadcaster.py    # 主播模型
│   └── viewer.py         # 观众模型
├── platform/
│   ├── policy_engine.py  # 政策干预模块
│   └── recommendation.py # 推荐算法
├── simulation/
│   ├── core.py           # 核心模拟引擎
│   ├── metrics.py        # 指标计算
│   └── config_loader.py  # 配置加载
├── analysis/
│   ├── visualize.py      # 可视化模块
│   └── reporter.py       # 报告生成
├── experiments/
│   ├── comparative.py    # 对比实验
│   └── sensitivity.py    # 敏感性分析
├── configs/
│   └── base.yaml         # 基础配置
└── utils/
    └── economics.py      # 经济指标工具
```

```bash
pip install -r requirements.txt
python experiments/comparative.py
python experiments/sensitivity.py --param network_effect_beta --range 0.1 0.2 --steps 5
python analysis/reporter.py --input results/exp1/ --output report/
```