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

Write-Host "Docker service:"
wsl -d $WslDistro -u root -- bash -lc "systemctl is-active docker || service docker status || true"

Write-Host ""
Write-Host "Containers:"
wsl -d $WslDistro -u root -- bash -lc "cd '$RepoWslPath' && docker compose ps -a"

Write-Host ""
Write-Host "Port proxy:"
netsh interface portproxy show v4tov4

