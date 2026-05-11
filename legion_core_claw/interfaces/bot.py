"""
Telegram Bot Interface - Consolidated from bot/vex_x_bot.py and bot/sandbox.py
Provides Telegram-based interaction with Legion Core Claw system.
"""

import logging
from typing import Dict, Any, Optional, List
import os
import time

from legion_core_claw.security import rate_limit, validate_input, require_permission


class TelegramBotInterface:
    """Telegram bot for interacting with Legion Core Claw system."""

    def __init__(self, bot_token: Optional[str] = None, allowed_users: Optional[List[str]] = None):
        """
        Initialize Telegram bot.
        
        Args:
            bot_token: Telegram bot token (from env if not provided)
            allowed_users: List of authorized user IDs
        """
        self.bot_token = bot_token or os.environ.get("BOT_TOKEN")
        self.allowed_users = allowed_users or (
            os.environ.get("ALLOWED_USERS", "").split(",") if os.environ.get("ALLOWED_USERS") else []
        )
        self.default_auth_token = os.environ.get("DEFAULT_AUTH_TOKEN", "[REDACTED_LAB_AUTH]")
        self.message_history: List[Dict] = []
        self.commands = {
            "/help": "Show available commands",
            "/list_tools": "List all available tools",
            "/call": "Call a tool with parameters",
            "/ask": "Ask AI assistant",
            "/status": "Get system status",
            "/voice": "Voice message support",
            "/spawn_agent": "Spawn a new agent",
            "/list_agents": "List active agents",
        }

    def is_authorized(self, user_id: str, token: str) -> bool:
        """Check if user is authorized."""
        if not token:
            return False
        if self.allowed_users and user_id not in self.allowed_users:
            return False
        return token == self.default_auth_token

    @rate_limit()
    @validate_input("bot_message")
    def handle_message(self, user_id: str, text: str, token: str) -> Dict[str, Any]:
        """
        Handle incoming message from user.
        
        Args:
            user_id: Telegram user ID
            text: Message content
            token: Authorization token
            
        Returns:
            Response dict with status and message
        """
        start_time = time.time()
        
        if not self.is_authorized(user_id, token):
            response = {
                "status": "unauthorized",
                "message": "Authorization failed. Please provide valid token."
            }
            # Record failed auth attempt
            try:
                from legion_core_claw.monitoring import metrics
                metrics.record_auth_attempt("failed")
                metrics.record_bot_message("command", "unauthorized")
            except ImportError:
                pass
            return response

        # Parse command vs free-form query
        if text.startswith("/"):
            response = self._handle_command(user_id, text)
            message_type = "command"
        else:
            response = self._handle_query(user_id, text)
            message_type = "query"
        
        duration = time.time() - start_time
        
        # Record successful message processing
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_auth_attempt("success")
            metrics.record_bot_message(message_type, response.get("status", "unknown"))
            if text.startswith("/"):
                cmd = text.split()[0]
                metrics.record_bot_command(cmd)
        except ImportError:
            pass
        
        return response

    def _handle_command(self, user_id: str, command: str) -> Dict[str, Any]:
        """Handle slash commands."""
        cmd = command.split()[0]
        args = command.split()[1:] if len(command.split()) > 1 else []

        if cmd == "/help":
            return self._cmd_help(user_id)
        elif cmd == "/list_tools":
            return self._cmd_list_tools(user_id)
        elif cmd == "/status":
            return self._cmd_status(user_id)
        elif cmd == "/spawn_agent":
            return self._cmd_spawn_agent(user_id, args)
        elif cmd == "/list_agents":
            return self._cmd_list_agents(user_id)
        else:
            return {"status": "error", "message": f"Unknown command: {cmd}"}

    def _handle_query(self, user_id: str, query: str) -> Dict[str, Any]:
        """Handle free-form query."""
        logger.info(f"Query from {user_id}: {query[:50]}...")
        return {
            "status": "received",
            "message": f"Processing query: {query[:100]}..."
        }

    def _cmd_help(self, user_id: str) -> Dict[str, Any]:
        """Help command."""
        help_text = "**Legion Core Claw Commands:**\n"
        for cmd, desc in self.commands.items():
            help_text += f"  {cmd}: {desc}\n"
        return {"status": "ok", "message": help_text}

    def _cmd_list_tools(self, user_id: str) -> Dict[str, Any]:
        """List available tools."""
        return {
            "status": "ok",
            "message": "Available tools: setup_dev_environment, dependency_scan, spawn_agent, etc."
        }

    def _cmd_status(self, user_id: str) -> Dict[str, Any]:
        """System status."""
        return {
            "status": "ok",
            "system_status": "operational",
            "message": "Legion Core Claw is operational"
        }

    def _cmd_spawn_agent(self, user_id: str, args: List[str]) -> Dict[str, Any]:
        """Spawn agent command."""
        role = args[0] if args else "assistant"
        return {
            "status": "ok",
            "message": f"Spawned agent with role: {role}"
        }

    def _cmd_list_agents(self, user_id: str) -> Dict[str, Any]:
        """List active agents."""
        return {
            "status": "ok",
            "agents": [],
            "message": "No active agents"
        }

    def send_message(self, user_id: str, text: str) -> bool:
        """Send message to user."""
        logger.info(f"Sending to {user_id}: {text[:50]}...")
        return True

    def get_message_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get message history for user."""
        return [m for m in self.message_history if m.get("user_id") == user_id][-limit:]

    def simulate_execution(self, function_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate function execution (sandbox mode)."""
        return {
            "function": function_name,
            "status": "simulated",
            "input": params,
            "result": f"Simulated result for {function_name}"
        }
