# test_pyqr.ps1

$ErrorActionPreference = "Stop"

# Set the working directory to the root of the repository
Set-Location $PSScriptRoot\..

# Verify dependencies
if (-not (Test-Path ".\dist\pyqr.vbs")) {
    Write-Error "pyqr.vbs not found in dist folder. Ensure all dependencies are installed."
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
    $output = cscript //nologo .\dist\pyqr.vbs
    $output | Out-File -FilePath "pyqr_output.log"
} catch {
    Write-Error "Failed to execute pyqr.vbs: $_"
    exit 1
}

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "pyqr.vbs failed to execute with exit code $LASTEXITCODE"
    exit 1
}

# Test for expected output
if ($output -notmatch "CrearArchivo" -or $output -notmatch "GenerarImagen") {
    Write-Error "Expected output not found in pyqr.vbs execution"
    exit 1
}

# Extract the file paths from the output
$createdFile = ($output -split "`n" | Select-String "CrearArchivo").ToString().Trim()
$generatedImage = ($output -split "`n" | Select-String "GenerarImagen").ToString().Trim()

# Check if the files were created
if (-not (Test-Path $createdFile) -or -not (Test-Path $generatedImage)) {
    Write-Error "Expected files not created by pyqr.vbs"
    exit 1
}

Write-Host "All tests for pyqr.vbs passed successfully"
