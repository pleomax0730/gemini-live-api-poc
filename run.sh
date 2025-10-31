#!/bin/bash
# Quick start script for Hotel Agent Center

echo "🏨 Hotel Agent Center - Starting..."
echo ""

# Check if frontend is built
if [ ! -d "frontend/dist" ]; then
    echo "📦 Building frontend..."
    cd frontend
    npm run build
    cd ..
    echo "✅ Frontend built"
    echo ""
fi

# Start backend server
echo "🚀 Starting backend server..."
echo "📍 App will be available at: http://localhost:8081"
echo "💡 Press Ctrl+C to stop"
echo ""

cd backend
uv run backend.py

