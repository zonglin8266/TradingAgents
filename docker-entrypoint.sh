#!/bin/bash

# Docker entrypoint script for TradingAgents

# Function to check if required environment variables are set
check_env_vars() {
    local missing_vars=()
    
    if [ -z "$OPENAI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
        missing_vars+=("At least one of: OPENAI_API_KEY, GOOGLE_API_KEY, or ANTHROPIC_API_KEY")
    fi
    
    if [ -z "$FINNHUB_API_KEY" ]; then
        missing_vars+=("FINNHUB_API_KEY")
    fi
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "ERROR: Missing required environment variables:"
        printf '  - %s\n' "${missing_vars[@]}"
        echo ""
        echo "Please set the required environment variables and try again."
        echo "You can get free API keys from:"
        echo "  - OpenAI: https://platform.openai.com/api-keys"
        echo "  - Google AI: https://aistudio.google.com/app/apikey"
        echo "  - Anthropic: https://console.anthropic.com/settings/keys"
        echo "  - FinnHub: https://finnhub.io/register"
        exit 1
    fi
}

# Function to display usage information
show_usage() {
    echo "TradingAgents Docker Container"
    echo ""
    echo "Usage: docker run [docker-options] tradingagents [command] [options]"
    echo ""
    echo "Commands:"
    echo "  cli                 Run the interactive CLI (default)"
    echo "  webui               Run the Chainlit WebUI"
    echo "  python [script]     Run a Python script"
    echo "  bash               Open a bash shell"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  docker run -it tradingagents cli"
    echo "  docker run -p 8000:8000 tradingagents webui"
    echo "  docker run -it tradingagents python main.py"
    echo "  docker run -it tradingagents python -m cli.main analyze"
    echo "  docker run -it tradingagents bash"
    echo ""
    echo "Required Environment Variables:"
    echo "  FINNHUB_API_KEY     - FinnHub API key for financial data"
    echo "  One of the following LLM API keys:"
    echo "    OPENAI_API_KEY    - OpenAI API key"
    echo "    GOOGLE_API_KEY    - Google AI API key"
    echo "    ANTHROPIC_API_KEY - Anthropic API key"
    echo ""
    echo "Optional Environment Variables:"
    echo "  TRADINGAGENTS_RESULTS_DIR - Directory for results (default: ./results)"
    echo "  REDIS_URL                 - Redis connection URL for caching"
}

# Main execution logic
case "${1:-cli}" in
    "help"|"--help"|"-h")
        show_usage
        exit 0
        ;;
    "cli")
        echo "Starting TradingAgents CLI..."
        check_env_vars
        exec python -m cli.main analyze
        ;;
    "webui")
        echo "Starting TradingAgents WebUI..."
        check_env_vars
        exec chainlit run app.py --host 0.0.0.0 --port 8000
        ;;
    "python")
        echo "Running Python script..."
        check_env_vars
        shift
        exec python "$@"
        ;;
    "bash")
        echo "Starting bash shell..."
        exec bash
        ;;
    *)
        echo "Running custom command: $@"
        check_env_vars
        exec "$@"
        ;;
esac