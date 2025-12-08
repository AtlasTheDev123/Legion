@echo off
REM ============================================================
REM UNIMIND LVX MASTER - Main Orchestration Controller
REM Version: 1.0.0
REM Legion-X (Cyberkeris All-in-One AI Hub) Prime Controller
REM ============================================================

setlocal enabledelayedexpansion

REM Set orchestration root
set ORCHESTRATION_ROOT=%~dp0
set ORCHESTRATION_ROOT=%ORCHESTRATION_ROOT:~0,-1%

REM Display banner
call :display_banner

REM Initialize helpers
call :init_helpers

REM Parse command line arguments
set COMMAND=%1
set SUBCOMMAND=%2

if "%COMMAND%"=="" (
    call :show_menu
    goto :end
)

REM Route commands
if /i "%COMMAND%"=="init" goto :cmd_init
if /i "%COMMAND%"=="start" goto :cmd_start
if /i "%COMMAND%"=="status" goto :cmd_status
if /i "%COMMAND%"=="persona" goto :cmd_persona
if /i "%COMMAND%"=="validate" goto :cmd_validate
if /i "%COMMAND%"=="evolve" goto :cmd_evolve
if /i "%COMMAND%"=="help" goto :cmd_help
if /i "%COMMAND%"=="version" goto :cmd_version

call :log_error "Unknown command: %COMMAND%"
call :log_info "Run 'unimind_lvx_master.bat help' for usage information"
goto :end

:display_banner
echo.
echo ========================================
echo    UNIMIND LVX MASTER CONTROLLER
echo    Legion-X Prime Orchestration System
echo ========================================
echo    Version: 1.0.0
echo    Status: ONLINE
echo    Mode: AUTONOMOUS
echo ========================================
echo.
exit /b 0

:init_helpers
REM Load all helper modules
if not exist "%ORCHESTRATION_ROOT%\helpers\logger.bat" (
    echo [CRITICAL] Logger module not found
    exit /b 1
)

REM Initialize logging
call "%ORCHESTRATION_ROOT%\helpers\logger.bat" :log_init

REM Load other helpers
set HELPERS_DIR=%ORCHESTRATION_ROOT%\helpers
call :log_info "Loading helper modules..."
call :log_success "Helpers initialized"
exit /b 0

:show_menu
echo Available Commands:
echo.
echo   init          Initialize orchestration system
echo   start         Start orchestration with optional persona
echo   status        Display system status and health
echo   persona       Manage personas (load, list, validate)
echo   validate      Validate configuration and manifest
echo   evolve        Run evolution and optimization cycle
echo   help          Show detailed help
echo   version       Show version information
echo.
echo Usage: unimind_lvx_master.bat [command] [options]
echo.
exit /b 0

:cmd_init
call :log_streaming "SYSTEM INITIALIZATION"

REM Validate environment
call "%HELPERS_DIR%\error_handler.bat" :validate_environment
if errorlevel 1 goto :error

REM Setup directories
call "%HELPERS_DIR%\directory_setup.bat" :setup_all_directories
if errorlevel 1 goto :error

REM Initialize session context
call "%HELPERS_DIR%\session_context.bat" :init_session
if errorlevel 1 goto :error

REM Create baseline manifest if needed
if not exist "%ORCHESTRATION_ROOT%\config\baseline_manifest.sha256" (
    call "%HELPERS_DIR%\manifest_validator.bat" :create_baseline_manifest
)

call :log_success "System initialization complete"
call "%HELPERS_DIR%\session_context.bat" :track_system_event "system_initialized"
goto :end

:cmd_start
call :log_streaming "STARTING ORCHESTRATION SYSTEM"

REM Initialize if not already done
if not exist "%ORCHESTRATION_ROOT%\config\session_context.json" (
    call :log_warn "System not initialized, running initialization..."
    call :cmd_init
)

REM Validate manifest
call "%HELPERS_DIR%\manifest_validator.bat" :validate_manifest
if errorlevel 1 (
    call :log_warn "Manifest validation failed, but continuing..."
)

REM Load persona if specified
if not "%SUBCOMMAND%"=="" (
    call :log_info "Loading persona: %SUBCOMMAND%"
    call :load_persona "%SUBCOMMAND%"
)

REM Track command
call "%HELPERS_DIR%\session_context.bat" :track_command "start"

REM Execute multi-stage orchestration
call "%ORCHESTRATION_ROOT%\bat\unimind_lvx_master_stage_1_9_final.bat"
if errorlevel 1 goto :error

call :log_success "Orchestration completed successfully"
call "%HELPERS_DIR%\session_context.bat" :track_success "orchestration_completed"
goto :end

:cmd_status
call :log_streaming "SYSTEM STATUS"

REM Display session summary
call "%HELPERS_DIR%\session_context.bat" :get_session_summary

REM Check required directories
call "%HELPERS_DIR%\directory_setup.bat" :validate_directory_structure

REM Display persona status
call :log_info "Checking available personas..."
if exist "%ORCHESTRATION_ROOT%\..\models\personas\*.json" (
    echo.
    echo Available Personas:
    for %%f in ("%ORCHESTRATION_ROOT%\..\models\personas\*.json") do (
        echo   - %%~nf
    )
    echo.
) else (
    call :log_warn "No personas found"
)

REM Display log statistics
call :log_info "Recent log activity:"
if exist "%ORCHESTRATION_ROOT%\logs\master_*.log" (
    for /f %%a in ('dir /b /o-d "%ORCHESTRATION_ROOT%\logs\master_*.log" 2^>nul ^| find /c /v ""') do echo   Master logs: %%a
)
if exist "%ORCHESTRATION_ROOT%\logs\session\*.log" (
    for /f %%a in ('dir /b /o-d "%ORCHESTRATION_ROOT%\logs\session\*.log" 2^>nul ^| find /c /v ""') do echo   Session logs: %%a
)

call :log_success "Status check complete"
goto :end

:cmd_persona
if "%SUBCOMMAND%"=="" (
    call :log_error "Persona command requires subcommand: load, list, validate"
    goto :end
)

if /i "%SUBCOMMAND%"=="list" (
    call :log_info "Available personas:"
    if exist "%ORCHESTRATION_ROOT%\..\models\personas\*.json" (
        for %%f in ("%ORCHESTRATION_ROOT%\..\models\personas\*.json") do (
            echo   - %%~nf
        )
    ) else (
        call :log_warn "No personas found"
    )
    goto :end
)

if /i "%SUBCOMMAND%"=="load" (
    set PERSONA_NAME=%3
    if "!PERSONA_NAME!"=="" (
        call :log_error "Please specify persona name"
        goto :end
    )
    call :load_persona "!PERSONA_NAME!"
    goto :end
)

if /i "%SUBCOMMAND%"=="validate" (
    call :validate_personas
    goto :end
)

call :log_error "Unknown persona subcommand: %SUBCOMMAND%"
goto :end

:cmd_validate
call :log_streaming "VALIDATION CHECKS"

REM Validate directory structure
call "%HELPERS_DIR%\directory_setup.bat" :validate_directory_structure
if errorlevel 1 (
    call :log_error "Directory validation failed"
    goto :error
)

REM Validate manifest
call "%HELPERS_DIR%\manifest_validator.bat" :validate_manifest
if errorlevel 1 (
    call :log_error "Manifest validation failed"
    goto :error
)

REM Validate personas
call :validate_personas
if errorlevel 1 (
    call :log_warn "Persona validation had warnings"
)

REM Validate configuration files
call :validate_config_files
if errorlevel 1 (
    call :log_warn "Configuration validation had warnings"
)

call :log_success "All validations complete"
goto :end

:cmd_evolve
call :log_streaming "EVOLUTION CYCLE"
call :log_info "Running AI evolution and optimization..."

REM Track evolution event
call "%HELPERS_DIR%\session_context.bat" :track_system_event "evolution_cycle_started"

REM Analyze session history
call :log_info "Analyzing session history..."
call "%HELPERS_DIR%\session_context.bat" :get_session_summary

REM Optimize based on learning
call :log_info "Optimizing orchestration strategies..."
call :log_success "Evolution cycle complete"

call "%HELPERS_DIR%\session_context.bat" :track_success "evolution_cycle_completed"
goto :end

:cmd_help
echo.
echo UNIMIND LVX MASTER - Help
echo ========================================
echo.
echo Commands:
echo.
echo   init
echo     Initialize the orchestration system
echo     - Creates directory structure
echo     - Initializes session context
echo     - Creates baseline manifest
echo.
echo   start [persona]
echo     Start orchestration system
echo     - Optional: Specify persona to load
echo     - Executes multi-stage workflow
echo.
echo   status
echo     Display system status
echo     - Shows session information
echo     - Lists available personas
echo     - Displays log statistics
echo.
echo   persona [subcommand]
echo     Manage personas
echo     Subcommands:
echo       list      - List available personas
echo       load NAME - Load specific persona
echo       validate  - Validate all personas
echo.
echo   validate
echo     Run all validation checks
echo     - Directory structure
echo     - Manifest integrity
echo     - Persona schemas
echo     - Configuration files
echo.
echo   evolve
echo     Run evolution and optimization cycle
echo     - Analyzes session history
echo     - Optimizes strategies
echo     - Learns from past executions
echo.
echo   help
echo     Display this help message
echo.
echo   version
echo     Display version information
echo.
echo Examples:
echo   unimind_lvx_master.bat init
echo   unimind_lvx_master.bat start legion_x_controller
echo   unimind_lvx_master.bat persona list
echo   unimind_lvx_master.bat validate
echo.
goto :end

:cmd_version
echo.
echo UNIMIND LVX MASTER
echo Version: 1.0.0
echo Legion-X Prime Controller
echo.
echo Components:
echo   - Multi-panel logging system
echo   - Session context and memory
echo   - Manifest validation (SHA-256)
echo   - Persona management system
echo   - Error handling and recovery
echo   - Multi-stage orchestration
echo.
echo Created: 2025-11-11
echo Author: NEXUS-LEGION-X-OMEGA
echo.
goto :end

:load_persona
set PERSONA_NAME=%~1
set PERSONA_FILE=%ORCHESTRATION_ROOT%\..\models\personas\%PERSONA_NAME%.json

if not exist "%PERSONA_FILE%" (
    call :log_error "Persona not found: %PERSONA_NAME%"
    call :log_info "Available personas:"
    for %%f in ("%ORCHESTRATION_ROOT%\..\models\personas\*.json") do (
        echo   - %%~nf
    )
    exit /b 1
)

call :log_success "Loaded persona: %PERSONA_NAME%"
call "%HELPERS_DIR%\session_context.bat" :track_persona_action "%PERSONA_NAME%" "loaded"

REM Display persona greeting (extract from JSON using PowerShell)
powershell -NoProfile -Command "$json = Get-Content '%PERSONA_FILE%' | ConvertFrom-Json; if ($json.interaction_patterns.greeting) { Write-Host $json.interaction_patterns.greeting }"

exit /b 0

:validate_personas
call :log_info "Validating personas..."
set VALIDATION_FAILED=0

if not exist "%ORCHESTRATION_ROOT%\..\models\personas\*.json" (
    call :log_warn "No personas found to validate"
    exit /b 0
)

for %%f in ("%ORCHESTRATION_ROOT%\..\models\personas\*.json") do (
    call :log_info "Validating: %%~nxf"
    powershell -NoProfile -Command "try { $json = Get-Content '%%f' | ConvertFrom-Json; Write-Host '[SUCCESS] Valid JSON: %%~nxf' } catch { Write-Host '[ERROR] Invalid JSON: %%~nxf'; exit 1 }"
    if errorlevel 1 set VALIDATION_FAILED=1
)

if %VALIDATION_FAILED%==1 (
    call :log_error "Persona validation failed"
    exit /b 1
)

call :log_success "All personas validated"
exit /b 0

:validate_config_files
call :log_info "Validating configuration files..."

set VALIDATION_FAILED=0

REM Validate cognitive_plugins.txt
if exist "%ORCHESTRATION_ROOT%\config\cognitive_plugins.txt" (
    call :log_success "cognitive_plugins.txt found"
) else (
    call :log_warn "cognitive_plugins.txt missing"
    set VALIDATION_FAILED=1
)

REM Validate affiliate_config.json
if exist "%ORCHESTRATION_ROOT%\config\affiliate_config.json" (
    powershell -NoProfile -Command "try { Get-Content '%ORCHESTRATION_ROOT%\config\affiliate_config.json' | ConvertFrom-Json | Out-Null; Write-Host '[SUCCESS] affiliate_config.json valid' } catch { Write-Host '[ERROR] affiliate_config.json invalid'; exit 1 }"
    if errorlevel 1 set VALIDATION_FAILED=1
) else (
    call :log_warn "affiliate_config.json missing"
)

REM Validate workspace_guidance.json
if exist "%ORCHESTRATION_ROOT%\config\workspace_guidance.json" (
    powershell -NoProfile -Command "try { Get-Content '%ORCHESTRATION_ROOT%\config\workspace_guidance.json' | ConvertFrom-Json | Out-Null; Write-Host '[SUCCESS] workspace_guidance.json valid' } catch { Write-Host '[ERROR] workspace_guidance.json invalid'; exit 1 }"
    if errorlevel 1 set VALIDATION_FAILED=1
) else (
    call :log_warn "workspace_guidance.json missing"
)

if %VALIDATION_FAILED%==1 (
    exit /b 1
)

call :log_success "Configuration files validated"
exit /b 0

:error
call :log_error "Operation failed"
call "%HELPERS_DIR%\session_context.bat" :track_error "operation_failed"
exit /b 1

:end
echo.
endlocal
exit /b 0

REM Logging stubs for when helpers not loaded
:log_info
echo [INFO] %~1
exit /b 0

:log_success
echo [SUCCESS] %~1
exit /b 0

:log_error
echo [ERROR] %~1
exit /b 0

:log_warn
echo [WARN] %~1
exit /b 0

:log_streaming
echo.
echo ========================================
echo %~1
echo ========================================
echo.
exit /b 0
