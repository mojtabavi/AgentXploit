# Full Assessment Example

Complete walkthrough of running a full two-stage assessment (pentest + remediation).

## Overview

This example demonstrates:
1. Configuration setup
2. Running full assessment
3. Analyzing vulnerabilities
4. Reviewing remediation strategies
5. Exporting results

## Code Example

```python
#!/usr/bin/env python3
"""
PentestAI Full Assessment Example

This example shows a complete two-stage assessment workflow:
- Stage 1: Pentest Module (vulnerability discovery)
- Stage 2: Remediation Module (optimal remediation planning)
"""

from pentestai import PentestAIController, PentestAIConfig
from pentestai.models.data import VulnerabilitySeverity
from datetime import datetime
import json

def main():
    print("="*80)
    print("PentestAI Full Assessment Example")
    print("="*80)
    
    # =========================================================================
    # STEP 1: Configuration
    # =========================================================================
    print("\n📋 Step 1: Configuring PentestAI...")
    
    config = PentestAIConfig(
        # Target system
        target="192.168.1.100",
        
        # LLM Configuration
        openai_api_key="sk-your-key-here",  # Replace with your key
        planner_model="gpt-4",
        executor_model="gpt-4",
        advisor_model="gpt-4",
        evaluator_model="gpt-4",
        utility_model="gpt-3.5-turbo",  # Cheaper for utilities
        
        # Pentest Settings
        max_iterations=30,          # Medium-length assessment
        counterfactual_rounds=3,    # Explore 3 attack paths
        use_instructor=True,        # Enable RAG guidance
        
        # Remediation Settings
        remediation_budget=100.0,           # Total budget
        budget_per_vulnerability=4.0,       # Budget per vuln
        enable_optimization=True,           # Use Group Knapsack
        
        # Safety (IMPORTANT!)
        sandbox_mode=True,  # Simulated execution - ALWAYS use for testing
        
        # Output
        output_directory="./results",
        save_attack_plan=True,
        save_execution_history=True,
        generate_report=True,
        export_format="json",
    )
    
    # Validate configuration
    errors = config.validate()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        return
    
    print("✅ Configuration valid")
    print(f"   Target: {config.target}")
    print(f"   Mode: {'Sandbox (Safe)' if config.sandbox_mode else 'MCP (Real)'}")
    print(f"   Max Iterations: {config.max_iterations}")
    print(f"   Remediation Budget: {config.remediation_budget}")
    
    # =========================================================================
    # STEP 2: Initialize Controller
    # =========================================================================
    print("\n🚀 Step 2: Initializing PentestAI Controller...")
    
    start_time = datetime.now()
    controller = PentestAIController(config)
    
    print("✅ Controller initialized")
    
    # =========================================================================
    # STEP 3: Run Full Assessment
    # =========================================================================
    print("\n🔍 Step 3: Running Full Assessment...")
    print("   This will take 5-10 minutes depending on target complexity...")
    
    try:
        pentest_result, remediation_result = controller.run_full_assessment()
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"\n✅ Assessment Complete! Took {duration:.1f}s")
        
    except Exception as e:
        print(f"\n❌ Assessment failed: {e}")
        return
    
    # =========================================================================
    # STEP 4: Analyze Vulnerabilities
    # =========================================================================
    print("\n" + "="*80)
    print("📊 Stage 1 Results: Vulnerabilities")
    print("="*80)
    
    vulnerabilities = pentest_result.vulnerabilities
    
    # Count by severity
    severity_counts = {
        VulnerabilitySeverity.CRITICAL: 0,
        VulnerabilitySeverity.HIGH: 0,
        VulnerabilitySeverity.MEDIUM: 0,
        VulnerabilitySeverity.LOW: 0,
        VulnerabilitySeverity.INFO: 0,
    }
    
    for vuln in vulnerabilities:
        severity_counts[vuln.severity] += 1
    
    # Display summary
    print(f"\n📈 Summary:")
    print(f"   Total Vulnerabilities: {len(vulnerabilities)}")
    print(f"   🔴 Critical: {severity_counts[VulnerabilitySeverity.CRITICAL]}")
    print(f"   🟠 High: {severity_counts[VulnerabilitySeverity.HIGH]}")
    print(f"   🟡 Medium: {severity_counts[VulnerabilitySeverity.MEDIUM]}")
    print(f"   🟢 Low: {severity_counts[VulnerabilitySeverity.LOW]}")
    print(f"   ℹ️  Info: {severity_counts[VulnerabilitySeverity.INFO]}")
    
    # Show statistics
    print(f"\n📊 Statistics:")
    print(f"   Tasks Executed: {pentest_result.statistics['tasks_executed']}")
    print(f"   Counterfactual Rounds: {pentest_result.statistics['counterfactual_rounds']}")
    print(f"   Duration: {pentest_result.statistics['duration_seconds']:.1f}s")
    
    # Display top 10 vulnerabilities
    if vulnerabilities:
        print(f"\n🔴 Top 10 Vulnerabilities (by CVSS score):")
        print("-"*80)
        
        sorted_vulns = sorted(
            vulnerabilities,
            key=lambda v: v.cvss_score,
            reverse=True
        )
        
        for i, vuln in enumerate(sorted_vulns[:10], 1):
            print(f"\n{i}. {vuln.name}")
            print(f"   Severity: {vuln.severity.value} (CVSS {vuln.cvss_score})")
            print(f"   Service: {vuln.service}")
            if vuln.port:
                print(f"   Port: {vuln.port}")
            if vuln.cve_id:
                print(f"   CVE: {vuln.cve_id}")
            print(f"   Exploit Method: {vuln.exploit_method}")
            print(f"   Description: {vuln.description[:100]}...")
    
    # =========================================================================
    # STEP 5: Analyze Remediation Strategies
    # =========================================================================
    print("\n" + "="*80)
    print("🛠️  Stage 2 Results: Remediation Strategies")
    print("="*80)
    
    selected_strategies = remediation_result.selected_strategies
    all_strategies = remediation_result.all_strategies
    
    print(f"\n📈 Summary:")
    print(f"   Total Strategies Proposed: {len(all_strategies)}")
    print(f"   Optimal Strategies Selected: {len(selected_strategies)}")
    print(f"   Optimization Score: {remediation_result.optimization_score:.2f}")
    
    # Calculate totals
    total_cost = sum(s.cost for s in selected_strategies)
    avg_effectiveness = sum(s.effectiveness for s in selected_strategies) / len(selected_strategies) if selected_strategies else 0
    
    print(f"   Total Cost: {total_cost:.1f}")
    print(f"   Average Effectiveness: {avg_effectiveness:.1%}")
    
    # Show severity groups
    print(f"\n📊 Vulnerabilities by Severity:")
    for severity, vulns in remediation_result.severity_groups.items():
        print(f"   {severity}: {len(vulns)} vulnerabilities")
    
    # Display selected strategies
    if selected_strategies:
        print(f"\n✅ Selected Remediation Strategies (Top 15):")
        print("-"*80)
        
        # Sort by effectiveness/cost ratio
        sorted_strategies = sorted(
            selected_strategies,
            key=lambda s: s.effectiveness / s.cost if s.cost > 0 else 0,
            reverse=True
        )
        
        for i, strategy in enumerate(sorted_strategies[:15], 1):
            print(f"\n{i}. {strategy.name}")
            print(f"   Type: {strategy.remediation_type.value}")
            print(f"   Cost: {strategy.cost:.1f}")
            print(f"   Effectiveness: {strategy.effectiveness:.1%}")
            print(f"   Implementation Time: {strategy.implementation_time}")
            print(f"   Required Skills: {', '.join(strategy.required_skills)}")
            print(f"   Description: {strategy.description[:100]}...")
    
    # =========================================================================
    # STEP 6: Attack Plan Analysis
    # =========================================================================
    print("\n" + "="*80)
    print("🌳 Attack Plan Tree")
    print("="*80)
    
    attack_plan = pentest_result.attack_plan
    
    if attack_plan:
        print(f"\nRoot: {attack_plan.get('description', 'Root node')}")
        print(f"   Children: {len(attack_plan.get('children', []))}")
        print(f"   Depth: {attack_plan.get('depth', 0)}")
        
        # Show attack path
        def show_path(node, prefix="", depth=0, max_depth=3):
            if depth > max_depth:
                return
            
            print(f"{prefix}➤ {node.get('description', 'Unknown')}")
            
            children = node.get('children', [])
            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                new_prefix = prefix + ("    " if is_last else "│   ")
                show_path(child, new_prefix, depth + 1, max_depth)
        
        print("\nAttack Path (first 3 levels):")
        show_path(attack_plan)
    
    # =========================================================================
    # STEP 7: Export Results
    # =========================================================================
    print("\n" + "="*80)
    print("💾 Exporting Results")
    print("="*80)
    
    output_dir = config.output_directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export as JSON
    results_path = f"{output_dir}/pentestai_results_{timestamp}.json"
    with open(results_path, 'w') as f:
        json.dump({
            "target": config.target,
            "timestamp": timestamp,
            "vulnerabilities": [v.to_dict() for v in vulnerabilities],
            "remediation_strategies": [s.to_dict() for s in selected_strategies],
            "statistics": {
                "pentest": pentest_result.statistics,
                "remediation": remediation_result.statistics,
            },
            "attack_plan": attack_plan,
        }, f, indent=2)
    
    print(f"✅ Results exported to: {results_path}")
    
    # Generate text report
    if config.generate_report:
        report_path = f"{output_dir}/pentestai_report_{timestamp}.txt"
        with open(report_path, 'w') as f:
            f.write(f"PentestAI Assessment Report\n")
            f.write(f"=" * 80 + "\n\n")
            f.write(f"Target: {config.target}\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            f.write(f"Duration: {duration:.1f}s\n\n")
            
            f.write(f"Vulnerabilities Found: {len(vulnerabilities)}\n")
            f.write(f"Remediation Strategies: {len(selected_strategies)}\n")
            f.write(f"Optimization Score: {remediation_result.optimization_score:.2f}\n\n")
            
            f.write(f"Top Vulnerabilities:\n")
            f.write("-" * 80 + "\n")
            for vuln in sorted_vulns[:10]:
                f.write(f"\n{vuln.name}\n")
                f.write(f"  Severity: {vuln.severity.value} (CVSS {vuln.cvss_score})\n")
                f.write(f"  {vuln.description}\n")
        
        print(f"✅ Report generated: {report_path}")
    
    # =========================================================================
    # STEP 8: Summary
    # =========================================================================
    print("\n" + "="*80)
    print("✅ Assessment Complete!")
    print("="*80)
    
    print(f"\n📊 Final Summary:")
    print(f"   Target: {config.target}")
    print(f"   Duration: {duration:.1f}s")
    print(f"   Vulnerabilities: {len(vulnerabilities)}")
    print(f"   Critical/High: {severity_counts[VulnerabilitySeverity.CRITICAL] + severity_counts[VulnerabilitySeverity.HIGH]}")
    print(f"   Remediation Strategies: {len(selected_strategies)}")
    print(f"   Total Remediation Cost: {total_cost:.1f}")
    print(f"   Average Effectiveness: {avg_effectiveness:.1%}")
    
    print(f"\n📁 Output Files:")
    print(f"   Results: {results_path}")
    if config.generate_report:
        print(f"   Report: {report_path}")
    if config.save_attack_plan:
        print(f"   Attack Plan: {output_dir}/attack_plan_{timestamp}.json")
    
    print("\n🎉 Assessment successful!")


if __name__ == "__main__":
    main()
```

## Expected Output

```
================================================================================
PentestAI Full Assessment Example
================================================================================

📋 Step 1: Configuring PentestAI...
✅ Configuration valid
   Target: 192.168.1.100
   Mode: Sandbox (Safe)
   Max Iterations: 30
   Remediation Budget: 100.0

🚀 Step 2: Initializing PentestAI Controller...
✅ Controller initialized

🔍 Step 3: Running Full Assessment...
   This will take 5-10 minutes depending on target complexity...

✅ Assessment Complete! Took 287.3s

================================================================================
📊 Stage 1 Results: Vulnerabilities
================================================================================

📈 Summary:
   Total Vulnerabilities: 23
   🔴 Critical: 2
   🟠 High: 5
   🟡 Medium: 11
   🟢 Low: 4
   ℹ️  Info: 1

📊 Statistics:
   Tasks Executed: 27
   Counterfactual Rounds: 3
   Duration: 183.5s

🔴 Top 10 Vulnerabilities (by CVSS score):
--------------------------------------------------------------------------------

1. SQL Injection in login form
   Severity: CRITICAL (CVSS 9.8)
   Service: web
   Port: 80
   CVE: CVE-2024-1234
   Exploit Method: sqlmap
   Description: Unsanitized user input allows SQL injection attacks...

2. Remote Code Execution via file upload
   Severity: CRITICAL (CVSS 9.3)
   Service: web
   Port: 8080
   Exploit Method: Malicious file upload
   Description: File upload endpoint does not validate file types...

...

================================================================================
🛠️  Stage 2 Results: Remediation Strategies
================================================================================

📈 Summary:
   Total Strategies Proposed: 67
   Optimal Strategies Selected: 15
   Optimization Score: 8.42
   Total Cost: 94.5
   Average Effectiveness: 87.3%

✅ Selected Remediation Strategies (Top 15):
--------------------------------------------------------------------------------

1. Apply CVE-2024-1234 patch for SQL injection
   Type: patch
   Cost: 5.0
   Effectiveness: 95.0%
   Implementation Time: 2 hours
   Required Skills: system_admin, developer
   Description: Upgrade framework to version 3.2.1 which includes SQL...

2. Implement input validation for file uploads
   Type: reconfigure
   Cost: 7.0
   Effectiveness: 92.0%
   Implementation Time: 4 hours
   Required Skills: developer
   Description: Add whitelist validation for uploaded file types...

...

================================================================================
💾 Exporting Results
================================================================================
✅ Results exported to: ./results/pentestai_results_20240206_145632.json
✅ Report generated: ./results/pentestai_report_20240206_145632.txt

================================================================================
✅ Assessment Complete!
================================================================================

📊 Final Summary:
   Target: 192.168.1.100
   Duration: 287.3s
   Vulnerabilities: 23
   Critical/High: 7
   Remediation Strategies: 15
   Total Remediation Cost: 94.5
   Average Effectiveness: 87.3%

📁 Output Files:
   Results: ./results/pentestai_results_20240206_145632.json
   Report: ./results/pentestai_report_20240206_145632.txt
   Attack Plan: ./results/attack_plan_20240206_145632.json

🎉 Assessment successful!
```

## Next Steps

- **Analyze Attack Plan**: Review `attack_plan.json` to understand attack paths
- **Implement Remediation**: Follow selected strategies
- **Re-run Assessment**: Verify fixes with another pentest
- **Export to Issue Tracker**: Import vulnerabilities into Jira/GitHub Issues

---

See also:
- [Pentest Only Example](pentest-only.md)
- [Remediation Only Example](remediation-only.md)
- [Configuration Guide](../core/configuration.md)
