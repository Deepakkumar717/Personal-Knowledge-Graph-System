@echo off
echo =========================================================
echo Setting Up Development Environment
echo Personal Knowledge Graph System
echo =========================================================

REM Check Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.11+.
    pause
    exit /b 1
)

REM Check Node.js installation
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH. Please install Node.js 18+.
    pause
    exit /b 1
)

echo [1/5] Creating Python virtual environment (env)...
if not exist env (
    python -m venv env
)

echo [2/5] Activating virtual environment and installing backend requirements...
call env\Scripts\activate.bat
pip install -r requirements.txt
pip install -e ./knowledge_sdk

echo [3/5] Applying database migrations with Alembic...
alembic upgrade head

echo [4/5] Loading seed data (optional)...
set LOAD_SEED=n
set /p LOAD_SEED="Would you like to load demo seed data? (y/N, default: N): "
if /i "%LOAD_SEED%"=="y" (
    python scripts\load_seed.py
) else (
    echo Starting with clean empty database.
)

echo [5/5] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo =========================================================
echo Setup complete!
echo Run 'runapplication.bat' to start the Backend and Frontend.
echo =========================================================
