# Python Environment Setup Guide

Complete automated setup for both Python 2.7 and Python 3.x environments.

---

## 📋 Overview

Two setup scripts are provided:
- **Batch version:** `setup_python_environments.bat` (Command Prompt)
- **PowerShell version:** `setup_python_environments.ps1` (PowerShell)

Both scripts do the same thing:
1. ✅ Check for Python 2.7 (download if missing)
2. ✅ Check for Python 3.x (download if missing)
3. ✅ Create Python 2.7 virtual environment (venv_py27)
4. ✅ Create Python 3.x virtual environment (venv_py3)
5. ✅ Install NAOqi SDK in Python 2.7 environment
6. ✅ Install AI backend dependencies in Python 3 environment

---

## 🚀 Quick Start

### Option 1: Using Command Prompt (Batch)

```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
setup_python_environments.bat
```

### Option 2: Using PowerShell

```powershell
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
.\setup_python_environments.ps1
```

**Typical runtime:** 10-30 minutes (depending on internet speed)

---

## 📝 What the Scripts Do

### Step 1: Verify Python 2.7

**If found:**
```
OK  Python 2.7.18
```

**If not found:**
- Script will display download link
- You must download and install Python 2.7
- Re-run script after installation

**Download:** https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi

**Installation Requirements:**
- ✅ Check "Add python.exe to PATH"
- ✅ Check "Install for all users"

---

### Step 2: Verify Python 3.x

**If found:**
```
OK  Python 3.11.x
```

**If not found:**
- Script will display download link
- You must download and install Python 3
- Re-run script after installation

**Download:** https://www.python.org/downloads/

**Recommended:** Python 3.11 or later

**Installation Requirements:**
- ✅ Check "Add Python to PATH"
- ✅ Check "Install for all users"

---

### Step 3: Create Python 2.7 Virtual Environment

Creates: `venv_py27/`

```
C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\venv_py27\
├── Scripts/
│   ├── activate.bat
│   ├── python.exe
│   └── pip.exe
├── Lib/
└── Include/
```

**If exists from before:**
- Script will ask if you want to delete and recreate it
- Choose `y` to start fresh, `n` to skip

---

### Step 4: Create Python 3 Virtual Environment

Creates: `venv_py3/`

```
C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\venv_py3\
├── Scripts/
│   ├── activate.bat
│   ├── python.exe
│   └── pip.exe
├── Lib/
└── Include/
```

**If exists from before:**
- Script will ask if you want to delete and recreate it
- Choose `y` to start fresh, `n` to skip

---

### Step 5: Install NAOqi SDK (Python 2.7)

**What gets installed:**
- NAOqi module for Python 2.7
- Required for robot control

**Installed from:**
```
pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/lib/
```

**Verification:**
```
python -c "from naoqi import ALProxy; print('NAOqi SDK: OK')"
```

---

### Step 6: Install AI Dependencies (Python 3)

**What gets installed:**

**Core Backend:**
- ✅ FastAPI - Web framework
- ✅ Uvicorn - ASGI server

**Neural Networks:**
- ✅ PyTorch - Deep learning
- ✅ Transformers - HuggingFace models

**Speech:**
- ✅ OpenAI Whisper - Speech-to-Text
- ✅ Piper TTS - Text-to-Speech

**Memory & RAG:**
- ✅ ChromaDB - Vector database
- ✅ Sentence Transformers - Embeddings

**LLM Integration:**
- ✅ Ollama - Local LLM interface

---

## ✅ Success Criteria

### You'll see this if everything succeeded:

```
======================================================================
SUCCESS: Python Environments Created!
======================================================================

Python 2.7 Environment (venv_py27):
  Location: C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\venv_py27
  Status: Ready
  Packages: NAOqi SDK (2.8.6.23)
  Usage: venv_py27\Scripts\activate

Python 3 Environment (venv_py3):
  Location: C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\venv_py3
  Status: Ready
  Packages: FastAPI, PyTorch, Transformers, Whisper, Piper, ChromaDB, Ollama
  Usage: venv_py3\Scripts\activate

======================================================================
NEXT STEPS:
======================================================================

1. Run Phase 0 Tests (Python 2.7):
   cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
   run_tests.bat

2. Later - Activate Python 3 environment:
   cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
   venv_py3\Scripts\activate
   python -m pip list

3. Quick Test - Check both environments:
   venv_py27\Scripts\python -c "from naoqi import ALProxy; print('Python 2.7: OK')"
   venv_py3\Scripts\python -c "import torch; print('Python 3: OK')"
```

---

## 🔧 Troubleshooting

### "python2.7: command not found"

**Solution 1:** Check PATH
```bash
python2.7 --version
```

**Solution 2:** Install Python 2.7
- Download from: https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi
- During installation: ✅ Check "Add python.exe to PATH"
- Restart Command Prompt or PowerShell

**Solution 3:** Add to PATH manually
```bash
# Find where Python 2.7 is installed
where python2.7

# Example: C:\Python27\python.exe

# Add to PATH (Windows Settings → Environment Variables)
# Add: C:\Python27
```

---

### "python: command not found" (Python 3)

**Solution 1:** Install Python 3
- Download from: https://www.python.org/downloads/
- During installation: ✅ Check "Add Python to PATH"
- Restart Command Prompt or PowerShell

**Solution 2:** Check Python 3 installation
```bash
python --version
python -c "import sys; print(sys.version)"
```

---

### "Failed to create virtual environment"

**For Python 2.7:**
```bash
# Install virtualenv
python2.7 -m pip install virtualenv

# Then re-run setup script
setup_python_environments.bat
```

**For Python 3:**
```bash
# venv is built-in, but check if it's available
python -m venv --help

# If that fails, reinstall Python 3 with venv support
```

---

### NAOqi SDK not found

**Error message:**
```
ERROR: NAOqi SDK not found at: ...pynaoqi-python2.7-2.8.6.23-win64-vs2015...
```

**Solution:**
```
1. Check folder exists in project root:
   C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\

2. If missing, download from your NAO robot documentation
   or contact your NAO provider

3. Extract to project root
   
4. Re-run setup script
```

---

### "Failed to install packages"

**This is usually OK!** The script will continue. You can install missing packages later:

```bash
# Activate environment
venv_py3\Scripts\activate

# Install specific package
pip install fastapi
pip install torch
pip install openai-whisper

# Check what's installed
pip list
```

---

## 📊 Directory Structure After Setup

```
C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\
├── venv_py27/                    ← Python 2.7 environment
│   ├── Scripts/
│   │   ├── activate.bat
│   │   ├── python.exe
│   │   └── pip.exe
│   ├── Lib/
│   │   └── site-packages/
│   │       └── naoqi/            ← NAOqi SDK
│   └── Include/
│
├── venv_py3/                     ← Python 3 environment
│   ├── Scripts/
│   │   ├── Activate.ps1
│   │   ├── python.exe
│   │   └── pip.exe
│   ├── Lib/
│   │   └── site-packages/
│   │       ├── fastapi/
│   │       ├── torch/
│   │       ├── transformers/
│   │       ├── whisper/
│   │       ├── piper/
│   │       ├── chromadb/
│   │       └── ollama/
│   └── Include/
│
├── pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/
│   └── lib/
│       └── naoqi SDK (reference)
│
├── setup_python_environments.bat
├── setup_python_environments.ps1
├── run_tests.bat
├── run_tests.ps1
└── (other project files)
```

---

## 🎯 Using the Environments

### Activate Python 2.7 (for robot control)

**Batch:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
venv_py27\Scripts\activate
python run_all_tests_py27.py
venv_py27\Scripts\deactivate
```

**PowerShell:**
```powershell
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
.\venv_py27\Scripts\Activate.ps1
python run_all_tests_py27.py
deactivate
```

---

### Activate Python 3 (for AI backend)

**Batch:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
venv_py3\Scripts\activate
python -m pip list
python -m src.ai_backend.main
venv_py3\Scripts\deactivate
```

**PowerShell:**
```powershell
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
.\venv_py3\Scripts\Activate.ps1
python -m pip list
python -m src.ai_backend.main
deactivate
```

---

## 🚀 Next Steps

### After successful setup:

**1. Run Phase 0 Tests (Immediately)**
```bash
run_tests.bat
```

This will:
- ✅ Test NAOqi connectivity
- ✅ Test network stability
- ✅ Test robot sensors
- ✅ Generate report: `TEST_RESULTS_SUMMARY.txt`

---

**2. Later: AI Backend Development (Phase 3+)**

When you're ready to develop the AI backend:
```bash
venv_py3\Scripts\activate
pip list    # View all installed packages
python -c "import torch; print(torch.__version__)"
```

---

**3. Verify Both Work**

Quick test:
```bash
# Test Python 2.7 + NAOqi
venv_py27\Scripts\python -c "from naoqi import ALProxy; print('Python 2.7: OK')"

# Test Python 3 + PyTorch
venv_py3\Scripts\python -c "import torch; print('Python 3: OK')"
```

---

## 📞 Need Help?

**If the setup script fails:**

1. Read the error message carefully
2. Check the troubleshooting section above
3. Verify Python installations:
   ```bash
   python2.7 --version
   python --version
   ```
4. Check NAOqi SDK location:
   ```bash
   dir pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649
   ```
5. Re-run the setup script

**Common issues:**
- Python not in PATH → Restart terminal after Python installation
- NAOqi SDK missing → Check project root directory
- Package installation failed → Often OK, can install later with pip
- Permission denied → Run as Administrator (right-click → Run as administrator)

---

## ✨ Summary

| Step | Command | Duration |
|------|---------|----------|
| 1. Run setup | `setup_python_environments.bat` | 1 minute |
| 2. Install Python (if needed) | Download + Install | 10 minutes |
| 3. Create environments | Automatic | 2 minutes |
| 4. Install NAOqi | Automatic | 1 minute |
| 5. Install AI packages | Automatic | 10-20 minutes |
| **Total** | **All steps** | **15-30 minutes** |

---

**Status:** ✅ Ready to use

**Created:** 2026-06-13

**Scripts:** `setup_python_environments.bat` and `setup_python_environments.ps1`
