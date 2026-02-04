#!/bin/bash

echo "[INFO] Starting Smart Knowledge Hub..."

# Start containers if not running
echo "[INFO] Ensuring containers are up..."
docker-compose up -d

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
