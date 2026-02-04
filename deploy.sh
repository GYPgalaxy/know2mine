#!/bin/bash

echo "[INFO] Starting deployment process..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if .env exists, if not, copy from example
if [ ! -f .env ]; then
    echo "[INFO] .env not found. Creating from .env.example..."
    cp .env.example .env
    echo "[WARNING] Please edit .env file to configure your API keys and other settings."
    sleep 5
fi

# Build and start containers
echo "[INFO] Building and starting Docker containers..."
docker-compose up -d --build

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to deploy containers."
    exit 1
fi

echo "[SUCCESS] Deployment completed!"
echo "[INFO] Web App: http://localhost:8501"
