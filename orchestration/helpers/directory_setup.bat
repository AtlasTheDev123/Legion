@echo off
REM ============================================================
REM UNIMIND LVX - Directory Setup Module
REM Creates and validates all required directories
REM ============================================================

:setup_all_directories
REM Create all required directories for orchestration

call :log_streaming "DIRECTORY SETUP - Creating orchestration structure"

REM Core directories
call :create_dir "%ORCHESTRATION_ROOT%\bat" "BAT Scripts"
call :create_dir "%ORCHESTRATION_ROOT%\helpers" "Helper Modules"
call :create_dir "%ORCHESTRATION_ROOT%\config" "Configuration"
call :create_dir "%ORCHESTRATION_ROOT%\logs" "Logs Root"
call :create_dir "%ORCHESTRATION_ROOT%\logs\code" "Code Logs"
call :create_dir "%ORCHESTRATION_ROOT%\logs\media" "Media Logs"
call :create_dir "%ORCHESTRATION_ROOT%\logs\affiliate" "Affiliate Logs"
call :create_dir "%ORCHESTRATION_ROOT%\logs\session" "Session Logs"
call :create_dir "%ORCHESTRATION_ROOT%\temp" "Temporary Files"
call :create_dir "%ORCHESTRATION_ROOT%\backups" "Backups"

REM Models and personas
call :create_dir "%ORCHESTRATION_ROOT%\..\models" "Models Root"
call :create_dir "%ORCHESTRATION_ROOT%\..\models\personas" "Personas"
call :create_dir "%ORCHESTRATION_ROOT%\..\models\templates" "Templates"

REM Plugins and extensions
call :create_dir "%ORCHESTRATION_ROOT%\..\plugins" "Plugins"
call :create_dir "%ORCHESTRATION_ROOT%\..\plugins\cognitive" "Cognitive Plugins"
call :create_dir "%ORCHESTRATION_ROOT%\..\plugins\affiliate" "Affiliate Plugins"
call :create_dir "%ORCHESTRATION_ROOT%\..\plugins\workspace" "Workspace Plugins"

call :log_success "Directory structure created successfully"
exit /b 0

:create_dir
REM Create a directory with logging
set DIR_PATH=%~1
set DIR_NAME=%~2

if exist "%DIR_PATH%" (
    call :log_info "Directory exists: %DIR_NAME%"
    exit /b 0
)

mkdir "%DIR_PATH%" 2>nul
if errorlevel 1 (
    call :log_error "Failed to create directory: %DIR_NAME% at %DIR_PATH%"
    exit /b 1
)

call :log_success "Created directory: %DIR_NAME%"
exit /b 0

:validate_directory_structure
REM Validate all required directories exist
call :log_info "Validating directory structure..."

set VALIDATION_FAILED=0

call :validate_dir "%ORCHESTRATION_ROOT%\bat" || set VALIDATION_FAILED=1
call :validate_dir "%ORCHESTRATION_ROOT%\helpers" || set VALIDATION_FAILED=1
call :validate_dir "%ORCHESTRATION_ROOT%\config" || set VALIDATION_FAILED=1
call :validate_dir "%ORCHESTRATION_ROOT%\logs" || set VALIDATION_FAILED=1

if %VALIDATION_FAILED%==1 (
    call :log_error "Directory validation failed"
    call :log_error "RESOLUTION: Run directory setup to create missing directories"
    exit /b 1
)

call :log_success "Directory structure validated"
exit /b 0

:validate_dir
REM Validate a single directory
set DIR_PATH=%~1

if not exist "%DIR_PATH%" (
    call :log_error "Required directory missing: %DIR_PATH%"
    exit /b 1
)

exit /b 0

:cleanup_temp
REM Clean up temporary files
call :log_info "Cleaning temporary files..."

if exist "%ORCHESTRATION_ROOT%\temp" (
    del /q "%ORCHESTRATION_ROOT%\temp\*.*" 2>nul
    call :log_success "Temporary files cleaned"
)

exit /b 0

:backup_config
REM Backup configuration files
set BACKUP_DIR=%ORCHESTRATION_ROOT%\backups\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

call :log_info "Creating configuration backup..."
call :create_dir "%BACKUP_DIR%" "Backup Directory"

if exist "%ORCHESTRATION_ROOT%\config\*.*" (
    xcopy /y /q "%ORCHESTRATION_ROOT%\config\*.*" "%BACKUP_DIR%\" >nul 2>&1
    if errorlevel 1 (
        call :log_warn "Backup failed or no files to backup"
    ) else (
        call :log_success "Configuration backed up to: %BACKUP_DIR%"
    )
)

exit /b 0

:log_info
echo [INFO] %~1
exit /b 0

:log_success
echo [SUCCESS] %~1
exit /b 0

:log_error
echo [ERROR] %~1
exit /b 0

:log_streaming
echo.
echo ========================================
echo %~1
echo ========================================
echo.
exit /b 0
