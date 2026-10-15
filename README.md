# 金融数据实时监控系统（历史原型 / 未完成）

这是一个保留了部分金融数据采集与可视化代码的 Python 项目脚手架，方向包括现货黄金、美元指数（USDX）和汇率数据。

> **当前状态：不能按现有 README 直接运行。** 经检查，`financial_monitor/main.py` 引用了仓库中不存在的 `financial_monitor/utils/logger.py` 和 `financial_monitor/utils/config.py`；仓库也没有根目录 `main.py` 或 README 曾提及的 `.env.example`。本仓库仅作为历史源码归档，不代表已完成或经过端到端验证的金融数据服务。

## 仓库内容

- `financial_monitor/api/`：部分金融数据 API 适配模块
- `financial_monitor/models/`：监控模型
- `financial_monitor/visualization/`：图表相关代码
- `financial_monitor/main.py`：命令行入口草稿
- `financial_monitor/config.example.json`：配置示例
- `requirements.txt`：Python 依赖清单

## 获取源码

```bash
git clone https://github.com/change979666/financial-monitor.git
cd financial-monitor
```

目前不提供可验证的快速运行步骤。若要继续开发，需要先恢复缺失的配置与日志模块、核对各数据源 API 的可用性和认证要求，再补充自动化测试。

## 配置与依赖（预期设计，当前不可运行）

以下为代码中预留/计划的用法，并非当前可直接执行的命令：

- **API Key**：按 `financial_monitor/models/financial_monitor.py` 的设计，密钥优先级为 `--api-key` 命令行参数 → 配置文件 `api_key` 字段 → 环境变量 `FINANCIAL_API_KEY`（均不硬编码进仓库）。
- **配置文件**：`financial_monitor/config.example.json` 仅为示例，其中 `api_key`、邮箱 `username/password` 等都是占位符；请勿把真实凭据填进去后提交。
- **依赖**：`requirements.txt` 列出 `requests / pandas / numpy / matplotlib / plotly / aiohttp / APScheduler / python-dotenv`。即使 `pip install -r requirements.txt` 成功，由于 `utils/logger.py`、`utils/config.py` 缺失，入口仍会在 import 阶段失败（`ModuleNotFoundError`）。

## 数据与使用边界

金融数据的来源、延迟、字段口径和 API 可用性需要单独验证。本项目不提供投资建议，不应将未经校验的数据直接用于交易或自动决策。

## License & Attribution / 许可与来源

Original project code authored for this repository is released under the MIT License; see [LICENSE](./LICENSE).

When reusing or redistributing a substantial portion, retain the LICENSE and its copyright notice. The copyright notice includes this original source URL: https://github.com/change979666/financial-monitor. Please keep the source link visible in your redistributed source or project documentation.

This license applies only to original material that the repository maintainer has the right to license. Third-party libraries, vendor code, platform SDKs, trademarks, screenshots, icons, fonts, and other external assets remain subject to their respective licenses and terms. Review those terms before reuse.

**Project status:** personal/archived project, shared as-is. Maintenance, compatibility, and production readiness are not guaranteed.