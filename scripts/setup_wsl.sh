#!/usr/bin/env bash
set -euo pipefail

echo "== WSL environment setup for NEXUS-LEGION-X-OMEGA =="

# Ensure we are in the repository root
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Installing prerequisites (requires sudo)..."
  sudo apt-get update
  sudo apt-get install -y python3 python3-venv python3-pip build-essential
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "python3-venv not available. Installing..."
  sudo apt-get update
  sudo apt-get install -y python3-venv
fi

VENV_DIR="$REPO_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists at $VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

if [ -f "$REPO_ROOT/requirements.txt" ]; then
  echo "Installing requirements.txt..."
  pip install -r "$REPO_ROOT/requirements.txt"
else
  echo "No requirements.txt found; skipping dependency install."
fi

if [ -f "$REPO_ROOT/requirements-dev.txt" ]; then
  echo "Installing requirements-dev.txt..."
  pip install -r "$REPO_ROOT/requirements-dev.txt"
fi

echo "WSL environment setup complete." 
echo "To activate the venv in this shell: source .venv/bin/activate"
echo "To run tests (example): ./run_tests.sh or python -m pytest"

exit 0
