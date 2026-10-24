@echo off
setlocal
cd /d "%~dp0"
title Sand Battery Studio
echo ====================================
echo   Sand Battery Studio - Local Start
echo ====================================
echo.
where py >nul 2>nul
if errorlevel 1 (
 echo ERROR: Windows Python launcher not found. Install Python 3.13.
 goto :failure
)
py -3.13 --version >nul 2>nul
if errorlevel 1 (
 echo ERROR: Python 3.13 not found. Install Python 3.13.
 goto :failure
)
if not exist ".venv\Scripts\python.exe" (
 echo [1/3] Creating virtual environment...
 py -3.13 -m venv .venv
 if errorlevel 1 goto :failure
 echo [2/3] Installing dependencies (first run only)...
 ".venv\Scripts\python.exe" -m pip install -r requirements.txt
 if errorlevel 1 goto :failure
) else (
 echo [1/3] Reusing existing environment.
 echo [2/3] Dependencies assumed installed; see README to update them.
)
echo [3/3] Starting application...
".venv\Scripts\python.exe" -m streamlit run streamlit_app.py
if errorlevel 1 goto :failure
exit /b 0
:failure
echo.
echo Startup failed. Check the error message above.
pause
exit /b 1
