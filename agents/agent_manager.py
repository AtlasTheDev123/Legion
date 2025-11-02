"""Simple agent manager stub."""
from typing import Dict, Any

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}

    def spawn(self, agent_id: str, config: dict):
        self.agents[agent_id] = {'config': config, 'status': 'idle'}
        return self.agents[agent_id]

    def list_agents(self):
        return list(self.agents.keys())
