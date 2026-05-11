# Legion Core Claw

⚡ **LEGION x L.X VEX — SERVING ATLAS** ⚡

A unified, modular **AI-driven DevSecOps and autonomous automation framework** combining multi-agent orchestration, advanced code generation, security testing, and full-stack deployment automation.

## Overview

**Legion Core Claw** is a consolidated, production-ready refactoring of the Legion framework, providing:

- **Autonomous Multi-Agent Orchestration** — Spawn and manage independent AI agents with task execution
- **Unified AI Engine** — Consolidated reasoning engine supporting OpenAI, Mistral, LocalAI, GitHub Copilot
- **Advanced Tool Registry** — 100+ AI-executable functions across 13+ languages
- **Multi-Interface Support** — Telegram bot, REST API, CLI, and programmatic access
- **Sandboxed Execution** — Safe code execution in isolated environments
- **Security Lab Suite** — Vulnerability scanning, penetration testing, remediation (lab-only)
- **Real-Time Monitoring** — Dashboard with WebSocket live updates
- **Audit & Compliance** — Complete audit trails, authorization tokens, security-first design

## Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional)
- Telegram Bot Token (for bot interface)

### Installation

```bash
# Clone repository
git clone https://github.com/AtlasTheDev123/Legion.git
cd Legion

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Telegram token and settings
```

### Usage

#### Interactive CLI

```bash
python -m legion_core_claw.main
```

#### As a Library

```python
from legion_core_claw import AIEngine, AgentOrchestrator, ToolRegistry

# Initialize components
ai_engine = AIEngine(model="gpt-4", provider="openai")
orchestrator = AgentOrchestrator(max_agents=10)
tools = ToolRegistry()

# Spawn an agent
agent = orchestrator.spawn_agent(role="security-scanner")

# Create and execute a task
task = orchestrator.create_task(
    description="Scan dependencies for vulnerabilities",
    agent_id=agent.agent_id
)
result = orchestrator.execute_task(task.task_id)
```

#### Telegram Bot

```bash
BOT_TOKEN="your-telegram-token" python -m legion_core_claw.interfaces.bot
```

Available commands:
- `/help` — Show available commands
- `/list_tools` — List all tools
- `/spawn_agent <role>` — Create new agent
- `/list_agents` — Show active agents
- `/status` — System status

## Project Structure

```
legion_core_claw/
├── core/               # AI reasoning engine
│   ├── ai_engine.py    # Unified LLM client
│   └── reasoning.py    # Planning and decomposition
├── agents/             # Multi-agent orchestration
│   ├── orchestrator.py # Agent lifecycle management
│   └── agent.py        # Individual agent implementation
├── tools/              # Function registry and execution
│   ├── registry.py     # Tool definitions and schemas
│   └── executor.py     # Sandboxed execution engine
├── interfaces/         # External communication
│   ├── bot.py          # Telegram bot interface
│   └── api.py          # REST API interface
├── config/             # Configuration management
│   └── __init__.py     # Config dataclass
├── utils/              # Utilities and helpers
│   └── __init__.py     # Audit logging, helpers
└── main.py             # CLI entry point
```

## Configuration

### Environment Variables

```bash
# LLM Configuration
LLM_PROVIDER=openai          # Provider: openai, mistral, localai, github-copilot
LLM_MODEL=gpt-4              # Model identifier

# Bot Configuration
BOT_TOKEN=your-telegram-token
ALLOWED_USERS=user1,user2
DEFAULT_AUTH_TOKEN=your-auth-token

# Execution Configuration
SANDBOX_MODE=simulated       # simulated, sandboxed, or direct
ALLOW_DIRECT_EXECUTION=0     # Enable direct code execution (dangerous)

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Agent Configuration
MAX_AGENTS=10
DEFAULT_AGENT_TIMEOUT=300

# Security
ENABLE_AUDIT_LOG=1
```

See `.env.example` for full configuration template.

## Available Tools

### Development
- `setup_dev_environment` — Initialize project scaffold and dependencies
- `generate_code` — Generate code in 13+ languages
- `dependency_scan` — Scan dependencies for vulnerabilities

### Security
- `dependency_scan` — Dependency vulnerability scanning
- `run_vulnerability_scan` — Network/port scanning (lab-only)
- `run_port_scan` — Targeted port scanning (lab-only)
- `create_remediation_patch` — Generate security patches

### Orchestration
- `spawn_agent` — Create autonomous agent instance
- `deploy_service` — Deploy to Docker, Kubernetes, or Lambda

## API Endpoints

### Health & Status
- `GET /health` — System health check
- `GET /status` — Detailed system status
- `GET /metrics` — Performance metrics

### Agents
- `GET /agents` — List active agents
- `POST /agents/spawn` — Spawn new agent
- `GET /agents/{id}/status` — Get agent status

### Tools
- `GET /tools` — List available tools
- `GET /tools/{category}` — Tools by category
- `POST /tools/execute` — Execute tool

### History
- `GET /history` — Execution history
- `GET /history/audit` — Audit trail

## Docker Deployment

```bash
# Build image
docker build -f runtime/Dockerfile -t legion-core-claw:latest .

# Run container
docker run -e BOT_TOKEN="your-token" \
           -e LLM_PROVIDER="openai" \
           -p 8000:8000 \
           legion-core-claw:latest
```

## Security Considerations

- **Lab Isolation** — Security tests run in isolated, authorized environments only
- **Auth Tokens** — Critical operations require explicit authorization tokens
- **Audit Logging** — All external actions logged with actor/timestamp
- **Sandboxing** — Code execution isolated by default (simulated mode)
- **No Committed Secrets** — `.env` files never committed
- **OWASP Top 10** — Security policies follow OWASP guidelines

## Testing

```bash
# Run test suite
./run_tests.sh

# Run specific test
pytest tests/test_functions_catalog.py -v
```

## Documentation

- [Architecture](docs/architecture.md) — System design and components
- [Deployment Guide](docs/deployment_guide.md) — Production setup
- [Function Reference](docs/function_reference_full.md) — Complete tool catalog
- [Telegram Integration](docs/telegram_integration.md) — Bot setup
- [Protocol Guide](docs/PROTOCOL_SANITIZED.md) — Safety-first implementation guide

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Licensed under the License file. See [LICENSE](LICENSE) for details.

## Support

- **Issues** — Report bugs or feature requests on GitHub
- **Discussions** — Ask questions in GitHub Discussions
- **Documentation** — See [docs/](docs/) for comprehensive guides

---

**Status**: v3.0.0-CORE-CLAW (Production Ready - Beta)  
**Maintained by**: ATLAS / NEXUS-LEGION  
**Last Updated**: 2026-05-11
