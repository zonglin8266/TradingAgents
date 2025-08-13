# TradingAgents 智能体系统分析

## 📋 系统概述

TradingAgents 是一个多智能体协作的股票分析系统，模拟真实交易公司的组织架构。系统包含 **12个专业智能体**，分为4个层级，通过协作和辩论来制定投资决策。

## 🏗️ 系统架构

```
第一层：数据分析师团队 (4个智能体)
    ├── 市场分析师 (Market Analyst)
    ├── 社交媒体分析师 (Social Media Analyst)  
    ├── 新闻分析师 (News Analyst)
    └── 基本面分析师 (Fundamentals Analyst)

第二层：研究团队 (3个智能体)
    ├── 多头研究员 (Bull Researcher)
    ├── 空头研究员 (Bear Researcher)
    └── 研究经理 (Research Manager)

第三层：交易团队 (1个智能体)
    └── 交易员 (Trader)

第四层：风险管理团队 (4个智能体)
    ├── 激进风险分析师 (Risky Debator)
    ├── 保守风险分析师 (Conservative Debator)
    ├── 中性风险分析师 (Neutral Debator)
    └── 风险经理 (Risk Manager)
```

## 🔍 智能体详细分析

### 第一层：数据分析师团队

#### 1. 市场分析师 (Market Analyst)
**文件位置**: `tradingagents/agents/analysts/market_analyst.py`

**核心职责**:
- 技术指标分析
- 价格趋势分析
- 成交量分析

**主要提示词**:
```
You are a trading assistant tasked with analyzing financial markets. Your role is to select the **most relevant indicators** for a given market condition or trading strategy from the following list. The goal is to choose up to **8 indicators** that provide complementary insights without redundancy.

Categories and each category's indicators are:

Moving Averages:
- close_50_sma: 50 SMA: A medium-term trend indicator
- close_200_sma: 200 SMA: A long-term trend benchmark  
- close_10_ema: 10 EMA: A responsive short-term average

[详细的技术指标说明...]
```

**可用工具**:
- `get_YFin_data_online` / `get_YFin_data`: 获取Yahoo Finance数据
- `get_stockstats_indicators_report_online` / `get_stockstats_indicators_report`: 获取技术指标报告

#### 2. 社交媒体分析师 (Social Media Analyst)
**文件位置**: `tradingagents/agents/analysts/social_media_analyst.py`

**核心职责**:
- 社交媒体情绪分析
- 公司相关新闻分析
- 公众情绪评估

**主要提示词**:
```
You are a social media and company specific news researcher/analyst tasked with analyzing social media posts, recent company news, and public sentiment for a specific company over the past week. 

Your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on this company's current state after looking at social media and what people are saying about that company, analyzing sentiment data of what people feel each day about the company, and looking at recent company news.

IMPORTANT: Please provide your entire social media and sentiment analysis report in Chinese (中文).
```

**可用工具**:
- `get_stock_news_openai`: 获取股票相关新闻
- `get_reddit_stock_info`: 获取Reddit股票信息

#### 3. 新闻分析师 (News Analyst)
**文件位置**: `tradingagents/agents/analysts/news_analyst.py`

**核心职责**:
- 全球新闻分析
- 宏观经济事件评估
- 行业趋势分析

**主要提示词**:
```
You are a news researcher tasked with analyzing recent news and trends over the past week. Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. 

Look at news from EODHD, and finnhub to be comprehensive. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions.

Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read.
```

**可用工具**:
- `get_global_news_openai`: 获取全球新闻
- `get_google_news`: 获取Google新闻
- `get_finnhub_news`: 获取Finnhub新闻
- `get_reddit_news`: 获取Reddit新闻

#### 4. 基本面分析师 (Fundamentals Analyst)
**文件位置**: `tradingagents/agents/analysts/fundamentals_analyst.py`

**核心职责**:
- 财务报表分析
- 公司基本面评估
- 内部人士情绪分析

**主要提示词**:
```
You are a researcher tasked with analyzing fundamental information over the past week about a company. Please write a comprehensive report of the company's fundamental information such as financial documents, company profile, basic company financials, company financial history, insider sentiment and insider transactions to gain a full view of the company's fundamental information to inform traders.

Make sure to include as much detail as possible. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions.

Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read.
```

**可用工具**:
- `get_fundamentals_openai`: 获取基本面数据
- `get_finnhub_company_insider_sentiment`: 获取内部人士情绪
- `get_finnhub_company_insider_transactions`: 获取内部人士交易
- `get_simfin_balance_sheet`: 获取资产负债表
- `get_simfin_cashflow`: 获取现金流量表
- `get_simfin_income_stmt`: 获取损益表

### 第二层：研究团队

#### 5. 多头研究员 (Bull Researcher)
**文件位置**: `tradingagents/agents/researchers/bull_researcher.py`

**核心职责**:
- 寻找看涨因素
- 反驳空头观点
- 强调增长潜力

**主要提示词**:
```
You are a Bull Analyst advocating for investing in the stock. Your task is to build a strong, evidence-based case emphasizing growth potential, competitive advantages, and positive market indicators.

Key points to focus on:
- Growth Potential: Highlight the company's market opportunities, revenue projections, and scalability
- Competitive Advantages: Emphasize factors like unique products, strong branding, or dominant market positioning
- Positive Indicators: Use financial health, industry trends, and recent positive news as evidence
- Bear Counterpoints: Critically analyze the bear argument with specific data and sound reasoning
- Engagement: Present your argument in a conversational style, engaging directly with the bear analyst's points

IMPORTANT: Please provide your entire bull analysis and argument in Chinese (中文).
```

#### 6. 空头研究员 (Bear Researcher)
**文件位置**: `tradingagents/agents/researchers/bear_researcher.py`

**核心职责**:
- 识别风险因素
- 反驳多头观点
- 强调潜在威胁

**主要提示词**:
```
You are a Bear Analyst making the case against investing in the stock. Your goal is to present a well-reasoned argument emphasizing risks, challenges, and negative indicators.

Key points to focus on:
- Risks and Challenges: Highlight factors like market saturation, financial instability, or macroeconomic threats
- Competitive Weaknesses: Emphasize vulnerabilities such as weaker market positioning, declining innovation
- Negative Indicators: Use evidence from financial data, market trends, or recent adverse news
- Bull Counterpoints: Critically analyze the bull argument with specific data and sound reasoning
- Engagement: Present your argument in a conversational style, directly engaging with the bull analyst's points

IMPORTANT: Please provide your entire bear analysis and argument in Chinese (中文).
```

#### 7. 研究经理 (Research Manager)
**文件位置**: `tradingagents/agents/managers/research_manager.py`

**核心职责**:
- 评估多空辩论
- 制定投资计划
- 做出最终研究决策

**主要提示词**:
```
As the portfolio manager and debate facilitator, your role is to critically evaluate this round of debate and make a definitive decision: align with the bear analyst, the bull analyst, or choose Hold only if it is strongly justified based on the arguments presented.

Your recommendation—Buy, Sell, or Hold—must be clear and actionable. Avoid defaulting to Hold simply because both sides have valid points; commit to a stance grounded in the debate's strongest arguments.

Additionally, develop a detailed investment plan for the trader. This should include:
- Your Recommendation: A decisive stance supported by the most convincing arguments
- Rationale: An explanation of why these arguments lead to your conclusion  
- Strategic Actions: Concrete steps for implementing the recommendation

IMPORTANT: Please provide your entire research management decision and analysis in Chinese (中文).
```

### 第三层：交易团队

#### 8. 交易员 (Trader)
**文件位置**: `tradingagents/agents/trader/trader.py`

**核心职责**:
- 执行交易决策
- 制定具体交易策略
- 提供最终交易建议

**主要提示词**:
```
You are a trading agent analyzing market data to make investment decisions. Based on your analysis, provide a specific recommendation to buy, sell, or hold. 

End with a firm decision and always conclude your response with 'FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**' to confirm your recommendation. 

Do not forget to utilize lessons from past decisions to learn from your mistakes.

IMPORTANT: Please provide your entire trading analysis and decision in Chinese (中文). All market analysis, investment rationale, trading strategy, and decision explanation should be written in Chinese. However, keep the final decision format in English: 'FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**'
```

### 第四层：风险管理团队

#### 9. 激进风险分析师 (Risky Debator)
**文件位置**: `tradingagents/agents/risk_mgmt/aggresive_debator.py`

**核心职责**:
- 倡导高风险高回报策略
- 强调增长机会
- 质疑保守观点

**主要提示词**:
```
As the Risky Risk Analyst, your role is to actively champion high-reward, high-risk opportunities, emphasizing bold strategies and competitive advantages. When evaluating the trader's decision or plan, focus intently on the potential upside, growth potential, and innovative benefits—even when these come with elevated risk.

Specifically, respond directly to each point made by the conservative and neutral analysts, countering with data-driven rebuttals and persuasive reasoning. Highlight where their caution might miss critical opportunities or where their assumptions may be overly conservative.

Engage actively by addressing any specific concerns raised, refuting the weaknesses in their logic, and asserting the benefits of risk-taking to outpace market norms.
```

#### 10. 保守风险分析师 (Conservative Debator)
**文件位置**: `tradingagents/agents/risk_mgmt/conservative_debator.py`

**核心职责**:
- 保护资产安全
- 最小化波动性
- 强调稳定增长

**主要提示词**:
```
As the Safe/Conservative Risk Analyst, your primary objective is to protect assets, minimize volatility, and ensure steady, reliable growth. You prioritize stability, security, and risk mitigation, carefully assessing potential losses, economic downturns, and market volatility.

When evaluating the trader's decision or plan, critically examine high-risk elements, pointing out where the decision may expose the firm to undue risk and where more cautious alternatives could secure long-term gains.

Your task is to actively counter the arguments of the Risky and Neutral Analysts, highlighting where their views may overlook potential threats or fail to prioritize sustainability.
```

#### 11. 中性风险分析师 (Neutral Debator)
**文件位置**: `tradingagents/agents/risk_mgmt/neutral_debator.py`

**核心职责**:
- 提供平衡观点
- 权衡利弊
- 倡导适度风险策略

**主要提示词**:
```
As the Neutral Risk Analyst, your role is to provide a balanced perspective, weighing both the potential benefits and risks of the trader's decision or plan. You prioritize a well-rounded approach, evaluating the upsides and downsides while factoring in broader market trends, potential economic shifts, and diversification strategies.

Your task is to challenge both the Risky and Safe Analysts, pointing out where each perspective may be overly optimistic or overly cautious.

Engage actively by analyzing both sides critically, addressing weaknesses in the risky and conservative arguments to advocate for a more balanced approach.
```

#### 12. 风险经理 (Risk Manager)
**文件位置**: `tradingagents/agents/managers/risk_manager.py`

**核心职责**:
- 评估风险辩论
- 调整交易计划
- 做出最终风险决策

**主要提示词**:
```
As the Risk Management Judge and Debate Facilitator, your goal is to evaluate the debate between three risk analysts—Risky, Neutral, and Safe/Conservative—and determine the best course of action for the trader. Your decision must result in a clear recommendation: Buy, Sell, or Hold.

Guidelines for Decision-Making:
1. Summarize Key Arguments: Extract the strongest points from each analyst
2. Provide Rationale: Support your recommendation with direct quotes and counterarguments
3. Refine the Trader's Plan: Start with the trader's original plan and adjust it based on analysts' insights
4. Learn from Past Mistakes: Use lessons from past experiences to improve decision-making

IMPORTANT: Please provide your entire risk management analysis and decision in Chinese (中文).
```

## 🔄 工作流程

1. **并行分析阶段**: 4个分析师同时工作，收集不同维度的数据
2. **研究辩论阶段**: 多头和空头研究员进行辩论，研究经理做出决策
3. **交易执行阶段**: 交易员基于研究结果制定具体交易策略
4. **风险评估阶段**: 3个风险分析师辩论，风险经理做出最终调整

## 🎯 系统特点

- **多维度分析**: 技术面、基本面、新闻面、情绪面全覆盖
- **辩论机制**: 通过多轮辩论确保决策质量
- **记忆学习**: 每个智能体都有记忆系统，能从历史经验中学习
- **中文输出**: 所有分析报告都使用中文，便于中文用户理解
- **工具集成**: 集成多种数据源和分析工具

## 📊 配置参数

- `max_debate_rounds`: 最大辩论轮数 (默认: 1)
- `max_risk_discuss_rounds`: 最大风险讨论轮数 (默认: 1)
- `online_tools`: 是否使用在线工具 (默认: true)
- `output_language`: 输出语言 (默认: chinese)

## 📊 数据源详细分析

### 数据源概览

TradingAgents 系统集成了多个专业的金融数据源，为各个智能体提供全面的市场信息：

#### 🏢 主要数据提供商

1. **Yahoo Finance (YFinance)**
   - 股价数据、技术指标
   - 公司基本信息、财务报表
   - 分析师建议、股息信息

2. **FinnHub API**
   - 公司新闻、内部人士情绪
   - 内部人士交易、SEC文件
   - 财务数据

3. **SimFin**
   - 标准化财务报表
   - 资产负债表、现金流量表
   - 损益表

4. **Reddit**
   - 社交媒体情绪
   - 散户投资者讨论
   - 热门股票话题

5. **Google News**
   - 全球新闻资讯
   - 公司相关新闻
   - 宏观经济新闻

6. **OpenAI API**
   - 智能新闻分析
   - 基本面数据整合
   - 全球宏观经济分析

### 各智能体数据源映射

#### 🔍 市场分析师 (Market Analyst)
**数据来源**:
- **Yahoo Finance**: 股价历史数据 (`get_YFin_data`)
- **StockStats**: 技术指标计算 (`get_stockstats_indicators_report`)

**具体数据**:
- OHLCV价格数据
- 移动平均线 (SMA, EMA)
- 技术指标 (RSI, MACD, 布林带等)
- 成交量分析
- 价格趋势分析

#### 📱 社交媒体分析师 (Social Media Analyst)
**数据来源**:
- **Reddit**: 社交媒体讨论 (`get_reddit_stock_info`)
- **OpenAI API**: 智能新闻分析 (`get_stock_news_openai`)

**具体数据**:
- Reddit热门帖子和评论
- 社交媒体情绪指标
- 散户投资者观点
- 公司相关社交媒体讨论
- 投资者情绪变化趋势

#### 📰 新闻分析师 (News Analyst)
**数据来源**:
- **FinnHub**: 公司新闻 (`get_finnhub_news`)
- **Google News**: 全球新闻 (`get_google_news`)
- **Reddit**: 新闻讨论 (`get_reddit_news`)
- **OpenAI API**: 全球宏观新闻 (`get_global_news_openai`)

**具体数据**:
- 公司公告和新闻
- 行业动态新闻
- 宏观经济新闻
- 监管政策变化
- 市场事件和趋势

#### 📈 基本面分析师 (Fundamentals Analyst)
**数据来源**:
- **FinnHub**: 内部人士数据 (`get_finnhub_company_insider_sentiment`, `get_finnhub_company_insider_transactions`)
- **SimFin**: 财务报表 (`get_simfin_balance_sheet`, `get_simfin_cashflow`, `get_simfin_income_stmt`)
- **OpenAI API**: 基本面整合分析 (`get_fundamentals_openai`)

**具体数据**:
- 资产负债表
- 损益表
- 现金流量表
- 内部人士交易记录
- 内部人士情绪指标
- 财务比率分析

### 数据获取模式

#### 🌐 在线模式 (online_tools = true)
- 实时获取最新数据
- 使用OpenAI API进行智能分析
- 数据更新及时，但API调用成本较高

**在线工具列表**:
- `get_YFin_data_online`: 实时Yahoo Finance数据
- `get_stockstats_indicators_report_online`: 实时技术指标
- `get_stock_news_openai`: OpenAI新闻分析
- `get_global_news_openai`: OpenAI全球新闻
- `get_fundamentals_openai`: OpenAI基本面分析

#### 💾 离线模式 (online_tools = false)
- 使用缓存的历史数据
- 降低API调用成本
- 适合回测和研究

**离线工具列表**:
- `get_YFin_data`: 缓存的Yahoo Finance数据
- `get_stockstats_indicators_report`: 缓存的技术指标
- `get_reddit_stock_info`: 缓存的Reddit数据
- `get_finnhub_news`: 缓存的FinnHub新闻
- `get_reddit_news`: 缓存的Reddit新闻

### 数据缓存机制

**缓存目录结构**:
```
data_cache/
├── market_data/
│   └── price_data/          # Yahoo Finance价格数据
├── finnhub_data/
│   ├── news_data/           # FinnHub新闻数据
│   ├── insider_senti/       # 内部人士情绪
│   ├── insider_trans/       # 内部人士交易
│   └── fin_as_reported/     # 财务报告
├── reddit_data/
│   ├── global_news/         # 全球新闻讨论
│   └── company_news/        # 公司相关讨论
└── google_news/             # Google新闻数据
```

### API密钥要求

**必需的API密钥**:
- `FINNHUB_API_KEY`: FinnHub数据访问
- `OPENAI_API_KEY`: OpenAI智能分析 (或其他LLM API)

**可选的API密钥**:
- `GOOGLE_API_KEY`: Google AI模型
- `ANTHROPIC_API_KEY`: Anthropic模型

### 数据更新频率

- **实时数据**: 股价、新闻 (分钟级更新)
- **日度数据**: 技术指标、社交媒体情绪
- **周度数据**: 内部人士交易
- **季度数据**: 财务报表

这个多智能体系统通过整合多元化的数据源，为用户提供全面、专业的股票投资分析和建议。
