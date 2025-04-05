$ErrorActionPreference = "Stop"

$pyPath = "py"
Write-Output "Python is running from ($pyPath)."
try {
  Push-Location "$PSScriptRoot\.."
  if ($null -eq $env:VIRTUAL_ENV) {
    if (-Not(Test-Path ".venv")) {
      & "$pyPath" -m venv .venv
      if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
      }
    }

    .\.venv\Scripts\Activate.ps1
    if ($LASTEXITCODE -ne 0) {
      exit $LASTEXITCODE
    }
  }

  pip install . --disable-pip-version-check
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  pip install .[dev] --disable-pip-version-check
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
} finally {
  Pop-Location
}
