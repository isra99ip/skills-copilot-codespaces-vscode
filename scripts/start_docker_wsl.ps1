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

Write-Host "Starting Docker service in WSL..."
wsl -d $WslDistro -u root -- bash -lc "systemctl start docker 2>/dev/null || service docker start"

Write-Host "Starting BetIntel AI containers..."
wsl -d $WslDistro -u root -- bash -lc "cd '$RepoWslPath' && docker compose up -d --build"

$ipLine = wsl -d $WslDistro -u root -- hostname -I
$wslIp = ($ipLine -split "\s+")[0]
if (-not $wslIp) {
  throw "Could not determine WSL IP address."
}

Write-Host "Configuring Windows localhost port proxy to WSL IP $wslIp..."
foreach ($port in $Ports) {
  netsh interface portproxy delete v4tov4 listenaddress=127.0.0.1 listenport=$port | Out-Null
  netsh interface portproxy add v4tov4 listenaddress=127.0.0.1 listenport=$port connectaddress=$wslIp connectport=$port | Out-Null
}

$keepAliveCheck = wsl -d $WslDistro -u root -- bash -lc 'if [ -f /tmp/betintel-wsl-keepalive.pid ]; then pid=$(cat /tmp/betintel-wsl-keepalive.pid); if kill -0 $pid 2>/dev/null; then echo running; fi; fi'
if ($keepAliveCheck -ne "running") {
  Write-Host "Starting WSL keepalive process..."
  $keepAliveCommand = 'echo $$ > /tmp/betintel-wsl-keepalive.pid; trap "rm -f /tmp/betintel-wsl-keepalive.pid; exit 0" TERM INT; while true; do sleep 3600; done'
  Start-Process -FilePath "wsl.exe" -ArgumentList @("-d", $WslDistro, "-u", "root", "--", "bash", "-lc", $keepAliveCommand) -WindowStyle Hidden | Out-Null
}

Start-Sleep -Seconds 3

Write-Host "Checking containers..."
wsl -d $WslDistro -u root -- bash -lc "cd '$RepoWslPath' && docker compose ps"

Write-Host ""
Write-Host "Ready:"
Write-Host "  API:       http://127.0.0.1:8000"
Write-Host "  API docs:  http://127.0.0.1:8000/docs"
Write-Host "  Dashboard: http://127.0.0.1:8501"
Write-Host "  Postgres:  127.0.0.1:5432"

