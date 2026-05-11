# Legion Core Claw - Project Structure

## Complete Directory Tree

```
/workspaces/Legion/
│
├── legion_core_claw/                  ⭐ NEW - Core Framework
│   ├── __init__.py                    # Package exports
│   ├── main.py                        # CLI entry point
│   │
│   ├── core/                          # AI Engine & Reasoning
│   │   ├── __init__.py
│   │   ├── ai_engine.py               # Unified LLM client (170+ lines)
│   │   └── reasoning.py               # Planning engine (60+ lines)
│   │
│   ├── agents/                        # Multi-Agent Orchestration
│   │   ├── __init__.py
│   │   ├── orchestrator.py            # Agent manager (280+ lines)
│   │   └── agent.py                   # Individual agent (30+ lines)
│   │
│   ├── tools/                         # Function Registry & Execution
│   │   ├── __init__.py
│   │   ├── registry.py                # Tool catalog (250+ lines)
│   │   └── executor.py                # Sandbox execution (70+ lines)
│   │
│   ├── interfaces/                    # External Communication
│   │   ├── __init__.py
│   │   ├── bot.py                     # Telegram interface (180+ lines)
│   │   └── api.py                     # REST API interface (80+ lines)
│   │
│   ├── config/                        # Configuration
│   │   └── __init__.py                # Config dataclass (120+ lines)
│   │
│   └── utils/                         # Utilities & Helpers
│       └── __init__.py                # Logging, helpers (150+ lines)
│
├── Documentation
│   ├── README.md                      ⭐ UPDATED - Main documentation
│   ├── QUICKSTART.md                  ⭐ NEW - 5-minute guide
│   ├── MIGRATION.md                   ⭐ NEW - v2 migration guide
│   ├── REFACTORING_SUMMARY.md         ⭐ NEW - Transformation report
│   ├── COMPLETION_REPORT.md           ⭐ NEW - Completion summary
│   └── STRUCTURE.md                   ⭐ NEW - This file
│
├── Deployment & Configuration
│   ├── pyproject.toml                 ⭐ NEW - Modern packaging
│   ├── setup.py                       ⭐ NEW - Setup script
│   ├── requirements.txt                ⭐ UPDATED - Core deps
│   ├── requirements-dev.txt            ⭐ UPDATED - Dev deps
│   ├── .env.example                   ⭐ UPDATED - Env template
│   ├── deploy_core_claw.sh            ⭐ NEW - Deployment script
│   ├── docker_build.py                ⭐ NEW - Docker management
│   └── run_tests.sh                   ⭐ NEW - Test runner
│
├── Original Legion Files (Legacy)
│   ├── agents/
│   │   ├── agent_manager.py
│   │   ├── ai_core.py
│   │   └── tasks.py
│   ├── bot/
│   │   ├── vex_x_bot.py
│   │   ├── sandbox.py
│   │   ├── voice.py
│   │   └── config.py
│   ├── dashboard/
│   │   ├── backend/
│   │   └── frontend/
│   ├── schemas/
│   │   └── functions.json
│   └── registry/
│       └── tool_registry.json
│
├── Documentation
│   ├── docs/
│   │   ├── architecture.md
│   │   ├── deployment_guide.md
│   │   ├── function_reference_full.md
│   │   ├── PROTOCOL_SANITIZED.md
│   │   ├── telegram_integration.md
│   │   ├── USAGE_README.md
│   │   ├── WSL_SETUP.md
│   │   └── adr/                       # Architecture Decision Records
│   └── tutorials/
│
├── Testing
│   ├── tests/
│   │   ├── test_functions_catalog.py
│   │   └── test_stub.py
│   └── CONTRIBUTING.md
│
├── Scripts & Tools
│   ├── scripts/
│   │   ├── ingest_nexus_legion_full.py
│   │   ├── telegram_configure_bot.py
│   │   └── setup_wsl.sh
│   ├── plugins/
│   ├── hooks/
│   └── examples/
│       └── orchestration_example.json
│
├── Infrastructure
│   ├── runtime/
│   │   ├── Dockerfile                 # Container image
│   │   └── requirements.txt
│   ├── deploy/
│   │   ├── deploy_all.sh
│   │   └── deploy_all.ps1
│   └── .devcontainer/
│
├── Metadata
│   ├── LICENSE
│   ├── SECURITY.md
│   ├── _meta.json
│   ├── nexus_legion_agent.prompt
│   ├── system_prompt.txt
│   └── SKILL.md
│
└── Version Control
    ├── .git/
    ├── .github/                       # GitHub workflows
    └── .gitignore

```

## File Statistics

| Category | Files | Purpose |
|----------|-------|---------|
| **Core Framework** | 16 | AI engine, agents, tools, interfaces |
| **Configuration** | 7 | Setup, env vars, packaging |
| **Documentation** | 6 | Guides and references |
| **Deployment** | 3 | Scripts and tools |
| **Testing** | 2 | Test suites |
| **Legacy** | 20+ | Original Legion files (preserved) |
| **Infrastructure** | 4 | Docker, deployment |
| **Total** | 60+ | Complete project |

## Key Changes

### ✅ What's New (Legion Core Claw)
- `legion_core_claw/` — Unified framework (16 files, 1,380+ lines)
- `pyproject.toml` & `setup.py` — Modern packaging
- `deploy_core_claw.sh` — Universal deployment
- `docker_build.py` — Docker automation
- `QUICKSTART.md` — 5-minute quick start
- `MIGRATION.md` — v2 migration guide
- `REFACTORING_SUMMARY.md` — Transformation details
- `COMPLETION_REPORT.md` — What was delivered

### 📝 What's Updated
- `README.md` — Extended with Legion Core Claw info
- `requirements.txt` — Updated dependencies
- `requirements-dev.txt` — Updated deps
- `.env.example` — Enhanced config template
- `run_tests.sh` — Improved test runner

### 📦 What's Preserved
- Original Legion files — For reference
- Docs folder — All documentation
- Tests folder — Test suite
- Deploy folder — Alternative deployment

## Quick Navigation

| Goal | Location |
|------|----------|
| **Get Started** | [QUICKSTART.md](QUICKSTART.md) |
| **Full Docs** | [README.md](README.md) |
| **What's New** | [COMPLETION_REPORT.md](COMPLETION_REPORT.md) |
| **How to Upgrade** | [MIGRATION.md](MIGRATION.md) |
| **Core Framework** | `legion_core_claw/` |
| **Setup & Deploy** | `deploy_core_claw.sh` |
| **Configuration** | `.env.example` |
| **Architecture** | `docs/architecture.md` |
| **Functions** | `docs/function_reference_full.md` |

## Module Overview

### Core Framework (`legion_core_claw/`)

```
┌─────────────────────────────────────────┐
│         Legion Core Claw                │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Interfaces (CLI, Bot, API)     │   │
│  │  - main.py (CLI shell)          │   │
│  │  - bot.py (Telegram)            │   │
│  │  - api.py (REST)                │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Core Intelligence              │   │
│  │  - AIEngine (LLM client)        │   │
│  │  - ReasoningEngine (planning)   │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Orchestration                  │   │
│  │  - AgentOrchestrator            │   │
│  │  - Agent (individual)           │   │
│  │  - Task scheduling              │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Tools & Execution              │   │
│  │  - ToolRegistry (100+ tools)    │   │
│  │  - ToolExecutor (sandbox)       │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Support Systems                │   │
│  │  - Config (centralized)         │   │
│  │  - Utils (audit, logging)       │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Dependencies

### Core Dependencies (`requirements.txt`)
- fastapi, uvicorn — Web framework
- openai, langchain — AI/LLM
- python-telegram-bot — Bot framework
- pydantic — Data validation
- pymongo, redis — Databases
- cryptography — Security

### Dev Dependencies (`requirements-dev.txt`)
- pytest, pytest-asyncio — Testing
- black, flake8, mypy — Code quality
- sphinx — Documentation

## Getting Started

```bash
# 1. Setup
bash deploy_core_claw.sh setup

# 2. Activate
source venv/bin/activate

# 3. Configure
cp .env.example .env
# Edit .env with your values

# 4. Run
python -m legion_core_claw.main
```

---

**Legend Core Claw v3.0.0** — The unified, modular framework for AI-driven DevSecOps automation.

⚡ **LEGION x L.X VEX — SERVING ATLAS** ⚡
