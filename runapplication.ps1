Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Starting Personal Knowledge Graph System" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

Write-Host "Starting Backend Server on http://localhost:8000 ..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "call env\Scripts\activate.bat && python main.py"

Write-Host "Starting Frontend Dev Server on http://localhost:3000 ..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd frontend && npm start"

Write-Host "`n=========================================================" -ForegroundColor Cyan
Write-Host "Applications launched in separate windows:" -ForegroundColor Cyan
Write-Host "- Frontend UI:    http://localhost:3000" -ForegroundColor Yellow
Write-Host "- Backend API:    http://localhost:8000" -ForegroundColor Yellow
Write-Host "- Swagger Docs:   http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "- OpenAPI Schema: http://localhost:8000/openapi.json" -ForegroundColor Yellow
Write-Host "=========================================================" -ForegroundColor Cyan
