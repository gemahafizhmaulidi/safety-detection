@echo off
echo ============================================================
echo    Safety Detection Dashboard
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if model directory exists
if not exist "model" (
    echo WARNING: Model directory not found
    echo Please ensure your YOLO model files are in the 'model' folder
    echo.
)

REM Create uploads directory if it doesn't exist
if not exist "uploads" mkdir uploads

echo Starting Safety Detection Dashboard...
echo.
echo Dashboard will be available at: http://localhost:5000/static/index.html
echo Press Ctrl+C to stop the server
echo.

REM Run the dashboard
python run_dashboard.py

pause
