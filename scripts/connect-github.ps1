param(
  [Parameter(Mandatory = $true)]
  [string]$RepositoryUrl
)

$ErrorActionPreference = "Stop"

$git = "C:\Users\naoya\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe"

if (-not (Test-Path $git)) {
  $git = "git"
}

& $git remote remove origin 2>$null
& $git remote add origin $RepositoryUrl
& $git branch -M main
& $git push -u origin main

Write-Host "GitHub push completed: $RepositoryUrl"
