# test_pyi25.ps1

$ErrorActionPreference = "Stop"

# Set the working directory to the root of the repository
Set-Location $PSScriptRoot\..

# Verify dependencies
if (-not (Test-Path ".\ejemplos\pyi25\pyi25.vbs")) {
    Write-Error "pyi25.vbs not found. Ensure all dependencies are installed."
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
    $output = cscript //nologo .\ejemplos\pyi25\pyi25.vbs
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
if ($output -notmatch "Version") {
    Write-Error "Version information not found in output"
    exit 1
}

if ($output -notmatch "Barras") {
    Write-Error "Barcode information not found in output"
    exit 1
}

if ($output -notmatch "Listo!") {
    Write-Error "Script did not complete successfully"
    exit 1
}

# Check if the output file was created
if (-not (Test-Path ".\ejemplos\pyi25\barras.png")) {
    Write-Error "Barcode image file was not created"
    exit 1
}

Write-Host "All tests for pyi25.vbs passed successfully"
