@echo off
REM ============================================================
REM UNIMIND LVX - Manifest Validator
REM SHA-256 manifest validation and security checks
REM ============================================================

:validate_manifest
REM Validate baseline manifest
set MANIFEST_FILE=%ORCHESTRATION_ROOT%\config\baseline_manifest.sha256

call :log_streaming "MANIFEST VALIDATION - Verifying system integrity"

if not exist "%MANIFEST_FILE%" (
    call :log_warn "Baseline manifest not found: %MANIFEST_FILE%"
    call :log_warn "Creating new baseline manifest..."
    call :create_baseline_manifest
    exit /b 0
)

call :log_info "Manifest file found: %MANIFEST_FILE%"

REM Use PowerShell to validate manifest
powershell -NoProfile -ExecutionPolicy Bypass -File "%ORCHESTRATION_ROOT%\helpers\verify_manifest.ps1" -ManifestPath "%MANIFEST_FILE%"

if errorlevel 1 (
    call :log_error "Manifest validation failed"
    call :log_error "RESOLUTION: Review manifest file or regenerate baseline"
    exit /b 1
)

call :log_success "Manifest validation passed"
exit /b 0

:create_baseline_manifest
REM Create baseline manifest with SHA-256 hashes
set MANIFEST_FILE=%ORCHESTRATION_ROOT%\config\baseline_manifest.sha256

call :log_info "Creating baseline manifest..."

REM Create manifest header
echo # UNIMIND LVX Baseline Manifest > "%MANIFEST_FILE%"
echo # Generated: %date% %time% >> "%MANIFEST_FILE%"
echo # Format: SHA256 *filename >> "%MANIFEST_FILE%"
echo. >> "%MANIFEST_FILE%"

REM Hash critical files using PowerShell
call :hash_file "%ORCHESTRATION_ROOT%\bat\unimind_lvx_master.bat"
call :hash_file "%ORCHESTRATION_ROOT%\helpers\logger.bat"
call :hash_file "%ORCHESTRATION_ROOT%\helpers\error_handler.bat"
call :hash_file "%ORCHESTRATION_ROOT%\helpers\session_context.bat"
call :hash_file "%ORCHESTRATION_ROOT%\helpers\directory_setup.bat"
call :hash_file "%ORCHESTRATION_ROOT%\helpers\manifest_validator.bat"

REM Hash configuration files
call :hash_file "%ORCHESTRATION_ROOT%\config\cognitive_plugins.txt"
if exist "%ORCHESTRATION_ROOT%\config\affiliate_config.json" call :hash_file "%ORCHESTRATION_ROOT%\config\affiliate_config.json"
if exist "%ORCHESTRATION_ROOT%\config\workspace_guidance.json" call :hash_file "%ORCHESTRATION_ROOT%\config\workspace_guidance.json"

REM Hash persona files
if exist "%ORCHESTRATION_ROOT%\..\models\personas\atlas_architect.json" call :hash_file "%ORCHESTRATION_ROOT%\..\models\personas\atlas_architect.json"
if exist "%ORCHESTRATION_ROOT%\..\models\personas\legion_x_controller.json" call :hash_file "%ORCHESTRATION_ROOT%\..\models\personas\legion_x_controller.json"

call :log_success "Baseline manifest created: %MANIFEST_FILE%"
exit /b 0

:hash_file
REM Hash a single file and append to manifest
set FILE_PATH=%~1

if not exist "%FILE_PATH%" (
    call :log_warn "File not found for hashing: %FILE_PATH%"
    exit /b 0
)

REM Use PowerShell to calculate SHA-256
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 '%FILE_PATH%').Hash"') do set HASH=%%i

echo %HASH% *%FILE_PATH% >> "%MANIFEST_FILE%"
call :log_info "Hashed: %~nx1"

exit /b 0

:verify_file_integrity
REM Verify a single file against manifest
set FILE_PATH=%~1
set MANIFEST_FILE=%ORCHESTRATION_ROOT%\config\baseline_manifest.sha256

if not exist "%MANIFEST_FILE%" (
    call :log_warn "Manifest not found, skipping verification"
    exit /b 0
)

if not exist "%FILE_PATH%" (
    call :log_error "File not found for verification: %FILE_PATH%"
    exit /b 1
)

REM Get current hash
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 '%FILE_PATH%').Hash"') do set CURRENT_HASH=%%i

REM Get expected hash from manifest
for /f "tokens=1" %%i in ('findstr /i "%FILE_PATH%" "%MANIFEST_FILE%"') do set EXPECTED_HASH=%%i

if not defined EXPECTED_HASH (
    call :log_warn "File not in manifest: %FILE_PATH%"
    exit /b 0
)

if /i "%CURRENT_HASH%"=="%EXPECTED_HASH%" (
    call :log_success "File integrity verified: %~nx1"
    exit /b 0
) else (
    call :log_error "File integrity check FAILED: %~nx1"
    call :log_error "Expected: %EXPECTED_HASH%"
    call :log_error "Current:  %CURRENT_HASH%"
    exit /b 1
)

:update_manifest
REM Update manifest with current file hashes
call :log_info "Updating baseline manifest..."
call :create_baseline_manifest
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
