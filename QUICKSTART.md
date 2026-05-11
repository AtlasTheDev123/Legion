# Legion Core Claw - Quick Start Guide

Get started with Legion Core Claw in 5 minutes!

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/AtlasTheDev123/Legion.git
cd Legion

# Run deployment script
bash deploy_core_claw.sh setup

# Activate virtual environment
source venv/bin/activate
```

## Configuration

```bash
# Create .env file
cp .env.example .env

# Edit with your settings (at minimum):
# - BOT_TOKEN: Your Telegram bot token
# - LLM_PROVIDER: openai, mistral, or localai
# - OPENAI_API_KEY: Your OpenAI key (if using OpenAI)
```

## First Run

### Option 1: Interactive CLI

```bash
python -m legion_core_claw.main
```

Then try these commands:
- `status` — Show system status
- `tools` — List available tools
- `spawn-agent security-scanner` — Create agent
- `help` — Show all commands

### Option 2: Python Script

```python
from legion_core_claw import AIEngine, AgentOrchestrator, ToolRegistry

# Initialize
ai = AIEngine()
orchestrator = AgentOrchestrator()
tools = ToolRegistry()

# Spawn agent
agent = orchestrator.spawn_agent(role="assistant")
print(f"Created agent: {agent.agent_id}")

# Create task
task = orchestrator.create_task(
    "Setup a Python development environment",
    agent.agent_id
)

# Execute task
result = orchestrator.execute_task(task.task_id)
print(f"Task result: {result}")
```

### Option 3: Telegram Bot

```bash
# Start the bot (requires BOT_TOKEN in .env)
python -m legion_core_claw.interfaces.bot
```

Available commands:
- `/help` — Show available commands
- `/list_tools` — See all tools
- `/spawn_agent security-scanner` — Create named agent
- `/status` — System status

### Option 4: REST API

```bash
# Start the API server
bash deploy_core_claw.sh start-server
```

API runs on `http://localhost:8000`

Endpoints:
- `GET /health` — Health check
- `GET /agents` — List agents
- `POST /agents/spawn` — Create agent
- `GET /tools` — List tools
- `POST /tools/execute` — Execute tool

## Common Tasks

### Create and Run an Agent

```python
from legion_core_claw import AgentOrchestrator

orchestrator = AgentOrchestrator()
agent = orchestrator.spawn_agent(role="developer")

task = orchestrator.create_task(
    "Generate a FastAPI REST API",
    agent.agent_id
)

result = orchestrator.execute_task(task.task_id)
```

### Use the AI Engine

```python
from legion_core_claw import AIEngine

ai = AIEngine(model="gpt-4", provider="openai")

# Get AI reasoning
plan = ai.reason("What are the top security vulnerabilities in Python?")
print(plan)
```

### Access Tools

```python
from legion_core_claw.tools import ToolRegistry

registry = ToolRegistry()

# List all tools
tools = registry.list_tools()
print(f"Available tools: {len(tools)}")

# List by category
security_tools = registry.list_tools(category="security")
print(f"Security tools: {security_tools}")

# Find tools by keyword
code_tools = registry.find_tools_by_keyword("code")
```

### Enable Audit Logging

```python
from legion_core_claw.utils import AuditLogger

audit = AuditLogger(enable_logging=True)
audit.log(
    event_type="agent_spawned",
    actor="system",
    action="spawn_agent",
    resource="security-agent-001"
)

print(audit.get_trail())
```

## Docker Deployment

```bash
# Build image
python docker_build.py --build --tag latest

# Run container
python docker_build.py --run --tag latest
```

Access at `http://localhost:8000`

## Next Steps

- Read the [full README](README.md)
- Check [API documentation](docs/function_reference_full.md)
- Review [architecture guide](docs/architecture.md)
- See [migration guide](MIGRATION.md) if upgrading from Legion v2

## Troubleshooting

### "BOT_TOKEN not configured"
Solution: Edit `.env` file and add your Telegram bot token

### "Module not found"
Solution: Ensure venv is activated:
```bash
source venv/bin/activate
```

### "Permission denied" on deploy_core_claw.sh
Solution: Make it executable:
```bash
chmod +x deploy_core_claw.sh
```

## Getting Help

- Check docs/ directory for detailed guides
- Review code examples in this file
- Open an issue on GitHub

## What's Next?

After exploring Legion Core Claw:

1. **Create your first agent** — Understand multi-agent orchestration
2. **Build a workflow** — Execute dependent tasks across agents
3. **Use custom tools** — Register your own tool functions
4. **Deploy to production** — Use Docker or cloud platforms
5. **Integrate with your stack** — Use REST API or Python library

---

**Version**: 3.0.0-core-claw  
**Status**: Production Ready (Beta)
