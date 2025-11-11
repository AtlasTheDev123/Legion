# ============================================================
# UNIMIND LVX - Setup Directories PowerShell Script
# Creates all required configuration directories
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$OrchestrationRoot
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DIRECTORY SETUP - PowerShell Module" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$directories = @(
    "$OrchestrationRoot\bat",
    "$OrchestrationRoot\helpers",
    "$OrchestrationRoot\config",
    "$OrchestrationRoot\logs",
    "$OrchestrationRoot\logs\code",
    "$OrchestrationRoot\logs\media",
    "$OrchestrationRoot\logs\affiliate",
    "$OrchestrationRoot\logs\session",
    "$OrchestrationRoot\temp",
    "$OrchestrationRoot\backups",
    "$OrchestrationRoot\..\models",
    "$OrchestrationRoot\..\models\personas",
    "$OrchestrationRoot\..\models\templates",
    "$OrchestrationRoot\..\plugins",
    "$OrchestrationRoot\..\plugins\cognitive",
    "$OrchestrationRoot\..\plugins\affiliate",
    "$OrchestrationRoot\..\plugins\workspace"
)

$created = 0
$existing = 0
$failed = 0

foreach ($dir in $directories) {
    $dirName = Split-Path $dir -Leaf
    
    if (Test-Path $dir) {
        Write-Host "[EXISTS] $dirName" -ForegroundColor Gray
        $existing++
    } else {
        try {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "[CREATED] $dirName" -ForegroundColor Green
            $created++
        } catch {
            Write-Host "[ERROR] Failed to create $dirName" -ForegroundColor Red
            Write-Host "  Error: $_" -ForegroundColor Red
            $failed++
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DIRECTORY SETUP SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Created:   $created" -ForegroundColor Green
Write-Host "Existing:  $existing" -ForegroundColor Gray
Write-Host "Failed:    $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($failed -gt 0) {
    Write-Host "[RESULT] Directory setup completed with ERRORS" -ForegroundColor Red
    exit 1
} else {
    Write-Host "[RESULT] Directory setup completed SUCCESSFULLY" -ForegroundColor Green
    exit 0
}
