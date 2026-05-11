"""Utility functions and helpers."""

import logging
import hashlib
from typing import Any, Dict
from datetime import datetime
import json

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def hash_text(text: str) -> str:
    """Generate SHA256 hash of text."""
    return hashlib.sha256(text.encode()).hexdigest()


def sanitize_dict(data: Dict[str, Any], sensitive_keys: list = None) -> Dict:
    """Remove sensitive information from dictionary."""
    if sensitive_keys is None:
        sensitive_keys = ["token", "password", "secret", "key", "auth"]
    
    sanitized = {}
    for k, v in data.items():
        if any(keyword in k.lower() for keyword in sensitive_keys):
            sanitized[k] = "[REDACTED]"
        elif isinstance(v, dict):
            sanitized[k] = sanitize_dict(v, sensitive_keys)
        else:
            sanitized[k] = v
    return sanitized


def log_audit_event(event_type: str, actor: str, action: str, 
                   resource: str = "", status: str = "success", **kwargs) -> Dict:
    """Create audit log entry."""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "actor": actor,
        "action": action,
        "resource": resource,
        "status": status,
        "metadata": kwargs
    }
    logger.info(f"[AUDIT] {event_type}: {action} by {actor} on {resource} - {status}")
    return audit_entry


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as JSON with indentation."""
    return json.dumps(data, indent=indent, default=str)


def parse_json_safe(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON string."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON: {e}")
        return default


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


class AuditLogger:
    """Centralized audit logging."""
    
    def __init__(self, enable_logging: bool = True):
        self.enable_logging = enable_logging
        self.audit_trail: list = []
    
    def log(self, event_type: str, actor: str, action: str, resource: str = "", **kwargs):
        """Log an audit event."""
        entry = log_audit_event(event_type, actor, action, resource, **kwargs)
        self.audit_trail.append(entry)
        if self.enable_logging:
            logger.info(f"[AUDIT LOG] {entry}")
    
    def get_trail(self) -> list:
        """Get audit trail."""
        return self.audit_trail
    
    def clear_trail(self) -> None:
        """Clear audit trail."""
        self.audit_trail = []
