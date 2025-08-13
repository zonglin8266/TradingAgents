# FinnHub 功能调用详解

## 📋 概述

TradingAgents 系统中的 FinnHub 集成主要用于获取金融数据，包括公司新闻、内部人士交易和情绪数据。系统采用**离线缓存模式**，预先下载并存储 FinnHub 数据，而不是实时 API 调用。

## 🔧 实现架构

### 数据流程
```
FinnHub API → 数据预处理 → 本地缓存 → TradingAgents 调用
```

### 核心组件
1. **finnhub_utils.py**: 数据读取工具
2. **interface.py**: 数据接口层
3. **agent_utils.py**: 智能体工具包装

## 📊 调用的 FinnHub 功能

### 1. 公司新闻 (Company News)
**功能**: `get_finnhub_news()`
**FinnHub API 端点**: `/api/v1/company-news`

**调用参数**:
- `ticker`: 股票代码 (如 AAPL, TSLA)
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)

**返回数据结构**:
```json
{
  "2024-01-15": [
    {
      "headline": "Apple Reports Strong Q4 Results",
      "summary": "Apple Inc. reported better-than-expected...",
      "url": "https://...",
      "source": "Reuters",
      "datetime": 1705334400
    }
  ]
}
```

**使用场景**:
- 新闻分析师获取公司相关新闻
- 分析市场事件对股价的影响

### 2. 内部人士情绪 (Insider Sentiment)
**功能**: `get_finnhub_company_insider_sentiment()`
**FinnHub API 端点**: `/api/v1/stock/insider-sentiment`

**调用参数**:
- `ticker`: 股票代码
- `curr_date`: 当前日期
- `look_back_days`: 回看天数 (默认30天)

**返回数据结构**:
```json
{
  "2024-01-15": [
    {
      "year": 2024,
      "month": 1,
      "change": 15000,
      "mspr": 0.85
    }
  ]
}
```

**字段说明**:
- `change`: 内部人士净买卖变化
- `mspr`: 月度股份购买比率 (Monthly Share Purchase Ratio)

**使用场景**:
- 基本面分析师评估内部人士信心
- 判断公司内部对股票前景的看法

### 3. 内部人士交易 (Insider Transactions)
**功能**: `get_finnhub_company_insider_transactions()`
**FinnHub API 端点**: `/api/v1/stock/insider-transactions`

**调用参数**:
- `ticker`: 股票代码
- `curr_date`: 当前日期
- `look_back_days`: 回看天数 (默认30天)

**返回数据结构**:
```json
{
  "2024-01-15": [
    {
      "filingDate": "2024-01-15",
      "name": "John Smith",
      "change": -5000,
      "share": 10000,
      "transactionPrice": 150.25,
      "transactionCode": "S",
      "transactionDate": "2024-01-14"
    }
  ]
}
```

**字段说明**:
- `change`: 持股变化数量 (负数表示卖出)
- `share`: 交易股份总数
- `transactionPrice`: 交易价格
- `transactionCode`: 交易类型 (S=卖出, P=购买)
- `name`: 内部人士姓名
- `filingDate`: 申报日期

**使用场景**:
- 基本面分析师追踪内部人士交易行为
- 识别重要的买卖信号

## 🏗️ 技术实现

### 1. 数据缓存机制

**缓存目录结构**:
```
data_dir/
└── finnhub_data/
    ├── news_data/
    │   └── AAPL_data_formatted.json
    ├── insider_senti/
    │   └── AAPL_data_formatted.json
    └── insider_trans/
        └── AAPL_data_formatted.json
```

### 2. 核心实现代码

#### finnhub_utils.py
```python
def get_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    从本地缓存读取 FinnHub 数据
    
    Args:
        ticker: 股票代码
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        data_type: 数据类型 (news_data, insider_senti, insider_trans)
        data_dir: 数据目录
        period: 周期 (annual/quarterly, 可选)
    
    Returns:
        dict: 过滤后的数据
    """
    # 构建文件路径
    if period:
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, 
            f"{ticker}_{period}_data_formatted.json"
        )
    else:
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, 
            f"{ticker}_data_formatted.json"
        )
    
    # 读取并过滤数据
    with open(data_path, "r") as f:
        data = json.load(f)
    
    # 按日期范围过滤
    filtered_data = {}
    for key, value in data.items():
        if start_date <= key <= end_date and len(value) > 0:
            filtered_data[key] = value
    
    return filtered_data
```

#### interface.py 实现示例
```python
def get_finnhub_news(ticker, curr_date, look_back_days):
    """获取公司新闻"""
    # 计算日期范围
    start_date = datetime.strptime(curr_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")
    
    # 从缓存读取数据
    result = get_data_in_range(ticker, before, curr_date, "news_data", DATA_DIR)
    
    if len(result) == 0:
        return ""
    
    # 格式化输出
    combined_result = ""
    for day, data in result.items():
        for entry in data:
            current_news = f"### {entry['headline']} ({day})\n{entry['summary']}"
            combined_result += current_news + "\n\n"
    
    return f"## {ticker} News, from {before} to {curr_date}:\n{combined_result}"
```

### 3. 智能体工具包装

#### agent_utils.py
```python
@tool
def get_finnhub_news(ticker, start_date, end_date):
    """
    智能体工具：获取 FinnHub 新闻
    """
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    look_back_days = (end_date_obj - start_date_obj).days
    
    return interface.get_finnhub_news(ticker, end_date, look_back_days)

@tool
def get_finnhub_company_insider_sentiment(ticker, curr_date):
    """
    智能体工具：获取内部人士情绪
    """
    return interface.get_finnhub_company_insider_sentiment(ticker, curr_date, 30)

@tool
def get_finnhub_company_insider_transactions(ticker, curr_date):
    """
    智能体工具：获取内部人士交易
    """
    return interface.get_finnhub_company_insider_transactions(ticker, curr_date, 30)
```

## 🔑 API 密钥配置

### 环境变量设置
```bash
# .env 文件
FINNHUB_API_KEY=your_finnhub_api_key_here
```

### 获取 API 密钥
1. 访问: https://finnhub.io/register
2. 免费注册账号
3. 在 Dashboard 获取 API Key
4. 免费版限制: 每分钟 60 次请求

## 📈 使用场景映射

### 新闻分析师 (News Analyst)
- **使用功能**: `get_finnhub_news()`
- **分析内容**: 公司公告、行业新闻、市场事件
- **输出**: 新闻摘要和影响分析

### 基本面分析师 (Fundamentals Analyst)
- **使用功能**: 
  - `get_finnhub_company_insider_sentiment()`
  - `get_finnhub_company_insider_transactions()`
- **分析内容**: 内部人士交易行为、管理层信心
- **输出**: 基本面健康度评估

## 🚀 数据预处理流程

### 1. 数据获取 (离线进行)
```python
# 伪代码：数据预处理脚本
import finnhub

client = finnhub.Client(api_key="YOUR_API_KEY")

# 获取公司新闻
news = client.company_news(symbol, _from=start_date, to=end_date)

# 获取内部人士情绪
sentiment = client.stock_insider_sentiment(symbol, _from=start_date, to=end_date)

# 获取内部人士交易
transactions = client.stock_insider_transactions(symbol, _from=start_date, to=end_date)
```

### 2. 数据格式化和存储
- 按日期组织数据结构
- 转换为标准 JSON 格式
- 存储到本地缓存目录

### 3. 实时调用
- 智能体通过工具接口调用
- 从本地缓存快速读取
- 按需过滤和格式化

## ⚠️ 注意事项

1. **离线模式**: 当前实现使用预缓存数据，不进行实时 API 调用
2. **数据更新**: 需要定期更新缓存数据以获取最新信息
3. **API 限制**: 免费版 FinnHub 有请求频率限制
4. **数据完整性**: 缓存数据的时间范围可能有限

## 🔄 扩展建议

1. **实时模式**: 添加在线 API 调用选项
2. **数据更新**: 实现自动数据更新机制
3. **更多端点**: 集成更多 FinnHub API 功能
4. **错误处理**: 增强 API 调用的错误处理和重试机制

这个文档详细说明了 TradingAgents 系统中 FinnHub 的集成方式和具体实现。系统主要使用离线缓存模式来提高性能和降低 API 调用成本。
