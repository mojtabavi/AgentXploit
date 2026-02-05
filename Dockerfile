# PentestAI Docker Image
# AI-Powered Penetration Testing & Remediation Framework

FROM hub.mirror.mojtabavi.dev/python:3.11-slim

LABEL description="PentestAI - Unified Pentesting & Remediation Framework"
LABEL version="1.0.0"

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    # Essential pentesting tools
    nmap \
    netcat-openbsd \
    curl \
    wget \
    git \
    # Network utilities
    net-tools \
    dnsutils \
    # Terminal utilities
    vim \
    && apt-get autoremove -y \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire PentestAI framework
COPY pentestai/ ./pentestai/
COPY pentestai_interactive.py .
COPY quickstart.py .
COPY pyproject.toml .
COPY README.md .

# Create output directory
RUN mkdir -p /app/pentestai_results

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color
ENV PENTESTAI_OUTPUT_DIRECTORY=/app/pentestai_results

# Create non-root user for security
RUN useradd -m -s /bin/bash pentester && \
    chown -R pentester:pentester /app

USER pentester

# Default command: interactive CLI
CMD ["python", "pentestai_interactive.py"]
