#!/usr/bin/env bash
# ============================================================
# UNIMIND LVX Master - Linux/WSL Wrapper
# Provides access to BAT orchestration from Linux/WSL
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCHESTRATION_ROOT="$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "========================================"
echo "  UNIMIND LVX Master - Linux/WSL Wrapper"
echo "========================================"
echo ""

# Check if running on WSL
if grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
    echo -e "${GREEN}[INFO]${NC} Running on WSL"
    WSL_MODE=true
else
    echo -e "${YELLOW}[INFO]${NC} Not running on WSL"
    WSL_MODE=false
fi

# Function to display help
show_help() {
    echo "Usage: unimind_lvx_wrapper.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  status          Display system status"
    echo "  validate        Validate configuration files"
    echo "  personas        List available personas"
    echo "  test            Run test suite"
    echo "  help            Show this help"
    echo ""
    echo "Note: This is a Linux/WSL wrapper. Full BAT functionality"
    echo "      requires Windows. Use this for validation and testing."
    echo ""
}

# Function to check system status
check_status() {
    echo -e "${BLUE}[STATUS]${NC} Checking UNIMIND LVX system..."
    echo ""
    
    # Check directories
    if [ -d "$ORCHESTRATION_ROOT/bat" ]; then
        echo -e "${GREEN}✓${NC} BAT scripts directory exists"
    else
        echo -e "${RED}✗${NC} BAT scripts directory missing"
    fi
    
    if [ -d "$ORCHESTRATION_ROOT/helpers" ]; then
        echo -e "${GREEN}✓${NC} Helpers directory exists"
    else
        echo -e "${RED}✗${NC} Helpers directory missing"
    fi
    
    if [ -d "$ORCHESTRATION_ROOT/config" ]; then
        echo -e "${GREEN}✓${NC} Config directory exists"
    else
        echo -e "${RED}✗${NC} Config directory missing"
    fi
    
    # Check key files
    if [ -f "$ORCHESTRATION_ROOT/bat/unimind_lvx_master.bat" ]; then
        echo -e "${GREEN}✓${NC} Main orchestration script found"
    else
        echo -e "${RED}✗${NC} Main orchestration script missing"
    fi
    
    if [ -f "$ORCHESTRATION_ROOT/config/cognitive_plugins.txt" ]; then
        echo -e "${GREEN}✓${NC} Cognitive plugins catalog found"
        PLUGIN_COUNT=$(grep -v '^#' "$ORCHESTRATION_ROOT/config/cognitive_plugins.txt" | grep -v '^$' | wc -l)
        echo -e "  ${BLUE}→${NC} Plugins available: $PLUGIN_COUNT"
    else
        echo -e "${RED}✗${NC} Cognitive plugins catalog missing"
    fi
    
    echo ""
}

# Function to validate configuration
validate_config() {
    echo -e "${BLUE}[VALIDATE]${NC} Validating configuration files..."
    echo ""
    
    # Validate JSON files
    for json_file in "$ORCHESTRATION_ROOT/config"/*.json; do
        if [ -f "$json_file" ]; then
            if python3 -m json.tool "$json_file" > /dev/null 2>&1; then
                echo -e "${GREEN}✓${NC} Valid JSON: $(basename "$json_file")"
            else
                echo -e "${RED}✗${NC} Invalid JSON: $(basename "$json_file")"
            fi
        fi
    done
    
    echo ""
}

# Function to list personas
list_personas() {
    echo -e "${BLUE}[PERSONAS]${NC} Available personas:"
    echo ""
    
    PERSONAS_DIR="$SCRIPT_DIR/../models/personas"
    
    if [ -d "$PERSONAS_DIR" ]; then
        for persona_file in "$PERSONAS_DIR"/*.json; do
            if [ -f "$persona_file" ]; then
                PERSONA_NAME=$(basename "$persona_file" .json)
                echo -e "  ${GREEN}•${NC} $PERSONA_NAME"
                
                # Try to extract persona name and role
                if command -v python3 &> /dev/null; then
                    DISPLAY_NAME=$(python3 -c "import json; f=open('$persona_file'); d=json.load(f); print(d.get('persona_metadata', {}).get('name', ''))" 2>/dev/null || echo "")
                    ROLE=$(python3 -c "import json; f=open('$persona_file'); d=json.load(f); print(d.get('core_identity', {}).get('role', ''))" 2>/dev/null || echo "")
                    
                    if [ -n "$DISPLAY_NAME" ]; then
                        echo -e "    Name: $DISPLAY_NAME"
                    fi
                    if [ -n "$ROLE" ]; then
                        echo -e "    Role: $ROLE"
                    fi
                fi
            fi
        done
    else
        echo -e "${YELLOW}⚠${NC} Personas directory not found"
    fi
    
    echo ""
}

# Function to run tests
run_tests() {
    echo -e "${BLUE}[TEST]${NC} Running test suite..."
    echo ""
    
    cd "$SCRIPT_DIR/.."
    
    if command -v python3 &> /dev/null; then
        if python3 -m pytest tests/test_orchestration_config.py -v; then
            echo ""
            echo -e "${GREEN}✓${NC} All tests passed"
        else
            echo ""
            echo -e "${RED}✗${NC} Some tests failed"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} Python3 not found, skipping tests"
    fi
    
    echo ""
}

# Main logic
COMMAND=${1:-help}

case "$COMMAND" in
    status)
        check_status
        ;;
    validate)
        validate_config
        ;;
    personas)
        list_personas
        ;;
    test)
        run_tests
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}[ERROR]${NC} Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac

echo "========================================"
echo ""
