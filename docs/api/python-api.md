# Python API Reference

Complete Python API documentation for PentestAI framework.

## Quick Start

```python
from pentestai import PentestAIController, PentestAIConfig

# Configure
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True
)

# Create controller
controller = PentestAIController(config)

# Run assessment
pentest_result, remediation_result = controller.run_full_assessment()
```

## Core Classes

### PentestAIController

Main orchestrator for the framework.

#### Constructor

```python
PentestAIController(config: PentestAIConfig)
```

**Parameters:**
- `config` (PentestAIConfig): Configuration object

**Example:**
```python
config = PentestAIConfig(target="192.168.1.100", openai_api_key="sk-...")
controller = PentestAIController(config)
```

#### Methods

##### `run_full_assessment()`

Run complete two-stage assessment (pentest + remediation).

```python
def run_full_assessment() -> tuple[PentestResult, RemediationResult]
```

**Returns:**
- `tuple[PentestResult, RemediationResult]`: Results from both stages

**Raises:**
- `ValueError`: If configuration is invalid

**Example:**
```python
pentest_result, remediation_result = controller.run_full_assessment()

print(f"Vulnerabilities: {len(pentest_result.vulnerabilities)}")
print(f"Strategies: {len(remediation_result.selected_strategies)}")
```

##### `run_pentest_only()`

Run only Stage 1 (penetration testing).

```python
def run_pentest_only() -> PentestResult
```

**Returns:**
- `PentestResult`: Vulnerability discovery results

**Example:**
```python
pentest_result = controller.run_pentest_only()

for vuln in pentest_result.vulnerabilities:
    print(f"🔴 {vuln.name} - {vuln.severity}")
```

##### `run_remediation_only(vulnerabilities)`

Run only Stage 2 (remediation planning).

```python
def run_remediation_only(vulnerabilities: list[Vulnerability]) -> RemediationResult
```

**Parameters:**
- `vulnerabilities` (list[Vulnerability]): List of vulnerabilities to remediate

**Returns:**
- `RemediationResult`: Optimal remediation strategies

**Example:**
```python
# Load vulnerabilities from previous run
vulnerabilities = load_vulnerabilities("results.json")

# Generate remediation
remediation_result = controller.run_remediation_only(vulnerabilities)
```

### PentestAIConfig

Configuration dataclass.

#### Constructor

```python
PentestAIConfig(
    target: str = "",
    openai_api_key: Optional[str] = None,
    sandbox_mode: bool = True,
    # ... 40+ more options
)
```

**Key Parameters:**
- `target`: Target system (IP/hostname/URL)
- `openai_api_key`: OpenAI API key or ArvanCloud token
- `sandbox_mode`: Safe simulation mode (default: True)
- `max_iterations`: Max pentest rounds (default: 50)
- `remediation_budget`: Budget for remediation (default: 100.0)

**See:** [Complete Configuration Guide](../core/configuration.md)

#### Class Methods

##### `from_json(path)`

Load configuration from JSON file.

```python
@classmethod
def from_json(cls, path: str) -> PentestAIConfig
```

**Example:**
```python
config = PentestAIConfig.from_json("config.json")
```

##### `from_dict(data)`

Create configuration from dictionary.

```python
@classmethod
def from_dict(cls, data: dict) -> PentestAIConfig
```

**Example:**
```python
config = PentestAIConfig.from_dict({
    "target": "192.168.1.100",
    "sandbox_mode": True,
})
```

##### `from_env()`

Load configuration from environment variables.

```python
@classmethod
def from_env(cls) -> PentestAIConfig
```

**Example:**
```python
# With environment variables set:
# export TARGET=192.168.1.100
# export OPENAI_API_KEY=sk-...
config = PentestAIConfig.from_env()
```

#### Instance Methods

##### `validate()`

Validate configuration.

```python
def validate() -> list[str]
```

**Returns:**
- `list[str]`: List of validation errors (empty if valid)

**Example:**
```python
errors = config.validate()
if errors:
    for error in errors:
        print(f"❌ {error}")
```

##### `to_dict()`

Convert to dictionary.

```python
def to_dict() -> dict[str, Any]
```

**Example:**
```python
config_dict = config.to_dict()
print(json.dumps(config_dict, indent=2))
```

## Data Models

### Vulnerability

Represents a discovered vulnerability.

```python
@dataclass
class Vulnerability:
    id: str
    name: str
    description: str
    severity: VulnerabilitySeverity
    cvss_score: float
    cve_id: Optional[str]
    service: str
    port: Optional[int]
    exploit_method: str
    discovered_at: datetime
    metadata: dict[str, Any]
```

**Example:**
```python
vuln = Vulnerability(
    name="SQL Injection in login form",
    description="Unsanitized input allows SQL injection",
    severity=VulnerabilitySeverity.HIGH,
    cvss_score=8.5,
    service="web",
    port=80,
    exploit_method="sqlmap"
)

print(f"{vuln.name} - CVSS {vuln.cvss_score}")
```

**Methods:**
- `to_dict()`: Convert to dictionary

### VulnerabilitySeverity

CVSS-based severity levels.

```python
class VulnerabilitySeverity(str, Enum):
    CRITICAL = "CRITICAL"  # 9.0-10.0
    HIGH = "HIGH"          # 7.0-8.9
    MEDIUM = "MEDIUM"      # 4.0-6.9
    LOW = "LOW"            # 0.1-3.9
    INFO = "INFO"          # 0.0
```

### RemediationStrategy

Represents a remediation strategy.

```python
@dataclass
class RemediationStrategy:
    id: str
    vulnerability_id: str
    name: str
    description: str
    remediation_type: RemediationType
    cost: float
    effectiveness: float
    implementation_time: str
    required_skills: list[str]
    metadata: dict[str, Any]
```

**Example:**
```python
strategy = RemediationStrategy(
    vulnerability_id="vuln-123",
    name="Apply CVE-2024-1234 patch",
    description="Update to version 2.5.1",
    remediation_type=RemediationType.PATCH,
    cost=5.0,
    effectiveness=0.95,
    implementation_time="2 hours",
    required_skills=["system_admin"]
)
```

### RemediationType

Types of remediation strategies.

```python
class RemediationType(str, Enum):
    PATCH = "patch"
    RECONFIGURE = "reconfigure"
    MONITOR = "monitor"
    ISOLATE = "isolate"
    COMPENSATING_CONTROL = "compensating_control"
```

### PentestResult

Result from Stage 1 (Pentest Module).

```python
@dataclass
class PentestResult:
    vulnerabilities: list[Vulnerability]
    attack_plan: AttackPlanNode
    commands_executed: list[ExecutedCommand]
    statistics: dict[str, Any]
    metadata: dict[str, Any]
```

**Example:**
```python
pentest_result = controller.run_pentest_only()

print(f"Vulnerabilities: {len(pentest_result.vulnerabilities)}")
print(f"Commands: {len(pentest_result.commands_executed)}")
print(f"Duration: {pentest_result.statistics['duration_seconds']}s")

# Export to JSON
pentest_result.to_json("results.json")
```

**Methods:**
- `to_dict()`: Convert to dictionary
- `to_json(path)`: Save to JSON file

### RemediationResult

Result from Stage 2 (Remediation Module).

```python
@dataclass
class RemediationResult:
    selected_strategies: list[RemediationStrategy]
    all_strategies: list[RemediationStrategy]
    severity_groups: dict[str, list[Vulnerability]]
    optimization_score: float
    statistics: dict[str, Any]
```

**Example:**
```python
remediation_result = controller.run_remediation_only(vulnerabilities)

print(f"Selected: {len(remediation_result.selected_strategies)}")
print(f"Total proposed: {len(remediation_result.all_strategies)}")
print(f"Optimization score: {remediation_result.optimization_score:.2f}")

# Show selected strategies
for strategy in remediation_result.selected_strategies:
    print(f"✅ {strategy.name} - Cost: {strategy.cost}, Effectiveness: {strategy.effectiveness:.2%}")
```

## Modules

### PentestModule

Stage 1: Vulnerability discovery.

```python
from pentestai.core.pentest_module import PentestModule

module = PentestModule(config, llm_clients)
result = module.run_pentest(target="192.168.1.100")
```

**Methods:**
- `run_pentest(target: str) -> PentestResult`

### RemediationModule

Stage 2: Optimal remediation planning.

```python
from pentestai.core.remediation_module import RemediationModule

module = RemediationModule(config, llm_clients)
result = module.run_remediation(vulnerabilities)
```

**Methods:**
- `run_remediation(vulnerabilities: list[Vulnerability]) -> RemediationResult`

## LLM Clients

### OpenAIClient

OpenAI API client.

```python
from pentestai.llm.client import OpenAIClient

client = OpenAIClient(
    api_key="sk-...",
    model="gpt-4",
    base_url=None,  # Optional custom URL
    use_apikey_auth=False
)

response = client.generate(
    messages=[
        {"role": "system", "content": "You are a penetration tester"},
        {"role": "user", "content": "Scan target 192.168.1.100"}
    ],
    temperature=0.7
)

print(response)
```

**Methods:**
- `generate(messages, temperature=0.7, max_tokens=4096) -> str`
- `stream(messages) -> Generator[str, None, None]`

### MockLLMClient

Mock client for testing (no API key required).

```python
from pentestai.llm.client import MockLLMClient

client = MockLLMClient()
response = client.generate([...])  # Returns simulated response
```

## MCP Integration

### MCPClient

Kali MCP server client.

```python
from pentestai.mcp.client import MCPClient

client = MCPClient(server_url="http://localhost:5000")

# Discover tools
tools = client.list_tools()
print(f"Available tools: {len(tools)}")

# Execute command
result = client.execute_tool(
    tool_name="nmap",
    arguments={"target": "192.168.1.100", "flags": "-sV"}
)

print(result["output"])
```

**Methods:**
- `list_tools() -> list[dict]`
- `execute_tool(tool_name: str, arguments: dict) -> dict`
- `get_tool_schema(tool_name: str) -> dict`

## Utilities

### Knowledge Base

Access built-in penetration testing knowledge.

```python
from pentestai.knowledge.base import KnowledgeBase

kb = KnowledgeBase()

# Get pattern for SQL injection
sql_pattern = kb.get_pattern("sql_injection")
print(f"Tools: {sql_pattern['tools']}")
print(f"Examples: {sql_pattern['examples']}")

# Search knowledge base
results = kb.search("XSS vulnerability")
```

### Result Export

```python
# Export as JSON
pentest_result.to_json("results.json")

# Export as CSV
pentest_result.to_csv("vulnerabilities.csv")

# Generate HTML report
controller.generate_report(pentest_result, remediation_result, "report.html")
```

## Complete Example

```python
#!/usr/bin/env python3
"""Complete PentestAI workflow example."""

from pentestai import PentestAIController, PentestAIConfig
from pentestai.models.data import VulnerabilitySeverity

# 1. Configure
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-...",
    sandbox_mode=True,
    max_iterations=30,
    counterfactual_rounds=3,
    remediation_budget=100.0,
    save_attack_plan=True,
    generate_report=True
)

# 2. Initialize controller
controller = PentestAIController(config)

# 3. Run full assessment
print("Starting assessment...")
pentest_result, remediation_result = controller.run_full_assessment()

# 4. Analyze vulnerabilities
print(f"\n{'='*60}")
print("VULNERABILITIES FOUND")
print('='*60)

critical = [v for v in pentest_result.vulnerabilities if v.severity == VulnerabilitySeverity.CRITICAL]
high = [v for v in pentest_result.vulnerabilities if v.severity == VulnerabilitySeverity.HIGH]

print(f"Critical: {len(critical)}")
print(f"High: {len(high)}")
print(f"Total: {len(pentest_result.vulnerabilities)}")

# 5. Show top vulnerabilities
for vuln in sorted(pentest_result.vulnerabilities, key=lambda v: v.cvss_score, reverse=True)[:5]:
    print(f"\n🔴 {vuln.name}")
    print(f"   Severity: {vuln.severity.value}")
    print(f"   CVSS: {vuln.cvss_score}")
    print(f"   Service: {vuln.service}")
    print(f"   Method: {vuln.exploit_method}")

# 6. Show selected remediation strategies
print(f"\n{'='*60}")
print("RECOMMENDED REMEDIATION")
print('='*60)

for strategy in remediation_result.selected_strategies[:10]:
    print(f"\n✅ {strategy.name}")
    print(f"   Type: {strategy.remediation_type.value}")
    print(f"   Cost: {strategy.cost:.1f}")
    print(f"   Effectiveness: {strategy.effectiveness:.1%}")
    print(f"   Time: {strategy.implementation_time}")

# 7. Show statistics
print(f"\n{'='*60}")
print("STATISTICS")
print('='*60)
print(f"Pentest duration: {pentest_result.statistics['duration_seconds']:.1f}s")
print(f"Commands executed: {len(pentest_result.commands_executed)}")
print(f"Optimization score: {remediation_result.optimization_score:.2f}")
print(f"Total remediation cost: {sum(s.cost for s in remediation_result.selected_strategies):.1f}")

# 8. Save results
pentest_result.to_json("pentestai_results.json")
print("\n✅ Results saved to pentestai_results.json")
```

---

See also:
- [REST API Reference](rest-api.md)
- [Configuration Guide](../core/configuration.md)
- [Data Models](data-models.md)
