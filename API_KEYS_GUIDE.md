# 🔑 API 密钥配置指南

## 必需的 API 密钥

### 1. 📊 FinnHub API Key（必需 - 金融数据）
- **作用**：获取股票价格、财务数据、新闻等
- **费用**：免费版每分钟 60 次请求，足够使用
- **获取步骤**：
  1. 访问：https://finnhub.io/register
  2. 免费注册账号
  3. 登录后在 Dashboard 找到 API Key
  4. 复制密钥到 .env 文件

### 2. 🤖 LLM API Key（至少选择一个）

#### 选项1：OpenAI（推荐）
- **作用**：AI 分析和决策
- **费用**：按使用量付费，新用户送 $5
- **获取步骤**：
  1. 访问：https://platform.openai.com/api-keys
  2. 注册 OpenAI 账号
  3. 创建新的 API Key
  4. 复制密钥到 .env 文件

#### 选项2：Google AI（免费额度大）
- **作用**：AI 分析和决策
- **费用**：免费版每分钟 15 次，每天 1500 次
- **获取步骤**：
  1. 访问：https://aistudio.google.com/app/apikey
  2. 登录 Google 账号
  3. 创建 API Key
  4. 复制密钥到 .env 文件

#### 选项3：Anthropic Claude
- **作用**：AI 分析和决策
- **费用**：按使用量付费，新用户送 $5
- **获取步骤**：
  1. 访问：https://console.anthropic.com/settings/keys
  2. 注册 Anthropic 账号
  3. 创建 API Key
  4. 复制密钥到 .env 文件

## 📝 配置步骤

### 1. 编辑 .env 文件
```bash
vim .env
# 或者使用任何文本编辑器
```

### 2. 替换模板值
将以下内容：
```bash
FINNHUB_API_KEY=your_finnhub_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

替换为真实的密钥：
```bash
FINNHUB_API_KEY=ck1234567890abcdef  # 你的实际 FinnHub 密钥
OPENAI_API_KEY=sk-1234567890abcdef  # 你的实际 OpenAI 密钥
```

### 3. 重启服务
```bash
make stop
make webui
```

## 💡 推荐配置

**最经济的配置：**
```bash
FINNHUB_API_KEY=你的FinnHub密钥（免费）
GOOGLE_API_KEY=你的Google密钥（免费额度大）
```

**最稳定的配置：**
```bash
FINNHUB_API_KEY=你的FinnHub密钥（免费）
OPENAI_API_KEY=你的OpenAI密钥（付费但稳定）
```

## 🚀 配置完成后

1. 重启 WebUI：`make stop && make webui`
2. 访问：http://localhost:8000
3. 输入股票代码测试，如：`AAPL`
4. 等待 AI 分析师团队分析

## 💰 费用估算

- **FinnHub**：免费
- **Google AI**：免费额度，每天可分析 10-20 只股票
- **OpenAI**：约 $0.1-0.5 每次分析（取决于复杂度）
- **Anthropic**：约 $0.1-0.3 每次分析

## ❓ 常见问题

**Q: 我只有 FinnHub 密钥，没有 LLM 密钥怎么办？**
A: 必须至少配置一个 LLM 密钥，推荐先用 Google AI（免费）。

**Q: 配置了密钥但还是报错？**
A: 检查密钥格式是否正确，确保没有多余空格，重启服务。

**Q: 想换不同的 LLM 怎么办？**
A: 编辑 .env 文件，配置对应的密钥即可，支持同时配置多个。