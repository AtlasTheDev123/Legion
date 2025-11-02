# NEXUS-LEGION-X-OMEGA

This repository contains the NEXUS-LEGION-X-OMEGA project: a collection of agent prompts, development guidance, and tools for local development and experimentation.

Files added by automation
-------------------------
- `docs/PROTOCOL_SANITIZED.md` — safety-first consolidated protocol for contributors.
- `docs/WSL_SETUP.md` — instructions for bootstrapping a WSL environment.
- `scripts/setup_wsl.sh` — bash script to create a Python venv and install requirements inside WSL.
- `.devcontainer/` — devcontainer configuration to run the project in VS Code Remote / Dev Containers.
- `.github/workflows/ci.yml` — GitHub Actions workflow to run tests on push/PR.
- `docs/experimental/` — speculative/vision docs are isolated and labeled EXPERIMENTAL.

Quick start (WSL)
------------------
1. Open your Ubuntu WSL distro and change to the repo folder:

```bash
cd /mnt/c/Users/Alan\ The\ Marvel/Downloads/NEXUS_LEGION_X_OMEGA/NEXUS-LEGION-X-OMEGA
```

2. Run the setup script:

```bash
chmod +x scripts/setup_wsl.sh
sudo bash scripts/setup_wsl.sh
source .venv/bin/activate
```

3. Run tests:

```bash
./run_tests.sh || python -m pytest -q
```

Devcontainer
------------
Open this repo in VS Code and use "Reopen in Container" to build the devcontainer. The container will create a `.venv` and install Python requirements.

Contributing
------------
See `CONTRIBUTING.md` in the repository root. Experimental ideas live under `docs/experimental/` and require ADRs before implementation.
![NEXUS-LEGION-X-OMEGA](https://raw.githubusercontent.com/nektos/act/master/docs/img/logo-150.png)

# NEXUS-LEGION X OMEGA

**Core Philosophy: "Next is now. We merge code, intelligence, and security into a singular, unstoppable framework."**

NEXUS-LEGION X OMEGA is a hyper-adaptive, self-aware AI framework designed for full-spectrum cyber-physical autonomy. It integrates advanced AI/ML, DevSecOps, multi-agent orchestration, hardware/sensor control, and secure networking into a unified, globally deployable system.

---

## 🔹 Core Capabilities

*   **Autonomous AI Core**: Multi-agent system with predictive planning, self-healing, and continuous learning from a persistent knowledge base.
*   **Telegram Bot Interface (`VEX_X_BOT`)**: Remote control via commands, voice, and real-time alerts.
*   **Multi-Language Sandbox**: Secure, containerized execution for Python, JavaScript, Rust, Go, C++, and more.
*   **Cyber-Physical Integration**: Control and monitor hardware, sensors, and actuators (GPIO, I2C, SPI, USB) for real-world interaction.
*   **Secure Global Network**: Encrypted agent communication, optional TOR/I2P routing, and federated intelligence.
*   **Live Web Dashboard**: FastAPI & React dashboard for real-time monitoring, analytics, heatmaps, and agent control.
*   **CI/CD & DevSecOps Automation**: Automated code analysis, patch generation, and pipeline triggers integrated with GitHub.
*   **Quantum-Ready**: Includes a quantum simulation module for advanced cryptographic and optimization tasks.
*   **Extensible Plugin Architecture**: Dynamically load new tools, AI models, and third-party integrations.

---

## 🚀 Deployment

The entire framework can be deployed with a single command.

1.  **Prerequisites**:
    *   Docker & Docker Compose
    *   Python 3.10+
    *   Node.js & npm (for the dashboard frontend)
    *   A running MongoDB instance

2.  **Configuration**:
    *   Create a `.env` file in the root directory.
    *   Add your `TELEGRAM_TOKEN`, `AUTHORIZED_USERS` (comma-separated user IDs), and `MONGO_URI`.

    ```
    TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
    AUTHORIZED_USERS=123456789
    MONGO_URI=mongodb://localhost:27017/
    ```

3.  **Launch**:
    Execute the deployment script. This will build the necessary Docker containers, install dependencies, and launch all services.

    ```bash
    chmod +x deploy/deploy_all.sh
    ./deploy/deploy_all.sh
    ```

---

⚡️ **SERVING ATLAS** ⚡️