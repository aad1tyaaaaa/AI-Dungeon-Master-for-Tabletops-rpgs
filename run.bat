@echo off
echo AI Dungeon Master - Windows Launcher
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import langchain" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your OpenAI API key
    pause
)

REM Run the game
echo Starting AI Dungeon Master FastAPI server...
python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
