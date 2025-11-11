# ============================================================
# UNIMIND LVX - Manifest Verification PowerShell Script
# Validates SHA-256 manifest integrity
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ManifestPath
)

Write-Host "[INFO] Starting manifest verification..." -ForegroundColor Cyan

if (-not (Test-Path $ManifestPath)) {
    Write-Host "[ERROR] Manifest file not found: $ManifestPath" -ForegroundColor Red
    exit 1
}

$manifestContent = Get-Content $ManifestPath
$totalFiles = 0
$validatedFiles = 0
$failedFiles = 0
$missingFiles = 0

foreach ($line in $manifestContent) {
    # Skip comments and empty lines
    if ($line -match '^\s*#' -or $line -match '^\s*$') {
        continue
    }

    # Parse line: HASH *filepath
    if ($line -match '^([0-9A-Fa-f]{64})\s+\*(.+)$') {
        $expectedHash = $matches[1]
        $filePath = $matches[2].Trim()
        $totalFiles++

        Write-Host "[VERIFY] Checking: $(Split-Path $filePath -Leaf)" -ForegroundColor Gray

        if (-not (Test-Path $filePath)) {
            Write-Host "[WARN] File missing: $filePath" -ForegroundColor Yellow
            $missingFiles++
            continue
        }

        try {
            $currentHash = (Get-FileHash -Algorithm SHA256 $filePath).Hash

            if ($currentHash -eq $expectedHash) {
                $validatedFiles++
            } else {
                Write-Host "[ERROR] Hash mismatch: $filePath" -ForegroundColor Red
                Write-Host "  Expected: $expectedHash" -ForegroundColor Red
                Write-Host "  Current:  $currentHash" -ForegroundColor Red
                $failedFiles++
            }
        } catch {
            Write-Host "[ERROR] Failed to hash file: $filePath" -ForegroundColor Red
            Write-Host "  Error: $_" -ForegroundColor Red
            $failedFiles++
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MANIFEST VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total Files:     $totalFiles" -ForegroundColor White
Write-Host "Validated:       $validatedFiles" -ForegroundColor Green
Write-Host "Failed:          $failedFiles" -ForegroundColor $(if ($failedFiles -gt 0) { "Red" } else { "Green" })
Write-Host "Missing:         $missingFiles" -ForegroundColor $(if ($missingFiles -gt 0) { "Yellow" } else { "Green" })
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($failedFiles -gt 0) {
    Write-Host "[RESULT] Manifest validation FAILED" -ForegroundColor Red
    exit 1
} elseif ($missingFiles -gt 0) {
    Write-Host "[RESULT] Manifest validation completed with WARNINGS" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "[RESULT] Manifest validation PASSED" -ForegroundColor Green
    exit 0
}
