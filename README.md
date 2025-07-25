it is securit and system check bot with python



to run the bot on cmd use 

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



to run with python 


import os
import subprocess
import requests

REPO_URL = "https://github.com/Tadelachewu/SecurityBotSystem.git"
REPO_DIR = "SecurityBotSystem"

# Clone the repo if not already cloned
if not os.path.exists(REPO_DIR):
    print("Cloning repo...")
    subprocess.run(["git", "clone", REPO_URL])
else:
    print("Repo already exists.")

# Run the bot or script inside
script_path = os.path.join(REPO_DIR, "securityBot.py")
if os.path.exists(script_path):
    print("Running the bot...")
    subprocess.run(["python", script_path])
else:
    print("No 'securityBot.py' found in the repo.")




to run on linux systems 


#!/bin/bash

REPO_URL="https://github.com/Tadelachewu/SecurityBotSystem.git"
REPO_NAME="SecurityBotSystem"

echo
echo "=== Security Bot Launcher (Linux) ==="
echo

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed. Please install it with:"
    echo "sudo apt install git"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed. Please install it with:"
    echo "sudo apt install python3"
    exit 1
fi

# Clone the repo if not already present
if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL"
else
    echo "Repository already exists. Skipping clone."
fi

# Navigate to the repo folder
cd "$REPO_NAME" || {
    echo "[ERROR] Could not enter directory $REPO_NAME"
    exit 1
}

# Run the script
if [ -f "securityBot.py" ]; then
    echo "Running securityBot.py..."
    python3 securityBot.py
else
    echo "[ERROR] securityBot.py not found in the repository."
    exit 1
fi



then 


chmod +x security_bot_launcher.sh



then


./security_bot_launcher.sh
