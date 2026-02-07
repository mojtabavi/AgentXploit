# PentestAI Documentation

![Logo](https://img.shields.io/badge/PentestAI-v1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> **AI-Powered Penetration Testing & Optimal Remediation Framework**

PentestAI is a unified two-stage framework combining automated penetration testing with intelligent remediation planning, powered by Large Language Models (LLMs).

## 🎯 Overview

PentestAI implements a complete AI-driven security assessment workflow:

**Stage 1: Pentest Module** - Autonomous vulnerability discovery with 6 specialized agents
- **Planner:** Creates attack plans with counterfactual reasoning
- **Executor:** Generates and executes penetration testing commands
- **Instructor:** Provides RAG-based guidance from knowledge base
- **Summarizer:** Condenses command outputs for efficient processing
- **Extractor:** Parses and categorizes identified vulnerabilities
- **Monitor:** Tracks progress and handles error recovery

**Stage 2: Remediation Module** - Optimal remediation planning with 4 specialized agents
- **Estimator:** Assigns CVSS severity scores to vulnerabilities
- **Advisor:** Generates remediation strategies with counterfactual analysis
- **Evaluator:** Scores effectiveness and cost of remediation strategies
- **Optimizer:** Selects optimal strategies using Group Knapsack algorithm

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **10 Specialized LLM Agents** working in concert for comprehensive security assessment
- **Counterfactual Reasoning** to explore multiple attack/remediation paths
- **RAG-Based Knowledge** with 15+ built-in penetration testing patterns

### 🔧 Real Execution Capabilities
- **Kali Linux MCP Integration** for executing real penetration testing tools
- **50+ Pentesting Tools** including nmap, sqlmap, nikto, metasploit, hydra
- **Isolated Docker Execution** for safe command execution
- **Real-time Streaming** of command outputs and progress

### 🌐 Modern Interfaces
- **React Web UI** - ChatGPT-style interface with real-time streaming
- **FastAPI Backend** - High-performance API with SSE streaming
- **Interactive CLI** - Terminal-based interface for power users
- **Gradio UI** - Legacy full-featured interface

### 🔒 Security & Safety
- **Sandbox Mode** - Simulated execution for safe testing
- **MCP Mode** - Real execution in isolated Kali Linux container
- **Network Isolation** - Host network access for local pentesting
- **Comprehensive Logging** - Full audit trail of all operations

### 🚀 Flexible Deployment
- **Docker Compose** - One-command deployment of entire stack
- **Multi-Provider LLM** - OpenAI, ArvanCloud (Iranian AI Gateway)
- **Custom Configurations** - JSON/YAML config files or environment variables
- **Result Export** - JSON, CSV, HTML reports with attack plans

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PentestAI Controller                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
   ┌────────────────┐        ┌────────────────┐
   │ Pentest Module │        │ Remediation    │
   │   (Stage 1)    │───────▶│   Module       │
   │                │        │   (Stage 2)    │
   └────────────────┘        └────────────────┘
            │                         │
   ┌────────┴────────┐       ┌────────┴────────┐
   ▼        ▼       ▼       ▼       ▼       ▼
 Planner Executor Inst.  Estimator Advisor Eval.
              │                              │
   ┌──────────┴──────────┐      ┌───────────┼──────────┐
   ▼                     ▼      ▼           ▼          ▼
Summarizer          Extractor  Group    Knowledge   Report
                               Knapsack    Base    Generator
                               Optimizer
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- OpenAI API Key or ArvanCloud Token

### Installation

```bash
# Clone repository
git clone https://github.com/pentestai/pentestai.git
cd pentestai

# Set environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Using React UI (Recommended)

```bash
# Start all services
docker-compose up -d --build

# Access UI
# React UI:  http://localhost:3000
# API Docs:  http://localhost:8000/docs
# Gradio UI: http://localhost:7860
```

### Using Python API

```python
from pentestai import PentestAIController, PentestAIConfig

# Configure
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True,  # Always use for safety!
)

# Run assessment
controller = PentestAIController(config)
pentest_result, remediation_result = controller.run_full_assessment()

# View results
print(f"Vulnerabilities: {len(pentest_result.vulnerabilities)}")
print(f"Remediation Strategies: {len(remediation_result.selected_strategies)}")
```

### Using CLI

```bash
# Full assessment
python -m pentestai.cli --target 192.168.1.100 --mode full --sandbox

# Interactive mode
python pentestai_interactive.py
```

## 📚 Documentation Structure

This documentation covers:

- **[Getting Started](getting-started.md)** - Installation and first steps
- **[Architecture](architecture.md)** - System design and components
- **[Core Components](core/)** - Controller, Config, Modules
- **[Agents](agents/)** - Detailed agent documentation
- **[API Reference](api/)** - Python API and REST API
- **[Deployment](deployment/)** - Docker, Kubernetes, production
- **[Configuration](configuration.md)** - All configuration options
- **[Usage Examples](examples/)** - Code examples and tutorials
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Development](development.md)** - Contributing and extending

## 🎓 Based on Research

This framework implements the architecture described in:
- **PenHeal Paper**: [arXiv:2407.17788v1](https://arxiv.org/html/2407.17788v1)
- **PentestGPT**: Interactive penetration testing with LLMs

## ⚠️ Ethical Use

**This tool is for RESEARCH and AUTHORIZED TESTING ONLY.**

- Always use `sandbox_mode=True` unless you have explicit authorization
- Only test systems you own or have permission to test
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## 📄 License

MIT License - See [LICENSE.md](../LICENSE.md) for details

## 🤝 Contributing

Contributions welcome! See [Development Guide](development.md) for details.

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/pentestai/pentestai/issues)
- **Documentation**: [https://pentestai.io/docs](https://pentestai.io/docs)
- **Discord**: [Join Community](https://discord.gg/pentestai)

---

Made with ❤️ by the PentestAI Team
