@echo off
REM ============================================================
REM UNIMIND LVX - Multi-Panel Logger
REM Provides logging to separate panels/files for different contexts
REM ============================================================

:log_init
REM Initialize logging directories
if not exist "%ORCHESTRATION_ROOT%\logs" mkdir "%ORCHESTRATION_ROOT%\logs"
if not exist "%ORCHESTRATION_ROOT%\logs\code" mkdir "%ORCHESTRATION_ROOT%\logs\code"
if not exist "%ORCHESTRATION_ROOT%\logs\media" mkdir "%ORCHESTRATION_ROOT%\logs\media"
if not exist "%ORCHESTRATION_ROOT%\logs\affiliate" mkdir "%ORCHESTRATION_ROOT%\logs\affiliate"
if not exist "%ORCHESTRATION_ROOT%\logs\session" mkdir "%ORCHESTRATION_ROOT%\logs\session"

REM Set timestamp for log files
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set LOG_TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%

REM Create log file paths
set LOG_CODE=%ORCHESTRATION_ROOT%\logs\code\code_%LOG_TIMESTAMP%.log
set LOG_MEDIA=%ORCHESTRATION_ROOT%\logs\media\media_%LOG_TIMESTAMP%.log
set LOG_AFFILIATE=%ORCHESTRATION_ROOT%\logs\affiliate\affiliate_%LOG_TIMESTAMP%.log
set LOG_SESSION=%ORCHESTRATION_ROOT%\logs\session\session_%LOG_TIMESTAMP%.log
set LOG_MASTER=%ORCHESTRATION_ROOT%\logs\master_%LOG_TIMESTAMP%.log

echo [%date% %time%] Logging system initialized >> "%LOG_MASTER%"
echo [%date% %time%] Log files created: >> "%LOG_MASTER%"
echo   - Code: %LOG_CODE% >> "%LOG_MASTER%"
echo   - Media: %LOG_MEDIA% >> "%LOG_MASTER%"
echo   - Affiliate: %LOG_AFFILIATE% >> "%LOG_MASTER%"
echo   - Session: %LOG_SESSION% >> "%LOG_MASTER%"
exit /b 0

:log_code
REM Log to code panel
set MSG=%~1
echo [%date% %time%] %MSG% >> "%LOG_CODE%"
echo [CODE] %MSG% >> "%LOG_MASTER%"
echo [CODE] %MSG%
exit /b 0

:log_media
REM Log to media panel
set MSG=%~1
echo [%date% %time%] %MSG% >> "%LOG_MEDIA%"
echo [MEDIA] %MSG% >> "%LOG_MASTER%"
echo [MEDIA] %MSG%
exit /b 0

:log_affiliate
REM Log to affiliate panel
set MSG=%~1
echo [%date% %time%] %MSG% >> "%LOG_AFFILIATE%"
echo [AFFILIATE] %MSG% >> "%LOG_MASTER%"
echo [AFFILIATE] %MSG%
exit /b 0

:log_session
REM Log to session context panel
set MSG=%~1
echo [%date% %time%] %MSG% >> "%LOG_SESSION%"
echo [SESSION] %MSG% >> "%LOG_MASTER%"
echo [SESSION] %MSG%
exit /b 0

:log_info
REM General info logging
set MSG=%~1
echo [%date% %time%] [INFO] %MSG% >> "%LOG_MASTER%"
echo [INFO] %MSG%
exit /b 0

:log_warn
REM Warning logging
set MSG=%~1
echo [%date% %time%] [WARN] %MSG% >> "%LOG_MASTER%"
echo [WARN] %MSG%
exit /b 0

:log_error
REM Error logging
set MSG=%~1
echo [%date% %time%] [ERROR] %MSG% >> "%LOG_MASTER%"
echo [ERROR] %MSG%
exit /b 0

:log_success
REM Success logging with visual indicator
set MSG=%~1
echo [%date% %time%] [SUCCESS] %MSG% >> "%LOG_MASTER%"
echo [SUCCESS] %MSG%
exit /b 0

:log_streaming
REM Progressive streaming log - real-time status updates
set MSG=%~1
echo [%date% %time%] [STREAM] %MSG% >> "%LOG_MASTER%"
echo.
echo ========================================
echo %MSG%
echo ========================================
echo.
exit /b 0
