@echo off
echo [INFO] Starting deployment process...

:: Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH. Please install Docker first.
    pause
    exit /b 1
)

:: Check if .env exists, if not, copy from example
if not exist .env (
    echo [INFO] .env not found. Creating from .env.example...
    copy .env.example .env
    echo [WARNING] Please edit .env file to configure your API keys and other settings.
    timeout /t 5
)

:: Build and start containers
echo [INFO] Building and starting Docker containers...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy containers.
    pause
    exit /b 1
)

echo [SUCCESS] Deployment completed!
echo [INFO] Web App: http://localhost:8501
pause
