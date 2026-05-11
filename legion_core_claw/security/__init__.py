"""Security enhancements for Legion Core Claw."""

import logging
import time
from typing import Dict, Any, Optional, Callable
from collections import defaultdict
import hashlib
import re
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for API endpoints and user actions."""

    def __init__(self, requests_per_minute: int = 60, burst_limit: int = 10):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.requests: Dict[str, list] = defaultdict(list)
        self.burst_counts: Dict[str, int] = defaultdict(int)
        self.burst_reset_time: Dict[str, float] = defaultdict(float)

    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed under rate limits."""
        current_time = time.time()

        # Clean old requests (older than 1 minute)
        self.requests[key] = [t for t in self.requests[key] if current_time - t < 60]

        # Check burst limit
        if current_time - self.burst_reset_time[key] > 1:  # Reset burst every second
            self.burst_counts[key] = 0
            self.burst_reset_time[key] = current_time

        if self.burst_counts[key] >= self.burst_limit:
            return False

        # Check rate limit
        if len(self.requests[key]) >= self.requests_per_minute:
            return False

        # Record request
        self.requests[key].append(current_time)
        self.burst_counts[key] += 1

        return True

    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests allowed for the key."""
        current_time = time.time()
        self.requests[key] = [t for t in self.requests[key] if current_time - t < 60]
        return max(0, self.requests_per_minute - len(self.requests[key]))


class InputValidator:
    """Input validation and sanitization."""

    def __init__(self):
        # Dangerous patterns to block
        self.dangerous_patterns = [
            r'(?i)(rm\s+-rf\s+/)',  # rm -rf /
            r'(?i)(format\s+c:)',  # format c:
            r'(?i)(del\s+/f\s+/s\s+/q)',  # del /f /s /q
            r'(?i)(shutdown\s+-s)',  # shutdown -s
            r'<script[^>]*>.*?</script>',  # XSS scripts
            r'javascript:',  # JavaScript URLs
            r'data:text/html',  # Data URLs
            r'(?i)(eval\s*\()',  # eval() calls
            r'(?i)(exec\s*\()',  # exec() calls
            r'(?i)(import\s+os\s*;?\s*os\.)',  # os module abuse
            r'(?i)(subprocess\.)',  # subprocess calls
        ]

        # SQL injection patterns
        self.sql_injection_patterns = [
            r'(\'|").*?(union|select|insert|delete|update|drop).*?(\'|")',
            r'(\'|").*?(--|#|/\*).*?(\'|")',
            r'(\'|").*?(or|and).*?(\'|")',
        ]

    def sanitize_input(self, input_text: str) -> str:
        """Sanitize user input by removing dangerous content."""
        if not input_text:
            return ""

        # Remove null bytes and other control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_text)

        # Limit length
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000] + "..."

        return sanitized.strip()

    def validate_input(self, input_text: str, context: str = "general") -> tuple[bool, Optional[str]]:
        """
        Validate input for security issues.

        Args:
            input_text: Input to validate
            context: Context (api, bot, tool_call, etc.)

        Returns:
            (is_valid, error_message)
        """
        if not input_text:
            return True, None

        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                return False, f"Dangerous content detected in {context}"

        # Context-specific validation
        if context == "sql":
            for pattern in self.sql_injection_patterns:
                if re.search(pattern, input_text, re.IGNORECASE):
                    return False, "Potential SQL injection detected"

        elif context == "file_path":
            # Prevent directory traversal
            if ".." in input_text or input_text.startswith("/"):
                return False, "Invalid file path"

        elif context == "url":
            if not re.match(r'^https?://', input_text):
                return False, "Invalid URL format"

        return True, None

    def validate_tool_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate tool call parameters."""
        if not parameters:
            return True, None

        # Tool-specific validation
        if tool_name == "run_vulnerability_scan":
            if "target" in parameters:
                target = parameters["target"]
                if not re.match(r'^([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|(\d{1,3}\.){3}\d{1,3})$', target):
                    return False, "Invalid scan target format"

        elif tool_name in ["setup_dev_environment", "deploy_service"]:
            if "project" in parameters:
                project = parameters["project"]
                if not re.match(r'^[a-zA-Z0-9_-]+$', project):
                    return False, "Invalid project name format"

        # General parameter validation
        for key, value in parameters.items():
            if isinstance(value, str):
                is_valid, error = self.validate_input(value, "parameter")
                if not is_valid:
                    return False, f"Invalid parameter '{key}': {error}"

        return True, None


class SecurityAuditor:
    """Security auditing and logging."""

    def __init__(self):
        self.audit_log: list = []
        self.suspicious_activities: Dict[str, int] = defaultdict(int)

    def log_security_event(self, event_type: str, user_id: str, details: Dict[str, Any]) -> None:
        """Log security-related events."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details,
            "severity": self._calculate_severity(event_type, details)
        }

        self.audit_log.append(event)

        # Track suspicious activities
        if event["severity"] >= 7:
            self.suspicious_activities[user_id] += 1

        logger.warning(f"Security event: {event_type} by {user_id} (severity: {event['severity']})")

    def _calculate_severity(self, event_type: str, details: Dict[str, Any]) -> int:
        """Calculate severity score for security events."""
        severity_map = {
            "auth_failure": 5,
            "rate_limit_hit": 3,
            "suspicious_input": 6,
            "unauthorized_access": 8,
            "tool_abuse": 7,
            "system_command": 9,
        }

        base_severity = severity_map.get(event_type, 1)

        # Increase severity based on details
        if details.get("dangerous_pattern"):
            base_severity += 2
        if details.get("repeated_offense"):
            base_severity += 1

        return min(base_severity, 10)

    def get_audit_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get security audit summary."""
        cutoff_time = time.time() - (hours * 3600)
        recent_events = [e for e in self.audit_log if e["timestamp"] > cutoff_time]

        return {
            "total_events": len(recent_events),
            "events_by_type": defaultdict(int),
            "suspicious_users": dict(self.suspicious_activities),
            "high_severity_events": [e for e in recent_events if e["severity"] >= 7]
        }

    def is_user_suspicious(self, user_id: str, threshold: int = 3) -> bool:
        """Check if user has suspicious activity pattern."""
        return self.suspicious_activities[user_id] >= threshold


class AuthorizationManager:
    """Enhanced authorization with role-based access control."""

    def __init__(self):
        self.user_roles: Dict[str, str] = {}
        self.role_permissions: Dict[str, set] = {
            "admin": {"all"},
            "operator": {"read", "execute_tools", "manage_agents"},
            "user": {"read", "execute_safe_tools"},
            "guest": {"read"}
        }

    def assign_role(self, user_id: str, role: str) -> None:
        """Assign role to user."""
        if role not in self.role_permissions:
            raise ValueError(f"Unknown role: {role}")
        self.user_roles[user_id] = role
        logger.info(f"Assigned role '{role}' to user {user_id}")

    def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission."""
        user_role = self.user_roles.get(user_id, "guest")
        user_permissions = self.role_permissions.get(user_role, set())

        return "all" in user_permissions or permission in user_permissions

    def get_user_permissions(self, user_id: str) -> set:
        """Get all permissions for user."""
        user_role = self.user_roles.get(user_id, "guest")
        return self.role_permissions.get(user_role, set())


# Global instances
rate_limiter = RateLimiter()
input_validator = InputValidator()
security_auditor = SecurityAuditor()
auth_manager = AuthorizationManager()

# Default role assignments
auth_manager.assign_role("admin", "admin")
auth_manager.assign_role("operator", "operator")


def require_permission(permission: str):
    """Decorator to require specific permission."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract user_id from arguments (assuming it's the first arg after self)
            user_id = args[1] if len(args) > 1 else "unknown"

            if not auth_manager.check_permission(user_id, permission):
                security_auditor.log_security_event(
                    "unauthorized_access",
                    user_id,
                    {"permission": permission, "function": func.__name__}
                )
                raise PermissionError(f"Permission '{permission}' required")

            return func(*args, **kwargs)
        return wrapper
    return decorator


def rate_limit(key_func=None):
    """Decorator to apply rate limiting."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate rate limit key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                # Default: use first argument as key
                key = str(args[0]) if args else "unknown"

            if not rate_limiter.is_allowed(key):
                security_auditor.log_security_event(
                    "rate_limit_hit",
                    key,
                    {"function": func.__name__}
                )
                try:
                    from legion_core_claw.monitoring import metrics
                    metrics.record_rate_limit_hit(func.__name__)
                except ImportError:
                    pass
                raise Exception("Rate limit exceeded")

            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_input(context: str = "general"):
    """Decorator to validate input parameters."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = str(args[1]) if len(args) > 1 else "unknown"

            # Validate all string arguments
            for arg in args[1:]:  # Skip self
                if isinstance(arg, str):
                    is_valid, error = input_validator.validate_input(arg, context)
                    if not is_valid:
                        security_auditor.log_security_event(
                            "suspicious_input",
                            user_id,
                            {"error": error, "input": arg[:100], "context": context}
                        )
                        raise ValueError(f"Input validation failed: {error}")

            # Validate keyword arguments
            for key, value in kwargs.items():
                if isinstance(value, str):
                    is_valid, error = input_validator.validate_input(value, context)
                    if not is_valid:
                        security_auditor.log_security_event(
                            "suspicious_input",
                            user_id,
                            {"error": error, "parameter": key, "context": context}
                        )
                        raise ValueError(f"Parameter '{key}' validation failed: {error}")

            return func(*args, **kwargs)
        return wrapper
    return decorator