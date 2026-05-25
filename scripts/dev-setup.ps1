param(
    [string]$PythonVersion = "3.12",
    [switch]$SkipMigrate
)

$ErrorActionPreference = "Stop"

function Invoke-External {
    param(
        [scriptblock]$Command,
        [string]$FailureMessage
    )

    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw $FailureMessage
    }
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv is required for this setup script. Install uv, then rerun scripts/dev-setup.ps1."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating .venv with Python $PythonVersion..."
    Invoke-External { uv venv --python $PythonVersion .venv } "Failed to create .venv."
}

$pythonExe = ".\.venv\Scripts\python.exe"

Write-Host "Installing dependencies..."
Invoke-External { uv pip install --python .venv -r requirements.txt } "Failed to install dependencies."

if (-not (Test-Path ".env.local")) {
    if (-not (Test-Path ".env.local.example")) {
        throw ".env.local.example was not found."
    }
    Copy-Item ".env.local.example" ".env.local"
    Write-Host "Created .env.local from template."
}

if (-not $SkipMigrate) {
    Write-Host "Applying migrations..."
    Invoke-External { & $pythonExe manage.py migrate } "Failed to run migrations."
}

Write-Host ""
Write-Host "Local development environment is ready."
Write-Host "Start server with: .\.venv\Scripts\python.exe manage.py runserver"
