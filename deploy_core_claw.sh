#!/bin/bash
# Legion Core Claw - Universal Deployment Script
# Supports: Linux, macOS, WSL on Windows
# Usage: ./deploy_core_claw.sh [--install-deps] [--run-tests] [--start-server]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_CMD="${PYTHON_CMD:-python3}"
PIP_CMD="$VENV_DIR/bin/pip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python
check_python() {
    if ! command -v $PYTHON_CMD &> /dev/null; then
        log_error "Python 3 not found. Please install Python 3.8 or later."
        exit 1
    fi
    PYTHON_VERSION=$($PYTHON_CMD --version | awk '{print $2}')
    log_info "Found Python $PYTHON_VERSION"
}

# Create virtual environment
setup_venv() {
    if [ -d "$VENV_DIR" ]; then
        log_warn "Virtual environment already exists at $VENV_DIR"
    else
        log_info "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
    fi
    
    # Activate venv
    source "$VENV_DIR/bin/activate"
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies..."
    $PIP_CMD install --upgrade pip setuptools wheel
    $PIP_CMD install -r "$PROJECT_DIR/requirements.txt"
    log_info "✓ Dependencies installed"
}

# Install dev dependencies
install_dev_dependencies() {
    log_info "Installing development dependencies..."
    $PIP_CMD install -r "$PROJECT_DIR/requirements-dev.txt"
    log_info "✓ Dev dependencies installed"
}

# Setup environment file
setup_env() {
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log_warn "No .env file found. Creating from template..."
        cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
        log_warn "Please edit .env with your configuration"
    else
        log_info "Using existing .env file"
    fi
}

# Run tests
run_tests() {
    log_info "Running tests..."
    cd "$PROJECT_DIR"
    $VENV_DIR/bin/pytest tests/ -v || log_warn "Tests completed with warnings"
}

# Start server
start_server() {
    log_info "Starting Legion Core Claw server..."
    cd "$PROJECT_DIR"
    $VENV_DIR/bin/uvicorn legion_core_claw.interfaces.api:APIInterface --host 0.0.0.0 --port 8000 --reload
}

# Start bot
start_bot() {
    log_info "Starting Telegram bot..."
    cd "$PROJECT_DIR"
    $VENV_DIR/bin/python -m legion_core_claw.interfaces.bot
}

# Start interactive CLI
start_cli() {
    log_info "Starting Legion Core Claw CLI..."
    cd "$PROJECT_DIR"
    source "$VENV_DIR/bin/activate"
    $PYTHON_CMD -m legion_core_claw.main
}

# Show help
show_help() {
    cat << EOF
Legion Core Claw - Deployment Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  setup             Setup virtual environment and install dependencies (default)
  install-deps      Install core dependencies
  install-dev-deps  Install development dependencies
  run-tests         Run test suite
  start-server      Start FastAPI server (API)
  start-bot         Start Telegram bot
  start-cli         Start interactive CLI
  help              Show this help message

Options:
  --dev             Install development dependencies

Examples:
  $0 setup           # Setup and install all dependencies
  $0 install-deps     # Install core dependencies only
  $0 run-tests       # Run tests
  $0 start-server    # Start API server
  $0 start-cli       # Start interactive CLI

EOF
}

# Parse arguments
COMMAND="${1:-setup}"

case "$COMMAND" in
    setup)
        check_python
        setup_venv
        setup_env
        install_dependencies
        log_info "✓ Setup complete. Use 'source venv/bin/activate' to activate the environment."
        ;;
    install-deps)
        check_python
        setup_venv
        install_dependencies
        ;;
    install-dev-deps)
        check_python
        setup_venv
        install_dev_dependencies
        ;;
    run-tests)
        check_python
        setup_venv
        run_tests
        ;;
    start-server)
        check_python
        setup_venv
        start_server
        ;;
    start-bot)
        check_python
        setup_venv
        start_bot
        ;;
    start-cli)
        check_python
        setup_venv
        start_cli
        ;;
    help)
        show_help
        ;;
    *)
        log_error "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac
