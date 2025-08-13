# Cursor CLI "/" 命令完整教程

## 简介

Cursor CLI 是一个强大的终端 AI 编程助手，通过 "/" 前缀命令可以直接在终端中执行各种开发任务。本教程将详细介绍所有可用的 "/" 命令及其使用方法。

## 基础使用

### 启动 Cursor CLI

```bash
# 交互模式
cursor-agent

# 非交互模式（适合脚本）
cursor-agent --print

# 指定模型
cursor-agent -m gpt-5
cursor-agent -m sonnet-4
```

### 登录认证

```bash
cursor-agent login
```

## "/" 命令完整列表

### 1. 帮助和状态命令

#### `/help`
- **功能**: 列出所有可用命令与用法
- **语法**: `/help`
- **示例**: 
  ```
  /help
  ```

#### `/status`
- **功能**: 显示当前 git 状态
- **语法**: `/status`
- **示例**: 
  ```
  /status
  ```
- **输出**: 显示分支信息、修改的文件、未跟踪的文件等

### 2. 文件和目录操作

#### `/ls [path]`
- **功能**: 列出目录内容
- **语法**: `/ls [可选路径]`
- **示例**: 
  ```
  /ls
  /ls tradingagents/
  /ls tradingagents/agents/
  ```

#### `/read path [start:end]`
- **功能**: 查看文件内容（可选择行范围）
- **语法**: `/read 文件路径 [起始行:结束行]`
- **示例**: 
  ```
  /read README.md
  /read tradingagents/default_config.py 1:50
  /read app.py 10:30
  ```

#### `/files "glob"`
- **功能**: 通过通配符模式查找文件
- **语法**: `/files "通配符模式"`
- **示例**: 
  ```
  /files "*.py"
  /files "tradingagents/**/*.py"
  /files "**/test_*.py"
  /files "**/*config*"
  ```

### 3. 搜索和查找

#### `/search "pattern" [glob]`
- **功能**: 在仓库中搜索文本内容
- **语法**: `/search "搜索模式" [可选文件模式]`
- **示例**: 
  ```
  /search "position_size"
  /search "class.*Agent" "*.py"
  /search "TODO" "**/*.py"
  /search "import pandas" "tradingagents/**/*.py"
  ```

### 4. Git 操作

#### `/diff [path]`
- **功能**: 查看 git 改动差异
- **语法**: `/diff [可选路径]`
- **示例**: 
  ```
  /diff
  /diff tradingagents/agents/trader/trader.py
  /diff tradingagents/
  ```

#### `/log [n]`
- **功能**: 查看最近的提交历史
- **语法**: `/log [提交数量]`
- **示例**: 
  ```
  /log
  /log 5
  /log 10
  ```

#### `/commit`
- **功能**: 智能分析改动并生成符合规范的提交信息
- **语法**: `/commit`
- **示例**: 
  ```
  /commit
  ```
- **特点**: 
  - 自动分析代码改动
  - 生成符合 Conventional Commits 规范的提交信息
  - 提供详细的提交描述

#### `/pr [base=分支] [title="标题"]`
- **功能**: 基于当前分支创建 Pull Request
- **语法**: `/pr [base=目标分支] [title="PR标题"]`
- **前提**: 需要安装并登录 GitHub CLI (`gh auth login`)
- **示例**: 
  ```
  /pr
  /pr base=main
  /pr base=main title="Add Docker support"
  /pr base=develop title="Implement new trading algorithm"
  ```

### 5. 代码执行和测试

#### `/run "command"`
- **功能**: 运行短时 shell 命令
- **语法**: `/run "shell命令"`
- **限制**: 有 30 秒超时限制，不适合长时间运行的任务
- **示例**: 
  ```
  /run "python --version"
  /run "python app.py --help"
  /run "pip list | grep pandas"
  /run "find . -name '*.py' | wc -l"
  ```

#### `/test [cmd]`
- **功能**: 运行测试套件
- **语法**: `/test [可选测试命令]`
- **默认**: 如果不指定命令，会尝试运行 `pytest -q`
- **示例**: 
  ```
  /test
  /test "python -m pytest tests/"
  /test "python -m unittest discover"
  /test "npm test"
  ```

#### `/fmt`
- **功能**: 运行代码格式化和静态检查
- **语法**: `/fmt`
- **支持的工具**: 
  - Python: black, isort, ruff, flake8
  - JavaScript/TypeScript: prettier, eslint
  - 其他语言的相应格式化工具
- **示例**: 
  ```
  /fmt
  ```

## 高级使用技巧

### 1. 组合使用命令

```bash
# 先查看状态，再查看差异，最后提交
/status
/diff
/commit
```

### 2. 项目分析工作流

```bash
# 1. 了解项目结构
/ls
/files "*.py"

# 2. 查看配置文件
/read pyproject.toml
/read requirements.txt

# 3. 搜索关键功能
/search "class.*Agent"
/search "def main"

# 4. 查看具体实现
/read tradingagents/agents/trader/trader.py
```

### 3. 开发工作流

```bash
# 1. 查看当前状态
/status

# 2. 运行测试
/test

# 3. 格式化代码
/fmt

# 4. 查看改动
/diff

# 5. 提交代码
/commit

# 6. 创建 PR
/pr base=main title="Feature: Add new trading strategy"
```

## 在您的 TradingAgents 项目中的应用示例

### 分析项目结构
```bash
/ls
/files "tradingagents/**/*.py"
/read tradingagents/default_config.py
```

### 查找特定功能
```bash
/search "trading_agent" "*.py"
/search "class.*Analyst" "tradingagents/**/*.py"
/search "def execute_trade" "**/*.py"
```

### 开发新功能
```bash
/status
/diff tradingagents/agents/
/test "python -m pytest tests/"
/commit
```

### 查看项目配置
```bash
/read pyproject.toml
/read requirements.txt
/read docker-compose.yml
```

## 注意事项

1. **超时限制**: `/run` 命令有 30 秒超时限制，避免运行长时间任务
2. **GitHub 集成**: `/pr` 命令需要先安装并登录 GitHub CLI (`gh auth login`)
3. **权限模式**: 默认权限模式下，某些命令可能需要用户确认
4. **文件路径**: 支持相对路径和绝对路径，支持通配符模式

## 快速参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `/help` | 显示帮助 | `/help` |
| `/status` | Git 状态 | `/status` |
| `/ls` | 列目录 | `/ls tradingagents/` |
| `/read` | 读文件 | `/read app.py 1:50` |
| `/files` | 查找文件 | `/files "*.py"` |
| `/search` | 搜索内容 | `/search "class.*Agent"` |
| `/diff` | 查看差异 | `/diff` |
| `/log` | 提交历史 | `/log 5` |
| `/commit` | 智能提交 | `/commit` |
| `/pr` | 创建 PR | `/pr base=main` |
| `/run` | 运行命令 | `/run "python --version"` |
| `/test` | 运行测试 | `/test` |
| `/fmt` | 格式化代码 | `/fmt` |

通过这些 "/" 命令，您可以直接在终端中完成大部分开发任务，大大提高开发效率！
