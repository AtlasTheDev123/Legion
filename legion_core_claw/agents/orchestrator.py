"""
Multi-Agent Orchestrator - Spawns, manages, and monitors autonomous sub-agents.
Consolidated from agent_manager.py and tasks.py with unified task execution.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import time

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent lifecycle states."""
    IDLE = "idle"
    ACTIVE = "active"
    EXECUTING = "executing"
    COMPLETED = "completed"
    ERROR = "error"
    TERMINATED = "terminated"


class Task:
    """Represents a task to be executed by an agent."""

    def __init__(self, task_id: str, description: str, agent_id: str, dependencies: Optional[List[str]] = None):
        self.task_id = task_id
        self.description = description
        self.agent_id = agent_id
        self.dependencies = dependencies or []
        self.status = "pending"
        self.created_at = datetime.now()
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "description": self.description[:50],
            "status": self.status,
            "dependencies": self.dependencies,
            "created_at": self.created_at.isoformat()
        }


class Agent:
    """Individual autonomous agent with task execution capability."""

    def __init__(self, agent_id: str, role: str, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.role = role
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.created_at = datetime.now()

    def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute single task."""
        self.status = AgentStatus.EXECUTING
        task.status = "executing"
        
        try:
            # Stub task execution
            result = {
                "task_id": task.task_id,
                "agent_id": self.agent_id,
                "status": "completed",
                "result": f"Task {task.task_id} executed by {self.role}"
            }
            task.  = "completed"
            task.result = result
        except Exception as e:
            task.status = "error"
            task.error = str(e)
            self.status = AgentStatus.ERROR
            
        self.completed_tasks.append(task)
        self.status = AgentStatus.IDLE
        return task.to_dict()

    def queue_task(self, task: Task) -> None:
        """Add task to execution queue."""
        self.task_queue.append(task)
        logger.info(f"Task {task.task_id} queued for agent {self.agent_id}")

    def get_status(self) -> Dict[str, Any]:
        """Get agent status snapshot."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": self.status.value,
            "queued_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "created_at": self.created_at.isoformat()
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": self.status.value,
            "config": self.config
        }


class AgentOrchestrator:
    """Central orchestrator for spawning, managing, and monitoring multi-agent workflows."""

    def __init__(self, max_agents: int = 10):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.max_agents = max_agents
        self.execution_history: List[Dict] = []

    def spawn_agent(self, role: str, agent_id: Optional[str] = None, config: Optional[Dict] = None) -> Agent:
        """
        Spawn a new autonomous agent.
        
        Args:
            role: Agent role/responsibility (e.g., 'security-scanner', 'dev-assistant')
            agent_id: Optional custom agent ID; auto-generated if not provided
            config: Agent configuration dict
            
        Returns:
            Created Agent instance
        """
        if len(self.agents) >= self.max_agents:
            raise RuntimeError(f"Maximum agent limit ({self.max_agents}) reached")

        agent_id = agent_id or f"{role}-{uuid.uuid4().hex[:8]}"
        agent = Agent(agent_id, role, config)
        self.agents[agent_id] = agent
        
        # Record metrics
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_agent_spawn(role)
        except ImportError:
            pass  # Monitoring not available
        
        logger.info(f"Spawned agent {agent_id} with role '{role}'")
        return agent

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all active agents with status."""
        return [agent.to_dict() for agent in self.agents.values()]

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed status of specific agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        return self.agents[agent_id].get_status()

    def create_task(self, description: str, agent_id: str, dependencies: Optional[List[str]] = None) -> Task:
        """Create and queue a task for an agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")

        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = Task(task_id, description, agent_id, dependencies)
        self.tasks[task_id] = task
        
        agent = self.agents[agent_id]
        agent.queue_task(task)
        
        # Record metrics
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_task_created(agent.role)
        except ImportError:
            pass  # Monitoring not available
        
        logger.info(f"Created task {task_id} for agent {agent_id}")
        return task

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a specific task on its assigned agent."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        agent = self.agents[task.agent_id]
        
        start_time = time.time()
        result = agent.execute_task(task)
        duration = time.time() - start_time
        
        # Record metrics
        try:
            from legion_core_claw.monitoring import metrics
            status = "completed" if task.status == "completed" else "error"
            metrics.record_task_completed(agent.role, status, duration)
        except ImportError:
            pass  # Monitoring not available
        
        self.execution_history.append({
            "task_id": task_id,
            "agent_id": task.agent_id,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        return result

    def execute_workflow(self, workflow_tasks: List[Dict[str, Any]]) -> List[Dict]:
        """
        Execute a workflow of dependent tasks.
        
        Args:
            workflow_tasks: List of task definitions with dependencies
            
        Returns:
            List of execution results
        """
        results = []
        for task_def in workflow_tasks:
            task = self.create_task(
                task_def["description"],
                task_def["agent_id"],
                task_def.get("dependencies", [])
            )
            result = self.execute_task(task.task_id)
            results.append(result)
        return results

    def terminate_agent(self, agent_id: str) -> None:
        """Terminate and remove an agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        agent.status = AgentStatus.TERMINATED
        del self.agents[agent_id]
        
        # Record metrics
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_agent_termination(agent.role)
        except ImportError:
            pass  # Monitoring not available
        
        logger.info(f"Terminated agent {agent_id}")

    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get overall orchestrator health and statistics."""
        return {
            "active_agents": len(self.agents),
            "total_tasks": len(self.tasks),
            "total_executions": len(self.execution_history),
            "max_agents": self.max_agents,
            "agents": self.list_agents()
        }
