"""
Legion Core Claw - Main Entry Point
====================================

Unified command-line interface for Legion Core Claw system.
"""

import logging
import sys
from typing import Optional

from legion_core_claw import AIEngine, AgentOrchestrator, ToolRegistry
from legion_core_claw.interfaces import TelegramBotInterface, APIInterface
from legion_core_claw.config import Config
from legion_core_claw.utils import setup_logging, AuditLogger
from legion_core_claw.monitoring import metrics, health_checker


def initialize_system(config: Optional[Config] = None) -> dict:
    """Initialize all Legion Core Claw components."""
    config = config or Config.from_env()
    
    # Validate configuration
    valid, error = config.validate()
    if not valid:
        raise RuntimeError(f"Configuration validation failed: {error}")
    
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Initializing Legion Core Claw v3.0-CORE-CLAW")
    
    # Initialize core components
    ai_engine = AIEngine(model=config.LLM_MODEL, provider=config.LLM_PROVIDER)
    orchestrator = AgentOrchestrator(max_agents=config.MAX_AGENTS)
    tool_registry = ToolRegistry()
    
    # Initialize interfaces
    bot = TelegramBotInterface(bot_token=config.BOT_TOKEN)
    api = APIInterface(host=config.API_HOST, port=config.API_PORT)
    
    # Audit logger
    audit_logger = AuditLogger(enable_logging=config.ENABLE_AUDIT_LOG)
    
    logger.info("✓ All components initialized successfully")
    
    return {
        "config": config,
        "ai_engine": ai_engine,
        "orchestrator": orchestrator,
        "tool_registry": tool_registry,
        "bot": bot,
        "api": api,
        "audit_logger": audit_logger,
        "metrics": metrics,
        "health_checker": health_checker
    }


def show_status(system: dict) -> None:
    """Display system status."""
    print("\n" + "="*60)
    print("  LEGION CORE CLAW - System Status")
    print("="*60)
    print(f"  Version: 3.0.0-core-claw")
    print(f"  Config: {system['config'].to_dict()}")
    print(f"  Tools Available: {system['tool_registry'].get_registry_stats()['total_tools']}")
    print(f"  Orchestrator: {system['orchestrator'].get_orchestrator_status()}")
    
    # Add monitoring status
    health_status = system['health_checker'].run_checks()
    print(f"  System Health: {health_status['overall_status'].upper()}")
    print(f"  Active Agents: {system['metrics'].active_agents._value}")
    print(f"  Queued Tasks: {system['metrics'].queued_tasks._value}")
    
    print("="*60 + "\n")


def interactive_mode(system: dict) -> None:
    """Interactive REPL mode."""
    logger = logging.getLogger(__name__)
    print("\nLegion Core Claw Interactive Mode")
    print("Type 'help' for commands, 'quit' to exit\n")
    
    while True:
        try:
            user_input = input(">> ").strip()
            
            if not user_input:
                continue
            elif user_input == "quit":
                print("Exiting Legion Core Claw")
                break
            elif user_input == "help":
                print("""
Available Commands:
  status      - Show system status
  tools       - List available tools
  spawn-agent - Spawn new agent
  history     - Show execution history
  metrics     - Show Prometheus metrics
  health      - Run health checks
  quit        - Exit program
                """)
            elif user_input == "status":
                show_status(system)
            elif user_input == "tools":
                tools = system['tool_registry'].list_tools()
                print(f"\nAvailable Tools ({len(tools)}):")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description'][:60]}...")
            elif user_input.startswith("spawn-agent"):
                parts = user_input.split()
                role = parts[1] if len(parts) > 1 else "assistant"
                agent = system['orchestrator'].spawn_agent(role)
                print(f"✓ Spawned agent: {agent.agent_id}")
            elif user_input == "metrics":
                print("\nPrometheus Metrics:")
                print(system['metrics'].get_metrics())
            elif user_input == "health":
                health = system['health_checker'].run_checks()
                print(f"\nSystem Health: {health['overall_status'].upper()}")
                for check_name, check_result in health['checks'].items():
                    status = check_result['status'].upper()
                    critical = "(CRITICAL)" if check_result['critical'] else ""
                    print(f"  {check_name}: {status} {critical}")
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")


def main():
    """Main entry point."""
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize system
        system = initialize_system()
        
        # Show welcome banner
        show_status(system)
        
        # Enter interactive mode
        interactive_mode(system)
        
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
