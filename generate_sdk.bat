@echo off
echo ===================================================
echo Generating Python SDK using OpenAPI Generator CLI
echo ===================================================

REM Ensure openapi-generator-cli is installed
call npx --yes @openapitools/openapi-generator-cli generate -i openapi.json -g python -o knowledge_sdk --additional-properties=packageName=knowledge_sdk,projectName=knowledge_sdk

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] SDK generation failed. Please check if Java is installed and in PATH.
    exit /b %ERRORLEVEL%
)

echo.
echo Python SDK successfully generated into knowledge_sdk/ folder!
