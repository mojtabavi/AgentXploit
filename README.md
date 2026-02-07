# PentestAI - Unified Penetration Testing & Remediation Framework

<div align="center">

**🔒 Automated AI-Powered Penetration Testing & Optimal Remediation Planning**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Unified framework combining PentestGPT and PenHeal*

</div>

## 🎯 Overview

**PentestAI** is a complete two-stage framework for automated penetration testing and intelligent remediation planning, powered by OpenAI's GPT models.

- **Stage 1: Pentest Module** - Automated vulnerability discovery with 6 specialized agents
- **Stage 2: Remediation Module** - Optimal remediation planning with 4 specialized agents

Based on the academic paper: [PenHeal (arXiv:2407.17788v1)](https://arxiv.org/html/2407.17788v1)

## ✨ Key Features

- **10 Specialized LLM Agents**: 6 for pentesting + 4 for remediation
- **🆕 React Web UI**: Real-time streaming ChatGPT-style interface
- **🆕 Kali Linux MCP Integration**: Real pentest execution with 50+ tools
- **OpenAI + ArvanCloud**: Support for multiple AI providers
- **Counterfactual Reasoning**: Explores multiple attack paths
- **Group Knapsack Optimization**: Maximizes remediation effectiveness
- **RAG-Based Knowledge**: 15+ built-in pentesting entries
- **Docker Support**: Fully containerized with MCP orchestration
- **Interactive CLI**: User-friendly menu-based interface
- **Sandbox Mode**: Safe simulated execution by default

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install openai pydantic python-dotenv

# Set API key
export OPENAI_API_KEY="sk-your-api-key-here"
```

### Basic Usage

```python
from pentestai import PentestAIController, PentestAIConfig

config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True,
)

controller = PentestAIController(config)
pentest_result, remediation_result = controller.run_full_assessment()

print(f"Vulnerabilities: {len(pentest_result.vulnerabilities)}")
print(f"Strategies: {len(remediation_result.selected_strategies)}")
```

### CLI Usage

```bash
# Full assessment
python -m pentestai.cli --target 192.168.1.100 --mode full --sandbox

# Interactive CLI
python pentestai_interactive.py

# With Docker and Kali MCP
docker-compose up

# React Web UI (Recommended)
# See setup guide below
```

### 🌐 React Web UI (NEW!)

Modern, real-time streaming interface with ChatGPT-style design:

```bash
# Quick start (Windows)
.\start_react_ui.ps1

# Quick start (Linux/Mac)
chmod +x start_react_ui.sh
./start_react_ui.sh

# Access the UI
# React UI:  http://localhost:3000 (Main interface)
# API Docs:  http://localhost:8000/docs
# Documentation: http://localhost:3001 (Docsify docs)
# Gradio UI: http://localhost:7860 (Legacy)
```

## 📚 Documentation

**Comprehensive documentation is now available with Docsify!**

### Start Documentation Server

```bash
# With Docker (Recommended)
docker-compose up -d pentestai-docs
# Access at: http://localhost:3001

# Or manually without Docker
# Windows
.\start_docs.ps1

# Linux/Mac
chmod +x start_docs.sh
./start_docs.sh

# Or manually
cd docs
npx docsify-cli serve --port 3001
```

**📖 Access documentation at: http://localhost:3001**

### Documentation Contents

- **[Getting Started](docs/getting-started.md)** - Installation, configuration, and your first pentest
- **[Architecture Overview](docs/architecture.md)** - System design, data flow, and technology stack
- **[Core Components](docs/core/)** - Controller, Configuration, Modules documented in detail
- **[10 Specialized Agents](docs/agents/)** - Complete agent documentation with prompts and workflows
- **[API Reference](docs/api/)** - Python API and REST API with examples
- **[Deployment Guide](docs/deployment/)** - Docker, Docker Compose, and production setup
- **[Usage Examples](docs/examples/)** - Full code examples and tutorials
- **[Configuration Guide](docs/core/configuration.md)** - All 50+ configuration options
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

**Features:**
- ✅ Real-time streaming with Server-Sent Events
- ✅ Connection status indicators
- ✅ LLM health checks at every step
- ✅ Dark theme with gradient design
- ✅ Simple configuration (target + mode)
- ✅ No API key inputs (configured via .env)
- ✅ Kali Linux network access for local pentesting

**Setup Guide:** [REACT_UI_SETUP.md](REACT_UI_SETUP.md)

## 📖 Documentation

**Quick Start Guides:**
- **[REACT_UI_SETUP.md](REACT_UI_SETUP.md)** - 🆕 React UI setup & usage (Recommended)
- **[KALI_MCP_QUICKSTART.md](KALI_MCP_QUICKSTART.md)** - 🆕 Kali MCP quick start (5 min)
- **[ARVANCLOUD_GUIDE.md](ARVANCLOUD_GUIDE.md)** - 🆕 Iranian AI Gateway integration
- **[UI_QUICKSTART.md](UI_QUICKSTART.md)** - Gradio UI guide (Legacy)

**Complete Documentation:**
- **[KALI_MCP_INTEGRATION.md](KALI_MCP_INTEGRATION.md)** - Complete Kali MCP guide
- **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** - Docker quick reference
- **[DOCKER_USAGE.md](DOCKER_USAGE.md)** - Complete Docker guide
- **[PENTESTAI_README.md](PENTESTAI_README.md)** - Framework documentation
- **[PENTESTAI_SUMMARY.md](PENTESTAI_SUMMARY.md)** - Architecture details

**Code Examples:**
- **[quickstart.py](quickstart.py)** - Basic usage examples
- **[example_kali_mcp.py](example_kali_mcp.py)** - 🆕 MCP usage examples

## 🐉 Kali Linux MCP Integration (NEW!)

Execute **real** penetration testing commands via Kali Linux container:

```bash
# Start with Kali MCP
docker-compose up

# Automatic features:
# ✓ 50+ Kali tools (nmap, sqlmap, nikto, metasploit, hydra...)
# ✓ Isolated Docker execution
# ✓ Tool discovery and suggestions
# ✓ Real-time command execution
```

**Quick Links:**
- [KALI_MCP_QUICKSTART.md](KALI_MCP_QUICKSTART.md) - Get started in 5 minutes
- [KALI_MCP_INTEGRATION.md](KALI_MCP_INTEGRATION.md) - Complete guide
- [example_kali_mcp.py](example_kali_mcp.py) - Usage examples

## 📚 Documentation

- **[PENTESTAI_README.md](PENTESTAI_README.md)** - Complete documentation
- **[PENTESTAI_SUMMARY.md](PENTESTAI_SUMMARY.md)** - Architecture & implementation details
- **[quickstart.py](quickstart.py)** - Usage examples with OpenAI

## 🛡️ Safety & Ethics

⚠️ **ALWAYS use `sandbox_mode=True`** unless you have explicit authorization!

This framework is for:
- Research and education
- Authorized penetration testing
- Controlled security assessment

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md)

---

For detailed documentation, see [PENTESTAI_README.md](PENTESTAI_README.md)
