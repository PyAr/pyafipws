# test_remito_electronico_carnico.ps1

$ErrorActionPreference = "Stop"

# Set the working directory to the root of the repository
Set-Location $PSScriptRoot\..

# Verify dependencies
if (-not (Test-Path ".\dist\remito_electronico_carnico.vbs")) {
    Write-Error "remito_electronico_carnico.vbs not found in dist folder. Ensure all dependencies are installed."
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
    $output = cscript //nologo .\dist\remito_electronico_carnico.vbs
    $output | Out-File -FilePath "remito_electronico_carnico_output.log"
} catch {
    Write-Error "Failed to execute remito_electronico_carnico.vbs: $_"
    exit 1
}

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "remito_electronico_carnico.vbs failed to execute with exit code $LASTEXITCODE"
    exit 1
}

# Test for expected output
$expectedOutputs = @(
    "InstallDir", "Token", "Sign", "Ultimo comprobante:", "Resultado:",
    "Cod Remito:", "Numero Remito:", "Cod Autorizacion:", "Fecha Emision",
    "Fecha Vencimiento", "Observaciones:", "Errores:", "Evento:"
)

foreach ($expected in $expectedOutputs) {
    if ($output -notmatch $expected) {
        Write-Error "Expected output not found: $expected"
        exit 1
    }
}

# Check for successful remito generation
if ($output -notmatch "Resultado: A") {
    Write-Error "Remito generation not successful"
    exit 1
}

# Check for Cod Remito
if ($output -notmatch "Cod Remito: \d+") {
    Write-Error "Cod Remito not obtained successfully"
    exit 1
}

# Check if QR file was created
if (-not (Test-Path "qr.png")) {
    Write-Error "QR code image file was not created"
    exit 1
}

Write-Host "All tests for remito_electronico_carnico.vbs passed successfully"
