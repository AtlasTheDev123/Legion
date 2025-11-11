@echo off
REM ============================================================
REM UNIMIND LVX - Session Context and Memory Tracker
REM Maintains context across runs for AI memory
REM ============================================================

:init_session
REM Initialize session context
set SESSION_FILE=%ORCHESTRATION_ROOT%\config\session_context.json

if not exist "%SESSION_FILE%" (
    call :create_session_file
)

REM Load session counter
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-Content '%SESSION_FILE%' | ConvertFrom-Json).session_count"') do set SESSION_COUNT=%%i
set /a SESSION_COUNT+=1

REM Update session file
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; $json.session_count = %SESSION_COUNT%; $json.last_run = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'; $json | ConvertTo-Json -Depth 10 | Set-Content '%SESSION_FILE%'"

call :log_session "Session #%SESSION_COUNT% initialized"
call :log_session "Last run: %date% %time%"
exit /b 0

:create_session_file
REM Create initial session context file
echo {> "%SESSION_FILE%"
echo   "session_count": 0,>> "%SESSION_FILE%"
echo   "last_run": "",>> "%SESSION_FILE%"
echo   "last_command": "",>> "%SESSION_FILE%"
echo   "last_persona": "",>> "%SESSION_FILE%"
echo   "last_action": "",>> "%SESSION_FILE%"
echo   "system_events": [],>> "%SESSION_FILE%"
echo   "error_history": [],>> "%SESSION_FILE%"
echo   "success_history": []>> "%SESSION_FILE%"
echo }>> "%SESSION_FILE%"
call :log_info "Session context file created"
exit /b 0

:track_command
REM Track command execution
set COMMAND=%~1

call :log_session "Command tracked: %COMMAND%"

REM Update session file with command
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; $json.last_command = '%COMMAND%'; $json.last_action = 'command_executed'; $json | ConvertTo-Json -Depth 10 | Set-Content '%SESSION_FILE%'"

exit /b 0

:track_persona_action
REM Track persona-related action
set PERSONA=%~1
set ACTION=%~2

call :log_session "Persona action: %PERSONA% - %ACTION%"

REM Update session file with persona action
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; $json.last_persona = '%PERSONA%'; $json.last_action = '%ACTION%'; $json | ConvertTo-Json -Depth 10 | Set-Content '%SESSION_FILE%'"

exit /b 0

:track_system_event
REM Track system event
set EVENT=%~1
set TIMESTAMP=%date% %time%

call :log_session "System event: %EVENT%"

REM Append to system events (PowerShell to handle JSON array)
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; $event = @{timestamp='%TIMESTAMP%'; event='%EVENT%'}; $json.system_events += $event; if ($json.system_events.Count -gt 50) { $json.system_events = $json.system_events[-50..-1] }; $json | ConvertTo-Json -Depth 10 | Set-Content '%SESSION_FILE%'"

exit /b 0

:track_error
REM Track error for learning
set ERROR_MSG=%~1
set TIMESTAMP=%date% %time%

call :log_session "Error tracked: %ERROR_MSG%"

REM Append to error history
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; $error = @{timestamp='%TIMESTAMP%'; error='%ERROR_MSG%'}; $json.error_history += $error; if ($json.error_history.Count -gt 20) { $json.error_history = $json.error_history[-20..-1] }; $json | ConvertTo-Json -Depth 10 | Set-Content '%SESSION_FILE%'"

exit /b 0

:track_success
REM Track success for learning
set SUCCESS_MSG=%~1
set TIMESTAMP=%date% %time%

call :log_session "Success tracked: %SUCCESS_MSG%"

REM Append to success history
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; $success = @{timestamp='%TIMESTAMP%'; success='%SUCCESS_MSG%'}; $json.success_history += $success; if ($json.success_history.Count -gt 20) { $json.success_history = $json.success_history[-20..-1] }; $json | ConvertTo-Json -Depth 10 | Set-Content '%SESSION_FILE%'"

exit /b 0

:get_last_command
REM Retrieve last command from session
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-Content '%SESSION_FILE%' | ConvertFrom-Json).last_command"') do set LAST_CMD=%%i
echo %LAST_CMD%
exit /b 0

:get_session_summary
REM Display session summary
call :log_streaming "SESSION CONTEXT SUMMARY"
echo.
powershell -NoProfile -Command "$json = Get-Content '%SESSION_FILE%' | ConvertFrom-Json; Write-Host 'Session Count:' $json.session_count; Write-Host 'Last Run:' $json.last_run; Write-Host 'Last Command:' $json.last_command; Write-Host 'Last Persona:' $json.last_persona; Write-Host 'Recent Errors:' $json.error_history.Count; Write-Host 'Recent Successes:' $json.success_history.Count"
echo.
exit /b 0

:log_session
echo [SESSION] %~1
exit /b 0

:log_info
echo [INFO] %~1
exit /b 0

:log_streaming
echo.
echo ========================================
echo %~1
echo ========================================
echo.
exit /b 0
