# test_remito_electronico_carnico.ps1

$ErrorActionPreference = "Stop"

# Run the VBS script and capture its output
$output = cscript //nologo ejemplos\remito_electronico_carnico.vbs

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "remito_electronico_carnico.vbs failed to execute"
    exit 1
}

# Test for expected output
$expectedOutputs = @(
    "InstallDir",
    "Token",
    "Sign",
    "Ultimo comprobante:",
    "Resultado:",
    "Cod Remito:",
    "Numero Remito:",
    "Cod Autorizacion:",
    "Fecha Emision",
    "Fecha Vencimiento",
    "Observaciones:",
    "Errores:",
    "Evento:"
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
