"""
Tests for PenHeal framework components.

Basic tests to verify the framework functionality.
"""

import pytest
from pathlib import Path

from pentestgpt.penheal.models import (
    Vulnerability,
    VulnerabilitySeverity,
    RemediationStrategy,
    AttackPlanTask,
    PentestPhase,
    TaskStatus,
)
from pentestgpt.penheal.pentest_module import (
    PlannerAgent,
    ExecutorAgent,
    InstructorAgent,
    SummarizerAgent,
    ExtractorAgent,
)
from pentestgpt.penheal.remediation_module import (
    EstimatorAgent,
    AdvisorAgent,
    EvaluatorAgent,
    OptimizerAgent,
)
from pentestgpt.penheal.controller import PenHealController


class TestDataModels:
    """Test data models."""
    
    def test_vulnerability_creation(self):
        """Test creating a vulnerability."""
        vuln = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="SQL Injection",
            service="Web",
            severity=VulnerabilitySeverity.HIGH,
        )
        
        assert vuln.vuln_id == "TEST-001"
        assert vuln.severity == VulnerabilitySeverity.HIGH
        
    def test_vulnerability_to_dict(self):
        """Test vulnerability serialization."""
        vuln = Vulnerability(
            vuln_id="TEST-002",
            target="test.com",
            vulnerability_type="XSS",
            service="Web",
        )
        
        data = vuln.to_dict()
        assert data["vuln_id"] == "TEST-002"
        assert "vulnerability_type" in data
        
    def test_remediation_strategy_creation(self):
        """Test creating a remediation strategy."""
        strategy = RemediationStrategy(
            strategy_id="STRAT-001",
            vuln_id="TEST-001",
            action_type="patch",
            description="Apply patch",
        )
        
        assert strategy.strategy_id == "STRAT-001"
        assert strategy.action_type == "patch"


class TestPentestModule:
    """Test Pentest Module agents."""
    
    def test_planner_initial_plan(self):
        """Test Planner creates initial plan."""
        planner = PlannerAgent()
        tasks = planner.create_initial_plan("test.com")
        
        assert len(tasks) > 0
        assert any(t.phase == PentestPhase.RECONNAISSANCE for t in tasks)
        assert any(t.phase == PentestPhase.SCANNING for t in tasks)
        
    def test_planner_counterfactual(self):
        """Test Planner counterfactual reasoning."""
        planner = PlannerAgent()
        planner.create_initial_plan("test.com")
        
        vuln = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="SQLi",
            service="Web",
        )
        
        cf_tasks = planner.apply_counterfactual_reasoning([vuln])
        assert planner.counterfactual_round == 1
        
    def test_executor_simulation(self):
        """Test Executor simulates actions."""
        executor = ExecutorAgent()
        task = AttackPlanTask(
            task_id="task-001",
            description="Scan ports",
            phase=PentestPhase.SCANNING,
        )
        
        result = executor.execute_task(task)
        assert result.success
        assert result.symbolic_result
        
    def test_instructor_guidance(self):
        """Test Instructor provides guidance."""
        instructor = InstructorAgent()
        task = AttackPlanTask(
            task_id="task-001",
            description="Test for SQL injection",
            phase=PentestPhase.ASSESSMENT,
        )
        
        guidance = instructor.get_guidance(task)
        assert len(guidance) > 0
        assert "Guidance" in guidance
        
    def test_summarizer(self):
        """Test Summarizer creates summaries."""
        summarizer = SummarizerAgent()
        task = AttackPlanTask(
            task_id="task-001",
            description="Test task",
            phase=PentestPhase.SCANNING,
            status=TaskStatus.COMPLETED,
        )
        
        from pentestgpt.penheal.models import ExecutionResult
        result = ExecutionResult(
            success=True,
            output="Task completed",
            symbolic_result="SUCCESS",
        )
        
        summary = summarizer.summarize_execution(task, result)
        assert len(summary) > 0
        assert "Test task" in summary
        
    def test_extractor(self):
        """Test Extractor extracts vulnerabilities."""
        extractor = ExtractorAgent()
        execution_history = [
            {
                "task_id": "task-001",
                "description": "SQL injection test",
                "result": {
                    "symbolic_result": "SQL_INJECTION_POSSIBLE",
                    "artifacts": {},
                },
            }
        ]
        
        vulns = extractor.extract_vulnerabilities(execution_history, "test.com")
        assert len(vulns) > 0
        assert vulns[0].vulnerability_type == "SQL Injection"


class TestRemediationModule:
    """Test Remediation Module agents."""
    
    def test_estimator(self):
        """Test Estimator assigns scores."""
        estimator = EstimatorAgent()
        vuln = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="SQL Injection",
            service="Web",
        )
        
        score = estimator.estimate_severity(vuln)
        assert 0.0 <= score <= 10.0
        
    def test_advisor(self):
        """Test Advisor generates strategies."""
        advisor = AdvisorAgent()
        vuln = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="SQL Injection",
            service="Web",
            cvss_score=8.5,
        )
        
        strategies = advisor.generate_strategies(vuln)
        assert len(strategies) > 0
        assert any(s.action_type == "patch" for s in strategies)
        
    def test_evaluator(self):
        """Test Evaluator assigns value and cost."""
        evaluator = EvaluatorAgent()
        vuln = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="SQL Injection",
            service="Web",
            cvss_score=8.5,
        )
        
        strategy = RemediationStrategy(
            strategy_id="STRAT-001",
            vuln_id="TEST-001",
            action_type="patch",
            description="Apply patch",
        )
        
        evaluated = evaluator.evaluate_strategies([strategy], [vuln])
        assert evaluated[0].value_score > 0
        assert evaluated[0].cost_score > 0
        
    def test_optimizer(self):
        """Test Optimizer creates optimal plan."""
        optimizer = OptimizerAgent()
        
        vuln1 = Vulnerability(
            vuln_id="TEST-001",
            target="test.com",
            vulnerability_type="SQLi",
            service="Web",
            cvss_score=8.0,
        )
        
        strategies = [
            RemediationStrategy(
                strategy_id="STRAT-001",
                vuln_id="TEST-001",
                action_type="patch",
                description="Patch",
                value_score=80.0,
                cost_score=30.0,
            ),
            RemediationStrategy(
                strategy_id="STRAT-002",
                vuln_id="TEST-001",
                action_type="monitor",
                description="Monitor",
                value_score=40.0,
                cost_score=10.0,
            ),
        ]
        
        plan = optimizer.optimize(strategies, [vuln1], budget=100.0)
        assert len(plan.selected_strategies) > 0
        assert plan.total_cost <= 100.0


class TestController:
    """Test PenHeal controller."""
    
    def test_controller_init(self):
        """Test controller initialization."""
        controller = PenHealController()
        assert controller.pentest_module is not None
        assert controller.remediation_module is not None
        
    def test_full_assessment_small(self):
        """Test running a small full assessment."""
        controller = PenHealController()
        
        results = controller.run_full_assessment(
            target="test.research.com",
            max_iterations=5,
            counterfactual_rounds=1,
            remediation_budget=100.0,
        )
        
        assert "session_id" in results
        assert "stage1_pentest" in results
        assert "stage2_remediation" in results
        assert results["stage1_pentest"]["vulnerabilities_found"] >= 0
        
    def test_pentest_only(self):
        """Test pentest-only mode."""
        controller = PenHealController()
        
        results = controller.run_pentest_only(
            target="test.com",
            max_iterations=5,
            counterfactual_rounds=1,
        )
        
        assert "vulnerabilities" in results
        assert "plan_summary" in results


class TestKnowledgeBase:
    """Test knowledge base functionality."""
    
    def test_knowledge_search(self):
        """Test searching knowledge base."""
        from pentestgpt.penheal.knowledge_base import search_knowledge
        
        results = search_knowledge("sql injection")
        assert len(results) > 0
        
    def test_knowledge_by_tags(self):
        """Test filtering by tags."""
        from pentestgpt.penheal.knowledge_base import get_knowledge_by_tags
        
        results = get_knowledge_by_tags(["sql"])
        assert len(results) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
