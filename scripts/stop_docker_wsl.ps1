$ErrorActionPreference = "Stop"

function ConvertTo-WslPath {
  param([Parameter(Mandatory = $true)][string]$WindowsPath)

  $fullPath = [System.IO.Path]::GetFullPath($WindowsPath)
  if ($fullPath -notmatch '^([A-Za-z]):\\(.*)$') {
    throw "Only drive-letter Windows paths are supported: $fullPath"
  }

  $drive = $Matches[1].ToLowerInvariant()
  $relativePath = $Matches[2] -replace '\\', '/'
  return "/mnt/$drive/$relativePath"
}

$WslDistro = "Ubuntu"
$RepoWindowsPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RepoWslPath = ConvertTo-WslPath $RepoWindowsPath
$Ports = @(8000, 8501, 5432)

Write-Host "Stopping BetIntel AI containers..."
wsl -d $WslDistro -u root -- bash -lc "cd '$RepoWslPath' && docker compose down"

Write-Host "Stopping WSL keepalive process..."
wsl -d $WslDistro -u root -- bash -lc 'if [ -f /tmp/betintel-wsl-keepalive.pid ]; then pid=$(cat /tmp/betintel-wsl-keepalive.pid); kill $pid 2>/dev/null || true; rm -f /tmp/betintel-wsl-keepalive.pid; fi'

Write-Host "Removing Windows localhost port proxy rules..."
foreach ($port in $Ports) {
  netsh interface portproxy delete v4tov4 listenaddress=127.0.0.1 listenport=$port | Out-Null
}

Write-Host "Stopped."

