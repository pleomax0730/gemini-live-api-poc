@echo off
REM Development mode with hot reload

echo Hotel Agent Center - Development Mode
echo.

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo.
)

echo Starting development servers...
echo.
echo Frontend (Vite Dev): http://localhost:3000
echo Backend (API): http://localhost:8081
echo.
echo Press Ctrl+C to stop
echo.

REM Start both frontend dev server and backend in parallel
start "Frontend Dev Server" cmd /c "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

cd backend
uv run backend.py
