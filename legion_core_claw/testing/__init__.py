"""Testing framework for Legion Core Claw."""

import logging
import unittest
import tempfile
import shutil
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import time
import json

logger = logging.getLogger(__name__)


class LegionTestCase(unittest.TestCase):
    """Base test case for Legion Core Claw components."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config = {
            "LLM_MODEL": "test-model",
            "LLM_PROVIDER": "test",
            "BOT_TOKEN": "test_token",
            "API_HOST": "localhost",
            "API_PORT": "8000",
            "MAX_AGENTS": 5,
            "ENABLE_AUDIT_LOG": False
        }

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_mock_config(self, **overrides) -> Dict[str, Any]:
        """Create mock configuration."""
        config = self.test_config.copy()
        config.update(overrides)
        return config

    def assert_event_published(self, event_type: str, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        """Assert that an event was published."""
        # This would integrate with the event system
        try:
            from legion_core_claw.events import get_recent_events
            events = get_recent_events(event_type, limit=10)
            for event in events:
                if event.event_type == event_type:
                    return event.to_dict()
        except ImportError:
            pass
        return None


class MockAIEngine:
    """Mock AI engine for testing."""

    def __init__(self, responses: Optional[Dict[str, str]] = None):
        self.responses = responses or {}
        self.call_history = []

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> str:
        """Mock reasoning."""
        self.call_history.append({"method": "reason", "prompt": prompt, "context": context})
        return self.responses.get("reason", "Mock reasoning response")

    def select_tools(self, task: str, available_tools: List[Dict[str, Any]]) -> List[str]:
        """Mock tool selection."""
        self.call_history.append({"method": "select_tools", "task": task, "tools": available_tools})
        return self.responses.get("select_tools", ["mock_tool"])

    def execute_with_tools(self, task: str, tools_config: List[Dict], execution_sandbox: str = "simulated") -> Dict[str, Any]:
        """Mock tool execution."""
        self.call_history.append({"method": "execute_with_tools", "task": task, "tools": tools_config})
        return {
            "task": task,
            "selected_tools": ["mock_tool"],
            "sandbox": execution_sandbox,
            "status": "executed"
        }


class MockToolRegistry:
    """Mock tool registry for testing."""

    def __init__(self, tools: Optional[List[Dict[str, Any]]] = None):
        self.tools = tools or []
        self.call_history = []

    def register(self, tool) -> None:
        """Mock tool registration."""
        self.call_history.append({"method": "register", "tool": tool.name if hasattr(tool, 'name') else str(tool)})

    def get_tool(self, tool_name: str):
        """Mock tool retrieval."""
        self.call_history.append({"method": "get_tool", "tool_name": tool_name})
        for tool in self.tools:
            if tool.get("name") == tool_name:
                return tool
        return None

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Mock tool listing."""
        self.call_history.append({"method": "list_tools", "category": category})
        if category:
            return [t for t in self.tools if t.get("category") == category]
        return self.tools

    def validate_tool_call(self, tool_name: str, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Mock tool validation."""
        self.call_history.append({"method": "validate_tool_call", "tool_name": tool_name, "params": params})
        return True, None

    def to_openai_format(self) -> List[Dict[str, Any]]:
        """Mock OpenAI format conversion."""
        return [{"type": "function", "function": {"name": t["name"], "description": t.get("description", "")}} for t in self.tools]


class MockAgentOrchestrator:
    """Mock agent orchestrator for testing."""

    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.call_history = []

    def spawn_agent(self, role: str, agent_id: Optional[str] = None, config: Optional[Dict] = None):
        """Mock agent spawning."""
        agent_id = agent_id or f"mock-{role}-{len(self.agents)}"
        agent = MockAgent(agent_id, role, config)
        self.agents[agent_id] = agent
        self.call_history.append({"method": "spawn_agent", "role": role, "agent_id": agent_id})
        return agent

    def create_task(self, description: str, agent_id: str, dependencies: Optional[List[str]] = None):
        """Mock task creation."""
        task_id = f"task-{len(self.tasks)}"
        task = MockTask(task_id, description, agent_id, dependencies)
        self.tasks[task_id] = task
        self.call_history.append({"method": "create_task", "description": description, "agent_id": agent_id})
        return task

    def execute_task(self, task_id: str):
        """Mock task execution."""
        self.call_history.append({"method": "execute_task", "task_id": task_id})
        return {"status": "completed"}

    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Mock status."""
        return {
            "active_agents": len(self.agents),
            "total_tasks": len(self.tasks)
        }


class MockAgent:
    """Mock agent for testing."""

    def __init__(self, agent_id: str, role: str, config: Optional[Dict] = None):
        self.agent_id = agent_id
        self.role = role
        self.config = config or {}
        self.status = "idle"
        self.task_queue = []
        self.completed_tasks = []

    def execute_task(self, task):
        """Mock task execution."""
        self.status = "executing"
        result = {"task_id": task.task_id, "status": "completed"}
        self.completed_tasks.append(task)
        self.status = "idle"
        return result

    def get_status(self) -> Dict[str, Any]:
        """Mock status."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": self.status,
            "queued_tasks": len(self.task_queue)
        }


class MockTask:
    """Mock task for testing."""

    def __init__(self, task_id: str, description: str, agent_id: str, dependencies: Optional[List[str]] = None):
        self.task_id = task_id
        self.description = description
        self.agent_id = agent_id
        self.dependencies = dependencies or []
        self.status = "pending"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "agent_id": self.agent_id,
            "status": self.status
        }


class TestSuite:
    """Custom test suite for Legion Core Claw."""

    def __init__(self, name: str):
        self.name = name
        self.tests = []
        self.results = []

    def add_test(self, test_func: Callable, test_name: str):
        """Add a test function."""
        self.tests.append({"func": test_func, "name": test_name})

    def run_tests(self) -> Dict[str, Any]:
        """Run all tests."""
        logger.info(f"Running test suite: {self.name}")

        passed = 0
        failed = 0

        for test in self.tests:
            try:
                logger.info(f"Running test: {test['name']}")
                start_time = time.time()
                test["func"]()
                duration = time.time() - start_time

                self.results.append({
                    "name": test["name"],
                    "status": "passed",
                    "duration": duration
                })
                passed += 1
                logger.info(f"✓ {test['name']} passed")

            except Exception as e:
                self.results.append({
                    "name": test["name"],
                    "status": "failed",
                    "error": str(e)
                })
                failed += 1
                logger.error(f"✗ {test['name']} failed: {e}")

        summary = {
            "suite_name": self.name,
            "total_tests": len(self.tests),
            "passed": passed,
            "failed": failed,
            "success_rate": passed / len(self.tests) if self.tests else 0,
            "results": self.results
        }

        logger.info(f"Test suite completed: {passed}/{len(self.tests)} passed")
        return summary


class IntegrationTestRunner:
    """Runner for integration tests."""

    def __init__(self):
        self.test_suites = {}

    def create_suite(self, name: str) -> TestSuite:
        """Create a test suite."""
        suite = TestSuite(name)
        self.test_suites[name] = suite
        return suite

    def run_all_suites(self) -> Dict[str, Any]:
        """Run all test suites."""
        results = {}
        total_passed = 0
        total_failed = 0

        for name, suite in self.test_suites.items():
            suite_result = suite.run_tests()
            results[name] = suite_result
            total_passed += suite_result["passed"]
            total_failed += suite_result["failed"]

        return {
            "total_suites": len(self.test_suites),
            "total_passed": total_passed,
            "total_failed": total_failed,
            "overall_success_rate": total_passed / (total_passed + total_failed) if (total_passed + total_failed) > 0 else 0,
            "suite_results": results
        }

    def generate_report(self, results: Dict[str, Any], output_file: Optional[str] = None) -> str:
        """Generate test report."""
        report = f"""
# Legion Core Claw Test Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Suites: {results['total_suites']}
- Total Tests: {results['total_passed'] + results['total_failed']}
- Passed: {results['total_passed']}
- Failed: {results['total_failed']}
- Success Rate: {results['overall_success_rate']:.1%}

## Suite Results
"""

        for suite_name, suite_result in results['suite_results'].items():
            report += f"""
### {suite_name}
- Tests: {suite_result['total_tests']}
- Passed: {suite_result['passed']}
- Failed: {suite_result['failed']}
- Success Rate: {suite_result['success_rate']:.1%}

#### Test Details
"""
            for test_result in suite_result['results']:
                status_icon = "✓" if test_result['status'] == 'passed' else "✗"
                report += f"- {status_icon} {test_result['name']}"
                if test_result['status'] == 'failed':
                    report += f" - Error: {test_result['error']}"
                report += "\n"

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)

        return report


# Global test runner instance
test_runner = IntegrationTestRunner()

# Example test suites
def create_unit_tests() -> TestSuite:
    """Create unit test suite."""
    suite = test_runner.create_suite("Unit Tests")

    def test_config_validation():
        from legion_core_claw.config import Config
        config = Config.from_dict({"LLM_MODEL": "test", "LLM_PROVIDER": "test"})
        assert config.LLM_MODEL == "test"

    def test_tool_registry():
        registry = MockToolRegistry()
        registry.register(type('MockTool', (), {'name': 'test_tool'})())
        assert len(registry.call_history) == 1

    suite.add_test(test_config_validation, "Config Validation")
    suite.add_test(test_tool_registry, "Tool Registry")

    return suite

def create_integration_tests() -> TestSuite:
    """Create integration test suite."""
    suite = test_runner.create_suite("Integration Tests")

    def test_agent_lifecycle():
        orchestrator = MockAgentOrchestrator()
        agent = orchestrator.spawn_agent("test_role")
        assert agent.agent_id.startswith("mock-test_role")
        assert len(orchestrator.call_history) == 1

    def test_task_execution():
        orchestrator = MockAgentOrchestrator()
        agent = orchestrator.spawn_agent("worker")
        task = orchestrator.create_task("test task", agent.agent_id)
        result = orchestrator.execute_task(task.task_id)
        assert result["status"] == "completed"

    suite.add_test(test_agent_lifecycle, "Agent Lifecycle")
    suite.add_test(test_task_execution, "Task Execution")

    return suite

# Auto-create default test suites
_unit_tests = create_unit_tests()
_integration_tests = create_integration_tests()

def run_all_tests() -> Dict[str, Any]:
    """Run all tests and return results."""
    return test_runner.run_all_suites()

def generate_test_report(output_file: str = "test_report.md") -> str:
    """Generate and save test report."""
    results = run_all_tests()
    return test_runner.generate_report(results, output_file)