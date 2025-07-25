@echo off
set REPO_URL=https://github.com/Tadelachewu/SecurityBotSystem.git
set REPO_NAME=SecurityBotSystem

echo.
echo === Security Bot Launcher ===
echo.

:: Check if Git is installed
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed. Please install Git from https://git-scm.com and try again.
    pause
    exit /b
)

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python from https://python.org and try again.
    pause
    exit /b
)

:: Clone the repo if not already present
if not exist %REPO_NAME% (
    echo Cloning repository...
    git clone %REPO_URL%
) else (
    echo Repository already exists. Skipping clone.
)

:: Navigate to the repo folder
cd %REPO_NAME%

:: Check for main.py
if existsecurityBot.py (
    echo RunningsecurityBot.py...
    python main.py
) else (
    echo [ERROR] securityBot.py not found in the repository.
    pause
    exit /b
)

echo.
pause
