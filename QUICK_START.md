# 🚀 TradingAgents 快速运行指南

## ⚡ 一分钟快速开始

### 1️⃣ 配置 API 密钥（必需）
```bash
# 复制环境变量模板
make setup

# 编辑 .env 文件，填入你的 API 密钥
vim .env  # 或使用你喜欢的编辑器
```

**最少需要配置：**
```bash
FINNHUB_API_KEY=your_finnhub_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 2️⃣ 选择运行方式

## 🌐 方式一：WebUI（推荐新手）

**最简单的图形界面方式！**

```bash
# 启动 WebUI
make webui

# 访问 http://localhost:8000
```

✨ **WebUI 特点：**
- 🎨 现代化聊天界面
- 📱 手机/平板友好
- 🤖 智能对话交互
- 📊 实时分析进度
- 💾 自动保存结果

## 💻 方式二：命令行 CLI

**适合熟悉命令行的用户**

```bash
# 启动交互式 CLI
make cli
```

✨ **CLI 特点：**
- 🖥️ 丰富的终端界面
- 📈 实时进度显示
- ⚡ 更快的响应速度
- 🎛️ 更多配置选项

## 📓 方式三：Jupyter Notebook

**适合开发和实验**

```bash
# 启动 Jupyter
make jupyter

# 访问 http://localhost:8888
```

✨ **Jupyter 特点：**
- 🔬 交互式开发环境
- 📝 支持代码和文档
- 🧪 适合实验和调试
- 📊 数据可视化友好

---

## 🎯 使用示例

### WebUI 使用方法
1. 打开 http://localhost:8000
2. 直接输入股票代码，如：`AAPL`, `TSLA`, `NVDA`
3. 等待 AI 分析师团队完成分析
4. 查看详细的投资建议报告

### CLI 使用方法
1. 运行 `make cli`
2. 按提示选择股票代码、日期、分析师等
3. 观看实时分析进度
4. 查看最终分析报告

### Python 脚本方法
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 初始化
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 分析股票
_, decision = ta.propagate("AAPL", "2024-01-15")
print(decision)
```

---

## 🔑 获取免费 API 密钥

### FinnHub（金融数据）- 必需
- 🆓 **免费额度**：每分钟 60 次请求
- 🔗 **注册地址**：https://finnhub.io/register
- 📋 **使用场景**：股价、财务数据、新闻

### OpenAI（推荐）- 选一个
- 💰 **费用**：按使用量付费，首次送 $5 额度
- 🔗 **注册地址**：https://platform.openai.com/api-keys
- 🤖 **模型**：GPT-4o、GPT-4o-mini

### Google AI（免费额度大）- 选一个
- 🆓 **免费额度**：每分钟 15 次请求，每天 1500 次
- 🔗 **注册地址**：https://aistudio.google.com/app/apikey
- 🤖 **模型**：Gemini 2.0 Flash

### Anthropic Claude（质量高）- 选一个
- 💰 **费用**：按使用量付费，首次送 $5 额度
- 🔗 **注册地址**：https://console.anthropic.com/settings/keys
- 🤖 **模型**：Claude 3.5 Sonnet

---

## 🛠️ 管理命令

```bash
# 查看所有命令
make help

# 查看服务状态
make status

# 查看日志
make logs

# 停止服务
make stop

# 清理资源
make clean
```

---

## ❓ 常见问题

### Q: API 密钥错误怎么办？
A: 检查 `.env` 文件中的密钥是否正确，确保没有多余的空格或引号。

### Q: 分析很慢怎么办？
A: 这是正常的，AI 需要调用多个数据源和进行深度分析。通常需要 2-5 分钟。

### Q: 可以分析哪些股票？
A: 支持美股主要股票，如 AAPL、TSLA、NVDA、GOOGL、MSFT、SPY 等。

### Q: 分析结果保存在哪里？
A: 保存在 `./results/股票代码/日期/` 目录下。

### Q: 如何更新到最新版本？
A: 运行 `make update` 重新构建镜像。

---

## ⚠️ 重要提示

1. **仅供研究**：本工具仅用于学术研究，不构成投资建议
2. **风险自担**：投资有风险，决策需谨慎
3. **API 费用**：注意 API 调用可能产生费用
4. **数据延迟**：市场数据可能有延迟

---

## 🎉 开始使用

选择你喜欢的方式，开始你的 AI 投资分析之旅吧！

```bash
# 🌐 WebUI（推荐新手）
make webui
# 然后访问 http://localhost:8000

# 💻 CLI（推荐进阶用户）  
make cli

# 📓 Jupyter（推荐开发者）
make jupyter
# 然后访问 http://localhost:8888
```

**祝你投资顺利！** 📈💰