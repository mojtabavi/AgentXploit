# Docker Deployment Guide

Complete guide for deploying PentestAI using Docker and Docker Compose.

## Overview

PentestAI consists of three Docker services:

1. **kali-mcp-server**: Official Kali Linux MCP server (50+ pentest tools)
2. **pentestai-api**: FastAPI backend with streaming support
3. **pentestai-react-ui**: React web interface (optional)

## Quick Start

```bash
# Clone repository
git clone https://github.com/pentestai/pentestai.git
cd pentestai

# Configure environment
cp .env.example .env
nano .env  # Add OPENAI_API_KEY

# Start all services
docker-compose up -d --build

# Verify services
docker-compose ps

# View logs
docker-compose logs -f
```

Access services:
- **React UI**: http://localhost:3000
- **API Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Kali MCP**: http://localhost:5000 (internal)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Host Network                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │  kali-mcp-server (host network)                    │ │
│  │  - Official Kali MCP package                       │ │
│  │  - 50+ pentest tools (nmap, sqlmap, metasploit)   │ │
│  │  - Port 5000 → localhost:5000                       │ │
│  │  - Needs host network for local LAN access         │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│             Bridge Network (172.30.0.0/24)               │
│  ┌────────────────────────────────────────────────────┐ │
│  │  pentestai-api (172.30.0.2)                        │ │
│  │  - FastAPI backend                                  │ │
│  │  - SSE streaming                                    │ │
│  │  - Port 8000 → localhost:8000                       │ │
│  │  - Connects to Kali via host.docker.internal:5000  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  pentestai-react-ui (172.30.0.3)                   │ │
│  │  - Vite + React 18                                  │ │
│  │  - Bun package manager                              │ │
│  │  - Port 3000 → localhost:3000                       │ │
│  │  - Connects to API at localhost:8000                │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Docker Compose Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  # Kali Linux MCP Server - Real pentesting tools
  kali-mcp-server:
    build:
      context: .
      dockerfile: Dockerfile.kali-mcp
    container_name: kali-mcp-server
    network_mode: host  # Required for local network access
    restart: unless-stopped
    environment:
      - MCP_SERVER_PORT=5000
    volumes:
      - kali-data:/root/.kali
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PentestAI API Server - FastAPI backend
  pentestai-api:
    build:
      context: .
      dockerfile: Dockerfile.pentestai
    container_name: pentestai-api
    ports:
      - "8000:8000"
    networks:
      - pentestai-network
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_BASE_URL=${OPENAI_BASE_URL:-}
      - ARVANCLOUD_API_KEY=${ARVANCLOUD_API_KEY:-}
      - LLM_MODEL=${LLM_MODEL:-gpt-4}
      - KALI_MCP_URL=http://host.docker.internal:5000
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./pentestai_results:/app/pentestai_results
    depends_on:
      - kali-mcp-server
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # React Web UI - Modern ChatGPT-style interface
  pentestai-react-ui:
    build:
      context: ./ui
      dockerfile: Dockerfile
    container_name: pentestai-react-ui
    ports:
      - "3000:3000"
    networks:
      - pentestai-network
    environment:
      - API_URL=http://localhost:8000
    depends_on:
      - pentestai-api
    restart: unless-stopped

networks:
  pentestai-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.30.0.0/24

volumes:
  kali-data:
    driver: local
```

## Dockerfiles

### Dockerfile.kali-mcp

Official Kali MCP server installation:

```dockerfile
FROM kalilinux/kali-rolling:latest

# Install Kali MCP server package
RUN apt-get update && \
    apt-get install -y kali-server-mcp curl && \
    apt-get clean

# Expose MCP server port
EXPOSE 5000

# Start MCP server
CMD ["kali-server-mcp", "--port", "5000", "--host", "0.0.0.0"]
```

### Dockerfile.pentestai

FastAPI backend:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential && \
    apt-get clean

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create results directory
RUN mkdir -p pentestai_results

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Expose API port
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ui/Dockerfile

React UI with Bun:

```dockerfile
FROM oven/bun:latest

WORKDIR /app

# Copy package files
COPY package.json bun.lockb* ./

# Install dependencies
RUN bun install

# Copy application code
COPY . .

# Expose dev server port
EXPOSE 3000

# Start Vite dev server
CMD ["bun", "run", "dev", "--host", "0.0.0.0"]
```

## Environment Variables

### .env File

```bash
# Required: LLM Provider API Key
OPENAI_API_KEY=sk-your-openai-key-here

# Or for ArvanCloud (Iranian AI Gateway)
ARVANCLOUD_API_KEY=your-arvancloud-token
OPENAI_BASE_URL=https://api.arvancloud.ir/llm/v1

# Optional: Model Selection
LLM_MODEL=gpt-4
PENTEST_MODEL=gpt-4
REMEDIATION_MODEL=gpt-4

# Optional: MCP Configuration
KALI_MCP_URL=http://host.docker.internal:5000

# Optional: Output Settings
OUTPUT_DIR=./pentestai_results
SANDBOX_MODE=true
```

### .env.example

```bash
# Copy this file to .env and fill in your values

# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
# OPENAI_BASE_URL=  # Optional: Custom OpenAI-compatible endpoint

# ArvanCloud Configuration (Iranian AI Gateway)
# ARVANCLOUD_API_KEY=your-token
# OPENAI_BASE_URL=https://api.arvancloud.ir/llm/v1

# Model Selection
LLM_MODEL=gpt-4

# MCP Server
KALI_MCP_URL=http://host.docker.internal:5000

# Safety
SANDBOX_MODE=true
```

## Common Commands

### Start Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d pentestai-api

# Build and start
docker-compose up -d --build

# Start with logs
docker-compose up --build
```

### Check Status

```bash
# View running containers
docker-compose ps

# Check health
docker-compose ps | grep "(healthy)"

# View service logs
docker-compose logs pentestai-api
docker-compose logs kali-mcp-server
docker-compose logs pentestai-react-ui

# Follow logs
docker-compose logs -f  # all services
docker-compose logs -f pentestai-api  # specific service
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop pentestai-api
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart pentestai-api
```

### Update Services

```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose build pentestai-api
docker-compose up -d pentestai-api
```

## Troubleshooting

### Issue: Kali MCP Server Not Starting

**Symptoms:**
```bash
$ docker logs kali-mcp-server
Error: Package kali-server-mcp not found
```

**Solution:**
```bash
# Update Kali package list in Dockerfile
RUN apt-get update && \
    apt-get update --allow-releaseinfo-change && \
    apt-get install -y kali-server-mcp
```

### Issue: Port Already in Use

**Symptoms:**
```
ERROR: port is already allocated
```

**Solution:**
```bash
# Find process using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Issue: API Cannot Connect to Kali MCP

**Symptoms:**
```
Connection refused: http://host.docker.internal:5000
```

**Solution:**
```bash
# Verify Kali is running
docker-compose ps kali-mcp-server

# Check Kali logs
docker logs kali-mcp-server

# Test from host
curl http://localhost:5000/health

# Test from API container
docker exec pentestai-api curl http://host.docker.internal:5000/health
```

### Issue: UI Shows Connection Error

**Symptoms:**
Browser shows: "Failed to connect to API"

**Solution:**
```bash
# Check API is running
docker-compose ps pentestai-api

# Test API health
curl http://localhost:8000/api/health

# Check CORS settings in api_server.py
allow_origins=["http://localhost:3000"]
```

### Issue: LLM Connection Failed

**Symptoms:**
```json
{"error": "LLM not connected"}
```

**Solution:**
```bash
# Verify API key in .env
cat .env | grep OPENAI_API_KEY

# Restart API with new env vars
docker-compose restart pentestai-api

# Check logs for LLM init
docker logs pentestai-api | grep "LLM"
```

### Issue: Docker Build Fails

**Symptoms:**
```
ERROR: failed to solve: dockerfile.Pentestai: not found
```

**Solution:**
```bash
# Check Dockerfile names (case-sensitive)
ls -la | grep Dockerfile

# Verify docker-compose.yml references
dockerfile: Dockerfile.pentestai  # Not Dockerfile.Pentestai
```

## Resource Management

### Memory Limits

```yaml
services:
  pentestai-api:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'
```

### Disk Space

```bash
# Check Docker disk usage
docker system df

# Clean up unused images
docker image prune -a

# Clean up volumes
docker volume prune

# Full cleanup
docker system prune -a --volumes
```

## Security Best Practices

1. **Never commit `.env` file**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use secrets for production**
   ```yaml
   services:
     pentestai-api:
       secrets:
         - openai_api_key
   
   secrets:
     openai_api_key:
       external: true
   ```

3. **Run as non-root user**
   ```dockerfile
   RUN useradd -m pentestai
   USER pentestai
   ```

4. **Network isolation**
   ```yaml
   networks:
     pentestai-network:
       driver: bridge
       internal: true  # No internet access
   ```

5. **Read-only filesystem**
   ```yaml
   services:
     pentestai-api:
       read_only: true
       tmpfs:
         - /tmp
   ```

## Monitoring

### Health Checks

```bash
# Check all health status
docker-compose ps

# Manual health check
curl http://localhost:8000/api/health
curl http://localhost:5000/health
```

### Logs

```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs pentestai-api

# Last 100 lines
docker-compose logs --tail=100

# Follow mode
docker-compose logs -f --tail=50
```

### Metrics (Prometheus)

Add to `api_server.py`:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

Access metrics: http://localhost:8000/metrics

## Backup and Restore

### Backup Results

```bash
# Backup results directory
docker cp pentestai-api:/app/pentestai_results ./backup/

# Or use volume mount
volumes:
  - ./pentestai_results:/app/pentestai_results
```

### Backup Kali Data

```bash
# Export Kali volume
docker run --rm -v kali-data:/data -v $(pwd):/backup alpine \
  tar czf /backup/kali-data.tar.gz -C /data .

# Restore
docker run --rm -v kali-data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/kali-data.tar.gz -C /data
```

---

Continue to [Production Deployment](production.md) →
