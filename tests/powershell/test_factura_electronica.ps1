# test_factura_electronica.ps1

$ErrorActionPreference = "Stop"

# Run the VBS script and capture its output
$output = cscript //nologo ejemplos\factura_electronica.vbs

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "factura_electronica.vbs failed to execute"
    exit 1
}

# Test for expected output
$expectedOutputs = @(
    "InstallDir",
    "Token",
    "Sign",
    "Ultimo comprobante:",
    "Resultado",
    "CAE",
    "Numero de comprobante:",
    "ErrMsg",
    "Obs",
    "Reprocesar:",
    "Reproceso:",
    "EmisionTipo:"
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
