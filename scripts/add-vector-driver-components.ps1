#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"

Write-Output "Moving Vector driver dlls."

try {
  Push-Location "$PSScriptRoot\driver-components\.."
  # Required for serial communication over a vector CAN Bus
  Move-Item -Path .\vxlapi.dll -Destination "$env:windir\System32"
  Move-Item -Path .\vxlapi64.dll -Destination "$env:windir\System32"

} finally {
  Pop-Location
}

Write-Output "Done!"
