"""Configuration module for Legion Core Claw."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class Config:
    """Centralized configuration for Legion Core Claw."""
    
    # AI Engine configuration
    LLM_PROVIDER: str = os.environ.get("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.environ.get("LLM_MODEL", "gpt-4")
    
    # Bot configuration
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    ALLOWED_USERS: list = None  # Loaded from env
    DEFAULT_AUTH_TOKEN: str = os.environ.get("DEFAULT_AUTH_TOKEN", "[REDACTED_LAB_AUTH]")
    
    # Sandbox configuration
    SANDBOX_MODE: str = os.environ.get("SANDBOX_MODE", "simulated")  # 'simulated', 'sandboxed', 'direct'
    ALLOW_DIRECT_EXECUTION: bool = os.environ.get("ALLOW_DIRECT_EXECUTION", "0") == "1"
    
    # API configuration
    API_HOST: str = os.environ.get("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.environ.get("API_PORT", "8000"))
    
    # Security
    ENABLE_AUDIT_LOG: bool = os.environ.get("ENABLE_AUDIT_LOG", "1") == "1"
    
    # Agent configuration
    MAX_AGENTS: int = int(os.environ.get("MAX_AGENTS", "10"))
    DEFAULT_AGENT_TIMEOUT: int = int(os.environ.get("DEFAULT_AGENT_TIMEOUT", "300"))
    
    def __post_init__(self):
        """Post-initialization setup."""
        if self.ALLOWED_USERS is None:
            allowed = os.environ.get("ALLOWED_USERS", "")
            self.ALLOWED_USERS = [u.strip() for u in allowed.split(",") if u.strip()]

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls()

    @classmethod
    def from_file(cls, filepath: str) -> "Config":
        """Load configuration from JSON file."""
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return cls(**config_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (with secrets masked)."""
        return {
            "llm_provider": self.LLM_PROVIDER,
            "llm_model": self.LLM_MODEL,
            "sandbox_mode": self.SANDBOX_MODE,
            "api_host": self.API_HOST,
            "api_port": self.API_PORT,
            "max_agents": self.MAX_AGENTS
        }

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate configuration."""
        if self.SANDBOX_MODE not in ["simulated", "sandboxed", "direct"]:
            return False, f"Invalid SANDBOX_MODE: {self.SANDBOX_MODE}"
        
        if not self.LLM_PROVIDER:
            return False, "LLM_PROVIDER not configured"
        
        if not self.BOT_TOKEN:
            return False, "BOT_TOKEN not configured"
        
        return True, None
