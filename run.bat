@echo off
REM Quick start script for Hotel Agent Center (Windows)

echo Hotel Agent Center - Starting...
echo.

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo.
)

REM Always rebuild frontend to ensure latest changes
echo Building frontend...
cd frontend
call npm run build
if errorlevel 1 (
    echo Frontend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo Frontend built successfully
echo.

REM Start backend server
echo Starting backend server...
echo App will be available at: http://localhost:8081
echo Press Ctrl+C to stop
echo.

cd backend
uv run backend.py

