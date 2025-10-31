@echo off
REM Quick start script for Hotel Agent Center (Windows)

echo Hotel Agent Center - Starting...
echo.

REM Check if frontend is built
if not exist "frontend\dist" (
    echo Building frontend...
    cd frontend
    call npm run build
    cd ..
    echo Frontend built successfully
    echo.
)

REM Start backend server
echo Starting backend server...
echo App will be available at: http://localhost:8081
echo Press Ctrl+C to stop
echo.

cd backend
uv run backend.py

