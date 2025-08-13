"""
TradingAgents Chainlit WebUI Application
"""

import chainlit as cl
import asyncio
from datetime import datetime, timedelta
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import os
import json
from pathlib import Path

# Initialize global variables
trading_graph = None
config = None

@cl.on_chat_start
async def start():
    """Initialize the TradingAgents when chat starts"""
    global trading_graph, config
    
    # Welcome message
    await cl.Message(
        content="🎉 **欢迎使用 TradingAgents WebUI！**\n\n"
                "我是你的AI交易分析助手，可以帮你分析股票并提供投资建议。\n\n"
                "**功能特点：**\n"
                "- 📊 多维度分析：技术面、基本面、新闻面、情绪面\n"
                "- 🤖 多智能体协作：分析师团队 → 研究团队 → 交易员 → 风控团队\n"
                "- 📈 实时数据：获取最新的市场数据和新闻\n"
                "- 🎯 智能决策：基于多轮辩论的投资建议\n\n"
                "**使用方法：**\n"
                "直接输入股票代码（如：AAPL, TSLA, NVDA）开始分析！"
    ).send()
    
    # Initialize configuration
    config = DEFAULT_CONFIG.copy()
    
    # Load LLM provider from environment
    llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
    config['llm_provider'] = llm_provider
    
    if llm_provider == 'google':
        config['backend_url'] = os.getenv('GOOGLE_BASE_URL', 'https://generativelanguage.googleapis.com/v1')
        config['deep_think_llm'] = os.getenv('GOOGLE_MODEL_DEEP', 'gemini-2.0-flash')
        config['quick_think_llm'] = os.getenv('GOOGLE_MODEL_QUICK', 'gemini-2.0-flash')
    elif llm_provider == 'anthropic':
        config['backend_url'] = os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com')
        config['deep_think_llm'] = os.getenv('ANTHROPIC_MODEL_DEEP', 'claude-3-5-sonnet-20241022')
        config['quick_think_llm'] = os.getenv('ANTHROPIC_MODEL_QUICK', 'claude-3-5-haiku-20241022')
    else:  # default to openai
        config['backend_url'] = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        config['deep_think_llm'] = os.getenv('OPENAI_MODEL_DEEP', 'gpt-4o-mini')
        config['quick_think_llm'] = os.getenv('OPENAI_MODEL_QUICK', 'gpt-4o-mini')
    
    # Check API keys
    missing_keys = []
    if not os.getenv('FINNHUB_API_KEY'):
        missing_keys.append('FINNHUB_API_KEY')
    
    if not any([os.getenv('OPENAI_API_KEY'), os.getenv('GOOGLE_API_KEY'), os.getenv('ANTHROPIC_API_KEY')]):
        missing_keys.append('至少一个LLM API密钥 (OPENAI_API_KEY, GOOGLE_API_KEY, 或 ANTHROPIC_API_KEY)')
    
    if missing_keys:
        await cl.Message(
            content=f"⚠️ **缺少必需的API密钥：**\n\n"
                   f"{'、'.join(missing_keys)}\n\n"
                   f"请设置环境变量后重启应用。\n\n"
                   f"**获取API密钥：**\n"
                   f"- FinnHub: https://finnhub.io/register\n"
                   f"- OpenAI: https://platform.openai.com/api-keys\n"
                   f"- Google AI: https://aistudio.google.com/app/apikey\n"
                   f"- Anthropic: https://console.anthropic.com/settings/keys"
        ).send()
        return
    
    # Initialize TradingAgents
    try:
        trading_graph = TradingAgentsGraph(debug=True, config=config)
        await cl.Message(content="✅ TradingAgents 初始化成功！请输入股票代码开始分析。").send()
    except Exception as e:
        await cl.Message(content=f"❌ 初始化失败：{str(e)}").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages"""
    global trading_graph, config
    
    if not trading_graph:
        await cl.Message(content="❌ 系统未初始化，请刷新页面重试。").send()
        return
    
    user_input = message.content.strip().upper()
    
    # Check if input looks like a stock ticker
    if not user_input or len(user_input) > 10:
        await cl.Message(
            content="请输入有效的股票代码（如：AAPL, TSLA, NVDA, SPY, BTC-USD）"
        ).send()
        return
    
    # Get analysis date (yesterday to avoid weekend/holiday issues)
    analysis_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Start analysis with detailed progress tracking
    await run_analysis_with_progress(user_input, analysis_date)

async def run_analysis_with_progress(ticker, analysis_date):
    """Run analysis with detailed progress updates"""
    global trading_graph
    
    # Create main progress message
    progress_msg = cl.Message(content="")
    await progress_msg.send()
    
    try:
        # Step 1: Initialize
        await update_progress(progress_msg, "🚀 初始化分析系统", f"正在为 **{ticker}** 准备多智能体分析框架...", "", "🔄")
        await asyncio.sleep(1)
        
        # Step 2: Start propagation with custom callback
        analysis_results = {}
        
        await update_progress(progress_msg, "📊 数据收集", f"正在获取 **{ticker}** 的市场数据...", "", "🔄")
        
        # Run analysis in thread but with progress callbacks
        final_state, decision = await run_analysis_with_callbacks(
            ticker, analysis_date, progress_msg, analysis_results
        )
        
        # Final report
        await update_progress(progress_msg, "✅ 分析完成", "正在生成完整报告...", "", "📄")
        
        # Format and display final report  
        report_content = format_detailed_analysis_report(final_state, decision, ticker, analysis_date, analysis_results)
        
        progress_msg.content = report_content
        await progress_msg.update()
        
        # Save results
        save_analysis_results(ticker, analysis_date, final_state, decision)
        
    except Exception as e:
        error_msg = f"❌ **分析过程中出现错误**\n\n```\n{str(e)}\n```\n\n请检查API密钥是否有效，或稍后重试。"
        progress_msg.content = error_msg
        await progress_msg.update()

async def run_analysis_with_callbacks(ticker, analysis_date, progress_msg, analysis_results):
    """Run analysis with real-time progress callbacks"""
    global trading_graph
    
    # Initialize progress tracking
    analysis_results["steps"] = []
    
    # Step 1: Start Analysis
    await update_progress_with_table(
        progress_msg, 
        "🚀 开始分析", 
        f"正在启动 {ticker} 的多智能体分析系统...", 
        analysis_results,
        "current_step", 
        "initializing"
    )
    await asyncio.sleep(2)
    
    # Step 2: Run Analysis with periodic updates
    await update_progress_with_table(
        progress_msg, 
        "⚙️ 执行分析", 
        "多智能体系统正在协作分析，请稍候...", 
        analysis_results,
        "current_step", 
        "analyzing"
    )
    
    # Run analysis in background with progress updates
    
    analysis_task = asyncio.create_task(
        asyncio.to_thread(trading_graph.propagate, ticker, analysis_date)
    )
    
    # Updated for parallel execution
    steps = [
        ("🚀 并行分析启动", "启动多个分析师并行执行"),
        ("📊 市场分析师", "获取价格数据和技术指标"),
        ("💭 社交媒体分析师", "分析社交媒体情绪"),
        ("📰 新闻分析师", "收集和分析相关新闻"),
        ("📈 基本面分析师", "评估财务基本面"),
        ("✅ 并行分析完成", "所有分析师同步完成"),
        ("🐂 多头研究员", "寻找看涨因素"),
        ("🐻 空头研究员", "识别看跌风险"),
        ("⚖️ 研究经理", "整合研究观点"),
        ("💰 交易员", "制定交易策略"),
        ("⚠️ 风险评估", "评估投资风险"),
        ("📋 投资组合经理", "最终投资建议")
    ]
    
    step_index = 0
    parallel_phase = True
    while not analysis_task.done():
        if step_index < len(steps):
            step_name, step_desc = steps[step_index]
            
            # Add current step to results
            analysis_results["steps"].append({
                "name": step_name,
                "description": step_desc,
                "status": "in_progress",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            await update_progress_with_table(
                progress_msg,
                step_name,
                f"{step_desc}...",
                analysis_results,
                "current_step",
                f"step_{step_index}"
            )
            
            # Special handling for parallel execution phase
            if step_index == 0:  # 🚀 并行分析启动
                await asyncio.sleep(1)
                # Start all parallel analysts at once
                for i in range(1, 5):  # Steps 1-4 are parallel analysts
                    if i < len(steps):
                        parallel_step_name, parallel_step_desc = steps[i]
                        analysis_results["steps"].append({
                            "name": parallel_step_name,
                            "description": parallel_step_desc,
                            "status": "in_progress",
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                
                # Show all parallel analysts running
                await update_progress_with_table(
                    progress_msg,
                    "🔄 并行分析进行中",
                    "4个分析师正在同时执行分析...",
                    analysis_results,
                    "current_step",
                    "parallel_execution"
                )
                step_index = 5  # Skip to completion step
                await asyncio.sleep(8)  # Wait for parallel execution
                
                # Mark all parallel analysts as completed
                for i in range(1, 5):
                    if i < len(analysis_results["steps"]):
                        analysis_results["steps"][i]["status"] = "completed"
                        
            else:
                step_index += 1
                await asyncio.sleep(2)
            
        else:
            # Wait for analysis to complete
            await asyncio.sleep(1)
        
        # Mark previous step as completed if analysis is still running
        if step_index > 0 and step_index <= len(analysis_results["steps"]):
            analysis_results["steps"][step_index-1]["status"] = "completed"
    
    # Mark all remaining steps as completed
    for i in range(len(analysis_results["steps"])):
        analysis_results["steps"][i]["status"] = "completed"
    
    # Get the final result
    final_state, decision = await analysis_task
    
    await update_progress_with_table(
        progress_msg,
        "✅ 分析完成",
        "正在生成详细报告...",
        analysis_results,
        "current_step",
        "completed"
    )
    
    return final_state, decision

async def update_progress(msg, title, description, step_info, icon):
    """Update progress message with current step"""
    content = f"# {icon} {title}\n\n"
    if step_info:
        content += f"**{step_info}**\n\n"
    content += f"{description}\n\n"
    content += "---\n\n"
    content += "*正在进行多维度投资分析，请稍候...*"
    
    msg.content = content
    await msg.update()

async def update_progress_with_table(msg, title, description, analysis_results, current_key, current_value):
    """Update progress message with real-time step table"""
    content = f"# 🔄 {title}\n\n"
    content += f"**{description}**\n\n"
    
    # Add progress table if steps exist
    if analysis_results.get("steps"):
        content += "## 📊 分析进度\n\n"
        content += "| 步骤 | 分析师 | 状态 | 时间 |\n"
        content += "|------|--------|------|------|\n"
        
        for i, step in enumerate(analysis_results["steps"], 1):
            status_icon = "✅" if step["status"] == "completed" else "🔄" if step["status"] == "in_progress" else "⏳"
            content += f"| {i} | {step['name']} | {status_icon} {step['status']} | {step['timestamp']} |\n"
        
        content += "\n"
    
    # Add current status
    content += f"**当前状态：** {description}\n\n"
    content += "---\n\n"
    content += "*🤖 多智能体系统正在协作分析，实时更新进度...*"
    
    msg.content = content
    await msg.update()

def format_analysis_report(final_state, decision, ticker, date):
    """Format the analysis report for display"""
    
    report = f"# 📊 {ticker} 分析报告\n"
    report += f"**分析日期：** {date}\n\n"
    
    # Executive Summary
    if decision:
        report += "## 🎯 投资决策\n\n"
        report += f"```\n{decision}\n```\n\n"
    
    # Analyst Team Reports
    report += "## 👥 分析师团队报告\n\n"
    
    if final_state.get('market_report'):
        report += "### 📊 市场分析\n"
        report += f"{final_state['market_report']}\n\n"
    
    if final_state.get('sentiment_report'):
        report += "### 💭 情绪分析\n"
        report += f"{final_state['sentiment_report']}\n\n"
    
    if final_state.get('news_report'):
        report += "### 📰 新闻分析\n"
        report += f"{final_state['news_report']}\n\n"
    
    if final_state.get('fundamentals_report'):
        report += "### 📈 基本面分析\n"
        report += f"{final_state['fundamentals_report']}\n\n"
    
    # Research Team
    if final_state.get('investment_debate_state'):
        report += "## 🔬 研究团队决策\n\n"
        debate_state = final_state['investment_debate_state']
        
        if debate_state.get('judge_decision'):
            report += f"{debate_state['judge_decision']}\n\n"
    
    # Trading Team
    if final_state.get('trader_investment_plan'):
        report += "## 💰 交易计划\n\n"
        report += f"{final_state['trader_investment_plan']}\n\n"
    
    # Risk Management
    if final_state.get('risk_debate_state'):
        report += "## ⚠️ 风险管理\n\n"
        risk_state = final_state['risk_debate_state']
        
        if risk_state.get('judge_decision'):
            report += f"{risk_state['judge_decision']}\n\n"
    
    # Footer
    report += "---\n"
    report += "⚠️ **风险提示：** 本分析仅供研究参考，不构成投资建议。投资有风险，决策需谨慎。\n\n"
    report += "💡 **提示：** 可以继续输入其他股票代码进行分析！"
    
    return report

def clean_state_for_json(state):
    """Clean state data to make it JSON serializable"""
    if isinstance(state, dict):
        cleaned = {}
        for key, value in state.items():
            try:
                # Try to clean the value
                cleaned_value = clean_state_for_json(value)
                # Test if it's serializable
                json.dumps(cleaned_value)
                cleaned[key] = cleaned_value
            except (TypeError, ValueError):
                # If not serializable, convert to string or skip
                if hasattr(value, '__dict__'):
                    cleaned[key] = str(value)
                elif isinstance(value, (list, tuple)):
                    cleaned[key] = [str(item) for item in value]
                else:
                    cleaned[key] = str(value)
        return cleaned
    elif isinstance(state, (list, tuple)):
        cleaned = []
        for item in state:
            try:
                cleaned_item = clean_state_for_json(item)
                json.dumps(cleaned_item)
                cleaned.append(cleaned_item)
            except (TypeError, ValueError):
                cleaned.append(str(item))
        return cleaned
    else:
        # For primitive types, return as-is
        return state

def save_analysis_results(ticker, date, final_state, decision):
    """Save analysis results to file"""
    try:
        results_dir = Path("./results") / ticker / date
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean the state to make it JSON serializable
        cleaned_state = clean_state_for_json(final_state)
        
        # Save full state
        with open(results_dir / "analysis_state.json", "w", encoding='utf-8') as f:
            json.dump(cleaned_state, f, ensure_ascii=False, indent=2)
        
        # Save decision
        if decision:
            with open(results_dir / "decision.txt", "w", encoding='utf-8') as f:
                f.write(str(decision))
                
        print(f"Analysis results saved to {results_dir}")
    except Exception as e:
        print(f"Failed to save results: {e}")

def format_detailed_analysis_report(final_state, decision, ticker, date, analysis_results):
    """Format detailed analysis report with progress information"""
    
    # Header with progress summary
    report = f"# 📊 {ticker} 完整分析报告\n"
    report += f"**分析日期：** {date} | **完成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Analysis Steps Summary
    if analysis_results.get('steps'):
        report += "## 🔄 分析流程\n\n"
        report += "| 步骤 | 分析师 | 状态 | 完成时间 |\n"
        report += "|------|--------|------|----------|\n"
        for i, step in enumerate(analysis_results['steps'], 1):
            status_icon = "✅" if step['status'] == 'completed' else "⏳"
            report += f"| {i} | {step['name']} | {status_icon} | {step['timestamp']} |\n"
        report += "\n"
    
    # Executive Summary with enhanced formatting
    if decision:
        report += "## 🎯 投资决策摘要\n\n"
        report += f"```\n{decision}\n```\n\n"
    
    # Detailed Analysis Sections
    report += "## 📈 详细分析报告\n\n"
    
    # Market Analysis with enhanced details
    if final_state.get('market_report'):
        report += "### 📊 市场技术分析\n\n"
        report += "**分析范围：** 价格动态、技术指标、成交量分析\n\n"
        report += f"{final_state['market_report']}\n\n"
        report += "---\n\n"
    
    # Sentiment Analysis
    if final_state.get('sentiment_report'):
        report += "### 💭 市场情绪分析\n\n"
        report += "**分析范围：** 社交媒体情绪、投资者心理、市场氛围\n\n"
        report += f"{final_state['sentiment_report']}\n\n"
        report += "---\n\n"
    
    # News Analysis  
    if final_state.get('news_report'):
        report += "### 📰 新闻事件分析\n\n"
        report += "**分析范围：** 相关新闻、宏观事件、行业动态\n\n"
        report += f"{final_state['news_report']}\n\n"
        report += "---\n\n"
    
    # Fundamentals Analysis
    if final_state.get('fundamentals_report'):
        report += "### 📈 基本面分析\n\n"
        report += "**分析范围：** 财务指标、估值水平、成长性评估\n\n"
        report += f"{final_state['fundamentals_report']}\n\n"
        report += "---\n\n"
    
    # Research Team Debate
    if final_state.get('investment_debate_state'):
        report += "## 🔬 多空观点辩论\n\n"
        debate_state = final_state['investment_debate_state']
        
        if debate_state.get('judge_decision'):
            report += "**研究经理综合判断：**\n\n"
            report += f"{debate_state['judge_decision']}\n\n"
        
        report += "---\n\n"
    
    # Trading Strategy
    if final_state.get('trader_investment_plan'):
        report += "## 📈 交易策略建议\n\n"
        report += "**交易员策略：**\n\n"
        report += f"{final_state['trader_investment_plan']}\n\n"
        report += "---\n\n"
    
    # Risk Assessment
    if final_state.get('risk_debate_state'):
        report += "## ⚠️ 风险评估报告\n\n"
        risk_state = final_state['risk_debate_state']
        
        if risk_state.get('judge_decision'):
            report += "**风险管理团队评估：**\n\n"
            report += f"{risk_state['judge_decision']}\n\n"
        
        report += "---\n\n"
    
    # Analysis Metadata
    report += "## 📋 分析元数据\n\n"
    report += f"- **分析框架：** TradingAgents 多智能体系统\n"
    report += f"- **LLM 提供商：** {config.get('llm_provider', 'Unknown').title()}\n"
    report += f"- **分析深度：** 多维度综合分析\n"
    report += f"- **数据源：** Yahoo Finance, FinnHub, 新闻聚合\n\n"
    
    # Disclaimer
    report += "---\n\n"
    report += "## ⚠️ 重要声明\n\n"
    report += "- **仅供参考：** 此分析报告仅供学术研究和参考，不构成投资建议\n"
    report += "- **风险提醒：** 投资有风险，入市需谨慎，请根据个人情况做出投资决策\n"
    report += "- **数据延迟：** 市场数据可能存在延迟，请以实时数据为准\n"
    report += "- **AI 生成：** 本报告由 AI 系统生成，请结合人工判断使用\n\n"
    report += "💡 **提示：** 可以继续输入其他股票代码进行分析！"
    
    return report

if __name__ == "__main__":
    # This is for running with chainlit run app.py
    pass