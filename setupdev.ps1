Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Setting Up Development Environment (PowerShell)" -ForegroundColor Cyan
Write-Host "Personal Knowledge Graph System" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion found." -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js $nodeVersion found." -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# 1. Create venv
Write-Host "`n[1/5] Creating Python virtual environment (env)..." -ForegroundColor Yellow
if (-not (Test-Path "env")) {
    python -m venv env
}

# 2. Install requirements
Write-Host "[2/5] Installing backend requirements..." -ForegroundColor Yellow
& ".\env\Scripts\pip.exe" install -r requirements.txt
& ".\env\Scripts\pip.exe" install -e ./knowledge_sdk

# 3. Alembic migrations
Write-Host "[3/5] Running Alembic database migrations..." -ForegroundColor Yellow
& ".\env\Scripts\alembic.exe" upgrade head

# 4. Seed data
Write-Host "[4/5] Loading seed data (optional)..." -ForegroundColor Yellow
$loadSeed = Read-Host "Would you like to load demo seed data? (y/N, default: N)"
if ($loadSeed -match "^[yY]$") {
    & ".\env\Scripts\python.exe" scripts/load_seed.py
} else {
    Write-Host "Starting with clean empty database." -ForegroundColor Gray
}

# 5. Frontend dependencies
Write-Host "[5/5] Installing frontend npm dependencies..." -ForegroundColor Yellow
Set-Location frontend
cmd /c npm install
Set-Location ..

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Run '.\runapplication.ps1' or '.\runapplication.bat' to start the app." -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
