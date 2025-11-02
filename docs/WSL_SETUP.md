## WSL setup (Windows Subsystem for Linux)

This document describes how to bootstrap a reproducible development environment for this repository in WSL.

### Prerequisites

- Windows with WSL2 enabled and a preferred Linux distro installed (Ubuntu recommended).
- Recommended: 4+ GB RAM and network access to download packages.

### Quick automated setup

From within your WSL distro, run the repository script:

```bash
cd /mnt/c/Users/Alan\ The\ Marvel/Downloads/NEXUS_LEGION_X_OMEGA/NEXUS-LEGION-X-OMEGA
bash scripts/setup_wsl.sh
```

The script will:

- Install python3 and python3-venv via apt if not present (requires sudo).
- Create a virtual environment at `.venv` in the repo root.
- Activate the virtual environment and install `requirements.txt` and `requirements-dev.txt` if present.

### Manual step-by-step (if you prefer)

1. Open your WSL distro and change to the repository folder. Example path mapping from Windows to WSL:

	```bash
	cd /mnt/c/Users/Alan\ The\ Marvel/Downloads/NEXUS_LEGION_X_OMEGA/NEXUS-LEGION-X-OMEGA
	```

1. Install system prerequisites (only if missing):

	```bash
	sudo apt-get update
	sudo apt-get install -y python3 python3-venv python3-pip build-essential
	```

1. Create and activate a virtual environment:

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

1. Upgrade pip and install dependencies:

	```bash
	python -m pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt || true
	pip install -r requirements-dev.txt || true
	```

1. Run tests / dev commands:

	```bash
	./run_tests.sh
	# or
	python -m pytest
	```

### Notes

- The `scripts/setup_wsl.sh` script is idempotent and safe to re-run.
- If your distro lacks `sudo` privileges, install dependencies from an account that has sudo or ask your admin.
- If you want this environment available in Windows PowerShell instead, activate the venv with:

	```powershell
	& ".\.venv\Scripts\Activate.ps1"
	```

### Need help?

- Tell me what OS/distro you use and I can provide tailored commands or create a devcontainer for VS Code.
