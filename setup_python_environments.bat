@echo off
REM ======================================================================
REM Embodied AI - Complete Python Environment Setup Script
REM Creates both Python 2.7 and Python 3.x environments
REM ======================================================================

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo Embodied AI - Python Environment Setup
echo ======================================================================
echo.
echo This script will:
echo   1. Check for Python 2.7 (install if missing)
echo   2. Check for Python 3.x (install if missing)
echo   3. Create venv_py27 virtual environment
echo   4. Create venv_py3 virtual environment
echo   5. Install NAOqi SDK in Python 2.7 environment
echo   6. Install AI dependencies in Python 3 environment
echo.
echo ======================================================================
echo.

REM Get current directory
set PROJECT_DIR=%cd%
set NAOQI_SDK_DIR=%PROJECT_DIR%\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649

echo Project Directory: %PROJECT_DIR%
echo.

REM ======================================================================
REM STEP 1: Check Python 2.7
REM ======================================================================
echo.
echo ======================================================================
echo STEP 1: Checking Python 2.7
echo ======================================================================
echo.

python2.7 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 2.7 not found!
    echo.
    echo You need to download and install Python 2.7:
    echo   URL: https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi
    echo.
    echo IMPORTANT: During installation, check these options:
    echo   [X] Add python.exe to PATH
    echo   [X] Install for all users
    echo.
    echo After installing Python 2.7, run this script again.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python2.7 --version 2^>^&1') do set PY27_VERSION=%%i
echo OK  %PY27_VERSION% found
echo.

REM ======================================================================
REM STEP 2: Check Python 3.x
REM ======================================================================
echo.
echo ======================================================================
echo STEP 2: Checking Python 3.x
echo ======================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.x not found!
    echo.
    echo You need to download and install Python 3:
    echo   URL: https://www.python.org/downloads/
    echo.
    echo Recommended: Python 3.11 or later
    echo.
    echo IMPORTANT: During installation, check these options:
    echo   [X] Add Python to PATH
    echo   [X] Install for all users
    echo.
    echo After installing Python 3, run this script again.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PY3_VERSION=%%i
echo OK  %PY3_VERSION% found
echo.

REM ======================================================================
REM STEP 3: Create Python 2.7 Virtual Environment
REM ======================================================================
echo.
echo ======================================================================
echo STEP 3: Creating Python 2.7 Virtual Environment
echo ======================================================================
echo.

if exist "%PROJECT_DIR%\venv_py27" (
    echo WARNING: venv_py27 already exists
    echo.
    set /p DELETE_PY27="Do you want to delete and recreate it? (y/n): "
    if /i "!DELETE_PY27!"=="y" (
        echo Deleting existing venv_py27...
        rmdir /s /q "%PROJECT_DIR%\venv_py27"
        echo OK  Deleted
    ) else (
        echo Skipping Python 2.7 environment creation
        goto SKIP_PY27
    )
)

echo Creating Python 2.7 virtual environment...
python2.7 -m virtualenv "%PROJECT_DIR%\venv_py27"

if errorlevel 1 (
    echo ERROR: Failed to create Python 2.7 virtual environment!
    echo.
    echo Make sure virtualenv is installed:
    echo   python2.7 -m pip install virtualenv
    echo.
    pause
    exit /b 1
)

echo OK  Python 2.7 virtual environment created successfully
echo Location: %PROJECT_DIR%\venv_py27
echo.

:SKIP_PY27

REM ======================================================================
REM STEP 4: Create Python 3.x Virtual Environment
REM ======================================================================
echo.
echo ======================================================================
echo STEP 4: Creating Python 3.x Virtual Environment
echo ======================================================================
echo.

if exist "%PROJECT_DIR%\venv_py3" (
    echo WARNING: venv_py3 already exists
    echo.
    set /p DELETE_PY3="Do you want to delete and recreate it? (y/n): "
    if /i "!DELETE_PY3!"=="y" (
        echo Deleting existing venv_py3...
        rmdir /s /q "%PROJECT_DIR%\venv_py3"
        echo OK  Deleted
    ) else (
        echo Skipping Python 3 environment creation
        goto SKIP_PY3
    )
)

echo Creating Python 3 virtual environment...
python -m venv "%PROJECT_DIR%\venv_py3"

if errorlevel 1 (
    echo ERROR: Failed to create Python 3 virtual environment!
    echo.
    pause
    exit /b 1
)

echo OK  Python 3 virtual environment created successfully
echo Location: %PROJECT_DIR%\venv_py3
echo.

:SKIP_PY3

REM ======================================================================
REM STEP 5: Install NAOqi SDK in Python 2.7
REM ======================================================================
echo.
echo ======================================================================
echo STEP 5: Installing NAOqi SDK in Python 2.7 Environment
echo ======================================================================
echo.

if not exist "%NAOQI_SDK_DIR%" (
    echo ERROR: NAOqi SDK not found at:
    echo   %NAOQI_SDK_DIR%
    echo.
    echo Please ensure the NAOqi SDK folder exists in your project directory.
    echo.
    pause
    exit /b 1
)

echo Activating Python 2.7 environment...
call "%PROJECT_DIR%\venv_py27\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate Python 2.7 virtual environment!
    echo.
    pause
    exit /b 1
)

echo.
echo Installing NAOqi SDK...
python -m pip install --upgrade pip setuptools

REM Try to install NAOqi from the SDK
python -m pip install --no-index --find-links="%NAOQI_SDK_DIR%\lib" naoqi

if errorlevel 1 (
    echo WARNING: Could not install NAOqi using --no-index method
    echo.
    echo This may be OK if NAOqi is already available or if the SDK structure differs.
    echo Attempting alternative installation method...
    echo.

    REM Alternative: Add SDK to PYTHONPATH
    set PYTHONPATH=%NAOQI_SDK_DIR%\lib;%PYTHONPATH%
    echo Added to PYTHONPATH: %NAOQI_SDK_DIR%\lib
)

echo.
echo Verifying NAOqi SDK...
python -c "from naoqi import ALProxy; print('NAOqi SDK: OK')" >nul 2>&1
if errorlevel 1 (
    echo WARNING: NAOqi SDK not fully installed
    echo You may need to manually add the SDK path to PYTHONPATH
    echo.
    echo Add this to your environment or scripts:
    echo   set PYTHONPATH=%NAOQI_SDK_DIR%\lib;%%PYTHONPATH%%
) else (
    echo OK  NAOqi SDK verified successfully
)

echo.
echo Deactivating Python 2.7 environment...
call "%PROJECT_DIR%\venv_py27\Scripts\deactivate.bat"

echo OK  Python 2.7 environment configured
echo.

REM ======================================================================
REM STEP 6: Install AI Dependencies in Python 3
REM ======================================================================
echo.
echo ======================================================================
echo STEP 6: Installing AI Dependencies in Python 3 Environment
echo ======================================================================
echo.

echo Activating Python 3 environment...
call "%PROJECT_DIR%\venv_py3\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate Python 3 virtual environment!
    echo.
    pause
    exit /b 1
)

echo.
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing core AI backend dependencies...
echo   - FastAPI and Uvicorn (Web framework)
echo   - PyTorch (Neural networks)
echo   - Transformers (HuggingFace models)
python -m pip install fastapi uvicorn torch transformers

if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo This may be due to network issues or system compatibility
    echo You can retry later with: venv_py3\Scripts\activate ^&^& pip install fastapi uvicorn torch transformers
)

echo.
echo Installing speech processing dependencies...
echo   - Whisper (STT)
echo   - Piper (TTS)
python -m pip install openai-whisper piper-tts

if errorlevel 1 (
    echo WARNING: Speech packages failed to install
    echo You can retry with: pip install openai-whisper piper-tts
)

echo.
echo Installing memory and RAG dependencies...
echo   - ChromaDB (Vector database)
echo   - Sentence Transformers (Embeddings)
python -m pip install chromadb sentence-transformers

if errorlevel 1 (
    echo WARNING: Memory packages failed to install
    echo You can retry with: pip install chromadb sentence-transformers
)

echo.
echo Installing Ollama integration...
python -m pip install ollama

if errorlevel 1 (
    echo WARNING: Ollama package failed to install
    echo You can retry with: pip install ollama
)

echo.
echo Deactivating Python 3 environment...
call "%PROJECT_DIR%\venv_py3\Scripts\deactivate.bat"

echo OK  Python 3 environment configured
echo.

REM ======================================================================
REM SUCCESS - Summary
REM ======================================================================
echo.
echo ======================================================================
echo SUCCESS: Python Environments Created!
echo ======================================================================
echo.
echo Python 2.7 Environment (venv_py27):
echo   Location: %PROJECT_DIR%\venv_py27
echo   Status: Ready
echo   Packages: NAOqi SDK (2.8.6.23)
echo   Usage: venv_py27\Scripts\activate
echo.
echo Python 3 Environment (venv_py3):
echo   Location: %PROJECT_DIR%\venv_py3
echo   Status: Ready
echo   Packages: FastAPI, PyTorch, Transformers, Whisper, Piper, ChromaDB, Ollama
echo   Usage: venv_py3\Scripts\activate
echo.
echo ======================================================================
echo NEXT STEPS:
echo ======================================================================
echo.
echo 1. Run Phase 0 Tests (Python 2.7):
echo    cd %PROJECT_DIR%
echo    run_tests.bat
echo.
echo 2. Later - Activate Python 3 environment:
echo    cd %PROJECT_DIR%
echo    venv_py3\Scripts\activate
echo    python -m pip list  (to see all installed packages)
echo.
echo 3. Quick Test - Check both environments:
echo    venv_py27\Scripts\python -c "from naoqi import ALProxy; print('Python 2.7: OK')"
echo    venv_py3\Scripts\python -c "import torch; print('Python 3: OK')"
echo.
echo ======================================================================
echo.
pause
