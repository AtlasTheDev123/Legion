<#
.SYNOPSIS
Collect basic system information, optionally test internet connectivity, and log results.

USAGE:
  .\system_info.ps1                # collect system info and log to $env:TEMP\windows_script.log
  .\system_info.ps1 -TestInternet # also test connectivity to github.com
#>

[CmdletBinding()]
param(
    [switch]$TestInternet,
    [string]$LogFile = "$env:TEMP\windows_script.log"
)

function Write-Log {
    param(
        [Parameter(Mandatory=$true)][string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = (Get-Date).ToString("s")
    $line = "$timestamp [$Level] $Message"
    $line | Tee-Object -FilePath $LogFile -Append
}

function Get-SystemInfo {
    try {
        $os = Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber
        $cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1 Name, NumberOfCores, NumberOfLogicalProcessors
        $mem = Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object TotalPhysicalMemory
        $disks = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, @{Name='SizeGB';Expression={[math]::Round($_.Size/1GB,2)}}, @{Name='FreeGB';Expression={[math]::Round($_.FreeSpace/1GB,2)}}
        [PSCustomObject]@{
            Time = (Get-Date)
            ComputerName = $env:COMPUTERNAME
            User = $env:USERNAME
            OS = $os
            CPU = $cpu
            MemoryGB = [math]::Round($mem.TotalPhysicalMemory/1GB,2)
            Disks = $disks
        }
    } catch {
        Write-Log "Failed to collect system info: $_" "ERROR"
        throw
    }
}

function Test-ConnectionSimple {
    param([string]$Host = "github.com")
    try {
        $result = Test-NetConnection -ComputerName $Host -WarningAction SilentlyContinue
        [PSCustomObject]@{
            Host = $Host
            Reachable = [bool]($result.TcpTestSucceeded -or $result.PingSucceeded)
            TcpTestSucceeded = $result.TcpTestSucceeded
            PingSucceeded = $result.PingSucceeded
            PingReply = if ($result.PingReplyDetails) { $result.PingReplyDetails.RoundtripTime } else { $null }
        }
    } catch {
        Write-Log "Network test failed for $Host: $_" "ERROR"
        [PSCustomObject]@{ Host = $Host; Reachable = $false }
    }
}

# Main
try {
    Write-Log "Script started" "INFO"
    $info = Get-SystemInfo
    Write-Log ($info | Out-String) "INFO"

    if ($TestInternet) {
        $net = Test-ConnectionSimple
        Write-Log ($net | Out-String) "INFO"
    }

    # Output structured results to console for further processing if needed
    $info
    if ($TestInternet) { $net }

    Write-Log "Script completed successfully" "INFO"
    exit 0
} catch {
    Write-Log "Unhandled error: $_" "ERROR"
    exit 1
}