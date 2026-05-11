"""Monitoring and metrics for Legion Core Claw."""

from prometheus_client import Counter, Gauge, Histogram, Summary, CollectorRegistry, generate_latest
from typing import Dict, Any, Optional
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Prometheus metrics collector for Legion Core Claw."""

    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()

        # Agent metrics
        self.active_agents = Gauge(
            'legion_active_agents',
            'Number of currently active agents',
            registry=self.registry
        )

        self.agent_spawns_total = Counter(
            'legion_agent_spawns_total',
            'Total number of agents spawned',
            ['role'],
            registry=self.registry
        )

        self.agent_lifecycle_duration = Histogram(
            'legion_agent_lifecycle_duration_seconds',
            'Time agents spend in different lifecycle states',
            ['state'],
            registry=self.registry
        )

        # Task metrics
        self.tasks_created_total = Counter(
            'legion_tasks_created_total',
            'Total number of tasks created',
            ['agent_role'],
            registry=self.registry
        )

        self.tasks_completed_total = Counter(
            'legion_tasks_completed_total',
            'Total number of tasks completed',
            ['agent_role', 'status'],
            registry=self.registry
        )

        self.task_execution_duration = Histogram(
            'legion_task_execution_duration_seconds',
            'Time taken to execute tasks',
            ['agent_role'],
            registry=self.registry
        )

        self.queued_tasks = Gauge(
            'legion_queued_tasks',
            'Number of tasks currently queued',
            registry=self.registry
        )

        # Tool execution metrics
        self.tool_executions_total = Counter(
            'legion_tool_executions_total',
            'Total number of tool executions',
            ['tool_name', 'status'],
            registry=self.registry
        )

        self.tool_execution_duration = Histogram(
            'legion_tool_execution_duration_seconds',
            'Time taken to execute tools',
            ['tool_name'],
            registry=self.registry
        )

        # API metrics
        self.api_requests_total = Counter(
            'legion_api_requests_total',
            'Total API requests',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )

        self.api_request_duration = Histogram(
            'legion_api_request_duration_seconds',
            'API request duration',
            ['method', 'endpoint'],
            registry=self.registry
        )

        # Bot metrics
        self.bot_messages_total = Counter(
            'legion_bot_messages_total',
            'Total bot messages processed',
            ['type', 'status'],
            registry=self.registry
        )

        self.bot_commands_total = Counter(
            'legion_bot_commands_total',
            'Total bot commands executed',
            ['command'],
            registry=self.registry
        )

        # System metrics
        self.uptime_seconds = Gauge(
            'legion_uptime_seconds',
            'System uptime in seconds',
            registry=self.registry
        )

        self.memory_usage_bytes = Gauge(
            'legion_memory_usage_bytes',
            'Current memory usage in bytes',
            registry=self.registry
        )

        # Error metrics
        self.errors_total = Counter(
            'legion_errors_total',
            'Total number of errors',
            ['type', 'component'],
            registry=self.registry
        )

        # AI/LLM metrics
        self.llm_requests_total = Counter(
            'legion_llm_requests_total',
            'Total LLM API requests',
            ['provider', 'model'],
            registry=self.registry
        )

        self.llm_tokens_used = Counter(
            'legion_llm_tokens_used_total',
            'Total tokens used by LLM',
            ['provider', 'model', 'type'],
            registry=self.registry
        )

        # Security metrics
        self.auth_attempts_total = Counter(
            'legion_auth_attempts_total',
            'Total authentication attempts',
            ['result'],
            registry=self.registry
        )

        self.rate_limit_hits_total = Counter(
            'legion_rate_limit_hits_total',
            'Total rate limit hits',
            ['endpoint'],
            registry=self.registry
        )

        # Initialize uptime
        self.start_time = time.time()
        self.uptime_seconds.set_function(lambda: time.time() - self.start_time)

    def record_agent_spawn(self, role: str) -> None:
        """Record agent spawn."""
        self.agent_spawns_total.labels(role=role).inc()
        self.active_agents.inc()

    def record_agent_termination(self, role: str) -> None:
        """Record agent termination."""
        self.active_agents.dec()

    def record_task_created(self, agent_role: str) -> None:
        """Record task creation."""
        self.tasks_created_total.labels(agent_role=agent_role).inc()
        self.queued_tasks.inc()

    def record_task_completed(self, agent_role: str, status: str, duration: float) -> None:
        """Record task completion."""
        self.tasks_completed_total.labels(agent_role=agent_role, status=status).inc()
        self.task_execution_duration.labels(agent_role=agent_role).observe(duration)
        self.queued_tasks.dec()

    def record_tool_execution(self, tool_name: str, status: str, duration: float) -> None:
        """Record tool execution."""
        self.tool_executions_total.labels(tool_name=tool_name, status=status).inc()
        self.tool_execution_duration.labels(tool_name=tool_name).observe(duration)

    def record_api_request(self, method: str, endpoint: str, status: int, duration: float) -> None:
        """Record API request."""
        status_str = str(status)
        self.api_requests_total.labels(method=method, endpoint=endpoint, status=status_str).inc()
        self.api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    def record_bot_message(self, message_type: str, status: str) -> None:
        """Record bot message."""
        self.bot_messages_total.labels(type=message_type, status=status).inc()

    def record_bot_command(self, command: str) -> None:
        """Record bot command execution."""
        self.bot_commands_total.labels(command=command).inc()

    def record_error(self, error_type: str, component: str) -> None:
        """Record error."""
        self.errors_total.labels(type=error_type, component=component).inc()

    def record_llm_request(self, provider: str, model: str) -> None:
        """Record LLM request."""
        self.llm_requests_total.labels(provider=provider, model=model).inc()

    def record_llm_tokens(self, provider: str, model: str, token_type: str, count: int) -> None:
        """Record LLM token usage."""
        self.llm_tokens_used.labels(provider=provider, model=model, type=token_type).inc(count)

    def record_auth_attempt(self, result: str) -> None:
        """Record authentication attempt."""
        self.auth_attempts_total.labels(result=result).inc()

    def record_rate_limit_hit(self, endpoint: str) -> None:
        """Record rate limit hit."""
        self.rate_limit_hits_total.labels(endpoint=endpoint).inc()

    def get_metrics(self) -> str:
        """Get all metrics in Prometheus format."""
        return generate_latest(self.registry).decode('utf-8')

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status with key metrics."""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'uptime_seconds': time.time() - self.start_time,
            'active_agents': self.active_agents._value,
            'queued_tasks': self.queued_tasks._value,
            'status': 'healthy'
        }


class HealthChecker:
    """Health check system for Legion Core Claw."""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.checks = {}

    def add_check(self, name: str, check_function, critical: bool = False) -> None:
        """Add a health check."""
        self.checks[name] = {
            'function': check_function,
            'critical': critical,
            'last_result': None,
            'last_check': None
        }

    def run_checks(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        overall_healthy = True

        for name, check_info in self.checks.items():
            try:
                result = check_info['function']()
                check_info['last_result'] = result
                check_info['last_check'] = datetime.utcnow()

                results[name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'critical': check_info['critical'],
                    'timestamp': check_info['last_check'].isoformat()
                }

                if check_info['critical'] and not result:
                    overall_healthy = False

            except Exception as e:
                logger.error(f"Health check '{name}' failed: {e}")
                results[name] = {
                    'status': 'error',
                    'critical': check_info['critical'],
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }
                if check_info['critical']:
                    overall_healthy = False

        return {
            'overall_status': 'healthy' if overall_healthy else 'unhealthy',
            'checks': results,
            'timestamp': datetime.utcnow().isoformat()
        }

    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        results = self.run_checks()
        return results['overall_status'] == 'healthy'


# Global instances
metrics = MetricsCollector()
health_checker = HealthChecker(metrics)

# Add default health checks
def check_database():
    """Check database connectivity."""
    try:
        from legion_core_claw.persistence import db_manager
        if db_manager.engine:
            # Simple connectivity check
            with db_manager.get_session() as session:
                session.execute("SELECT 1")
            return True
        return False
    except Exception:
        return False

def check_memory():
    """Check memory usage is reasonable."""
    import psutil
    memory_percent = psutil.virtual_memory().percent
    return memory_percent < 90  # Less than 90% usage

def check_disk():
    """Check disk space is sufficient."""
    import psutil
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent < 95  # Less than 95% usage

# Register default checks
health_checker.add_check('database', check_database, critical=True)
health_checker.add_check('memory', check_memory, critical=False)
health_checker.add_check('disk', check_disk, critical=False)
