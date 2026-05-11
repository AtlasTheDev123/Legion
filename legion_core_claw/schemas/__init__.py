"""JSON schemas for Legion Core Claw."""

import json
from typing import Dict, Any, Optional
from pathlib import Path


# Tool definition schema
TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
            "description": "Tool name (alphanumeric and underscores only)"
        },
        "description": {
            "type": "string",
            "minLength": 10,
            "maxLength": 500,
            "description": "Tool description"
        },
        "category": {
            "type": "string",
            "enum": ["security", "deployment", "development", "orchestration", "utility"],
            "description": "Tool category"
        },
        "parameters": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["object"]},
                "properties": {"type": "object"},
                "required": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["type", "properties"]
        },
        "example": {
            "type": "object",
            "description": "Example usage"
        },
        "authorization_required": {
            "type": "boolean",
            "description": "Whether tool requires authorization"
        }
    },
    "required": ["name", "description", "parameters"]
}

# Agent configuration schema
AGENT_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "role": {
            "type": "string",
            "minLength": 3,
            "maxLength": 50,
            "description": "Agent role/responsibility"
        },
        "max_tasks": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
            "description": "Maximum concurrent tasks"
        },
        "timeout": {
            "type": "integer",
            "minimum": 10,
            "maximum": 3600,
            "description": "Task timeout in seconds"
        },
        "capabilities": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Agent capabilities"
        },
        "llm_config": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "temperature": {"type": "number", "minimum": 0, "maximum": 2},
                "max_tokens": {"type": "integer", "minimum": 1}
            }
        }
    },
    "required": ["role"]
}

# Task definition schema
TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {
            "type": "string",
            "minLength": 10,
            "maxLength": 1000,
            "description": "Task description"
        },
        "agent_id": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_-]+$",
            "description": "Assigned agent ID"
        },
        "dependencies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Task dependencies"
        },
        "priority": {
            "type": "string",
            "enum": ["low", "normal", "high", "critical"],
            "description": "Task priority"
        },
        "timeout": {
            "type": "integer",
            "minimum": 10,
            "maximum": 3600,
            "description": "Task timeout in seconds"
        },
        "parameters": {
            "type": "object",
            "description": "Task parameters"
        }
    },
    "required": ["description", "agent_id"]
}

# Workflow definition schema
WORKFLOW_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 100,
            "description": "Workflow name"
        },
        "description": {
            "type": "string",
            "minLength": 10,
            "maxLength": 1000,
            "description": "Workflow description"
        },
        "tasks": {
            "type": "array",
            "items": TASK_SCHEMA,
            "minItems": 1,
            "description": "Workflow tasks"
        },
        "agents": {
            "type": "array",
            "items": AGENT_CONFIG_SCHEMA,
            "description": "Required agents"
        },
        "max_execution_time": {
            "type": "integer",
            "minimum": 60,
            "maximum": 86400,
            "description": "Maximum execution time in seconds"
        },
        "error_handling": {
            "type": "object",
            "properties": {
                "on_task_failure": {
                    "type": "string",
                    "enum": ["stop", "continue", "retry"],
                    "description": "Action on task failure"
                },
                "max_retries": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 10,
                    "description": "Maximum retry attempts"
                }
            }
        }
    },
    "required": ["name", "description", "tasks"]
}

# API request/response schemas
API_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "method": {
            "type": "string",
            "enum": ["GET", "POST", "PUT", "DELETE"],
            "description": "HTTP method"
        },
        "endpoint": {
            "type": "string",
            "pattern": "^/[a-zA-Z0-9/_-]*$",
            "description": "API endpoint"
        },
        "parameters": {
            "type": "object",
            "description": "Request parameters"
        },
        "headers": {
            "type": "object",
            "description": "Request headers"
        },
        "body": {
            "type": "object",
            "description": "Request body"
        }
    },
    "required": ["method", "endpoint"]
}

API_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "status_code": {
            "type": "integer",
            "minimum": 100,
            "maximum": 599,
            "description": "HTTP status code"
        },
        "headers": {
            "type": "object",
            "description": "Response headers"
        },
        "body": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "message": {"type": "string"},
                "data": {"type": "object"},
                "timestamp": {"type": "string"}
            },
            "required": ["status"]
        }
    },
    "required": ["status_code", "body"]
}

# Bot message schemas
BOT_MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "User identifier"
        },
        "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4096,
            "description": "Message text"
        },
        "token": {
            "type": "string",
            "description": "Authorization token"
        },
        "timestamp": {
            "type": "string",
            "description": "Message timestamp"
        }
    },
    "required": ["user_id", "text"]
}

BOT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["ok", "error", "unauthorized"],
            "description": "Response status"
        },
        "message": {
            "type": "string",
            "description": "Response message"
        },
        "data": {
            "type": "object",
            "description": "Response data"
        },
        "timestamp": {
            "type": "string",
            "description": "Response timestamp"
        }
    },
    "required": ["status"]
}

# Configuration schema
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "LLM_MODEL": {
            "type": "string",
            "description": "LLM model identifier"
        },
        "LLM_PROVIDER": {
            "type": "string",
            "enum": ["openai", "mistral", "localai", "github-copilot", "anthropic"],
            "description": "LLM provider"
        },
        "BOT_TOKEN": {
            "type": "string",
            "description": "Telegram bot token"
        },
        "API_HOST": {
            "type": "string",
            "description": "API server host"
        },
        "API_PORT": {
            "type": "integer",
            "minimum": 1024,
            "maximum": 65535,
            "description": "API server port"
        },
        "MAX_AGENTS": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100,
            "description": "Maximum number of agents"
        },
        "ENABLE_AUDIT_LOG": {
            "type": "boolean",
            "description": "Enable audit logging"
        },
        "LOG_LEVEL": {
            "type": "string",
            "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            "description": "Logging level"
        }
    }
}

# Event schemas
EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {
            "type": "string",
            "pattern": "^[a-zA-Z_][a-zA-Z0-9_.:]*$",
            "description": "Event type identifier"
        },
        "data": {
            "type": "object",
            "description": "Event data payload"
        },
        "source": {
            "type": "string",
            "description": "Event source component"
        },
        "priority": {
            "type": "string",
            "enum": ["low", "normal", "high", "critical"],
            "description": "Event priority"
        },
        "timestamp": {
            "type": "number",
            "description": "Event timestamp"
        }
    },
    "required": ["event_type", "data", "source", "timestamp"]
}

# Plugin schemas
PLUGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
            "description": "Plugin name"
        },
        "version": {
            "type": "string",
            "pattern": "^\\d+\\.\\d+\\.\\d+$",
            "description": "Plugin version (semver)"
        },
        "description": {
            "type": "string",
            "minLength": 10,
            "maxLength": 500,
            "description": "Plugin description"
        },
        "type": {
            "type": "string",
            "enum": ["tool", "interface", "processor"],
            "description": "Plugin type"
        },
        "dependencies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Plugin dependencies"
        },
        "config": {
            "type": "object",
            "description": "Plugin configuration"
        }
    },
    "required": ["name", "version", "description", "type"]
}


class SchemaValidator:
    """JSON schema validator for Legion Core Claw."""

    def __init__(self):
        try:
            import jsonschema
            self.jsonschema = jsonschema
            self.available = True
        except ImportError:
            self.available = False
            logger.warning("jsonschema not available, validation disabled")

    def validate(self, data: Dict[str, Any], schema: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate data against schema.

        Args:
            data: Data to validate
            schema: JSON schema

        Returns:
            (is_valid, error_message)
        """
        if not self.available:
            return True, None

        try:
            self.jsonschema.validate(data, schema)
            return True, None
        except self.jsonschema.ValidationError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Schema validation error: {e}"

    def validate_tool(self, tool_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate tool definition."""
        return self.validate(tool_data, TOOL_SCHEMA)

    def validate_agent_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate agent configuration."""
        return self.validate(config, AGENT_CONFIG_SCHEMA)

    def validate_task(self, task_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate task definition."""
        return self.validate(task_data, TASK_SCHEMA)

    def validate_workflow(self, workflow_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate workflow definition."""
        return self.validate(workflow_data, WORKFLOW_SCHEMA)

    def validate_config(self, config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate system configuration."""
        return self.validate(config, CONFIG_SCHEMA)

    def validate_event(self, event_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate event data."""
        return self.validate(event_data, EVENT_SCHEMA)

    def validate_plugin(self, plugin_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate plugin definition."""
        return self.validate(plugin_data, PLUGIN_SCHEMA)


# Global schema validator instance
schema_validator = SchemaValidator()

# Convenience validation functions
def validate_tool_definition(tool_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate tool definition."""
    return schema_validator.validate_tool(tool_data)

def validate_agent_configuration(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate agent configuration."""
    return schema_validator.validate_agent_config(config)

def validate_task_definition(task_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate task definition."""
    return schema_validator.validate_task(task_data)

def validate_workflow_definition(workflow_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate workflow definition."""
    return schema_validator.validate_workflow(workflow_data)

def validate_system_config(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate system configuration."""
    return schema_validator.validate_config(config)


# Schema registry
SCHEMA_REGISTRY = {
    "tool": TOOL_SCHEMA,
    "agent_config": AGENT_CONFIG_SCHEMA,
    "task": TASK_SCHEMA,
    "workflow": WORKFLOW_SCHEMA,
    "api_request": API_REQUEST_SCHEMA,
    "api_response": API_RESPONSE_SCHEMA,
    "bot_message": BOT_MESSAGE_SCHEMA,
    "bot_response": BOT_RESPONSE_SCHEMA,
    "config": CONFIG_SCHEMA,
    "event": EVENT_SCHEMA,
    "plugin": PLUGIN_SCHEMA
}

def get_schema(schema_name: str) -> Optional[Dict[str, Any]]:
    """Get schema by name."""
    return SCHEMA_REGISTRY.get(schema_name)

def list_schemas() -> List[str]:
    """List available schemas."""
    return list(SCHEMA_REGISTRY.keys())

def save_schemas_to_file(file_path: str = "schemas.json") -> None:
    """Save all schemas to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(SCHEMA_REGISTRY, f, indent=2)

def load_schemas_from_file(file_path: str = "schemas.json") -> Dict[str, Any]:
    """Load schemas from a JSON file."""
    if Path(file_path).exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return SCHEMA_REGISTRY