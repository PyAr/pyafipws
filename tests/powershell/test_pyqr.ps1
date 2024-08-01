# test_pyqr.ps1

$ErrorActionPreference = "Stop"

# Run the VBS script and capture its output
$output = cscript //nologo ejemplos\pyqr\pyqr.vbs

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "pyqr.vbs failed to execute"
    exit 1
}

# Test for expected output
if ($output -notmatch "CrearArchivo") {
    Write-Error "CrearArchivo output not found"
    exit 1
}

if ($output -notmatch "GenerarImagen") {
    Write-Error "GenerarImagen output not found"
    exit 1
}

# Extract the file paths from the output
$createdFile = ($output -split "`n" | Select-String "CrearArchivo").ToString().Trim()
$generatedImage = ($output -split "`n" | Select-String "GenerarImagen").ToString().Trim()

# Check if the files were created
if (-not (Test-Path $createdFile)) {
    Write-Error "Created file does not exist: $createdFile"
    exit 1
}

if (-not (Test-Path $generatedImage)) {
    Write-Error "Generated image does not exist: $generatedImage"
    exit 1
}

Write-Host "All tests for pyqr.vbs passed successfully"
