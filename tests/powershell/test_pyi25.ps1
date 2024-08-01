# test_pyi25.ps1

$ErrorActionPreference = "Stop"

# Run the VBS script and capture its output
$output = cscript //nologo ejemplos\pyi25\pyi25.vbs

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "pyi25.vbs failed to execute"
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
if (-not (Test-Path "ejemplos\pyi25\barras.png")) {
    Write-Error "Barcode image file was not created"
    exit 1
}

Write-Host "All tests for pyi25.vbs passed successfully"
