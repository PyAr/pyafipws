# test_factura_electronica.ps1

$ErrorActionPreference = "Stop"

# Set the working directory to the root of the repository
Set-Location $PSScriptRoot\..

# Verify dependencies
if (-not (Test-Path ".\dist\factura_electronica.vbs")) {
    Write-Error "factura_electronica.vbs not found in dist folder. Ensure all dependencies are installed."
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
    $output = cscript //nologo .\dist\factura_electronica.vbs
    $output | Out-File -FilePath "factura_electronica_output.log"
} catch {
    Write-Error "Failed to execute factura_electronica.vbs: $_"
    exit 1
}

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "factura_electronica.vbs failed to execute with exit code $LASTEXITCODE"
    exit 1
}

# Test for expected output
$expectedOutputs = @(
    "InstallDir", "Token", "Sign", "Ultimo comprobante:", "Resultado",
    "CAE", "Numero de comprobante:", "ErrMsg", "Obs", "Reprocesar:",
    "Reproceso:", "EmisionTipo:"
)

foreach ($expected in $expectedOutputs) {
    if ($output -notmatch $expected) {
        Write-Error "Expected output not found: $expected"
        exit 1
    }
}

# Check for successful CAE solicitation
if ($output -notmatch "CAE: \d+") {
    Write-Error "CAE not obtained successfully"
    exit 1
}

# Check for successful result
if ($output -notmatch "Resultado: A") {
    Write-Error "Invoice authorization not successful"
    exit 1
}

Write-Host "All tests for factura_electronica.vbs passed successfully"
