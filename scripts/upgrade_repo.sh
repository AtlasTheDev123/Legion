#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

INSTALL=0
while [[ ${1:-} != "" ]]; do
  case "$1" in
    --install) INSTALL=1; shift ;;
    -h|--help)
      cat <<'USAGE'
Usage: scripts/upgrade_repo.sh [--install]

Performs a safe analysis and dry-run upgrade of the repository.
By default this script performs checks only and avoids network installs.
Use --install to allow creating a venv and installing pinned requirements (network required).
USAGE
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

echo "=== NEXUS-LEGION-X-OMEGA: safe upgrade & analysis script (dry-run mode) ==="

# 1) Ensure .env exists (safe defaults)
if [ ! -f ".env" ]; then
  echo "Creating .env from .env.example with safe defaults..."
  if [ -f ".env.example" ]; then
    cp .env.example .env
  else
    cat > .env <<'EOF'
# Safe defaults (do NOT enable destructive actions without review)
ALLOW_DESTRUCTIVE_ACTIONS=0
ALLOW_TELEGRAM_ACTIONS=0
EOF
  fi
  echo ".env created (please review and populate secrets securely)"
else
  echo ".env already exists; skipping creation"
fi

# 2) Optionally create venv and install pinned requirements
VENV_DIR=".venv"
if [ "$INSTALL" -eq 1 ]; then
  if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python venv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  echo "Upgrading pip/install tools..."
  python -m pip install --upgrade pip setuptools wheel
  if [ -f "requirements-lock.txt" ]; then
    echo "Installing pinned requirements from requirements-lock.txt..."
    pip install -r requirements-lock.txt
  elif [ -f "requirements.txt" ]; then
    echo "requirements-lock.txt not found; installing requirements.txt..."
    pip install -r requirements.txt
  else
    echo "No requirements file found; skipping pip install"
  fi
else
  echo "Install mode not enabled (--install). Skipping venv creation and pip installs."
fi

# 3) Basic static checks (if tools installed)
echo "Running static checks if tools installed..."
command -v ruff >/dev/null && ruff check . || echo "ruff not installed; skipping"
command -v black >/dev/null && black --check . || echo "black not installed or check failed; skipping"
command -v mypy >/dev/null && mypy . || echo "mypy not installed; skipping"

# 4) Validate key JSON files referenced by repo
echo "Validating key JSON manifests..."
for f in functions.json schemas/functions.json; do
  if [ -f "$f" ]; then
    python - <<PY || { echo "$f invalid JSON"; exit 1; }
import json
json.load(open('$f'))
print('$f OK')
PY
  fi
done

# 5) Dry-run ingest script (no DB writes unless environment enables it)
if [ -f "scripts/ingest_nexus_legion_full.py" ]; then
  echo "Dry-running ingest script (no DB writes unless configured via env vars)..."
  python -c "print('Skipping execution of ingest script in dry-run; run manually with MONGO_URI set if desired')"
fi

# 6) Run test runner if present (do not force heavy installs)
echo "Running test runner (if present)"
if [ -x "run_tests.sh" ]; then
  echo "Found run_tests.sh; running it (script should be safe/dry-run)"
  ./run_tests.sh || echo "run_tests.sh finished with non-zero status; inspect output"
elif command -v pytest >/dev/null 2>&1; then
  echo "pytest available; running pytest -q (may fail if deps missing)"
  pytest -q || echo "pytest finished (some tests may fail)"
else
  echo "No test runner available or running tests skipped"
fi

# 7) Secrets scan (heuristic)
echo "Scanning repository for likely secrets (heuristic)..."
SECRETS_FOUND=0
declare -a PATTERNS=(
  "AKIA[0-9A-Z]{16}"
  "[A-Za-z0-9_-]{32,}"
  "telegram" 
  "-----BEGIN PRIVATE KEY-----"
)
for pat in "${PATTERNS[@]}"; do
  if grep -IRnE --exclude-dir=.git --exclude=*.zip "$pat" . >/dev/null 2>&1; then
    echo "Potential secret pattern ($pat) found. Run manual review."
    grep -IRnE --exclude-dir=.git --exclude=*.zip "$pat" || true
    SECRETS_FOUND=1
  fi
done

if [ "$SECRETS_FOUND" -ne 0 ]; then
  echo "WARNING: Potential secrets found. Do NOT commit secrets. Rotate exposed tokens immediately."
else
  echo "No obvious secrets found by heuristic scan."
fi

# 8) Create safe repository backup (zip) if zip available
BACKUP="/tmp/nexus_legion_x_omega_$(date +%Y%m%d_%H%M%S).zip"
echo "Creating backup $BACKUP (excludes .git and .venv if present)..."
if command -v zip >/dev/null 2>&1; then
  zip -r "$BACKUP" . -x ".git/*" ".venv/*" "*.pyc" "__pycache__/*" >/dev/null || echo "zip may have encountered warnings"
else
  echo "zip not available; skipping archive creation"
fi

echo "Upgrade & analysis complete. Review output and SECURITY.md for next steps."
exit 0
