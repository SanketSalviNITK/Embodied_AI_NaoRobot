# Python Environment Setup Guide

**Question:** Do we need separate Python environments for Python 2.7 and Python 3.x?

**Answer:** **YES - Absolutely!** Here's why and how.

---

## 🎯 Why Separate Environments?

### The Problem with Mixed Python Versions

```
Python 2.7 (NAOqi)  ←→ Python 3.x (AI Backend)
     ↓                        ↓
  Old libraries          Modern libraries
  Different syntax       Different syntax
  Different packages     Different packages
```

**If mixed:** Compatibility issues, import errors, version conflicts

---

## 📋 Your Two Python Environments

### **Environment 1: Python 2.7 (Robot Control)**
```
Purpose: NAOqi communication, robot control, pre-Phase 0 tests
Uses:
  - NAOqi SDK 2.8.6.23
  - Robot bridge scripts
  - Motion control
  - Sensor reading
  - Pre-Phase 0 test suite

Location: C:\Python27\ (or wherever Python 2.7 is installed)
```

### **Environment 2: Python 3.x (AI Backend)**
```
Purpose: LLM, embeddings, web server, modern AI
Uses:
  - FastAPI (Python 3 only)
  - Torch/TensorFlow (Python 3)
  - Whisper, Piper (Python 3)
  - Ollama integration (Python 3)
  - ChromaDB (Python 3)
  - Frontend dashboard (Node.js)

Location: C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\venv_py3\
```

---

## 🛠️ Recommended Setup

### Option 1: Virtual Environments (RECOMMENDED) ✅

```
EmbodiedAI/
├── venv_py27/              ← Python 2.7 virtual environment
│   ├── Scripts/
│   ├── Lib/
│   └── (NAOqi SDK packages)
│
├── venv_py3/               ← Python 3.x virtual environment
│   ├── Scripts/
│   ├── Lib/
│   └── (FastAPI, Torch, etc.)
│
├── run_tests.bat           ← Uses venv_py27
├── run_backend.bat         ← Uses venv_py3
└── (project files)
```

**Advantages:**
- ✅ Isolated dependencies
- ✅ No version conflicts
- ✅ Can activate independently
- ✅ Easy to recreate
- ✅ Safe for collaboration

---

## 🚀 How to Set Up

### Step 1: Create Python 2.7 Virtual Environment

**Check if you have Python 2.7:**
```bash
python2.7 --version
```

**If you have it, create venv:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
python2.7 -m virtualenv venv_py27
```

**Activate it (Windows):**
```bash
venv_py27\Scripts\activate
```

**Install NAOqi SDK in venv:**
```bash
pip install --no-index --find-links=pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/lib naoqi
```

---

### Step 2: Create Python 3.x Virtual Environment

**Create it:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
python -m venv venv_py3
```

**Activate it (Windows):**
```bash
venv_py3\Scripts\activate
```

**Install AI backend dependencies:**
```bash
pip install fastapi uvicorn torch transformers
pip install openai-whisper piper-tts
pip install chromadb sentence-transformers
pip install ollama
```

---

## 📝 Updated Test Runner Script

### run_tests_with_venv.bat (Python 2.7)

```batch
@echo off
REM Activate Python 2.7 virtual environment and run tests

call venv_py27\Scripts\activate.bat

echo.
echo ======================================================================
echo NAOqi Python 2.7 Test Suite (Using Virtual Environment)
echo ======================================================================
echo.

python run_all_tests_py27.py

set TEST_RESULT=%ERRORLEVEL%
call venv_py27\Scripts\deactivate.bat

exit /b %TEST_RESULT%
```

### run_backend.bat (Python 3.x)

```batch
@echo off
REM Activate Python 3.x virtual environment and run backend

call venv_py3\Scripts\activate.bat

echo.
echo ======================================================================
echo Embodied AI Backend (Python 3.x)
echo ======================================================================
echo.

python -m src.ai_backend.main

call venv_py3\Scripts\deactivate.bat
```

---

## 🔄 How They Work Together

```
┌─────────────────────────────────────────────────────────────┐
│                    USER / DASHBOARD                         │
│               (Browser - http://localhost:3000)             │
└──────────────────┬────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
   HTTP │      REST│    WS    │ WebSocket
        │          │          │
        ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────┐
│          AI BACKEND (Python 3.x / venv_py3)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • FastAPI Server                                     │  │
│  │ • LLM (Mistral via Ollama)                          │  │
│  │ • Speech (Whisper STT, Piper TTS)                   │  │
│  │ • Memory & RAG (ChromaDB)                           │  │
│  │ • Gesture Controller                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│              TCP Socket │ (port 9559)                      │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │ Robot Bridge (Python 2.7 / venv_py27)              │  │
│  │                                                      │  │
│  │ • NAOqi Proxies                                    │  │
│  │ • Motion Commands                                  │  │
│  │ • Sensor Streaming                                │  │
│  │ • Audio I/O                                        │  │
│  └──────────────────────┬─────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                    NAOqi  │
                           │
                           ▼
                   ┌─────────────────┐
                   │  NAO ROBOT V4   │
                   │                 │
                   │ • Motors        │
                   │ • Sensors       │
                   │ • Audio I/O     │
                   │ • Cameras       │
                   └─────────────────┘
```

---

## 📊 Comparison: Different Approaches

### Approach 1: Separate Virtual Environments (RECOMMENDED) ✅

```
Pros:
✅ Complete isolation
✅ No dependency conflicts
✅ Easy to manage
✅ Safe for team collaboration
✅ Can use different package versions

Cons:
❌ Two environments to maintain
❌ Slightly larger disk space
```

**Best For:** Production, team projects, long-term maintenance

---

### Approach 2: Single Python 2.7 (NOT RECOMMENDED) ❌

```
Pros:
✅ Single environment
✅ Smaller disk space

Cons:
❌ Modern AI libraries don't support Python 2.7
❌ Many packages incompatible
❌ Will hit walls in Phase 4+
❌ Not maintainable long-term
```

---

### Approach 3: Single Python 3.x with Subprocess (POSSIBLE) ⚠️

```
Pros:
✅ Main environment is modern (Python 3)

Cons:
❌ NAOqi SDK doesn't work in Python 3
❌ Would need wrapper script
❌ Adds complexity
❌ Communication overhead
```

---

## 🎯 Recommendation for Your Project

**Use Approach 1: Separate Virtual Environments**

### Why?

1. **Phase 0-1:** You'll use Python 2.7 for robot control
2. **Phase 3-4:** You'll start using Python 3 for AI (Whisper, LLM, etc.)
3. **Phase 5+:** Heavy Python 3 usage (neural networks, embeddings)

By separating now, you avoid problems later.

---

## ✅ Quick Setup Steps (For You Now)

### Step 1: Create Both Environments
```bash
# Python 2.7 environment for robot control
python2.7 -m virtualenv venv_py27

# Python 3 environment for AI backend
python -m venv venv_py3
```

### Step 2: Activate and Run Tests
```bash
# Activate Python 2.7 venv
venv_py27\Scripts\activate

# Run Phase 0 tests
python run_all_tests_py27.py

# Deactivate
venv_py27\Scripts\deactivate
```

### Step 3: For AI Backend (Later, Phase 3+)
```bash
# Activate Python 3 venv
venv_py3\Scripts\activate

# Install AI packages
pip install fastapi uvicorn torch transformers openai-whisper

# Run backend
python -m src.ai_backend.main
```

---

## 📌 Important Notes

### Don't Do This ❌
```bash
# DON'T: Mix Python 2.7 and 3 in same environment
pip install naoqi  # Python 2.7 package
pip install fastapi  # Python 3 package
# → This will fail or cause conflicts
```

### Do This Instead ✅
```bash
# DO: Use separate virtual environments
venv_py27\Scripts\activate
pip install naoqi

venv_py27\Scripts\deactivate
venv_py3\Scripts\activate
pip install fastapi
```

---

## 🔄 Phase-by-Phase Environment Usage

| Phase | Environment | Tools | Purpose |
|-------|---|---|---|
| 0 | Python 2.7 (venv_py27) | NAOqi, test scripts | Robot assessment |
| 1 | Python 2.7 (venv_py27) | NAOqi, ROS2 | Bridge service |
| 2 | Python 3 (venv_py3) | FastAPI, React | Dashboard |
| 3 | Python 3 (venv_py3) | Whisper, Piper | Speech pipeline |
| 4 | Python 3 (venv_py3) | Ollama, LLM | Conversational AI |
| 5+ | Python 3 (venv_py3) | Torch, transformers | Full AI features |

---

## 💾 Project Structure with Virtual Environments

```
C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\
├── venv_py27/                    ← Python 2.7 virtual env (robot control)
│   ├── Scripts/
│   ├── Lib/
│   ├── Include/
│   └── pyvenv.cfg
│
├── venv_py3/                     ← Python 3.x virtual env (AI backend)
│   ├── Scripts/
│   ├── Lib/
│   ├── Include/
│   └── pyvenv.cfg
│
├── pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/
│   └── lib/                      ← NAOqi SDK (reference only)
│
├── src/                          ← Source code
│   ├── robot_bridge/            ← Uses venv_py27
│   ├── ai_backend/              ← Uses venv_py3
│   └── web_dashboard/           ← Uses Node.js (separate)
│
├── run_tests.bat                ← Uses venv_py27
├── run_backend.bat              ← Uses venv_py3
└── (documentation, config, etc.)
```

---

## ✨ Summary

| Question | Answer |
|----------|--------|
| **Do we need separate envs?** | YES ✅ |
| **Which approach?** | Virtual Environments (venv) ✅ |
| **For Phase 0 tests?** | Python 2.7 venv ✅ |
| **For AI Backend?** | Python 3 venv ✅ |
| **How many disk GBs?** | ~2-3 GB total (reasonable) |
| **Setup difficulty?** | Easy - just run two commands |

---

**Ready to set up the environments?** I can create the setup scripts for you! 🚀
