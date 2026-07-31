@echo off
TITLE ChatLens AI - Windows Server Automated Production Installer
COLOR 0A
echo =========================================================================
echo       CHATLENS AI - WINDOWS SERVER PRODUCTION AUTOMATED INSTALLER
echo =========================================================================
echo.
echo [1/4] Checking Python Environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python 3.11+ is not installed or not in PATH. Please install Python first.
    pause
    exit /b 1
)

echo [2/4] Installing Backend Python Dependencies...
pip install -r ..\backend\requirements.txt

echo [3/4] Building Frontend Production Web Bundle...
cd ..\frontend
call npm install
call npm run build
cd ..\deploy

echo [4/4] Registering ChatLens AI as NSSM Windows Service...
echo Executing Service Deployment PowerShell Script...
powershell -ExecutionPolicy Bypass -File nssm_service.ps1

echo =========================================================================
echo       CHATLENS AI SERVER DEPLOYMENT COMPLETE!
echo       Backend Service: http://localhost:8000
echo       Production Web App: http://localhost:5173
echo =========================================================================
pause
