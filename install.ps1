# AI Dungeon Master - PowerShell Installation Script

Write-Host "AI Dungeon Master - Installation Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python from https://python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    pause
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to install dependencies. Error: $_" -ForegroundColor Red
    pause
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please edit .env file with your OpenAI API key" -ForegroundColor Yellow
}

# Test the setup
Write-Host "Testing setup..." -ForegroundColor Yellow
try {
    python test_setup.py
    Write-Host "Setup complete! Run 'python main.py' to start the game." -ForegroundColor Green
} catch {
    Write-Host "Setup test failed. Error: $_" -ForegroundColor Red
}

pause
