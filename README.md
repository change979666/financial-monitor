# 金融数据实时监控系统

## 项目简介
这是一个基于Python的实时金融数据监控工具，可获取现货黄金价格、美元指数(USDX)和人民币汇率等关键金融指标数据。

## 安装方法
```bash
# 克隆仓库
git clone https://github.com/yourusername/financial-monitor.git
cd financial-monitor

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，添加您的API密钥
```

## 使用方法
```python
# 运行主程序
python main.py

# 或者作为模块导入
from financial_monitor import FinancialMonitor
monitor = FinancialMonitor()
gold_price = monitor.get_gold_price()
print(f"当前金价: {gold_price} USD/oz")
```

## 功能特性
- 实时获取金融数据（黄金、美元指数、汇率）
- 数据可视化展示
- 价格预警系统
- 历史数据分析

## 项目结构
```
financial_monitor/
├── api/                # API接口模块
├── data/               # 数据存储目录
├── models/             # 数据模型
├── utils/              # 工具函数
├── visualization/      # 数据可视化模块
├── config.py           # 配置文件
└── main.py             # 主程序入口
```

## 许可证
MIT 