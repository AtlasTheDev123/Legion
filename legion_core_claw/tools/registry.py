"""
Consolidated Tool Registry - Manages all available tools and functions with JSON schema definitions.
Merged from registry/tool_registry.json and schemas/functions.json
"""

import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class Tool:
    """Individual tool/function definition with schema."""

    def __init__(self, name: str, description: str, parameters: Dict[str, Any], 
                 example: Optional[Dict] = None, authorization_required: bool = False):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.example = example or {}
        self.authorization_required = authorization_required
        self.category = self._infer_category()

    def _infer_category(self) -> str:
        """Infer tool category from name and parameters."""
        if any(keyword in self.name for keyword in ["scan", "vuln", "security", "auth"]):
            return "security"
        elif any(keyword in self.name for keyword in ["deploy", "docker", "k8s"]):
            return "deployment"
        elif any(keyword in self.name for keyword in ["code", "gen", "dev"]):
            return "development"
        elif any(keyword in self.name for keyword in ["agent", "spawn", "task"]):
            return "orchestration"
        else:
            return "utility"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": self.parameters,
            "example": self.example,
            "authorization_required": self.authorization_required
        }

    def validate_parameters(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate parameters against schema."""
        required = self.parameters.get("required", [])
        for req_field in required:
            if req_field not in params:
                return False, f"Missing required parameter: {req_field}"
        return True, None


class ToolRegistry:
    """Central registry for all available tools and functions."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._load_default_tools()

    def _load_default_tools(self) -> None:
        """Load default tool catalog."""
        default_tools = [
            Tool(
                name="setup_dev_environment",
                description="Create project scaffold, init venv/container, and install base dependencies.",
                parameters={
                    "type": "object",
                    "properties": {
                        "project": {"type": "string"},
                        "language": {"type": "string"},
                        "dependencies": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["project", "language"]
                }
            ),
            Tool(
                name="dependency_scan",
                description="Run dependency/security scanner over a codebase.",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "tool": {"type": "string"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high"]}
                    },
                    "required": ["path", "tool"]
                }
            ),
            Tool(
                name="run_vulnerability_scan",
                description="Run network/vulnerability scan inside an isolated lab.",
                parameters={
                    "type": "object",
                    "properties": {
                        "target": {"type": "string"},
                        "scan_profile": {"type": "string"},
                        "authorization_token": {"type": "string"}
                    },
                    "required": ["target", "scan_profile", "authorization_token"]
                },
                authorization_required=True
            ),
            Tool(
                name="spawn_agent",
                description="Create and start an orchestration agent instance.",
                parameters={
                    "type": "object",
                    "properties": {
                        "role": {"type": "string"},
                        "config": {"type": "object"}
                    },
                    "required": ["role"]
                }
            ),
            Tool(
                name="generate_code",
                description="Generate code for specified language and requirements.",
                parameters={
                    "type": "object",
                    "properties": {
                        "language": {"type": "string"},
                        "requirements": {"type": "string"},
                        "framework": {"type": "string"}
                    },
                    "required": ["language", "requirements"]
                }
            ),
            Tool(
                name="deploy_service",
                description="Deploy service to Kubernetes, Docker, or serverless platform.",
                parameters={
                    "type": "object",
                    "properties": {
                        "service": {"type": "string"},
                        "platform": {"type": "string", "enum": ["docker", "k8s", "lambda"]},
                        "environment": {"type": "string"}
                    },
                    "required": ["service", "platform"]
                }
            )
        ]

        for tool in default_tools:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        """Register a new tool in the registry."""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Retrieve a tool by name."""
        return self.tools.get(tool_name)

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tools, optionally filtered by category."""
        tools = self.tools.values()
        if category:
            tools = [t for t in tools if t.category == category]
        return [t.to_dict() for t in tools]

    def list_categories(self) -> List[str]:
        """Get all tool categories."""
        return list(set(t.category for t in self.tools.values()))

    def find_tools_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Find tools matching keyword in name or description."""
        matches = [
            t for t in self.tools.values()
            if keyword.lower() in t.name.lower() or keyword.lower() in t.description.lower()
        ]
        return [t.to_dict() for t in matches]

    def validate_tool_call(self, tool_name: str, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate that a tool call is properly formatted."""
        tool = self.get_tool(tool_name)
        if not tool:
            return False, f"Unknown tool: {tool_name}"
        
        if tool.authorization_required and "authorization_token" not in params:
            return False, "Authorization token required"
        
        return tool.validate_parameters(params)

    def to_openai_format(self) -> List[Dict[str, Any]]:
        """Export registry to OpenAI function calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_tools": len(self.tools),
            "categories": self.list_categories(),
            "tools_by_category": {
                cat: len([t for t in self.tools.values() if t.category == cat])
                for cat in self.list_categories()
            },
            "authorization_required": [t.name for t in self.tools.values() if t.authorization_required]
        }
