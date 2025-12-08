@echo off
REM ============================================================
REM UNIMIND LVX - Error Handler and Validation Module
REM Provides robust error handling and validation routines
REM ============================================================

:check_directory
REM Validate directory exists, create if missing
set DIR_PATH=%~1
set DIR_NAME=%~2

if exist "%DIR_PATH%" (
    call :log_info "Directory validated: %DIR_NAME% at %DIR_PATH%"
    exit /b 0
) else (
    call :log_warn "Directory missing: %DIR_NAME% at %DIR_PATH%"
    call :log_info "Creating directory: %DIR_PATH%"
    mkdir "%DIR_PATH%" 2>nul
    if errorlevel 1 (
        call :log_error "Failed to create directory: %DIR_PATH%"
        exit /b 1
    )
    call :log_success "Directory created: %DIR_PATH%"
    exit /b 0
)

:check_file
REM Validate file exists
set FILE_PATH=%~1
set FILE_NAME=%~2

if exist "%FILE_PATH%" (
    call :log_info "File validated: %FILE_NAME% at %FILE_PATH%"
    exit /b 0
) else (
    call :log_error "File missing: %FILE_NAME% at %FILE_PATH%"
    call :log_error "RESOLUTION: Please ensure %FILE_NAME% exists at the expected location"
    exit /b 1
)

:check_required_tools
REM Check if required tools are available
call :log_info "Checking required tools..."

REM Check PowerShell
where powershell.exe >nul 2>&1
if errorlevel 1 (
    call :log_error "PowerShell not found. PowerShell 5.1 or higher is required."
    exit /b 1
)
call :log_success "PowerShell found"

REM Check Python (optional but recommended)
where python.exe >nul 2>&1
if errorlevel 1 (
    call :log_warn "Python not found. Some features may be limited."
) else (
    call :log_success "Python found"
)

exit /b 0

:validate_environment
REM Validate environment variables are set
if not defined ORCHESTRATION_ROOT (
    call :log_error "ORCHESTRATION_ROOT not defined"
    call :log_error "RESOLUTION: Set ORCHESTRATION_ROOT to the orchestration directory path"
    exit /b 1
)

if not exist "%ORCHESTRATION_ROOT%" (
    call :log_error "ORCHESTRATION_ROOT directory does not exist: %ORCHESTRATION_ROOT%"
    exit /b 1
)

call :log_success "Environment validated"
exit /b 0

:handle_error
REM Generic error handler
set ERROR_CODE=%~1
set ERROR_MSG=%~2
set ERROR_CONTEXT=%~3

call :log_error "Error occurred in %ERROR_CONTEXT%"
call :log_error "Error Code: %ERROR_CODE%"
call :log_error "Message: %ERROR_MSG%"
call :log_error "Timestamp: %date% %time%"

REM Log to session context for AI memory
echo [ERROR] Context: %ERROR_CONTEXT% >> "%LOG_SESSION%"
echo [ERROR] Code: %ERROR_CODE% >> "%LOG_SESSION%"
echo [ERROR] Message: %ERROR_MSG% >> "%LOG_SESSION%"

exit /b %ERROR_CODE%

:safe_delete_file
REM Safely delete a file with validation
set FILE_PATH=%~1

if not exist "%FILE_PATH%" (
    call :log_warn "File does not exist, skipping deletion: %FILE_PATH%"
    exit /b 0
)

del /f /q "%FILE_PATH%" 2>nul
if errorlevel 1 (
    call :log_error "Failed to delete file: %FILE_PATH%"
    exit /b 1
)

call :log_info "File deleted: %FILE_PATH%"
exit /b 0

:safe_copy_file
REM Safely copy a file with validation
set SRC=%~1
set DEST=%~2

if not exist "%SRC%" (
    call :log_error "Source file does not exist: %SRC%"
    exit /b 1
)

xcopy /y /q "%SRC%" "%DEST%*" >nul 2>&1
if errorlevel 1 (
    call :log_error "Failed to copy file from %SRC% to %DEST%"
    exit /b 1
)

call :log_success "File copied: %SRC% -> %DEST%"
exit /b 0

:check_admin_rights
REM Check if running with administrator privileges
net session >nul 2>&1
if errorlevel 1 (
    call :log_warn "Not running with administrator privileges"
    call :log_warn "Some operations may require elevated permissions"
    exit /b 1
) else (
    call :log_info "Running with administrator privileges"
    exit /b 0
)

:log_info
echo [INFO] %~1
exit /b 0

:log_warn
echo [WARN] %~1
exit /b 0

:log_error
echo [ERROR] %~1
exit /b 0

:log_success
echo [SUCCESS] %~1
exit /b 0
