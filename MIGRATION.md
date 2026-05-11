# Migration Guide: Legion → Legion Core Claw

## Overview

This guide explains how to migrate from the original Legion framework to the new **Legion Core Claw** modular architecture.

## Key Changes

### 1. Module Structure

**Before (Legion)**:
```
agents/
  ├── agent_manager.py
  ├── ai_core.py
  └── tasks.py
bot/
  ├── vex_x_bot.py
  ├── sandbox.py
  ├── voice.py
  └── config.py
dashboard/
  ├── backend/
  └── frontend/
```

**After (Legion Core Claw)**:
```
legion_core_claw/
├── core/           # Unified AI engine
├── agents/         # Multi-agent orchestration
├── tools/          # Function registry
├── interfaces/     # Bot, API, CLI
├── config/         # Configuration
└── utils/          # Utilities
```

### 2. Import Changes

**Before**:
```python
from agents.ai_core import summarize
from agents.agent_manager import AgentManager
from bot.sandbox import simulate_execution
```

**After**:
```python
from legion_core_claw import AIEngine, AgentOrchestrator, ToolRegistry
from legion_core_claw.interfaces import TelegramBotInterface
```

### 3. Configuration

**Before**: Scattered across bot/config.py, environment variables
**After**: Centralized in Config dataclass with validation

```python
from legion_core_claw.config import Config

config = Config.from_env()
valid, error = config.validate()
```

### 4. Tool Registry

**Before**: Schemas in separate JSON files
**After**: Unified ToolRegistry with JSON schema support

```python
registry = ToolRegistry()
tools = registry.list_tools(category="security")
```

### 5. Agent Orchestration

**Before**: Simple agent_manager with stubs
**After**: Full orchestrator with task scheduling, execution history

```python
orchestrator = AgentOrchestrator(max_agents=10)
agent = orchestrator.spawn_agent(role="security-scanner")
task = orchestrator.create_task("Scan dependencies", agent.agent_id)
result = orchestrator.execute_task(task.task_id)
```

## Migration Steps

### Step 1: Update Imports

Replace old imports:
```python
# Old
from agents.ai_core import summarize
from agents.agent_manager import AgentManager
from bot.vex_x_bot import TelegramBotInterface

# New
from legion_core_claw import AIEngine, AgentOrchestrator
from legion_core_claw.interfaces import TelegramBotInterface
```

### Step 2: Update Configuration

Move configuration to .env file:
```bash
cp .env.example .env
# Edit .env with your values
```

### Step 3: Update Initialization

**Before**:
```python
from agents.ai_core import summarize
from agents.agent_manager import AgentManager
from bot.config import is_authorized

manager = AgentManager()
manager.spawn("agent-1", {"role": "assistant"})
```

**After**:
```python
from legion_core_claw import AIEngine, AgentOrchestrator
from legion_core_claw.config import Config

config = Config.from_env()
orchestrator = AgentOrchestrator(max_agents=config.MAX_AGENTS)
agent = orchestrator.spawn_agent(role="assistant")
```

### Step 4: Update Tool Calls

**Before**:
```python
from bot.sandbox import simulate_execution

result = simulate_execution("scan_dependencies", {"path": "/project"})
```

**After**:
```python
from legion_core_claw.tools import ToolExecutor, ToolRegistry

registry = ToolRegistry()
executor = ToolExecutor(sandbox_mode="simulated")
result = executor.execute("dependency_scan", {"path": "/project"})
```

### Step 5: Update Bot Integration

**Before**:
```python
from bot.vex_x_bot import TelegramBotInterface
from bot.config import is_authorized, BOT_TOKEN

bot = TelegramBotInterface()
```

**After**:
```python
from legion_core_claw.interfaces import TelegramBotInterface
from legion_core_claw.config import Config

config = Config.from_env()
bot = TelegramBotInterface(bot_token=config.BOT_TOKEN)
```

## Backward Compatibility

The original Legion files are still present in the repository but are now considered legacy. New code should use the Legion Core Claw modules.

## Common Patterns

### Creating Multi-Agent Workflow

```python
from legion_core_claw import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Spawn multiple agents
security_agent = orchestrator.spawn_agent(role="security-scanner")
dev_agent = orchestrator.spawn_agent(role="developer")

# Create workflow
workflow = [
    {"description": "Scan dependencies", "agent_id": security_agent.agent_id},
    {"description": "Fix vulnerabilities", "agent_id": dev_agent.agent_id},
]

results = orchestrator.execute_workflow(workflow)
```

### Using AI Engine

```python
from legion_core_claw import AIEngine

ai = AIEngine(model="gpt-4", provider="openai")

# Reason about task
plan = ai.reason("Analyze this security report for risks")

# Select appropriate tools
tools = ai.select_tools(plan, available_tools)

# Execute with tools
result = ai.execute_with_tools(plan, tools)
```

### Registering Custom Tools

```python
from legion_core_claw.tools import ToolRegistry, Tool

registry = ToolRegistry()

custom_tool = Tool(
    name="custom-scanner",
    description="My custom security scanner",
    parameters={
        "type": "object",
        "properties": {
            "target": {"type": "string"}
        },
        "required": ["target"]
    }
)

registry.register(custom_tool)
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'legion_core_claw'`
**Solution**: Ensure you're in the correct directory and venv is activated:
```bash
cd /path/to/Legion
source venv/bin/activate
```

### Configuration Errors

**Problem**: `Configuration validation failed: BOT_TOKEN not configured`
**Solution**: Create and populate .env file:
```bash
cp .env.example .env
# Edit .env with your values
```

### Tool Registry Empty

**Problem**: No tools available in registry
**Solution**: Ensure ToolRegistry is initialized properly:
```python
from legion_core_claw.tools import ToolRegistry
registry = ToolRegistry()  # Loads default tools
print(registry.get_registry_stats())
```

## Additional Resources

- [API Documentation](docs/function_reference_full.md)
- [Architecture Guide](docs/architecture.md)
- [Deployment Guide](docs/deployment_guide.md)
