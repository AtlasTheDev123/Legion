"""State management for Legion Core Claw."""

import logging
import json
import threading
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class StateBackend(ABC):
    """Abstract base class for state backends."""

    @abstractmethod
    def load_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Load state for a key."""
        pass

    @abstractmethod
    def save_state(self, key: str, state: Dict[str, Any]) -> None:
        """Save state for a key."""
        pass

    @abstractmethod
    def delete_state(self, key: str) -> bool:
        """Delete state for a key."""
        pass

    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix."""
        pass


class MemoryStateBackend(StateBackend):
    """In-memory state backend."""

    def __init__(self):
        self.states: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.RLock()

    def load_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Load state from memory."""
        with self.lock:
            return self.states.get(key)

    def save_state(self, key: str, state: Dict[str, Any]) -> None:
        """Save state to memory."""
        with self.lock:
            self.states[key] = state.copy()

    def delete_state(self, key: str) -> bool:
        """Delete state from memory."""
        with self.lock:
            if key in self.states:
                del self.states[key]
                return True
            return False

    def list_keys(self, prefix: str = "") -> List[str]:
        """List keys with prefix."""
        with self.lock:
            return [k for k in self.states.keys() if k.startswith(prefix)]


class FileStateBackend(StateBackend):
    """File-based state backend."""

    def __init__(self, storage_dir: str = "state"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()

    def _get_file_path(self, key: str) -> Path:
        """Get file path for a key."""
        # Sanitize key for filename
        safe_key = "".join(c for c in key if c.isalnum() or c in "._-").strip()
        return self.storage_dir / f"{safe_key}.json"

    def load_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Load state from file."""
        file_path = self._get_file_path(key)
        with self.lock:
            try:
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load state for {key}: {e}")
        return None

    def save_state(self, key: str, state: Dict[str, Any]) -> None:
        """Save state to file."""
        file_path = self._get_file_path(key)
        with self.lock:
            try:
                with open(file_path, 'w') as f:
                    json.dump(state, f, indent=2)
            except Exception as e:
                logger.error(f"Failed to save state for {key}: {e}")

    def delete_state(self, key: str) -> bool:
        """Delete state file."""
        file_path = self._get_file_path(key)
        with self.lock:
            try:
                if file_path.exists():
                    file_path.unlink()
                    return True
            except Exception as e:
                logger.error(f"Failed to delete state for {key}: {e}")
        return False

    def list_keys(self, prefix: str = "") -> List[str]:
        """List keys with prefix."""
        with self.lock:
            keys = []
            for file_path in self.storage_dir.glob("*.json"):
                key = file_path.stem
                if key.startswith(prefix):
                    keys.append(key)
            return keys


class AgentStateManager:
    """Manages agent state and memory."""

    def __init__(self, backend: Optional[StateBackend] = None):
        self.backend = backend or MemoryStateBackend()
        self.lock = threading.RLock()

    def save_agent_state(self, agent_id: str, state: Dict[str, Any]) -> None:
        """Save agent state."""
        key = f"agent:{agent_id}"
        state_with_meta = {
            "agent_id": agent_id,
            "data": state,
            "last_updated": time.time(),
            "version": state.get("version", 1)
        }
        self.backend.save_state(key, state_with_meta)
        logger.debug(f"Saved state for agent {agent_id}")

    def load_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent state."""
        key = f"agent:{agent_id}"
        state_data = self.backend.load_state(key)
        if state_data:
            return state_data.get("data", {})
        return None

    def delete_agent_state(self, agent_id: str) -> bool:
        """Delete agent state."""
        key = f"agent:{agent_id}"
        return self.backend.delete_state(key)

    def list_agents(self) -> List[str]:
        """List all agents with saved state."""
        keys = self.backend.list_keys("agent:")
        return [k.replace("agent:", "") for k in keys]

    def save_agent_memory(self, agent_id: str, memory_type: str, memory_data: Dict[str, Any]) -> None:
        """Save agent memory."""
        key = f"agent:{agent_id}:memory:{memory_type}"
        memory_with_meta = {
            "agent_id": agent_id,
            "memory_type": memory_type,
            "data": memory_data,
            "timestamp": time.time()
        }
        self.backend.save_state(key, memory_with_meta)

    def load_agent_memory(self, agent_id: str, memory_type: str) -> Optional[Dict[str, Any]]:
        """Load agent memory."""
        key = f"agent:{agent_id}:memory:{memory_type}"
        memory_data = self.backend.load_state(key)
        if memory_data:
            return memory_data.get("data", {})
        return None

    def get_agent_memory_types(self, agent_id: str) -> List[str]:
        """Get available memory types for agent."""
        prefix = f"agent:{agent_id}:memory:"
        keys = self.backend.list_keys(prefix)
        return [k.replace(prefix, "") for k in keys]


class WorkflowStateManager:
    """Manages workflow and task state."""

    def __init__(self, backend: Optional[StateBackend] = None):
        self.backend = backend or MemoryStateBackend()

    def save_workflow_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        """Save workflow state."""
        key = f"workflow:{workflow_id}"
        state_with_meta = {
            "workflow_id": workflow_id,
            "data": state,
            "last_updated": time.time()
        }
        self.backend.save_state(key, state_with_meta)

    def load_workflow_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Load workflow state."""
        key = f"workflow:{workflow_id}"
        state_data = self.backend.load_state(key)
        if state_data:
            return state_data.get("data", {})
        return None

    def save_task_state(self, task_id: str, state: Dict[str, Any]) -> None:
        """Save task state."""
        key = f"task:{task_id}"
        state_with_meta = {
            "task_id": task_id,
            "data": state,
            "last_updated": time.time()
        }
        self.backend.save_state(key, state_with_meta)

    def load_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Load task state."""
        key = f"task:{task_id}"
        state_data = self.backend.load_state(key)
        if state_data:
            return state_data.get("data", {})
        return None

    def list_active_workflows(self) -> List[str]:
        """List active workflows."""
        keys = self.backend.list_keys("workflow:")
        return [k.replace("workflow:", "") for k in keys]

    def list_pending_tasks(self) -> List[str]:
        """List pending tasks."""
        keys = self.backend.list_keys("task:")
        pending_tasks = []
        for key in keys:
            task_id = key.replace("task:", "")
            state = self.load_task_state(task_id)
            if state and state.get("status") == "pending":
                pending_tasks.append(task_id)
        return pending_tasks


class SystemStateManager:
    """Manages system-wide state."""

    def __init__(self, backend: Optional[StateBackend] = None):
        self.backend = backend or MemoryStateBackend()

    def save_system_config(self, config: Dict[str, Any]) -> None:
        """Save system configuration."""
        key = "system:config"
        config_with_meta = {
            "data": config,
            "last_updated": time.time(),
            "version": config.get("version", "1.0.0")
        }
        self.backend.save_state(key, config_with_meta)

    def load_system_config(self) -> Optional[Dict[str, Any]]:
        """Load system configuration."""
        key = "system:config"
        config_data = self.backend.load_state(key)
        if config_data:
            return config_data.get("data", {})
        return None

    def save_system_stats(self, stats: Dict[str, Any]) -> None:
        """Save system statistics."""
        key = "system:stats"
        stats_with_meta = {
            "data": stats,
            "timestamp": time.time()
        }
        self.backend.save_state(key, stats_with_meta)

    def load_system_stats(self) -> Optional[Dict[str, Any]]:
        """Load system statistics."""
        key = "system:stats"
        stats_data = self.backend.load_state(key)
        if stats_data:
            return stats_data.get("data", {})
        return None

    def save_user_session(self, user_id: str, session_data: Dict[str, Any]) -> None:
        """Save user session."""
        key = f"user:{user_id}:session"
        session_with_meta = {
            "user_id": user_id,
            "data": session_data,
            "last_active": time.time()
        }
        self.backend.save_state(key, session_with_meta)

    def load_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user session."""
        key = f"user:{user_id}:session"
        session_data = self.backend.load_state(key)
        if session_data:
            return session_data.get("data", {})
        return None

    def cleanup_expired_sessions(self, max_age_seconds: int = 86400) -> int:
        """Clean up expired user sessions."""
        keys = self.backend.list_keys("user:")
        cleaned = 0
        current_time = time.time()

        for key in keys:
            if ":session" in key:
                session_data = self.backend.load_state(key)
                if session_data:
                    last_active = session_data.get("last_active", 0)
                    if current_time - last_active > max_age_seconds:
                        self.backend.delete_state(key)
                        cleaned += 1

        return cleaned


class StateManager:
    """Unified state management system."""

    def __init__(self, backend: Optional[StateBackend] = None):
        self.backend = backend or FileStateBackend()
        self.agent_manager = AgentStateManager(self.backend)
        self.workflow_manager = WorkflowStateManager(self.backend)
        self.system_manager = SystemStateManager(self.backend)

    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of all managed state."""
        return {
            "agents": {
                "count": len(self.agent_manager.list_agents()),
                "agents": self.agent_manager.list_agents()
            },
            "workflows": {
                "count": len(self.workflow_manager.list_active_workflows()),
                "workflows": self.workflow_manager.list_active_workflows()
            },
            "tasks": {
                "pending_count": len(self.workflow_manager.list_pending_tasks()),
                "pending_tasks": self.workflow_manager.list_pending_tasks()
            },
            "backend_type": type(self.backend).__name__
        }


# Global state manager instance
state_manager = StateManager()

# Convenience functions
def save_agent_state(agent_id: str, state: Dict[str, Any]) -> None:
    """Save agent state."""
    state_manager.agent_manager.save_agent_state(agent_id, state)

def load_agent_state(agent_id: str) -> Optional[Dict[str, Any]]:
    """Load agent state."""
    return state_manager.agent_manager.load_agent_state(agent_id)

def save_workflow_state(workflow_id: str, state: Dict[str, Any]) -> None:
    """Save workflow state."""
    state_manager.workflow_manager.save_workflow_state(workflow_id, state)

def load_workflow_state(workflow_id: str) -> Optional[Dict[str, Any]]:
    """Load workflow state."""
    return state_manager.workflow_manager.load_workflow_state(workflow_id)

def save_system_config(config: Dict[str, Any]) -> None:
    """Save system configuration."""
    state_manager.system_manager.save_system_config(config)

def load_system_config() -> Optional[Dict[str, Any]]:
    """Load system configuration."""
    return state_manager.system_manager.load_system_config()