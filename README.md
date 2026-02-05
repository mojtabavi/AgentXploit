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
- **OpenAI Integration**: GPT-4, GPT-3.5-turbo support
- **Counterfactual Reasoning**: Explores multiple attack paths
- **Group Knapsack Optimization**: Maximizes remediation effectiveness
- **RAG-Based Knowledge**: 15+ built-in pentesting entries
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

# Quick start examples
python quickstart.py
```

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
