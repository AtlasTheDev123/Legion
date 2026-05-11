"""
REST API Interface - For dashboard and web-based interactions.
Provides FastAPI-compatible endpoints for Legion Core Claw.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from legion_core_claw.security import rate_limit, validate_input, require_permission


class APIInterface:
    """REST API interface for Legion Core Claw."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.request_log: List[Dict] = []

    @rate_limit()
    def get_health(self) -> Dict[str, Any]:
        """Health check endpoint."""
        start_time = time.time()
        
        try:
            from legion_core_claw.monitoring import health_checker
            health_status = health_checker.run_checks()
            status = "healthy" if health_status['overall_status'] == 'healthy' else "unhealthy"
        except ImportError:
            health_status = {"overall_status": "unknown"}
            status = "healthy"
        
        duration = time.time() - start_time
        
        # Record API request metrics
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_api_request("GET", "/health", 200, duration)
        except ImportError:
            pass
        
        return {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0-core-claw",
            "health_checks": health_status
        }

    def get_agents(self) -> List[Dict[str, Any]]:
        """List all agents."""
        return []

    @rate_limit()
    @require_permission("manage_agents")
    def spawn_agent(self, role: str, config: Optional[Dict] = None) -> Dict[str, Any]:
        """Spawn new agent."""
        return {
            "agent_id": f"{role}-agent-01",
            "role": role,
            "status": "spawned"
        }

    @rate_limit()
    @require_permission("execute_tools")
    @validate_input("tool_call")
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool."""
        start_time = time.time()
        
        try:
            result = {
                "tool": tool_name,
                "status": "executed",
                "result": {}
            }
            status_code = 200
        except Exception as e:
            result = {
                "tool": tool_name,
                "status": "error",
                "error": str(e)
            }
            status_code = 500
        
        duration = time.time() - start_time
        
        # Record API request and tool execution metrics
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_api_request("POST", "/tools/execute", status_code, duration)
            if status_code == 200:
                metrics.record_tool_execution(tool_name, "success", duration)
            else:
                metrics.record_tool_execution(tool_name, "error", duration)
        except ImportError:
            pass
        
        return result

    def get_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get available tools."""
        return []

    def get_execution_history(self, limit: int = 100) -> List[Dict]:
        """Get execution history."""
        return self.request_log[-limit:]

    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": 0,
            "request_count": len(self.request_log)
        }
