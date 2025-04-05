$ErrorActionPreference = "Stop"

if ($null -eq $env:VIRTUAL_ENV) {
  & "$PSScriptRoot\setup.ps1"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
}


isort .
black .
pylint .
