@echo off
REM Quick start script for Hotel Agent Center (Windows)

echo 🏨 Hotel Agent Center - Starting...
echo.

REM Check if frontend is built
if not exist "dist" (
    echo 📦 Building frontend...
    call npm run build
    echo ✅ Frontend built
    echo.
)

REM Start backend server
echo 🚀 Starting backend server...
echo 📍 App will be available at: http://localhost:8081
echo 💡 Press Ctrl+C to stop
echo.

uv run backend_simple.py

