@echo off
echo =========================================================
echo Starting Personal Knowledge Graph System
echo =========================================================

echo Starting Backend Server on http://localhost:8000 ...
start "Knowledge Graph Backend" cmd /k "call env\Scripts\activate.bat && python main.py"

echo Starting Frontend Dev Server on http://localhost:3000 ...
start "Knowledge Graph Frontend" cmd /k "cd frontend && npm start"

echo.
echo =========================================================
echo Applications launched in separate windows:
echo - Frontend UI:    http://localhost:3000
echo - Backend API:    http://localhost:8000
echo - Swagger Docs:   http://localhost:8000/docs
echo - OpenAPI Schema: http://localhost:8000/openapi.json
echo =========================================================
