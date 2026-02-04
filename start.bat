@echo off
echo [INFO] Starting Smart Knowledge Hub...

:: Check if containers are running
docker compose ps | findstr "Up" >nul
if %errorlevel% neq 0 (
    echo [INFO] Containers are not running. Starting them...
    docker compose up -d
    if %errorlevel% neq 0 (
         docker-compose up -d
    )
) else (
    echo [INFO] Containers are already running.
)

:: Wait for a moment to ensure services are ready
timeout /t 3 /nobreak >nul

:: Open browser
echo [INFO] Opening application in browser...
start http://localhost:8501

echo [SUCCESS] Application started!
pause
