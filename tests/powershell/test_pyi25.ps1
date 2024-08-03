# test_pyi25.ps1

$ErrorActionPreference = "Stop"

# Set the working directory to the root of the repository
Set-Location $PSScriptRoot\..

# Verify dependencies
if (-not (Test-Path ".\dist\pyi25.vbs")) {
    Write-Error "pyi25.vbs not found in dist folder. Ensure all dependencies are installed."
    exit 1
}

# Set execution policy for this script
try {
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
} catch {
    Write-Warning "Failed to set execution policy. Script may fail if not run with appropriate permissions."
}

# Run the VBS script and capture its output
try {
    $output = cscript //nologo .\dist\pyi25.vbs
    $output | Out-File -FilePath "pyi25_output.log"
} catch {
    Write-Error "Failed to execute pyi25.vbs: $_"
    exit 1
}

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "pyi25.vbs failed to execute with exit code $LASTEXITCODE"
    exit 1
}

# Test for expected output
if ($output -notmatch "Version" -or $output -notmatch "Barras" -or $output -notmatch "Listo!") {
    Write-Error "Expected output not found in pyi25.vbs execution"
    exit 1
}

# Check if the output file was created
if (-not (Test-Path ".\dist\barras.png")) {
    Write-Error "Barcode image file was not created"
    exit 1
}

Write-Host "Current directory: $(Get-Location)"
Write-Host "Contents of dist folder:"
Get-ChildItem .\dist
