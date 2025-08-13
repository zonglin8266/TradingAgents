# TradingAgents Docker Makefile
# Provides convenient commands for Docker operations

.PHONY: help build run cli bash clean logs status stop restart setup test

# Default target
.DEFAULT_GOAL := help

# Variables
IMAGE_NAME := tradingagents
CONTAINER_NAME := tradingagents
COMPOSE_FILE := docker-compose.yml

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## 显示帮助信息
	@echo "$(GREEN)TradingAgents Docker 操作命令$(NC)"
	@echo ""
	@echo "$(YELLOW)设置命令:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(setup|build)"
	@echo ""
	@echo "$(YELLOW)运行命令:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(run|cli|bash|webui|jupyter)"
	@echo ""
	@echo "$(YELLOW)管理命令:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(logs|status|stop|restart|clean)"
	@echo ""
	@echo "$(YELLOW)测试命令:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(test)"

setup: ## 初始化设置（复制环境变量模板）
	@echo "$(GREEN)设置 TradingAgents Docker 环境...$(NC)"
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "$(YELLOW)已创建 .env 文件，请编辑并填入你的 API 密钥$(NC)"; \
		echo "$(RED)重要: 请编辑 .env 文件并填入以下必需的 API 密钥:$(NC)"; \
		echo "  - FINNHUB_API_KEY"; \
		echo "  - OPENAI_API_KEY (或其他 LLM API 密钥)"; \
	else \
		echo "$(YELLOW).env 文件已存在$(NC)"; \
	fi
	@mkdir -p results data_cache notebooks
	@echo "$(GREEN)设置完成!$(NC)"

build: ## 构建 Docker 镜像
	@echo "$(GREEN)构建 TradingAgents Docker 镜像...$(NC)"
	@docker-compose build

run: ## 运行完整服务（后台模式）
	@echo "$(GREEN)启动 TradingAgents 服务...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)服务已启动! 使用 'make logs' 查看日志$(NC)"

cli: ## 启动交互式 CLI
	@echo "$(GREEN)启动 TradingAgents CLI...$(NC)"
	@docker-compose run --rm tradingagents cli

bash: ## 进入容器 bash shell
	@echo "$(GREEN)进入 TradingAgents 容器...$(NC)"
	@docker-compose run --rm tradingagents bash

webui: ## 启动 Chainlit WebUI 服务
	@echo "$(GREEN)启动 TradingAgents WebUI...$(NC)"
	@docker-compose --profile webui up -d
	@echo "$(GREEN)WebUI 已启动! 访问: http://localhost:8000$(NC)"

jupyter: ## 启动 Jupyter notebook 服务
	@echo "$(GREEN)启动 Jupyter Notebook 服务...$(NC)"
	@docker-compose --profile jupyter up -d
	@echo "$(GREEN)Jupyter 已启动! 访问: http://localhost:8888$(NC)"

logs: ## 查看服务日志
	@docker-compose logs -f

status: ## 查看服务状态
	@echo "$(GREEN)TradingAgents 服务状态:$(NC)"
	@docker-compose ps

stop: ## 停止所有服务
	@echo "$(GREEN)停止 TradingAgents 服务...$(NC)"
	@docker-compose down

restart: ## 重启服务
	@echo "$(GREEN)重启 TradingAgents 服务...$(NC)"
	@docker-compose down
	@docker-compose up -d
	@echo "$(GREEN)服务已重启!$(NC)"

clean: ## 清理 Docker 资源
	@echo "$(GREEN)清理 Docker 资源...$(NC)"
	@docker-compose down -v
	@docker image rm $(IMAGE_NAME) 2>/dev/null || true
	@docker system prune -f
	@echo "$(GREEN)清理完成!$(NC)"

test: ## 测试部署
	@echo "$(GREEN)测试 TradingAgents 部署...$(NC)"
	@echo "1. 检查环境变量..."
	@if [ ! -f .env ]; then \
		echo "$(RED)错误: .env 文件不存在，请先运行 'make setup'$(NC)"; \
		exit 1; \
	fi
	@echo "2. 构建镜像..."
	@docker-compose build
	@echo "3. 测试导入..."
	@docker-compose run --rm tradingagents python -c "import tradingagents; print('✓ TradingAgents 导入成功')"
	@echo "4. 测试 API 连接..."
	@docker-compose run --rm tradingagents python -c "import os; print('✓ FinnHub API Key:', 'FINNHUB_API_KEY' in os.environ); print('✓ OpenAI API Key:', 'OPENAI_API_KEY' in os.environ)"
	@echo "$(GREEN)测试完成!$(NC)"

# 快速命令别名
up: run ## 别名：启动服务
down: stop ## 别名：停止服务
shell: bash ## 别名：进入 shell

# 开发命令
dev: ## 开发模式（挂载源码）
	@echo "$(GREEN)启动开发模式...$(NC)"
	@docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 生产命令
prod: ## 生产模式
	@echo "$(GREEN)启动生产模式...$(NC)"
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 备份和恢复
backup: ## 备份数据
	@echo "$(GREEN)备份数据...$(NC)"
	@tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz results/ data_cache/
	@echo "$(GREEN)备份完成!$(NC)"

# 监控命令
monitor: ## 监控资源使用
	@echo "$(GREEN)监控 TradingAgents 资源使用:$(NC)"
	@docker stats $(CONTAINER_NAME) --no-stream

# 检查健康状态
health: ## 检查服务健康状态
	@echo "$(GREEN)检查服务健康状态:$(NC)"
	@docker-compose ps
	@echo ""
	@docker inspect tradingagents_tradingagents_1 2>/dev/null | grep -A 10 '"Health"' || echo "健康检查信息不可用"

# 更新镜像
update: ## 更新并重建镜像
	@echo "$(GREEN)更新 TradingAgents...$(NC)"
	@docker-compose down
	@docker-compose build --no-cache
	@docker-compose up -d
	@echo "$(GREEN)更新完成!$(NC)"