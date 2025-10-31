#!/bin/bash
# Quick start script for Hotel Agent Center

echo "🏨 Hotel Agent Center - Starting..."
echo ""

# Check if frontend is built
if [ ! -d "dist" ]; then
    echo "📦 Building frontend..."
    npm run build
    echo "✅ Frontend built"
    echo ""
fi

# Start backend server
echo "🚀 Starting backend server..."
echo "📍 App will be available at: http://localhost:8080"
echo "💡 Press Ctrl+C to stop"
echo ""

uv run backend_simple.py

