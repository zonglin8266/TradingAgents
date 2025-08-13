# Use Python 3.13 as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY pyproject.toml .
COPY setup.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the project in development mode
RUN pip install -e .

# Create necessary directories
RUN mkdir -p /app/results \
    && mkdir -p /app/tradingagents/dataflows/data_cache

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port for potential web interface
EXPOSE 8000

# Create entrypoint script
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["cli"]