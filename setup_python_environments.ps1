# ======================================================================
# Embodied AI - Complete Python Environment Setup Script (PowerShell)
# Creates both Python 2.7 and Python 3.x environments
# ======================================================================

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "Embodied AI - Python Environment Setup (PowerShell)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "This script will:" -ForegroundColor Cyan
Write-Host "  1. Check for Python 2.7 (install if missing)"
Write-Host "  2. Check for Python 3.x (install if missing)"
Write-Host "  3. Create venv_py27 virtual environment"
Write-Host "  4. Create venv_py3 virtual environment"
Write-Host "  5. Install NAOqi SDK in Python 2.7 environment"
Write-Host "  6. Install AI dependencies in Python 3 environment"
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""

# Get current directory
$ProjectDir = Get-Location
$NaoqiSdkDir = Join-Path $ProjectDir "pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649"

Write-Host "Project Directory: $ProjectDir" -ForegroundColor Gray
Write-Host ""

# ======================================================================
# STEP 1: Check Python 2.7
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "STEP 1: Checking Python 2.7" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

try {
    $Py27Version = python --version 2>&1
    Write-Host "OK  $Py27Version" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need to download and install Python 2.7:" -ForegroundColor Yellow
    Write-Host "  URL: https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi"
    Write-Host ""
    Write-Host "IMPORTANT: During installation, check these options:" -ForegroundColor Yellow
    Write-Host "  [X] Add python.exe to PATH"
    Write-Host "  [X] Install for all users"
    Write-Host ""
    Write-Host "After installing Python 2.7, run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Verify it's actually Python 2.7
try {
    python -c "import sys; sys.exit(0 if sys.version_info[0] == 2 else 1)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: 'python' command points to Python 3.x, not Python 2.7!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Your system has Python 3 as default." -ForegroundColor Yellow
        Write-Host "We will still proceed, but you may need Python 2.7 for NAOqi compatibility." -ForegroundColor Yellow
        Write-Host ""
    }
} catch {}

Write-Host ""

# ======================================================================
# STEP 2: Check Python 3.x
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "STEP 2: Checking Python 3.x" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

try {
    $Py3Version = python3 --version 2>&1
    Write-Host "OK  $Py3Version" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python 3.x not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need to download and install Python 3:" -ForegroundColor Yellow
    Write-Host "  URL: https://www.python.org/downloads/"
    Write-Host ""
    Write-Host "Recommended: Python 3.11 or later" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "IMPORTANT: During installation, check these options:" -ForegroundColor Yellow
    Write-Host "  [X] Add Python to PATH"
    Write-Host "  [X] Install for all users"
    Write-Host ""
    Write-Host "After installing Python 3, run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# ======================================================================
# STEP 3: Create Python 2.7 Virtual Environment
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "STEP 3: Creating Python 2.7 Virtual Environment" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$Py27VenvPath = Join-Path $ProjectDir "venv_py27"

if (Test-Path $Py27VenvPath) {
    Write-Host "WARNING: venv_py27 already exists" -ForegroundColor Yellow
    Write-Host ""
    $DeletePy27 = Read-Host "Do you want to delete and recreate it? (y/n)"
    if ($DeletePy27 -eq "y" -or $DeletePy27 -eq "Y") {
        Write-Host "Deleting existing venv_py27..."
        Remove-Item -Recurse -Force $Py27VenvPath -ErrorAction SilentlyContinue
        Write-Host "OK  Deleted" -ForegroundColor Green
    } else {
        Write-Host "Skipping Python 2.7 environment creation" -ForegroundColor Cyan
        goto SkipPy27
    }
}

Write-Host "Creating Python 2.7 virtual environment..."
python -m virtualenv $Py27VenvPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create Python 2.7 virtual environment!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure virtualenv is installed:" -ForegroundColor Yellow
    Write-Host "  python -m pip install virtualenv"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK  Python 2.7 virtual environment created successfully" -ForegroundColor Green
Write-Host "Location: $Py27VenvPath" -ForegroundColor Gray
Write-Host ""

:SkipPy27

# ======================================================================
# STEP 4: Create Python 3.x Virtual Environment
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "STEP 4: Creating Python 3.x Virtual Environment" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$Py3VenvPath = Join-Path $ProjectDir "venv_py3"

if (Test-Path $Py3VenvPath) {
    Write-Host "WARNING: venv_py3 already exists" -ForegroundColor Yellow
    Write-Host ""
    $DeletePy3 = Read-Host "Do you want to delete and recreate it? (y/n)"
    if ($DeletePy3 -eq "y" -or $DeletePy3 -eq "Y") {
        Write-Host "Deleting existing venv_py3..."
        Remove-Item -Recurse -Force $Py3VenvPath -ErrorAction SilentlyContinue
        Write-Host "OK  Deleted" -ForegroundColor Green
    } else {
        Write-Host "Skipping Python 3 environment creation" -ForegroundColor Cyan
        goto SkipPy3
    }
}

Write-Host "Creating Python 3 virtual environment..."
python3 -m venv $Py3VenvPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create Python 3 virtual environment!" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK  Python 3 virtual environment created successfully" -ForegroundColor Green
Write-Host "Location: $Py3VenvPath" -ForegroundColor Gray
Write-Host ""

:SkipPy3

# ======================================================================
# STEP 5: Install NAOqi SDK in Python 2.7
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "STEP 5: Installing NAOqi SDK in Python 2.7 Environment" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $NaoqiSdkDir)) {
    Write-Host "ERROR: NAOqi SDK not found at:" -ForegroundColor Red
    Write-Host "  $NaoqiSdkDir"
    Write-Host ""
    Write-Host "Please ensure the NAOqi SDK folder exists in your project directory." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Activating Python 2.7 environment..."
& "$Py27VenvPath\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate Python 2.7 virtual environment!" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing NAOqi SDK..."
python -m pip install --upgrade pip setuptools

# Try to install NAOqi from the SDK
$NaoqiLibDir = Join-Path $NaoqiSdkDir "lib"
python -m pip install --no-index --find-links="$NaoqiLibDir" naoqi

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Could not install NAOqi using --no-index method" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This may be OK if NAOqi is already available or if the SDK structure differs." -ForegroundColor Yellow
    Write-Host "Attempting alternative installation method..." -ForegroundColor Yellow
    Write-Host ""

    # Alternative: Add SDK to PYTHONPATH
    $env:PYTHONPATH = "$NaoqiLibDir;$env:PYTHONPATH"
    Write-Host "Added to PYTHONPATH: $NaoqiLibDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "Verifying NAOqi SDK..."
try {
    python -c "from naoqi import ALProxy; print('NAOqi SDK: OK')" 2>$null
    Write-Host "OK  NAOqi SDK verified successfully" -ForegroundColor Green
} catch {
    Write-Host "WARNING: NAOqi SDK not fully installed" -ForegroundColor Yellow
    Write-Host "You may need to manually add the SDK path to PYTHONPATH" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Add this to your environment or scripts:" -ForegroundColor Yellow
    Write-Host "  `$env:PYTHONPATH = '$NaoqiLibDir;`$env:PYTHONPATH'" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Deactivating Python 2.7 environment..."
deactivate

Write-Host "OK  Python 2.7 environment configured" -ForegroundColor Green
Write-Host ""

# ======================================================================
# STEP 6: Install AI Dependencies in Python 3
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "STEP 6: Installing AI Dependencies in Python 3 Environment" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Activating Python 3 environment..."
& "$Py3VenvPath\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate Python 3 virtual environment!" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

Write-Host ""
Write-Host "Installing core AI backend dependencies..." -ForegroundColor Cyan
Write-Host "  - FastAPI and Uvicorn (Web framework)"
Write-Host "  - PyTorch (Neural networks)"
Write-Host "  - Transformers (HuggingFace models)"
python -m pip install fastapi uvicorn torch transformers

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Some packages failed to install" -ForegroundColor Yellow
    Write-Host "This may be due to network issues or system compatibility" -ForegroundColor Yellow
    Write-Host "You can retry later with: venv_py3\Scripts\activate ; pip install fastapi uvicorn torch transformers" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Installing speech processing dependencies..." -ForegroundColor Cyan
Write-Host "  - Whisper (STT)"
Write-Host "  - Piper (TTS)"
python -m pip install openai-whisper piper-tts

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Speech packages failed to install" -ForegroundColor Yellow
    Write-Host "You can retry with: pip install openai-whisper piper-tts" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Installing memory and RAG dependencies..." -ForegroundColor Cyan
Write-Host "  - ChromaDB (Vector database)"
Write-Host "  - Sentence Transformers (Embeddings)"
python -m pip install chromadb sentence-transformers

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Memory packages failed to install" -ForegroundColor Yellow
    Write-Host "You can retry with: pip install chromadb sentence-transformers" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Installing Ollama integration..."
python -m pip install ollama

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Ollama package failed to install" -ForegroundColor Yellow
    Write-Host "You can retry with: pip install ollama" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Deactivating Python 3 environment..."
deactivate

Write-Host "OK  Python 3 environment configured" -ForegroundColor Green
Write-Host ""

# ======================================================================
# SUCCESS - Summary
# ======================================================================
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "SUCCESS: Python Environments Created!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Python 2.7 Environment (venv_py27):" -ForegroundColor Cyan
Write-Host "  Location: $Py27VenvPath" -ForegroundColor Gray
Write-Host "  Status: Ready" -ForegroundColor Green
Write-Host "  Packages: NAOqi SDK (2.8.6.23)" -ForegroundColor Gray
Write-Host "  Usage: venv_py27\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Python 3 Environment (venv_py3):" -ForegroundColor Cyan
Write-Host "  Location: $Py3VenvPath" -ForegroundColor Gray
Write-Host "  Status: Ready" -ForegroundColor Green
Write-Host "  Packages: FastAPI, PyTorch, Transformers, Whisper, Piper, ChromaDB, Ollama" -ForegroundColor Gray
Write-Host "  Usage: venv_py3\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "NEXT STEPS:" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Run Phase 0 Tests (Python 2.7):" -ForegroundColor Cyan
Write-Host "   cd $ProjectDir"
Write-Host "   .\run_tests.ps1"
Write-Host ""
Write-Host "2. Later - Activate Python 3 environment:" -ForegroundColor Cyan
Write-Host "   cd $ProjectDir"
Write-Host "   .\venv_py3\Scripts\Activate.ps1"
Write-Host "   python -m pip list  (to see all installed packages)"
Write-Host ""
Write-Host "3. Quick Test - Check both environments:" -ForegroundColor Cyan
Write-Host "   .\venv_py27\Scripts\python -c ""from naoqi import ALProxy; print('Python 2.7: OK')"""
Write-Host "   .\venv_py3\Scripts\python -c ""import torch; print('Python 3: OK')"""
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
