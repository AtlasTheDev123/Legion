#!/usr/bin/env bash
set -euo pipefail

echo "Running devcontainer post-create steps..."

# Ensure in workspace root
cd "$(dirname "$0")/.."

# Create a virtual environment if not present
if [ ! -d ".venv" ]; then
  echo "Creating Python venv at .venv"
  python3 -m venv .venv
fi

echo "Activating venv and installing requirements (if present)"
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt || true
fi
if [ -f "requirements-dev.txt" ]; then
  pip install -r requirements-dev.txt || true
fi

echo "Post-create steps finished. To activate the venv in your shell: source .venv/bin/activate"
