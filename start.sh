#!/bin/bash

echo "[INFO] Starting Smart Knowledge Hub..."

# Start containers if not running
echo "[INFO] Ensuring containers are up..."
if docker compose version &> /dev/null; then
    docker compose up -d
elif command -v docker-compose &> /dev/null; then
    docker-compose up -d
else
    echo "[ERROR] Docker Compose not found."
    exit 1
fi

# Wait for a moment
sleep 3

# Open browser (Linux/Mac support)
echo "[INFO] Opening application in browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501
elif command -v open &> /dev/null; then
    open http://localhost:8501
else
    echo "[INFO] Please open http://localhost:8501 in your browser."
fi

echo "[SUCCESS] Application started!"
