# TradingAgents Docker 部署指南

这个指南将帮助你使用 Docker 部署 TradingAgents 项目，确保所有功能都可以正常使用。

## 🚀 快速开始

### 1. 准备 API 密钥

在开始之前，你需要获取以下 API 密钥：

#### 必需的 API 密钥：
- **FinnHub API Key**: 用于获取金融数据
  - 免费注册：https://finnhub.io/register
  - 免费版本已足够使用

#### LLM API 密钥（至少需要一个）：
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **Google AI API Key**: https://aistudio.google.com/app/apikey  
- **Anthropic API Key**: https://console.anthropic.com/settings/keys

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，填入你的 API 密钥
vim .env
```

最少需要配置：
```bash
FINNHUB_API_KEY=your_finnhub_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 构建和运行

#### 方式一：使用 Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d --build

# 查看日志
docker-compose logs -f tradingagents

# 停止服务
docker-compose down
```

#### 方式二：使用 Docker 命令

```bash
# 构建镜像
docker build -t tradingagents .

# 运行容器（交互式 CLI）
docker run -it --rm \
  --env-file .env \
  -v $(pwd)/results:/app/results \
  tradingagents cli

# 运行 Python 脚本
docker run -it --rm \
  --env-file .env \
  -v $(pwd)/results:/app/results \
  tradingagents python main.py
```

## 📋 可用的服务

### 主要服务

1. **TradingAgents CLI**: 交互式命令行界面
   ```bash
   docker-compose up tradingagents
   ```

2. **Redis**: 缓存服务（自动启动）
   - 端口：6379
   - 用于缓存数据以提高性能

### 可选服务

3. **Jupyter Notebook**: 开发环境（可选）
   ```bash
   docker-compose --profile jupyter up
   ```
   - 访问：http://localhost:8888
   - 无需密码或令牌

## 🎯 使用示例

### CLI 交互模式

```bash
# 启动交互式 CLI
docker-compose up tradingagents

# 或者直接运行分析
docker-compose run --rm tradingagents python -m cli.main analyze
```

### 编程模式

创建一个 Python 脚本 `my_analysis.py`：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 创建自定义配置
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 2
config["online_tools"] = True

# 初始化交易代理图
ta = TradingAgentsGraph(debug=True, config=config)

# 运行分析
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

运行脚本：
```bash
docker-compose run --rm tradingagents python my_analysis.py
```

## 🔧 配置选项

### 环境变量配置

在 `.env` 文件中可以配置以下选项：

```bash
# LLM 提供商选择
LLM_PROVIDER=openai  # openai, google, anthropic

# 模型选择
OPENAI_MODEL_DEEP=o4-mini
OPENAI_MODEL_QUICK=gpt-4o-mini

# 研究深度
MAX_DEBATE_ROUNDS=1
MAX_RISK_DISCUSS_ROUNDS=1

# 在线工具
ONLINE_TOOLS=true

# 调试模式
DEBUG=true
```

### 数据持久化

以下目录会被持久化到宿主机：

- `./results`: 分析结果
- `./data_cache`: 数据缓存
- `redis_data`: Redis 数据（Docker volume）

## 🛠️ 故障排除

### 常见问题

1. **API 密钥错误**
   ```
   ERROR: Missing required environment variables
   ```
   - 检查 `.env` 文件是否存在且包含正确的 API 密钥

2. **权限问题**
   ```bash
   # 确保脚本有执行权限
   chmod +x docker-entrypoint.sh
   ```

3. **端口冲突**
   ```bash
   # 修改 docker-compose.yml 中的端口映射
   ports:
     - "8001:8000"  # 改为其他端口
   ```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs tradingagents
docker-compose logs redis

# 实时查看日志
docker-compose logs -f tradingagents
```

### 进入容器调试

```bash
# 进入运行中的容器
docker-compose exec tradingagents bash

# 或者启动一个新的调试容器
docker-compose run --rm tradingagents bash
```

## 📊 性能优化

### 1. 缓存配置

Redis 缓存已配置，可以显著提高重复查询的性能。

### 2. 资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  tradingagents:
    # ... 其他配置
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 3. 并行处理

通过配置文件调整并行度：

```python
config["max_debate_rounds"] = 2  # 增加辩论轮数
config["online_tools"] = True    # 启用在线工具
```

## 🔒 安全注意事项

1. **API 密钥安全**
   - 不要将 `.env` 文件提交到版本控制
   - 使用环境变量或密钥管理服务

2. **网络安全**
   - 默认配置仅允许本地访问
   - 生产环境请配置适当的防火墙规则

3. **数据安全**
   - 分析结果可能包含敏感信息
   - 确保适当的访问控制

## 📈 监控和维护

### 健康检查

Docker Compose 已配置健康检查：

```bash
# 查看服务状态
docker-compose ps

# 查看健康状态
docker inspect tradingagents_tradingagents_1 | grep -A 5 Health
```

### 日志轮转

建议配置日志轮转以防止磁盘空间不足：

```yaml
services:
  tradingagents:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🎯 下一步

1. 阅读原项目文档了解更多功能
2. 尝试不同的股票符号和日期
3. 调整配置以适应你的需求
4. 集成到你的交易工作流中

## 📞 支持

如果遇到问题，请：

1. 检查日志输出
2. 确认 API 密钥有效
3. 查看 GitHub Issues
4. 提交新的 Issue

---

**注意**: TradingAgents 仅用于研究目的，不构成投资建议。请谨慎使用并承担相应风险。