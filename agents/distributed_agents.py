"""
Distributed Multi-Agent Coordination System
===========================================
Enables multiple AI agents to work together on complex tasks with:
- Agent spawning and lifecycle management
- Inter-agent communication
- Task decomposition and delegation
- Consensus building
- Conflict resolution
"""

import uuid
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
from queue import Queue, Empty
import json


class AgentRole(Enum):
    """Predefined agent roles"""
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    CODER = "coder"
    ANALYST = "analyst"
    CRITIC = "critic"
    EXECUTOR = "executor"
    SPECIALIST = "specialist"


class AgentStatus(Enum):
    """Agent lifecycle states"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


class MessageType(Enum):
    """Inter-agent message types"""
    TASK_ASSIGNMENT = "task_assignment"
    QUERY = "query"
    RESPONSE = "response"
    STATUS_UPDATE = "status_update"
    VOTE = "vote"
    CONSENSUS = "consensus"
    ALERT = "alert"


@dataclass
class AgentMessage:
    """Message structure for inter-agent communication"""
    message_id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    content: Any
    timestamp: str
    reply_to: Optional[str] = None
    requires_response: bool = False


@dataclass
class AgentTask:
    """Task assigned to an agent"""
    task_id: str
    description: str
    priority: int
    assigned_by: str
    deadline: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Any] = None
    status: str = "pending"


@dataclass
class Agent:
    """Autonomous agent with specific role and capabilities"""
    agent_id: str
    name: str
    role: AgentRole
    status: AgentStatus
    capabilities: List[str]
    current_task: Optional[AgentTask] = None
    task_history: List[AgentTask] = field(default_factory=list)
    message_queue: Queue = field(default_factory=Queue)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        if isinstance(self.message_queue, dict):
            self.message_queue = Queue()


class DistributedAgentSystem:
    """
    Manages distributed multi-agent coordination
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_log: List[AgentMessage] = []
        self.task_graph: Dict[str, AgentTask] = {}
        self.active_threads: Dict[str, threading.Thread] = {}
        self.lock = threading.Lock()
        self.running = True
        
        # Statistics
        self.total_tasks_completed = 0
        self.total_messages_sent = 0
        
        print("[DISTRIBUTED SYSTEM] Multi-agent coordination initialized")
    
    def spawn_agent(
        self,
        name: str,
        role: AgentRole,
        capabilities: List[str]
    ) -> str:
        """
        Spawn a new agent
        
        Args:
            name: Agent name
            role: Agent role
            capabilities: List of capabilities
            
        Returns:
            Agent ID
        """
        agent_id = f"{role.value}_{uuid.uuid4().hex[:8]}"
        
        agent = Agent(
            agent_id=agent_id,
            name=name,
            role=role,
            status=AgentStatus.IDLE,
            capabilities=capabilities
        )
        
        with self.lock:
            self.agents[agent_id] = agent
        
        print(f"[AGENT SPAWNED] {name} ({agent_id}) - Role: {role.value}")
        return agent_id
    
    def terminate_agent(self, agent_id: str):
        """Terminate an agent"""
        with self.lock:
            if agent_id in self.agents:
                self.agents[agent_id].status = AgentStatus.TERMINATED
                print(f"[AGENT TERMINATED] {agent_id}")
    
    def assign_task(
        self,
        agent_id: str,
        description: str,
        priority: int = 5,
        assigned_by: str = "system",
        dependencies: Optional[List[str]] = None
    ) -> str:
        """
        Assign task to agent
        
        Args:
            agent_id: Target agent ID
            description: Task description
            priority: Priority level (1-10)
            assigned_by: Who assigned the task
            dependencies: Task dependencies
            
        Returns:
            Task ID
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        task = AgentTask(
            task_id=task_id,
            description=description,
            priority=priority,
            assigned_by=assigned_by,
            dependencies=dependencies or []
        )
        
        with self.lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.current_task = task
                agent.status = AgentStatus.WORKING
                self.task_graph[task_id] = task
        
        # Send task assignment message
        self.send_message(
            from_agent="system",
            to_agent=agent_id,
            message_type=MessageType.TASK_ASSIGNMENT,
            content={"task_id": task_id, "description": description}
        )
        
        print(f"[TASK ASSIGNED] {task_id} → {agent_id}: {description[:50]}...")
        return task_id
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        content: Any,
        requires_response: bool = False
    ) -> str:
        """
        Send message between agents
        
        Args:
            from_agent: Sender agent ID
            to_agent: Recipient agent ID
            message_type: Type of message
            content: Message content
            requires_response: Whether response is required
            
        Returns:
            Message ID
        """
        message_id = f"msg_{uuid.uuid4().hex[:8]}"
        
        message = AgentMessage(
            message_id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            timestamp=datetime.now().isoformat(),
            requires_response=requires_response
        )
        
        with self.lock:
            # Add to recipient's queue
            if to_agent in self.agents:
                self.agents[to_agent].message_queue.put(message)
            
            # Log message
            self.message_log.append(message)
            self.total_messages_sent += 1
        
        return message_id
    
    def broadcast_message(
        self,
        from_agent: str,
        message_type: MessageType,
        content: Any,
        exclude: Optional[List[str]] = None
    ):
        """Broadcast message to all agents"""
        exclude = exclude or []
        
        with self.lock:
            for agent_id in self.agents.keys():
                if agent_id not in exclude and agent_id != from_agent:
                    self.send_message(from_agent, agent_id, message_type, content)
    
    def get_messages(self, agent_id: str, timeout: float = 0.1) -> List[AgentMessage]:
        """Get pending messages for agent"""
        messages = []
        
        if agent_id not in self.agents:
            return messages
        
        agent = self.agents[agent_id]
        
        try:
            while True:
                message = agent.message_queue.get(timeout=timeout)
                messages.append(message)
        except Empty:
            pass
        
        return messages
    
    def complete_task(self, agent_id: str, result: Any):
        """Mark agent's current task as completed"""
        with self.lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                if agent.current_task:
                    agent.current_task.result = result
                    agent.current_task.status = "completed"
                    agent.task_history.append(agent.current_task)
                    
                    task_id = agent.current_task.task_id
                    self.task_graph[task_id].status = "completed"
                    self.task_graph[task_id].result = result
                    
                    agent.current_task = None
                    agent.status = AgentStatus.IDLE
                    self.total_tasks_completed += 1
                    
                    print(f"[TASK COMPLETED] {task_id} by {agent_id}")
    
    def request_consensus(
        self,
        coordinator_id: str,
        question: str,
        options: List[str]
    ) -> Dict[str, int]:
        """
        Request consensus from all agents
        
        Args:
            coordinator_id: Coordinator agent ID
            question: Question to vote on
            options: Available options
            
        Returns:
            Vote counts per option
        """
        # Broadcast vote request
        self.broadcast_message(
            from_agent=coordinator_id,
            message_type=MessageType.VOTE,
            content={"question": question, "options": options},
            exclude=[coordinator_id]
        )
        
        # Wait for responses (simplified - in production use proper async)
        time.sleep(0.5)
        
        # Tally votes
        votes = {option: 0 for option in options}
        
        for message in self.message_log[-len(self.agents):]:
            if message.message_type == MessageType.VOTE and isinstance(message.content, dict):
                vote = message.content.get("vote")
                if vote in votes:
                    votes[vote] += 1
        
        return votes
    
    def decompose_task(
        self,
        task_description: str,
        num_subtasks: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Decompose complex task into subtasks
        
        Args:
            task_description: Main task description
            num_subtasks: Number of subtasks to create
            
        Returns:
            List of subtask definitions
        """
        subtasks = []
        
        # Simple decomposition (in production, use AI to decompose)
        for i in range(num_subtasks):
            subtasks.append({
                "subtask_id": f"subtask_{i+1}",
                "description": f"{task_description} - Part {i+1}/{num_subtasks}",
                "priority": 5,
                "dependencies": [f"subtask_{i}"] if i > 0 else []
            })
        
        return subtasks
    
    def assign_task_to_best_agent(
        self,
        task_description: str,
        required_capability: Optional[str] = None
    ) -> Optional[str]:
        """
        Find and assign task to most suitable agent
        
        Args:
            task_description: Task description
            required_capability: Required capability
            
        Returns:
            Assigned agent ID or None
        """
        best_agent = None
        best_score = -1
        
        with self.lock:
            for agent_id, agent in self.agents.items():
                if agent.status == AgentStatus.IDLE:
                    score = 0
                    
                    # Check capability match
                    if required_capability and required_capability in agent.capabilities:
                        score += 10
                    
                    # Prefer agents with less task history
                    score -= len(agent.task_history)
                    
                    if score > best_score:
                        best_score = score
                        best_agent = agent_id
        
        if best_agent:
            return self.assign_task(best_agent, task_description)
        
        return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        with self.lock:
            status = {
                "total_agents": len(self.agents),
                "active_agents": sum(1 for a in self.agents.values() if a.status == AgentStatus.WORKING),
                "idle_agents": sum(1 for a in self.agents.values() if a.status == AgentStatus.IDLE),
                "total_tasks": len(self.task_graph),
                "completed_tasks": self.total_tasks_completed,
                "pending_tasks": sum(1 for t in self.task_graph.values() if t.status == "pending"),
                "total_messages": self.total_messages_sent,
                "agents": []
            }
            
            for agent in self.agents.values():
                status["agents"].append({
                    "id": agent.agent_id,
                    "name": agent.name,
                    "role": agent.role.value,
                    "status": agent.status.value,
                    "capabilities": agent.capabilities,
                    "tasks_completed": len(agent.task_history)
                })
        
        return status
    
    def shutdown(self):
        """Shutdown the distributed system"""
        self.running = False
        
        with self.lock:
            for agent_id in list(self.agents.keys()):
                self.terminate_agent(agent_id)
        
        print("[DISTRIBUTED SYSTEM] Shutdown complete")


def demo_distributed_agents():
    """Demonstrate distributed multi-agent system"""
    print("=" * 70)
    print("DISTRIBUTED MULTI-AGENT SYSTEM - Demo")
    print("=" * 70)
    
    system = DistributedAgentSystem()
    
    # Spawn diverse team
    print("\n[1] Spawning Agent Team:")
    coordinator = system.spawn_agent(
        "TaskMaster",
        AgentRole.COORDINATOR,
        ["planning", "coordination", "delegation"]
    )
    
    researcher = system.spawn_agent(
        "InfoGatherer",
        AgentRole.RESEARCHER,
        ["research", "data_collection", "analysis"]
    )
    
    coder = system.spawn_agent(
        "CodeWizard",
        AgentRole.CODER,
        ["coding", "debugging", "optimization"]
    )
    
    analyst = system.spawn_agent(
        "DataAnalyst",
        AgentRole.ANALYST,
        ["analysis", "visualization", "reporting"]
    )
    
    critic = system.spawn_agent(
        "QualityChecker",
        AgentRole.CRITIC,
        ["review", "testing", "validation"]
    )
    
    # Assign tasks
    print("\n[2] Task Assignment:")
    system.assign_task(
        researcher,
        "Research best practices for API security",
        priority=8
    )
    
    system.assign_task(
        coder,
        "Implement JWT authentication middleware",
        priority=9
    )
    
    system.assign_task(
        analyst,
        "Analyze system performance metrics",
        priority=6
    )
    
    # Inter-agent communication
    print("\n[3] Inter-Agent Communication:")
    system.send_message(
        from_agent=coordinator,
        to_agent=researcher,
        message_type=MessageType.QUERY,
        content="What's the status on security research?",
        requires_response=True
    )
    
    system.send_message(
        from_agent=researcher,
        to_agent=coordinator,
        message_type=MessageType.RESPONSE,
        content="Research 80% complete. Found OWASP Top 10 recommendations."
    )
    
    # Simulate task completion
    print("\n[4] Task Completion:")
    system.complete_task(researcher, {
        "findings": ["Use HTTPS", "Implement rate limiting", "Add input validation"],
        "confidence": 0.95
    })
    
    system.complete_task(coder, {
        "implementation": "JWT middleware implemented with refresh tokens",
        "tests_passing": True
    })
    
    # Consensus building
    print("\n[5] Consensus Building:")
    votes = system.request_consensus(
        coordinator_id=coordinator,
        question="Which database should we use?",
        options=["PostgreSQL", "MongoDB", "Redis"]
    )
    print(f"Vote results: {votes}")
    
    # Task decomposition
    print("\n[6] Task Decomposition:")
    subtasks = system.decompose_task(
        "Build complete authentication system",
        num_subtasks=4
    )
    print(f"Decomposed into {len(subtasks)} subtasks:")
    for st in subtasks:
        print(f"  - {st['description']}")
    
    # System status
    print("\n[7] System Status:")
    status = system.get_system_status()
    print(json.dumps(status, indent=2))
    
    # Shutdown
    system.shutdown()
    
    print("\n" + "=" * 70)
    print("⚡ Distributed Multi-Agent System Demo Complete ⚡")
    print("=" * 70)


if __name__ == "__main__":
    demo_distributed_agents()
