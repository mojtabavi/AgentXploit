# Getting Started

This guide will help you get PentestAI up and running in minutes.

## Prerequisites

Before you begin, make sure you have:

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Python** 3.9+ (if running locally without Docker)
- **Git** for cloning the repository
- **OpenAI API Key** or **ArvanCloud Token** for LLM access

## Installation

### Option 1: Docker (Recommended)

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/pentestai/pentestai.git
cd pentestai

# Copy environment template
cp .env.example .env

# Edit .env with your API key
nano .env
# Add: OPENAI_API_KEY=sk-your-key-here
# Or:  ARVANCLOUD_API_KEY=your-arvancloud-key

# Start all services
docker-compose up -d --build

# Check service status
docker-compose ps
```

This will start three services:

- **React UI**: http://localhost:3000 (Modern ChatGPT-style interface)
- **API Server**: http://localhost:8000 (FastAPI backend with streaming)
- **Kali MCP Server**: http://localhost:5000 (Penetration testing tools)

### Option 2: Local Python Installation

For development or if you prefer not to use Docker:

```bash
# Clone repository
git clone https://github.com/pentestai/pentestai.git
cd pentestai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Set environment variables
export OPENAI_API_KEY=sk-your-key-here

# Run interactive CLI
python pentestai_interactive.py
```

## Configuration

### Environment Variables

Create a `.env` file or set these environment variables:

```bash
# Required: LLM Provider
OPENAI_API_KEY=sk-your-key-here
# Or for ArvanCloud (Iranian AI Gateway):
ARVANCLOUD_API_KEY=your-arvancloud-key

# Optional: Override default settings
PENTEST_MODEL=gpt-4o
REMEDIATION_MODEL=gpt-4
TARGET_URL=http://192.168.1.100
SANDBOX_MODE=true
```

### Configuration File

Alternatively, create a JSON config file:

```json
{
  "target": "192.168.1.100",
  "openai_api_key": "sk-...",
  "sandbox_mode": true,
  "pentest_model": "gpt-4o",
  "max_rounds": 5,
  "enable_remediation": true,
  "output_dir": "./results"
}
```

## Your First Pentest

### Using React UI (Easiest)

1. Navigate to http://localhost:3000
2. Check that "Connection Status" shows "Connected"
3. Enter target: `192.168.1.100`
4. Select mode: `Full Assessment`
5. Click "Start Pentest"
6. Watch real-time streaming results!

### Using Python API

```python
from pentestai import PentestAIController, PentestAIConfig

# Always use sandbox mode for safety!
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True,  # IMPORTANT: Simulated execution
    max_rounds=3
)

# Create controller
controller = PentestAIController(config)

# Run full assessment (Pentest + Remediation)
pentest_result, remediation_result = controller.run_full_assessment()

# View results
print(f"✅ Found {len(pentest_result.vulnerabilities)} vulnerabilities")
print(f"✅ Generated {len(remediation_result.selected_strategies)} remediation strategies")

# Show top vulnerability
if pentest_result.vulnerabilities:
    vuln = pentest_result.vulnerabilities[0]
    print(f"\n🔴 {vuln.name}")
    print(f"   Severity: {vuln.severity}")
    print(f"   Description: {vuln.description}")

# Show optimal remediation
if remediation_result.selected_strategies:
    strategy = remediation_result.selected_strategies[0]
    print(f"\n🛠️ {strategy.name}")
    print(f"   Cost: {strategy.cost}")
    print(f"   Effectiveness: {strategy.effectiveness}")
```

### Using Interactive CLI

```bash
# Start interactive session
python pentestai_interactive.py

# Follow prompts:
> Target: 192.168.1.100
> Mode: full
> Sandbox: yes
> Max Rounds: 5
```

### Using Command-Line Interface

```bash
# Full assessment with sandbox mode
python -m pentestai.cli \
    --target 192.168.1.100 \
    --mode full \
    --sandbox \
    --max-rounds 5

# Pentest only
python -m pentestai.cli \
    --target 192.168.1.100 \
    --mode scan_only \
    --sandbox

# From config file
python -m pentestai.cli --config config.json
```

## Understanding Results

After running a pentest, you'll find results in `pentestai_results/`:

```
pentestai_results/
├── pentestai_results_YYYYMMDD_HHMMSS.json  # Full results
├── pentestai_report_YYYYMMDD_HHMMSS.txt     # Human-readable report
└── attack_plan_YYYYMMDD_HHMMSS.json         # Attack tree visualization
```

### Result Structure

**PentestResult** contains:
- `vulnerabilities[]`: List of discovered vulnerabilities
- `attack_plan`: Tree structure of attack paths
- `commands_executed[]`: All commands run (sandbox or real)
- `thoughts[]`: Agent reasoning at each step

**RemediationResult** contains:
- `selected_strategies[]`: Optimal remediation strategies (Group Knapsack solution)
- `all_strategies[]`: All proposed strategies
- `severity_groups{}`: Vulnerabilities grouped by CVSS score
- `optimization_score`: Total effectiveness/cost ratio

## Safety First

⚠️ **Critical Safety Guidelines**:

1. **Always start with `sandbox_mode=True`** for testing
2. **Only test systems you own or have permission to test**
3. **MCP mode executes REAL commands** - use with caution
4. **Local network access required** for MCP mode (host network)
5. **No production systems** - PentestAI is for research and authorized testing

### Sandbox vs MCP Mode

**Sandbox Mode** (Safe):
```python
config = PentestAIConfig(
    target="192.168.1.100",
    sandbox_mode=True,  # Simulated execution
)
```

**MCP Mode** (Real Execution):
```python
config = PentestAIConfig(
    target="192.168.1.100",
    sandbox_mode=False,  # REAL commands executed!
    mcp_server_url="http://localhost:5000",  # Kali MCP server
)
```

## Troubleshooting

### Docker Issues

**Container not starting**:
```bash
# Check logs
docker-compose logs pentestai-api
docker-compose logs kali-mcp-server

# Rebuild
docker-compose down -v
docker-compose up -d --build
```

**Port already in use**:
```bash
# Find process
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # Linux/Mac

# Or change port in docker-compose.yml
```

### LLM Connection Issues

**OpenAI API Error**:
- Verify API key in `.env` file
- Check balance: https://platform.openai.com/usage
- Test connection: http://localhost:8000/api/health

**ArvanCloud Gateway**:
```bash
# ArvanCloud uses different auth format
ARVANCLOUD_API_KEY=your-key
# API will automatically add "apikey " prefix
```

### UI Not Loading

**React UI blank screen**:
```bash
# Check logs
docker logs pentestai-react-ui

# Rebuild UI container
docker-compose up -d --build pentestai-react-ui
```

**API not responding**:
```bash
# Test API health
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","llm_model":"gpt-4","version":"1.0.0"}
```

## Next Steps

Now that you have PentestAI running:

1. **Explore the Architecture** - Learn about the [Two-Stage Framework](two-stage-framework.md)
2. **Deep Dive into Agents** - Understand how [10 specialized agents](agent-system.md) work together
3. **Advanced Configuration** - Customize behavior with [configuration options](core/configuration.md)
4. **Production Deployment** - Set up [production-ready deployment](deployment/production.md)
5. **Contribute** - Join development with our [contributing guide](development/contributing.md)

## Quick Reference

| Task | Command |
|------|---------|
| Start all services | `docker-compose up -d --build` |
| Access React UI | http://localhost:3000 |
| Access API docs | http://localhost:8000/docs |
| View logs | `docker-compose logs -f` |
| Stop services | `docker-compose down` |
| Full rebuild | `docker-compose down -v && docker-compose up -d --build` |
| Interactive CLI | `python pentestai_interactive.py` |
| Command-line | `python -m pentestai.cli --help` |

## Need Help?

- 📖 **Documentation**: Browse the [full documentation](/)
- 🐞 **Issues**: Report bugs on [GitHub Issues](https://github.com/pentestai/pentestai/issues)
- 💬 **Discord**: Join our [community](https://discord.gg/pentestai)
- 📧 **Email**: support@pentestai.io

---

Ready to explore? Continue to [Architecture Overview](architecture.md) →
