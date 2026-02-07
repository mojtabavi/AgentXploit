# Docker Services Overview

Complete overview of all Docker services in PentestAI.

## Services Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Docker Services                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐│
│  │  React UI       │  │  API Server     │  │  Documentation   ││
│  │  Port: 3000     │  │  Port: 8000     │  │  Port: 3001      ││
│  │  pentestai-ui   │  │  pentestai-api  │  │  pentestai-docs  ││
│  └────────┬────────┘  └────────┬────────┘  └────────┬─────────┘│
│           │                    │                     │           │
│           └────────────────────┴─────────────────────┘           │
│                                │                                 │
│                     Bridge Network (172.30.0.0/24)              │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                                 │
                                 │ host.docker.internal
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Host Network                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Kali MCP Server                                          │  │
│  │  Port: 5000 (on host)                                     │  │
│  │  kali-mcp-server                                          │  │
│  │  50+ penetration testing tools                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Service Details

### 1. pentestai-react-ui

**Modern React Web Interface**

- **Container:** `pentestai-react-ui`
- **Port:** 3000 → http://localhost:3000
- **Technology:** React 18 + Vite + Bun
- **Features:**
  - ChatGPT-style interface
  - Real-time streaming
  - Markdown rendering with syntax highlighting
  - Connection status monitoring
  - Target configuration
  - Mode selection (Full/Pentest only)

**Build:**
```bash
docker-compose build pentestai-react-ui
docker-compose up -d pentestai-react-ui
```

**Logs:**
```bash
docker logs -f pentestai-react-ui
```

### 2. pentestai-api

**FastAPI Backend Server**

- **Container:** `pentestai-api`
- **Port:** 8000 → http://localhost:8000
- **Technology:** FastAPI + Uvicorn
- **Features:**
  - REST API with SSE streaming
  - LLM integration (OpenAI/ArvanCloud)
  - MCP client for Kali tools
  - Health check endpoint
  - Automatic API documentation

**Endpoints:**
- `GET /api/health` - Health check
- `POST /api/pentest/stream` - Start pentest with streaming
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc UI

**Build:**
```bash
docker-compose build pentestai-api
docker-compose up -d pentestai-api
```

**Environment Variables:**
```bash
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=
ARVANCLOUD_API_KEY=
LLM_MODEL=gpt-4
KALI_MCP_URL=http://host.docker.internal:5000
```

### 3. pentestai-docs

**Documentation Interface** ✨ NEW!

- **Container:** `pentestai-docs`
- **Port:** 3001 → http://localhost:3001
- **Technology:** Docsify + Node.js
- **Features:**
  - Full documentation with search
  - Syntax highlighting
  - Mobile responsive
  - Copy code buttons
  - Purple gradient theme

**Contents:**
- Getting Started guide
- Architecture overview
- Complete API reference
- Configuration guide (50+ options)
- Deployment instructions
- Troubleshooting guide
- Full code examples

**Build:**
```bash
docker-compose build pentestai-docs
docker-compose up -d pentestai-docs
```

### 4. kali-mcp-server

**Official Kali Linux MCP Server**

- **Container:** `kali-mcp-server`
- **Port:** 5000 (host network)
- **Technology:** Official Kali package
- **Network:** Host mode (for local network access)
- **Features:**
  - 50+ penetration testing tools
  - Real command execution
  - MCP protocol support
  - Tool discovery

**Available Tools:**
- nmap (network scanning)
- sqlmap (SQL injection)
- nikto (web vulnerability scanner)
- metasploit (exploitation framework)
- hydra (password cracking)
- dirb (directory brute-force)
- gobuster (directory enumeration)
- And 40+ more...

**Build:**
```bash
docker-compose build kali-mcp-server
docker-compose up -d kali-mcp-server
```

**Health Check:**
```bash
curl http://localhost:5000/health
```

## Quick Commands

### Start All Services

```bash
# Build and start everything
docker-compose up -d --build

# Start without rebuilding
docker-compose up -d

# Start specific service
docker-compose up -d pentestai-api
```

### Check Status

```bash
# View all services
docker-compose ps

# Expected output:
# NAME                 STATUS              PORTS
# kali-mcp-server      Up (healthy)        (host network)
# pentestai-api        Up (healthy)        0.0.0.0:8000->8000/tcp
# pentestai-docs       Up                  0.0.0.0:3001->3001/tcp
# pentestai-react-ui   Up                  0.0.0.0:3000->3000/tcp

# Check health
docker-compose ps | grep "(healthy)"
```

### View Logs

```bash
# All services
docker-compose logs

# Follow all logs
docker-compose logs -f

# Specific service
docker-compose logs pentestai-api

# Follow specific service
docker-compose logs -f pentestai-api

# Last 100 lines
docker-compose logs --tail=100
```

### Stop Services

```bash
# Stop all
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

# Restart specific service
docker-compose restart pentestai-api
```

### Rebuild Services

```bash
# Rebuild all
docker-compose build

# Rebuild specific service
docker-compose build pentestai-api

# Rebuild and start
docker-compose up -d --build
```

## Resource Usage

### Default Limits

```yaml
pentestai-api:
  limits:
    cpus: '2'
    memory: 4G
  reservations:
    cpus: '1'
    memory: 2G

kali-mcp-server:
  limits:
    cpus: '4'
    memory: 8G
  reservations:
    cpus: '2'
    memory: 4G
```

### Monitor Resources

```bash
# View resource usage
docker stats

# Specific container
docker stats pentestai-api
```

## Port Mapping

| Service | Internal Port | External Port | URL |
|---------|--------------|---------------|-----|
| React UI | 3000 | 3000 | http://localhost:3000 |
| API Server | 8000 | 8000 | http://localhost:8000 |
| Documentation | 3001 | 3001 | http://localhost:3001 |
| Kali MCP | 5000 | 5000 | http://localhost:5000 |

## Network Configuration

### Bridge Network

- **Name:** `pentestai-network`
- **Subnet:** 172.30.0.0/24
- **Gateway:** 172.30.0.1
- **Services:** pentestai-react-ui, pentestai-api, pentestai-docs

### Host Network

- **Service:** kali-mcp-server
- **Reason:** Needs access to local network for pentesting
- **Connection:** Other services use `host.docker.internal:5000`

## Volumes

```bash
# View volumes
docker volume ls | grep pentestai

# Inspect volume
docker volume inspect pentestai_pentestai-results

# Backup results
docker cp pentestai-api:/app/pentestai_results ./backup/
```

### Volume Mounts

| Service | Volume | Purpose |
|---------|--------|---------|
| pentestai-api | `./pentestai_results:/app/pentestai_results` | Pentest results |
| kali-mcp-server | `./kali_results:/opt/kali-mcp-server/results` | Command outputs |
| pentestai-react-ui | `./ui:/app` | Hot reload (dev) |
| pentestai-docs | `./docs:/docs` | Hot reload docs |

## Health Checks

### API Server

```bash
curl http://localhost:8000/api/health

# Expected:
# {"status":"ok","llm_connected":true,"llm_model":"gpt-4"}
```

### Kali MCP

```bash
curl http://localhost:5000/health

# Expected:
# {"status":"healthy","tools_count":50}
```

### React UI

```bash
curl http://localhost:3000

# Should return HTML
```

### Documentation

```bash
curl http://localhost:3001

# Should return Docsify HTML
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs pentestai-api

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Port Conflict

```bash
# Check what's using port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Container Unhealthy

```bash
# Check health
docker-compose ps

# Restart unhealthy service
docker-compose restart kali-mcp-server

# Check logs
docker logs kali-mcp-server
```

### Network Issues

```bash
# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

## Production Deployment

### Security Hardening

```yaml
# Run as non-root
user: "1000:1000"

# Read-only filesystem
read_only: true

# Drop capabilities
cap_drop:
  - ALL

# No new privileges
security_opt:
  - no-new-privileges:true
```

### Use Secrets

```yaml
secrets:
  openai_api_key:
    external: true

services:
  pentestai-api:
    secrets:
      - openai_api_key
```

### Enable HTTPS

Use nginx reverse proxy:

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
```

---

**All services documented!** Return to [Docker Deployment Guide](docker.md) →
