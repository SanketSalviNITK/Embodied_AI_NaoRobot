# 🤖 Embodied AI Platform - NAO Robot V4 Modernization

**A comprehensive platform for AI-powered robot interaction using NAO V4 and cutting-edge machine learning.**

---

## 📊 Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| **Setup** | ✅ Complete | Python 2.7 & 3.x environments ready |
| **Phase 0** | ✅ Ready | Robot assessment & baseline documentation |
| **Phase 1-11** | 📋 Planned | Full roadmap defined |

**Robot IP:** `169.254.175.171` (NEW)

---

## 🚀 Quick Start (5 Minutes)

### 1. Verify Robot Connection
```bash
ping 169.254.175.171
```

### 2. Test NAOqi
```bash
python -c "from naoqi import ALProxy; ALProxy('ALMotion', '169.254.175.171', 9559); print('OK')"
```

### 3. Run Phase 0 Tests
```bash
scripts/run_phase0_tests.bat
```

**Expected Result:** All 5 tests pass ✅

---

## 📁 Project Structure

```
EmbodiedAI/
├── README.md                    ← You are here
├── CLAUDE.md                    ← Claude Code configuration
│
├── docs/                        ← 📚 All documentation
│   ├── README.md               ← Documentation index (START HERE)
│   ├── guides/                 ← How-to guides
│   ├── references/             ← API & technical references
│   └── phases/                 ← Phase-specific documentation
│
├── tests/                       ← 🧪 Test scripts
│   ├── phase0/                 ← Phase 0 comprehensive tests
│   ├── legacy/                 ← Pre-phase 0 tests
│   └── utils/                  ← Test utilities
│
├── scripts/                     ← 🔧 Setup & utility scripts
│   ├── setup_python_environments.bat
│   ├── setup_python_environments.ps1
│   ├── update_robot_ip.bat
│   ├── update_robot_ip.ps1
│   └── run_phase0_tests.bat
│
├── config/                      ← ⚙️ Configuration templates
│
├── src/                         ← 💻 Source code (Phase 1+)
│   ├── robot_bridge/
│   ├── ai_backend/
│   └── web_dashboard/
│
├── venv_py27/                   ← Python 2.7 environment
├── venv_py3/                    ← Python 3.x environment
│
├── results/                     ← 📊 Test results (git-ignored)
│
└── .gitignore                   ← Git configuration

```

---

## 📚 Documentation

**Start with:** `docs/README.md` for complete documentation index

**Key Documents:**
- 🚀 **Quick Start:** `docs/guides/GETTING_STARTED_CHECKLIST.md`
- 🔧 **Setup:** `docs/guides/ENVIRONMENT_SETUP_README.md`
- 🎯 **Phase 0:** `docs/phases/PHASE0_READY.md`
- 🗺️ **Vision:** `docs/phases/EMBODIED_AI_ROADMAP.md`
- 📖 **APIs:** `docs/references/NAOQI_SDK_API_REFERENCE.md`

---

## 🧪 Testing

### Phase 0: Robot Assessment (Complete)
```bash
scripts/run_phase0_tests.bat
```

**Tests included:**
1. ✅ Joint Control (22 DOF)
2. ✅ Motion & Walking
3. ✅ Sensor Analysis
4. ✅ Audio & Speech
5. ✅ LED Control

**Duration:** 30-45 minutes  
**Results saved to:** `results/phase0_results/`

---

## 🔌 Robot Configuration

### Current Setup
- **Robot:** NAO V4
- **IP Address:** 169.254.175.171 (LAN/wired)
- **NAOqi:** 2.8.6.23 (Python 2.7)
- **Network:** 169.254.x.x direct connection

### Available Connections
- ✅ **LAN (Wired):** Primary, stable, always available
- ✅ **WiFi (Wireless):** Flexible, mobile (see `docs/guides/WIFI_CONNECTION_GUIDE.md`)

---

## 🛠️ Setup & Installation

### Python Environments
Two isolated environments are configured:

**Python 2.7 (venv_py27)**
- NAOqi SDK 2.8.6.23
- Robot control & testing
- Phase 0 test suite

**Python 3.x (venv_py3)**
- FastAPI, PyTorch, Transformers
- Speech: Whisper, Piper
- Memory: ChromaDB, Embeddings
- Ready for Phase 2+

### Quick Setup
```bash
scripts/setup_python_environments.bat
```

**What it does:**
- ✅ Checks for Python 2.7 & 3.x
- ✅ Creates virtual environments
- ✅ Installs NAOqi SDK
- ✅ Installs AI dependencies

---

## 📊 Project Scope

### 11-Phase Development Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 0 | Robot Assessment | ✅ Ready |
| 1 | Connectivity Layer | 📋 Planned |
| 2 | Web Dashboard | 📋 Planned |
| 3 | Speech Pipeline | 📋 Planned |
| 4 | Conversational AI | 📋 Planned |
| 5-11 | Advanced AI Features | 📋 Planned |

See `docs/phases/EMBODIED_AI_ROADMAP.md` for complete roadmap.

---

## 🎯 Key Features

### Robot Control
- ✅ All 22 joints (DOF) controllable
- ✅ Predefined postures (Stand, Sit, Crouch, etc.)
- ✅ Walking & locomotion
- ✅ Motion planning

### Sensing
- ✅ Accelerometer (IMU)
- ✅ Gyroscope
- ✅ Foot pressure sensors (8 total)
- ✅ Touch sensors (head)
- ✅ Joint encoders
- ✅ Battery & temperature monitoring

### Audio & Speech
- ✅ Text-to-speech (TTS)
- ✅ Multi-language support
- ✅ Microphone input
- ✅ Speaker output

### Visual
- ✅ LED control (full RGB)
- ✅ Camera access
- ✅ Face detection (framework ready)

---

## 🚀 Next Steps

### Immediate (This Week)
1. ✅ Run Phase 0 tests: `scripts/run_phase0_tests.bat`
2. ✅ Document baseline: `docs/phases/PHASE0_BASELINE_TEMPLATE.md`
3. ✅ Review results

### Phase 0 (Next Week)
- Robot assessment & diagnostics
- Hardware baseline documentation
- Issue identification & resolution

### Phase 1 (Following Week)
- Robot connectivity layer
- Bridge service development
- ROS2 integration (optional)

---

## 📞 Resources

### Documentation
- **Complete Index:** `docs/README.md`
- **NAOqi API Ref:** `docs/references/NAOQI_SDK_API_REFERENCE.md` (40+ services)
- **Phase 0 Guide:** `docs/phases/PHASE0_ASSESSMENT_GUIDE.md`
- **Setup Guide:** `docs/guides/ENVIRONMENT_SETUP_README.md`

### Test Scripts
- **Phase 0:** `tests/phase0/` (5 comprehensive tests)
- **Legacy:** `tests/legacy/` (pre-phase 0)
- **Utilities:** `tests/utils/`

### Utility Scripts
- **Python Setup:** `scripts/setup_python_environments.bat`
- **IP Update:** `scripts/update_robot_ip.bat`
- **Phase 0 Runner:** `scripts/run_phase0_tests.bat`

---

## 🔧 Common Tasks

### Update Robot IP
```bash
scripts/update_robot_ip.bat
```

### Setup Python Environments
```bash
scripts/setup_python_environments.bat
```

### Run Phase 0 Tests
```bash
scripts/run_phase0_tests.bat
```

### View Test Results
```bash
type results\phase0_results\test_1_joint_control.log
```

---

## 📋 Repository Organization

**Clean Structure:**
- ✅ All tests in `tests/`
- ✅ All docs in `docs/`
- ✅ All scripts in `scripts/`
- ✅ Results in `results/` (git-ignored)
- ✅ Source code ready in `src/`

**Git Ignored:**
- Virtual environments (`venv_*/`)
- Test results (`results/`)
- Temporary files (`*.pyc`, `__pycache__/`)
- IDE files (`.vscode/`, `.idea/`)

---

## 👥 Team & Contact

**Project Lead:** [Your Name]  
**Robot IP:** 169.254.175.171  
**NAOqi:** 2.8.6.23 (Python 2.7)  

**GitHub:** https://github.com/SanketSalviNITK/Embodied_AI_NaoRobot

---

## ✅ Ready to Start?

### 1. Read Documentation
```
docs/README.md
```

### 2. Verify Setup
```bash
ping 169.254.175.171
scripts/setup_python_environments.bat
```

### 3. Run Phase 0
```bash
scripts/run_phase0_tests.bat
```

### 4. Review Results
```
results/phase0_results/
```

---

**Status:** 🚀 **READY FOR PHASE 0**

Created: 2026-06-13  
Last Updated: 2026-06-13

