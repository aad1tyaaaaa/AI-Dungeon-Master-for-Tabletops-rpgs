# AI Dungeon Master - Windows Setup Guide

## Prerequisites Check

### 1. Check Python Installation
Open Command Prompt (Win+R, type `cmd`, press Enter) and run:
```cmd
where python
```

If Python is not found:
- Download Python from https://python.org/downloads/
- **Important**: During installation, check "Add Python to PATH"
- Restart Command Prompt after installation

### 2. Verify Python Installation
```cmd
python --version
pip --version
```

## Installation Steps

### Method 1: Using Python Directly
```cmd
python -m pip install -r requirements.txt
```

### Method 2: Using Full Path
If Python is installed but not in PATH, find Python location:
```cmd
where python
```
Then use full path:
```cmd
"C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt
```

### Method 3: Using Windows Store Python
```cmd
py -m pip install -r requirements.txt
```

### Method 4: Using VS Code Terminal
1. Open VS Code
2. Press Ctrl+` (backtick) to open terminal
3. Run:
```cmd
python -m pip install -r requirements.txt
```

## Alternative Installation Methods

### Using Anaconda/Miniconda
1. Install Anaconda from https://anaconda.com
2. Open Anaconda Prompt
3. Navigate to project folder:
```cmd
cd "C:\Users\aadit\Documents\vs code\ai dungeon master for tabletops rpgs"
```
4. Run:
```cmd
conda install pip
pip install -r requirements.txt
```

### Using Windows PowerShell
1. Right-click Start button → Windows PowerShell (Admin)
2. Run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m pip install -r requirements.txt
```

## Troubleshooting

### Python Not Found
1. **Check Python installation**:
   - Go to Settings → Apps → Apps & features
   - Search for "Python"
   - If not found, install from python.org

2. **Add Python to PATH manually**:
   - Search "Environment Variables" in Windows
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "User variables", find "Path", click "Edit"
   - Add Python installation path (usually `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\`)

### pip Not Found
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Permission Issues
```cmd
python -m pip install --user -r requirements.txt
```

## Quick Start Commands

Once Python is properly installed:
```cmd
# Navigate to project folder
cd "C:\Users\aadit\Documents\vs code\ai dungeon master for tabletops rpgs"

# Install dependencies
python -m pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env file with your Gemini API key
# IMPORTANT: Use a valid Gemini API key to avoid API_KEY_INVALID errors

# Test setup
python test_setup.py

# Start game
python main.py
```

## Verification Commands
```cmd
python --version
pip --version
python -c "import sys; print(sys.executable)"
```

## Need Help?
- Check Python installation: https://docs.python.org/3/using/windows.html
- Microsoft Store Python: https://aka.ms/python
- VS Code Python setup: https://code.visualstudio.com/docs/python/python-tutorial
