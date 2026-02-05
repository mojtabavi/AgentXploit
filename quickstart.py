"""
Quick Start Guide for PentestAI with OpenAI Integration

This guide shows how to use the unified PentestAI framework with OpenAI LLM.
"""

import os
from pentestai import PentestAIController, PentestAIConfig


def example_with_openai_api():
    """Example using OpenAI API (requires OPENAI_API_KEY environment variable)"""
    
    # Option 1: Set API key via environment variable (recommended)
    # export OPENAI_API_KEY="sk-..."
    
    # Option 2: Set API key in config (not recommended for production)
    config = PentestAIConfig(
        target="192.168.1.100",
        max_iterations=20,
        counterfactual_rounds=2,
        remediation_budget=50.0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),  # Load from environment
        planner_model="gpt-4",
        executor_model="gpt-4",
        advisor_model="gpt-4",
        evaluator_model="gpt-4",
        utility_model="gpt-3.5-turbo",
        sandbox_mode=True,  # ALWAYS use sandbox mode for safety!
        output_directory="./results",
    )
    
    # Create controller
    controller = PentestAIController(config)
    
    # Run full two-stage assessment
    print("Starting PentestAI assessment with OpenAI...")
    pentest_result, remediation_result = controller.run_full_assessment()
    
    # Display results
    print(f"\n{'='*60}")
    print("ASSESSMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Vulnerabilities discovered: {len(pentest_result.vulnerabilities)}")
    print(f"Remediation strategies generated: {len(remediation_result.all_strategies)}")
    print(f"Optimal strategies selected: {len(remediation_result.selected_strategies)}")
    print(f"Total value: {remediation_result.total_value:.2f}")
    print(f"Total cost: {remediation_result.total_cost:.2f}")
    print(f"Budget utilization: {remediation_result.budget_used:.1f}%")
    
    # Show vulnerabilities
    print(f"\n{'='*60}")
    print("DISCOVERED VULNERABILITIES")
    print(f"{'='*60}")
    for vuln in pentest_result.vulnerabilities:
        print(f"\n[{vuln.severity.name}] {vuln.name}")
        print(f"  CVE: {vuln.cve_id or 'N/A'}")
        print(f"  CVSS: {vuln.cvss_score}/10")
        print(f"  Service: {vuln.service} (Port {vuln.port})")
        print(f"  Description: {vuln.description}")
    
    # Show selected remediations
    print(f"\n{'='*60}")
    print("RECOMMENDED REMEDIATION STRATEGIES")
    print(f"{'='*60}")
    for i, strategy in enumerate(remediation_result.selected_strategies, 1):
        print(f"\n{i}. {strategy.description}")
        print(f"   Type: {strategy.type.name}")
        print(f"   Effectiveness: {strategy.value_score:.1f}/10")
        print(f"   Cost: {strategy.cost_score:.1f}/10")
        print(f"   Time: {strategy.estimated_time} minutes")
        print(f"   Risk: {strategy.risk_level}")
        if strategy.commands:
            print(f"   Commands:")
            for cmd in strategy.commands[:3]:  # Show first 3 commands
                print(f"     {cmd}")


def example_with_config_file():
    """Example using configuration file"""
    
    # Create config.json:
    # {
    #   "target": "192.168.1.100",
    #   "max_iterations": 20,
    #   "openai_api_key": "sk-...",
    #   "planner_model": "gpt-4",
    #   "sandbox_mode": true
    # }
    
    config = PentestAIConfig.from_file("config.json")
    controller = PentestAIController(config)
    pentest_result, remediation_result = controller.run_full_assessment()
    
    print(f"Assessment complete: {len(pentest_result.vulnerabilities)} vulnerabilities")


def example_with_environment_variables():
    """Example using environment variables"""
    
    # Set environment variables:
    # export OPENAI_API_KEY="sk-..."
    # export PENTESTAI_TARGET="192.168.1.100"
    # export PENTESTAI_MAX_ITERATIONS=20
    # export PENTESTAI_SANDBOX_MODE=true
    
    config = PentestAIConfig.from_env()
    config.target = config.target or "192.168.1.100"  # Fallback
    
    controller = PentestAIController(config)
    pentest_result, remediation_result = controller.run_full_assessment()
    
    print(f"Assessment complete: {len(pentest_result.vulnerabilities)} vulnerabilities")


def example_pentest_only():
    """Example running only Stage 1 (vulnerability discovery)"""
    
    config = PentestAIConfig(
        target="192.168.1.100",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        sandbox_mode=True,
    )
    
    controller = PentestAIController(config)
    pentest_result = controller.run_pentest_only()
    
    print(f"Pentesting complete: {len(pentest_result.vulnerabilities)} vulnerabilities found")
    for vuln in pentest_result.vulnerabilities:
        print(f"  - {vuln.name} ({vuln.severity.name})")


def example_remediation_only():
    """Example running only Stage 2 (remediation planning)"""
    
    from pentestai.models.data import Vulnerability, VulnerabilitySeverity
    
    # Sample vulnerabilities (could be from previous pentest or external source)
    vulnerabilities = [
        Vulnerability(
            name="vsFTPd 2.3.4 Backdoor",
            description="Backdoor allowing remote code execution",
            severity=VulnerabilitySeverity.CRITICAL,
            cvss_score=10.0,
            cve_id="CVE-2011-2523",
            service="FTP",
            port=21,
            exploit_method="Backdoor trigger",
        ),
        Vulnerability(
            name="SQL Injection",
            description="SQL injection in web application",
            severity=VulnerabilitySeverity.HIGH,
            cvss_score=8.5,
            service="HTTP",
            port=80,
            exploit_method="SQL injection",
        ),
    ]
    
    config = PentestAIConfig(
        remediation_budget=30.0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    controller = PentestAIController(config)
    remediation_result = controller.run_remediation_only(vulnerabilities)
    
    print(f"Remediation planning complete: {len(remediation_result.selected_strategies)} strategies selected")
    for strategy in remediation_result.selected_strategies:
        print(f"  - {strategy.description} (Value: {strategy.value_score:.1f}, Cost: {strategy.cost_score:.1f})")


def example_without_api_key():
    """Example using mock LLM (no API key required - for testing only)"""
    
    # When no API key is provided, framework uses mock LLM with simulated responses
    config = PentestAIConfig(
        target="192.168.1.100",
        max_iterations=10,
        sandbox_mode=True,
        # No openai_api_key provided
    )
    
    controller = PentestAIController(config)
    pentest_result, remediation_result = controller.run_full_assessment()
    
    print(f"Mock assessment complete: {len(pentest_result.vulnerabilities)} vulnerabilities")
    print("Note: This used mock LLM responses. Set OPENAI_API_KEY for real assessment.")


if __name__ == "__main__":
    print("PentestAI Quick Start Examples")
    print("="*60)
    
    # Check if API key is available
    if os.getenv("OPENAI_API_KEY"):
        print("\n✓ OpenAI API key found - running real example\n")
        example_with_openai_api()
    else:
        print("\n⚠ No OpenAI API key found - running mock example")
        print("Set OPENAI_API_KEY environment variable for real assessment\n")
        example_without_api_key()
    
    print("\n" + "="*60)
    print("More examples available:")
    print("  - example_with_config_file()")
    print("  - example_with_environment_variables()")
    print("  - example_pentest_only()")
    print("  - example_remediation_only()")
