"""
Legion Core Claw - Unified AI DevSecOps Framework
================================================

A consolidated, modular AI-driven orchestration system combining:
- Autonomous multi-agent orchestration
- Advanced code generation and analysis
- Security testing and vulnerability management
- Full-stack deployment automation
- Real-time monitoring and intelligence

Version: 3.0-CORE-CLAW
Author: ATLAS / NEXUS-LEGION
"""

__version__ = "3.0.0-core-claw"
__author__ = "ATLAS"
__name__ = "Legion Core Claw"

from .core.ai_engine import AIEngine
from .agents.orchestrator import AgentOrchestrator
from .tools.registry import ToolRegistry
from .interfaces.bot import TelegramBotInterface

__all__ = [
    "AIEngine",
    "AgentOrchestrator",
    "ToolRegistry",
    "TelegramBotInterface",
]
