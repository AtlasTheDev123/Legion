# UNIMIND LVX Orchestration System - Quick Start Examples

This file contains example commands and use cases for the UNIMIND LVX Master Orchestration System.

## Basic Usage Examples

### 1. First Time Setup
```batch
REM Navigate to orchestration directory
cd orchestration\bat

REM Initialize the system (creates directories, manifest, session context)
unimind_lvx_master.bat init

REM Verify installation
unimind_lvx_master.bat validate
```

### 2. Starting the Orchestration System
```batch
REM Start with default settings
unimind_lvx_master.bat start

REM Start with Legion-X Prime Controller persona
unimind_lvx_master.bat start legion_x_controller

REM Start with Atlas Architect persona
unimind_lvx_master.bat start atlas_architect
```

### 3. Checking System Status
```batch
REM Display comprehensive system status
unimind_lvx_master.bat status

REM This shows:
REM - Session information and history
REM - Available personas
REM - Directory structure validation
REM - Recent log activity
```

### 4. Managing Personas
```batch
REM List all available personas
unimind_lvx_master.bat persona list

REM Load a specific persona
unimind_lvx_master.bat persona load legion_x_controller

REM Validate all persona schemas
unimind_lvx_master.bat persona validate
```

### 5. Security and Validation
```batch
REM Run all validation checks
unimind_lvx_master.bat validate

REM This validates:
REM - Directory structure
REM - Manifest integrity (SHA-256)
REM - Persona schemas
REM - Configuration files
```

### 6. Evolution and Learning
```batch
REM Run evolution cycle (analyzes session history and optimizes)
unimind_lvx_master.bat evolve
```

## Advanced Usage

### PowerShell Direct Operations

#### Verify Manifest
```powershell
cd orchestration\helpers
.\verify_manifest.ps1 -ManifestPath "..\config\baseline_manifest.sha256"
```

#### Setup Directories
```powershell
cd orchestration\helpers
.\setup_directories.ps1 -OrchestrationRoot ".."
```

### Python Integration

#### Load and Display Persona
```python
import json

# Load Legion-X Controller persona
with open('models/personas/legion_x_controller.json', 'r') as f:
    persona = json.load(f)

# Display greeting
print(persona['interaction_patterns']['greeting'])

# Check capabilities
print(f"Primary functions: {len(persona['capabilities']['primary_functions'])}")
print(f"Cognitive plugins: {len(persona['capabilities']['cognitive_plugins'])}")
```

#### Analyze Session Context
```python
import json

# Load session context
with open('orchestration/config/session_context.json', 'r') as f:
    context = json.load(f)

# Display statistics
print(f"Session count: {context['session_count']}")
print(f"Last run: {context['last_run']}")
print(f"Success count: {len(context['success_history'])}")
print(f"Error count: {len(context['error_history'])}")
```

## Common Workflows

### Workflow 1: Daily Development Session
```batch
REM 1. Check status
unimind_lvx_master.bat status

REM 2. Load development persona
unimind_lvx_master.bat persona load atlas_architect

REM 3. Start orchestration
unimind_lvx_master.bat start atlas_architect

REM 4. Review logs after completion
type orchestration\logs\session\session_*.log
```

### Workflow 2: Security Audit
```batch
REM 1. Validate all systems
unimind_lvx_master.bat validate

REM 2. Check manifest integrity
cd orchestration\helpers
powershell -ExecutionPolicy Bypass -File verify_manifest.ps1 -ManifestPath "..\config\baseline_manifest.sha256"

REM 3. Review persona safety policies
type models\personas\legion_x_controller.json | findstr "safety"
```

### Workflow 3: Fresh Installation
```batch
REM 1. Initialize system
cd orchestration\bat
unimind_lvx_master.bat init

REM 2. Validate installation
unimind_lvx_master.bat validate

REM 3. Run first orchestration with Legion-X
unimind_lvx_master.bat start legion_x_controller

REM 4. Check status
unimind_lvx_master.bat status

REM 5. Review all logs
dir orchestration\logs\*.log
```

### Workflow 4: Continuous Learning
```batch
REM After several sessions, analyze learning
unimind_lvx_master.bat status

REM Run evolution to optimize
unimind_lvx_master.bat evolve

REM Review session context
type orchestration\config\session_context.json
```

## Troubleshooting Examples

### Problem: Manifest validation fails
```batch
REM Regenerate manifest
cd orchestration\bat
unimind_lvx_master.bat init

REM This will create a fresh baseline_manifest.sha256
```

### Problem: Missing directories
```batch
REM Use PowerShell to recreate all directories
cd orchestration\helpers
powershell -ExecutionPolicy Bypass -File setup_directories.ps1 -OrchestrationRoot ".."
```

### Problem: Session context corrupted
```batch
REM Delete and reinitialize
del orchestration\config\session_context.json
unimind_lvx_master.bat init
```

### Problem: Need detailed debug info
```batch
REM Review all log files
dir /s orchestration\logs\*.log

REM Check specific log panel
type orchestration\logs\session\session_*.log
type orchestration\logs\code\code_*.log
```

## Configuration Examples

### Example 1: Add Custom Cognitive Plugin

Edit `orchestration/config/cognitive_plugins.txt`:
```
custom_plugin|My Custom Plugin|1.0.0|custom_capability|python,custom_lib
```

### Example 2: Configure Affiliate Platform

Edit `orchestration/config/affiliate_config.json`:
```json
{
  "platforms": [
    {
      "id": "my_platform",
      "name": "My Affiliate Platform",
      "enabled": true,
      "referral_link": "https://example.com/ref/myid",
      "categories": ["custom", "tools"]
    }
  ]
}
```

### Example 3: Add Custom Tutorial

Edit `orchestration/config/workspace_guidance.json`:
```json
{
  "tutorials": [
    {
      "id": "my_tutorial",
      "title": "My Custom Tutorial",
      "difficulty": "beginner",
      "duration_minutes": 15,
      "topics": ["custom_topic"],
      "steps": [
        {
          "step": 1,
          "title": "First Step",
          "description": "Description of first step"
        }
      ]
    }
  ]
}
```

## Integration Examples

### Example 1: Integrate with Python Application
```python
import subprocess
import json

# Run orchestration from Python
result = subprocess.run(
    ['orchestration/bat/unimind_lvx_master.bat', 'start'],
    capture_output=True,
    text=True
)

print(result.stdout)
```

### Example 2: Monitor Logs Programmatically
```python
import os
from pathlib import Path

logs_dir = Path('orchestration/logs')

# Get latest master log
master_logs = sorted(logs_dir.glob('master_*.log'), reverse=True)
if master_logs:
    latest_log = master_logs[0]
    with open(latest_log, 'r') as f:
        print(f.read())
```

### Example 3: Load Multiple Personas
```python
import json
from pathlib import Path

personas_dir = Path('models/personas')

for persona_file in personas_dir.glob('*.json'):
    with open(persona_file, 'r') as f:
        persona = json.load(f)
        print(f"Loaded: {persona['persona_metadata']['name']}")
        print(f"  Role: {persona['core_identity']['role']}")
        print(f"  Safety Level: {persona['safety_metadata']['safety_level']}")
        print()
```

## Performance Tips

1. **Log Management**: Periodically clean old logs
   ```batch
   REM Keep only last 30 days of logs
   forfiles /p "orchestration\logs" /s /m *.log /d -30 /c "cmd /c del @path"
   ```

2. **Session Context**: Monitor size of session context
   ```batch
   REM If session_context.json grows too large, archive and reset
   copy orchestration\config\session_context.json orchestration\backups\
   del orchestration\config\session_context.json
   unimind_lvx_master.bat init
   ```

3. **Manifest Updates**: Regenerate after major changes
   ```batch
   unimind_lvx_master.bat init
   ```

## Best Practices

1. Always run `validate` before and after major changes
2. Use personas appropriate to the task (development vs orchestration)
3. Review session logs regularly for learning opportunities
4. Keep configuration files in version control
5. Backup session context before major operations
6. Use progressive logging for long-running operations
7. Monitor affiliate tracking for compliance
8. Regularly run evolution cycles for optimization

---

For complete documentation, see: orchestration/README.md
