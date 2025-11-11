# UNIMIND LVX Master Orchestration System

## Overview

The **UNIMIND LVX Master Orchestration System** is a comprehensive Windows BAT-based orchestration framework designed for the NEXUS-LEGION-X-OMEGA (Legion-X / Cyberkeris All-in-One AI Hub) platform. It provides modular, robust, and secure automation for AI system initialization, persona management, multi-stage workflows, and continuous evolution.

## Architecture

### Core Components

1. **BAT Scripts** (`orchestration/bat/`)
   - `unimind_lvx_master.bat` - Main orchestration controller
   - `unimind_lvx_master_stage_1_9_final.bat` - Multi-stage installation workflow

2. **Helper Modules** (`orchestration/helpers/`)
   - `logger.bat` - Multi-panel logging system
   - `error_handler.bat` - Robust error handling and validation
   - `manifest_validator.bat` - SHA-256 integrity checking
   - `directory_setup.bat` - Directory management
   - `session_context.bat` - Context tracking and AI memory
   - `verify_manifest.ps1` - PowerShell manifest verification
   - `setup_directories.ps1` - PowerShell directory setup

3. **Configuration** (`orchestration/config/`)
   - `cognitive_plugins.txt` - Catalog of AI cognitive plugins
   - `baseline_manifest.sha256` - Security manifest with file hashes
   - `affiliate_config.json` - Affiliate tracking and monetization
   - `workspace_guidance.json` - Tutorial and onboarding system
   - `session_context.json` - Dynamic session state (auto-generated)

4. **Personas** (`models/personas/`)
   - `atlas_architect.json` - Master architect persona
   - `legion_x_controller.json` - Legion-X prime controller persona

## Features

### 🔹 Modular Architecture
- Reusable BAT helper modules eliminate code duplication
- Clean separation of concerns
- Easy to extend and maintain

### 🔹 Multi-Panel Logging
- **Code Panel**: Development and code-related logs
- **Media Panel**: Media processing logs
- **Affiliate Panel**: Affiliate tracking and analytics
- **Session Panel**: Context and memory tracking
- **Master Log**: Consolidated view of all activities

Logs are stored in: `orchestration/logs/`

### 🔹 Robust Error Handling
- Comprehensive validation of files and directories
- Graceful degradation with actionable error messages
- Automatic recovery mechanisms
- Detailed error logging for debugging

### 🔹 Security & Integrity
- SHA-256 manifest validation for critical files
- Persona safety policy enforcement
- Secure logging with sensitive data protection
- Compliance with GDPR, CCPA, and security standards

### 🔹 Session Context & Memory
- Tracks commands, actions, and system events
- Maintains error and success history
- Enables AI to learn from past executions
- Persistent context across sessions

### 🔹 Progressive Streaming
- Real-time status updates during execution
- Visual progress indicators
- Stage-by-stage feedback
- Live log streaming to console

### 🔹 Persona System
- Enhanced persona schema with:
  - Affiliate task definitions
  - Workspace guidance roles
  - Panel awareness
  - Safety metadata
  - Context management
  - Evolution parameters
- Easy persona loading and switching
- Validation of persona schemas

### 🔹 Affiliate & Monetization
- Dynamic affiliate link generation
- Click and conversion tracking
- Banner creation support
- Revenue analytics
- Multi-platform support

### 🔹 Workspace Guidance
- Interactive tutorials
- Contextual help system
- Role-based guidance
- Progressive onboarding
- Documentation integration

## Installation

### Prerequisites
- Windows 10 or later
- PowerShell 5.1 or higher
- Python 3.8+ (optional, for enhanced features)

### Setup Steps

1. **Initialize the orchestration system:**
   ```batch
   cd orchestration\bat
   unimind_lvx_master.bat init
   ```

   This will:
   - Create all required directories
   - Initialize session context
   - Generate baseline manifest
   - Set up logging system

2. **Verify installation:**
   ```batch
   unimind_lvx_master.bat validate
   ```

3. **Check status:**
   ```batch
   unimind_lvx_master.bat status
   ```

## Usage

### Basic Commands

```batch
# Show available commands
unimind_lvx_master.bat

# Initialize system
unimind_lvx_master.bat init

# Start orchestration
unimind_lvx_master.bat start

# Start with specific persona
unimind_lvx_master.bat start legion_x_controller

# Check system status
unimind_lvx_master.bat status

# List available personas
unimind_lvx_master.bat persona list

# Load a persona
unimind_lvx_master.bat persona load atlas_architect

# Validate system
unimind_lvx_master.bat validate

# Run evolution cycle
unimind_lvx_master.bat evolve

# Show help
unimind_lvx_master.bat help

# Show version
unimind_lvx_master.bat version
```

### Multi-Stage Orchestration

The `start` command executes a comprehensive 9-stage workflow:

1. **Stage 1**: Environment validation
2. **Stage 2**: Dependency installation
3. **Stage 3**: Configuration setup
4. **Stage 4**: Plugin initialization
5. **Stage 5**: Persona loading
6. **Stage 6**: Security validation
7. **Stage 7**: System integration
8. **Stage 8**: Testing & verification
9. **Stage 9**: Evolution & optimization

Each stage provides streaming progress updates and comprehensive logging.

## Configuration

### Cognitive Plugins

Edit `orchestration/config/cognitive_plugins.txt` to customize available plugins:

```
plugin_id|plugin_name|version|capabilities|dependencies
```

### Affiliate System

Configure `orchestration/config/affiliate_config.json`:

```json
{
  "platforms": [...],
  "tracking": {...},
  "banners": {...}
}
```

### Workspace Guidance

Customize `orchestration/config/workspace_guidance.json`:

```json
{
  "tutorials": [...],
  "role_guidance": {...}
}
```

## Persona System

### Creating Custom Personas

Create a JSON file in `models/personas/` with the following structure:

```json
{
  "persona_metadata": {
    "id": "your_persona",
    "name": "Your Persona Name",
    "version": "1.0.0"
  },
  "core_identity": {...},
  "capabilities": {...},
  "workspace_guidance": {...},
  "affiliate_tasks": {...},
  "safety_metadata": {...},
  "context_management": {...}
}
```

See `atlas_architect.json` or `legion_x_controller.json` for complete examples.

### Loading Personas

```batch
unimind_lvx_master.bat persona load your_persona
```

## Security

### Manifest Validation

The system uses SHA-256 hashes to verify file integrity:

```batch
# Generate new manifest
unimind_lvx_master.bat init

# Validate current manifest
unimind_lvx_master.bat validate
```

### Safety Policies

Each persona includes safety metadata:
- Content filters
- Compliance settings
- Risk assessment parameters
- Operational constraints

## Logging

### Log Locations

- **Master Log**: `orchestration/logs/master_YYYYMMDD_HHMMSS.log`
- **Code Logs**: `orchestration/logs/code/code_YYYYMMDD_HHMMSS.log`
- **Media Logs**: `orchestration/logs/media/media_YYYYMMDD_HHMMSS.log`
- **Affiliate Logs**: `orchestration/logs/affiliate/affiliate_YYYYMMDD_HHMMSS.log`
- **Session Logs**: `orchestration/logs/session/session_YYYYMMDD_HHMMSS.log`

### Log Levels

- `[INFO]` - General information
- `[SUCCESS]` - Successful operations
- `[WARN]` - Warnings (non-critical)
- `[ERROR]` - Errors requiring attention
- `[STREAM]` - Progressive status updates

## Troubleshooting

### Common Issues

**Problem**: "ORCHESTRATION_ROOT not defined"
**Solution**: Run from `orchestration/bat/` directory or set the variable manually

**Problem**: Manifest validation fails
**Solution**: Regenerate manifest with `unimind_lvx_master.bat init`

**Problem**: PowerShell errors
**Solution**: Ensure PowerShell 5.1+ is installed and execution policy allows scripts

**Problem**: Directory creation fails
**Solution**: Check permissions or run as administrator

### Debug Mode

For detailed debugging:
1. Review logs in `orchestration/logs/`
2. Check session context: `orchestration/config/session_context.json`
3. Validate configuration files manually

## Advanced Features

### Session Context

View session history:
```batch
type orchestration\config\session_context.json
```

Track custom events:
```batch
call helpers\session_context.bat :track_system_event "custom_event"
```

### Evolution Cycle

The evolution cycle analyzes:
- Session history
- Error patterns
- Success rates
- Performance metrics

Run manually:
```batch
unimind_lvx_master.bat evolve
```

### Configuration Backup

Automatic backups are created in:
```
orchestration/backups/backup_YYYYMMDD_HHMMSS/
```

## Integration

### Python Integration

The orchestration system works alongside Python components:

```python
# Example: Load persona from Python
import json

with open('models/personas/legion_x_controller.json', 'r') as f:
    persona = json.load(f)
    print(persona['interaction_patterns']['greeting'])
```

### API Integration

The system logs can be consumed by APIs or monitoring tools.

## Contributing

When extending the orchestration system:

1. Follow the modular pattern
2. Add comprehensive error handling
3. Include logging at key points
4. Update documentation
5. Validate with `unimind_lvx_master.bat validate`

## License

Part of NEXUS-LEGION-X-OMEGA project. See main repository for license details.

## Support

For issues or questions:
- Review logs in `orchestration/logs/`
- Check configuration in `orchestration/config/`
- Run validation: `unimind_lvx_master.bat validate`

---

**⚡ LEGION-X Prime Controller - NEXUS-LEGION-X-OMEGA - SERVING ATLAS ⚡**
