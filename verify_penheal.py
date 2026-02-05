"""
PenHeal Installation Verification Script

Run this script to verify that PenHeal is properly installed and working.
"""

import sys
from pathlib import Path


def check_imports():
    """Check if all required modules can be imported."""
    print("Checking imports...")
    
    try:
        # Core imports
        from pentestgpt.penheal import (
            PenHealController,
            PentestModule,
            RemediationModule,
        )
        print("✓ Core modules imported successfully")
        
        # Model imports
        from pentestgpt.penheal.models import (
            Vulnerability,
            RemediationStrategy,
            AttackPlanTask,
        )
        print("✓ Data models imported successfully")
        
        # Agent imports
        from pentestgpt.penheal.pentest_module import (
            PlannerAgent,
            ExecutorAgent,
            InstructorAgent,
        )
        from pentestgpt.penheal.remediation_module import (
            EstimatorAgent,
            AdvisorAgent,
            OptimizerAgent,
        )
        print("✓ Agent classes imported successfully")
        
        # Config imports
        from pentestgpt.penheal.config import PenHealConfig
        print("✓ Configuration module imported successfully")
        
        # Knowledge base
        from pentestgpt.penheal.knowledge_base import KNOWLEDGE_BASE
        print(f"✓ Knowledge base loaded ({len(KNOWLEDGE_BASE)} entries)")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from pentestgpt.penheal import PenHealController
        from pentestgpt.penheal.models import Vulnerability, VulnerabilitySeverity
        
        # Test 1: Controller initialization
        controller = PenHealController()
        print("✓ Controller initialized")
        
        # Test 2: Create a vulnerability
        vuln = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="Test Vulnerability",
            service="Test Service",
            severity=VulnerabilitySeverity.MEDIUM,
        )
        print("✓ Vulnerability object created")
        
        # Test 3: Serialize to dict
        vuln_dict = vuln.to_dict()
        assert "vuln_id" in vuln_dict
        print("✓ Vulnerability serialization works")
        
        # Test 4: Planner agent
        from pentestgpt.penheal.pentest_module import PlannerAgent
        planner = PlannerAgent()
        tasks = planner.create_initial_plan("test-target.com")
        assert len(tasks) > 0
        print(f"✓ Planner created {len(tasks)} tasks")
        
        # Test 5: Estimator agent
        from pentestgpt.penheal.remediation_module import EstimatorAgent
        estimator = EstimatorAgent()
        score = estimator.estimate_severity(vuln)
        assert 0 <= score <= 10
        print(f"✓ Estimator assigned score: {score:.1f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_available():
    """Test if CLI is accessible."""
    print("\nTesting CLI availability...")
    
    try:
        import importlib.util
        spec = importlib.util.find_spec("pentestgpt.penheal.cli")
        if spec is not None:
            print("✓ CLI module found")
            print("  Run with: python -m pentestgpt.penheal.cli --help")
            return True
        else:
            print("✗ CLI module not found")
            return False
    except Exception as e:
        print(f"✗ CLI check failed: {e}")
        return False


def test_examples_available():
    """Test if examples are accessible."""
    print("\nTesting examples availability...")
    
    try:
        import importlib.util
        spec = importlib.util.find_spec("pentestgpt.penheal.examples")
        if spec is not None:
            print("✓ Examples module found")
            print("  Run with: python -m pentestgpt.penheal.examples")
            return True
        else:
            print("✗ Examples module not found")
            return False
    except Exception as e:
        print(f"✗ Examples check failed: {e}")
        return False


def check_documentation():
    """Check if documentation files exist."""
    print("\nChecking documentation...")
    
    docs = [
        "pentestgpt/penheal/README.md",
        "pentestgpt/penheal/QUICKSTART.md",
        "pentestgpt/penheal/ARCHITECTURE.md",
        "PENHEAL_IMPLEMENTATION.md",
    ]
    
    all_found = True
    for doc in docs:
        path = Path(doc)
        if path.exists():
            print(f"✓ {doc}")
        else:
            print(f"✗ {doc} not found")
            all_found = False
    
    return all_found


def main():
    """Run all verification checks."""
    print("=" * 80)
    print("PenHeal Installation Verification")
    print("=" * 80)
    
    results = {
        "Imports": check_imports(),
        "Basic Functionality": test_basic_functionality(),
        "CLI": test_cli_available(),
        "Examples": test_examples_available(),
        "Documentation": check_documentation(),
    }
    
    print("\n" + "=" * 80)
    print("Verification Summary")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "=" * 80)
        print("✓ ALL CHECKS PASSED")
        print("=" * 80)
        print("\nPenHeal is properly installed and ready to use!")
        print("\nNext steps:")
        print("  1. Read the documentation: pentestgpt/penheal/README.md")
        print("  2. Try the quick start: pentestgpt/penheal/QUICKSTART.md")
        print("  3. Run examples: python -m pentestgpt.penheal.examples")
        print("  4. Use the CLI: python -m pentestgpt.penheal.cli --help")
        return 0
    else:
        print("\n" + "=" * 80)
        print("✗ SOME CHECKS FAILED")
        print("=" * 80)
        print("\nPlease check the errors above and ensure:")
        print("  1. All files are present in pentestgpt/penheal/")
        print("  2. The package is properly installed: pip install -e .")
        print("  3. Python version is 3.9 or higher")
        return 1


if __name__ == "__main__":
    sys.exit(main())
