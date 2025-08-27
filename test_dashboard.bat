@echo off
echo ============================================================
echo    Safety Detection Dashboard - API Testing
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if requests is installed
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing requests for testing...
    pip install requests
)

echo Starting API tests...
echo Make sure the dashboard server is running first!
echo.

python test_api.py

echo.
echo Testing completed!
pause
