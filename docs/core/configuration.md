# Configuration Guide

Complete reference for configuring PentestAI framework.

## Overview

PentestAIConfig is the central configuration dataclass that controls all aspects of the framework:

- **Pentest Module**: Vulnerability discovery settings
- **Remediation Module**: Optimal remediation planning
- **LLM Settings**: Model selection and parameters
- **Output Settings**: Results export and formatting
- **Safety Settings**: Sandbox mode and security controls

## Configuration Methods

### Method 1: Python Dictionary

```python
from pentestai import PentestAIController, PentestAIConfig

config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True,
    max_iterations=30,
    remediation_budget=50.0
)

controller = PentestAIController(config)
```

### Method 2: JSON File

```json
{
  "target": "192.168.1.100",
  "openai_api_key": "sk-...",
  "sandbox_mode": true,
  "max_iterations": 30,
  "remediation_budget": 50.0,
  "cost_weights": {
    "patch": 2.0,
    "reconfigure": 2.0,
    "monitor": 3.0
  }
}
```

```python
config = PentestAIConfig.from_json("config.json")
controller = PentestAIController(config)
```

### Method 3: Environment Variables

```bash
export TARGET=192.168.1.100
export OPENAI_API_KEY=sk-...
export SANDBOX_MODE=true
export MAX_ITERATIONS=30
```

```python
config = PentestAIConfig.from_env()
controller = PentestAIController(config)
```

## Complete Configuration Reference

### Pentest Module Settings

#### `target` (str, **required**)
Target system IP address, hostname, or URL.

```python
target="192.168.1.100"
target="testapp.example.com"
target="http://localhost:8080"
```

#### `max_iterations` (int, default: 50)
Maximum number of pentest iterations. Each iteration includes:
- Planning attack
- Executing command
- Summarizing output
- Extracting vulnerabilities

```python
max_iterations=30  # Faster, less thorough
max_iterations=50  # Balanced (recommended)
max_iterations=100 # Comprehensive, slower
```

#### `counterfactual_rounds` (int, default: 3)
Number of counterfactual reasoning rounds for Planner agent. Higher values explore more attack paths but take longer.

```python
counterfactual_rounds=1  # Single path
counterfactual_rounds=3  # Multiple paths (recommended)
counterfactual_rounds=5  # Extensive exploration
```

#### `use_instructor` (bool, default: True)
Enable RAG-based Instructor agent for contextual guidance.

```python
use_instructor=True  # Use knowledge base
use_instructor=False # Pure LLM reasoning
```

#### `knowledge_base_path` (str | None, default: None)
Path to custom knowledge base JSON file. If None, uses built-in knowledge.

```python
knowledge_base_path=None  # Built-in knowledge (15+ patterns)
knowledge_base_path="./custom_kb.json"  # Custom knowledge
```

### Remediation Module Settings

#### `remediation_budget` (float, default: 100.0)
Total budget for remediation strategies (arbitrary units).

```python
remediation_budget=50.0   # Low budget
remediation_budget=100.0  # Medium budget
remediation_budget=200.0  # High budget
```

#### `budget_per_vulnerability` (float, default: 4.0)
Default budget allocated per vulnerability for strategy generation.

```python
budget_per_vulnerability=2.0  # Few strategies per vuln
budget_per_vulnerability=4.0  # Balanced
budget_per_vulnerability=8.0  # Many strategies per vuln
```

#### `cost_weights` (dict, default: see below)
Cost multipliers for different remediation types. Lower = cheaper.

```python
cost_weights={
    "patch": 2.0,                  # Software updates
    "reconfigure": 2.0,            # Configuration changes
    "monitor": 3.0,                # Add monitoring
    "isolate": 5.0,                # Network isolation
    "compensating_control": 7.0,   # Alternative controls
    "shutdown_service": 10.0,      # Service shutdown
}
```

#### `enable_optimization` (bool, default: True)
Enable Group Knapsack optimization for optimal strategy selection.

```python
enable_optimization=True   # Optimal selection (recommended)
enable_optimization=False  # Select all proposed strategies
```

### LLM Settings

#### `openai_api_key` (str | None, **required for OpenAI**)
OpenAI API key or ArvanCloud token.

```python
openai_api_key="sk-..."  # OpenAI
openai_api_key="your-arvancloud-token"  # ArvanCloud
```

#### `openai_base_url` (str | None, default: None)
Custom API base URL for API-compatible providers.

```python
openai_base_url=None  # Use OpenAI default
openai_base_url="https://api.arvancloud.ir/llm/v1"  # ArvanCloud
```

#### `use_apikey_auth` (bool, default: False)
Add "apikey " prefix to authentication (required for ArvanCloud).

```python
use_apikey_auth=False  # Standard Bearer auth (OpenAI)
use_apikey_auth=True   # "apikey" prefix auth (ArvanCloud)
```

#### Model Selection

Each agent can use a different model for cost/performance optimization:

```python
# High-capability models for critical agents
planner_model="gpt-4"       # Attack planning
advisor_model="gpt-4"       # Remediation strategies

# Mid-tier models for balanced agents
executor_model="gpt-4"      # Command generation
evaluator_model="gpt-4"     # Strategy evaluation

# Fast models for utility agents
utility_model="gpt-3.5-turbo"  # Summarization, extraction
```

**Available Models**:
- `gpt-4`: Most capable, expensive
- `gpt-4-turbo`: Fast GPT-4, cost-effective
- `gpt-3.5-turbo`: Fast, cheap, good for utilities
- `gpt-4o`: OpenAI's optimized model

#### `temperature` (float, default: 0.7)
LLM sampling temperature. Lower = more deterministic.

```python
temperature=0.0  # Deterministic (reproducible)
temperature=0.7  # Balanced creativity
temperature=1.0  # Highly creative
```

#### `max_tokens` (int, default: 4096)
Maximum tokens per LLM request.

```python
max_tokens=2048  # Shorter responses
max_tokens=4096  # Balanced (recommended)
max_tokens=8192  # Long responses
```

### Output Settings

#### `output_directory` (str, default: "./pentestai_results")
Directory for all output files.

```python
output_directory="./results"
output_directory="/var/pentestai/results"
```

Generated files:
```
pentestai_results/
├── pentestai_results_20240206_123456.json
├── pentestai_report_20240206_123456.txt
└── attack_plan_20240206_123456.json
```

#### `save_attack_plan` (bool, default: True)
Save attack plan tree as JSON.

```python
save_attack_plan=True   # Save attack tree
save_attack_plan=False  # Skip attack tree
```

#### `save_execution_history` (bool, default: True)
Save complete command execution history.

```python
save_execution_history=True   # Full audit trail
save_execution_history=False  # Results only
```

#### `generate_report` (bool, default: True)
Generate human-readable text report.

```python
generate_report=True   # Generate TXT report
generate_report=False  # JSON only
```

#### `export_format` (str, default: "json")
Result export format.

```python
export_format="json"  # JSON (recommended)
export_format="csv"   # CSV tables
export_format="html"  # HTML report
```

### Safety Settings

#### `sandbox_mode` (bool, default: True)
**CRITICAL**: Simulate command execution instead of running real commands.

```python
sandbox_mode=True   # SAFE: Simulated execution
sandbox_mode=False  # DANGEROUS: Real execution via MCP
```

⚠️ **Always use `sandbox_mode=True` unless you have explicit authorization**

#### `use_mcp` (bool, default: False)
Use Kali MCP server for real tool execution.

```python
use_mcp=False  # Sandbox mode
use_mcp=True   # Real execution (requires mcp_server_url)
```

#### `mcp_server_url` (str, default: "http://localhost:5000")
Kali MCP server URL (only used if `use_mcp=True`).

```python
mcp_server_url="http://localhost:5000"
```

#### `require_confirmation` (bool, default: False)
Require user confirmation for high-risk operations.

```python
require_confirmation=False  # Auto-execute
require_confirmation=True   # Prompt before execution
```

#### `max_command_length` (int, default: 500)
Maximum allowed command length (safety limit).

```python
max_command_length=500
```

#### `blocked_commands` (list[str], default: [])
Patterns to block (safety filter).

```python
blocked_commands=["rm -rf", "dd if=", "mkfs"]
```

## Example Configurations

### Basic Safe Testing

```python
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True,  # SAFE
    max_iterations=20,
)
```

### Full Assessment (Simulated)

```python
config = PentestAIConfig(
    target="testapp.example.com",
    openai_api_key="sk-...",
    sandbox_mode=True,
    max_iterations=50,
    counterfactual_rounds=3,
    remediation_budget=100.0,
    save_attack_plan=True,
    generate_report=True,
)
```

### Real MCP Execution (AUTHORIZED ONLY)

```python
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=False,  # REAL EXECUTION
    use_mcp=True,
    mcp_server_url="http://localhost:5000",
    require_confirmation=True,
    max_iterations=30,
)
```

### ArvanCloud (Iranian AI Gateway)

```python
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="your-arvancloud-token",
    openai_base_url="https://api.arvancloud.ir/llm/v1",
    use_apikey_auth=True,  # Add "apikey" prefix
    planner_model="gpt-4",
    sandbox_mode=True,
)
```

### Cost-Optimized (Mixed Models)

```python
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    planner_model="gpt-4",           # Critical thinking
    advisor_model="gpt-4",           # Strategy generation
    executor_model="gpt-3.5-turbo",  # Command generation
    utility_model="gpt-3.5-turbo",   # Utilities
    sandbox_mode=True,
)
```

## Validation

Configuration is validated automatically before execution:

```python
config = PentestAIConfig(target="", openai_api_key=None)
controller = PentestAIController(config)

# Raises ValueError with specific errors:
# - Target cannot be empty
# - OpenAI API key required (or use mock mode)
controller.run_full_assessment()
```

Manual validation:

```python
errors = config.validate()
if errors:
    for error in errors:
        print(f"❌ {error}")
```

## Environment Variable Reference

All configuration options can be set via environment variables:

```bash
# Pentest Settings
export TARGET=192.168.1.100
export MAX_ITERATIONS=50
export COUNTERFACTUAL_ROUNDS=3
export USE_INSTRUCTOR=true
export KNOWLEDGE_BASE_PATH=./kb.json

# Remediation Settings
export REMEDIATION_BUDGET=100.0
export BUDGET_PER_VULNERABILITY=4.0
export ENABLE_OPTIMIZATION=true

# LLM Settings
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.arvancloud.ir/llm/v1
export USE_APIKEY_AUTH=true
export PLANNER_MODEL=gpt-4
export EXECUTOR_MODEL=gpt-4
export TEMPERATURE=0.7

# Output Settings
export OUTPUT_DIRECTORY=./results
export SAVE_ATTACK_PLAN=true
export GENERATE_REPORT=true
export EXPORT_FORMAT=json

# Safety Settings
export SANDBOX_MODE=true
export USE_MCP=false
export MCP_SERVER_URL=http://localhost:5000
export REQUIRE_CONFIRMATION=false
```

## Best Practices

1. **Always start with sandbox mode** for testing
2. **Use counterfactual reasoning** (3 rounds) for better coverage
3. **Enable Instructor agent** for RAG-based guidance
4. **Set realistic budgets** based on your remediation capacity
5. **Save attack plans** for vulnerability analysis
6. **Use mixed models** to optimize costs
7. **Validate config** before long-running assessments

## Troubleshooting

### Issue: "Target cannot be empty"
```python
# ❌ Wrong
config = PentestAIConfig(target="")

# ✅ Correct
config = PentestAIConfig(target="192.168.1.100")
```

### Issue: "OpenAI API key required"
```python
# ❌ Wrong
config = PentestAIConfig(target="...", openai_api_key=None)

# ✅ Correct
config = PentestAIConfig(target="...", openai_api_key="sk-...")
```

### Issue: ArvanCloud authentication fails
```python
# ❌ Wrong (missing apikey prefix)
config = PentestAIConfig(
    openai_api_key="token",
    openai_base_url="https://api.arvancloud.ir/llm/v1"
)

# ✅ Correct
config = PentestAIConfig(
    openai_api_key="token",
    openai_base_url="https://api.arvancloud.ir/llm/v1",
    use_apikey_auth=True  # Adds "apikey" prefix
)
```

---

Continue to [Python API Reference](../api/python-api.md) →
