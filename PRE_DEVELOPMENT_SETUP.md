# Pre-Development Setup Guide

Complete this checklist before starting Phase 0 to ensure smooth development across all phases.

## 1️⃣ Hardware & Infrastructure Setup

### 1.1 Robot Hardware (Phase 0 Prerequisite)

**Assessment Checklist:**
- [ ] **Robot Physical Condition**
  - [ ] All 22 joints move freely without grinding
  - [ ] No visible cracks or damage
  - [ ] Head, arms, legs responsive
  - [ ] Feet/base stable

- [ ] **Power System**
  - [ ] Battery installed and charged
  - [ ] Power adapter working
  - [ ] Battery holds charge for 2+ hours
  - [ ] No battery leaks or swelling

- [ ] **Sensors**
  - [ ] All 4 microphones responsive (test with audio)
  - [ ] Front camera operational
  - [ ] Bottom camera operational
  - [ ] IMU/accelerometer functional
  - [ ] Joint encoders working

- [ ] **Audio/Video**
  - [ ] Speakers produce clear audio
  - [ ] Microphone array captures speech
  - [ ] Camera feeds clear and stable

- [ ] **Network**
  - [ ] Robot can connect to WiFi
  - [ ] OR robot can connect via Ethernet
  - [ ] Network latency <50ms to server
  - [ ] Static IP assigned to robot

**Documentation Required:**
- [ ] Hardware inventory spreadsheet
- [ ] Robot IP address: _______________
- [ ] NAO OS version: _______________
- [ ] NAOqi version: _______________
- [ ] List any repairs needed

### 1.2 Server Hardware

**Minimum Requirements:**
- [ ] CPU: 8+ cores (Intel i7/i9 or AMD Ryzen 7/9)
- [ ] RAM: 32GB (minimum 16GB)
- [ ] GPU: NVIDIA 12GB+ VRAM (RTX 4070/4080 recommended)
- [ ] Storage: 256GB+ SSD available
- [ ] Network: 1Gbps Ethernet connection

**Verification:**
```bash
# Check specs on Linux
lscpu                    # CPU info
free -h                  # RAM info
df -h                    # Disk space
nvidia-smi              # GPU info (if NVIDIA)
```

**Recommendations:**
- [ ] Dedicated server machine (not shared laptop)
- [ ] Wired Ethernet connection (WiFi backup)
- [ ] UPS/power backup for server
- [ ] Monitor + keyboard for initial setup

### 1.3 Network Setup

**Network Configuration:**
- [ ] Robot and server on same LAN
- [ ] Static IP for robot: _______________
- [ ] Static IP for server: _______________
- [ ] Firewall rules allowing robot-server communication
- [ ] Test ping latency (target <50ms):
  ```bash
  ping -c 10 <robot-ip>
  ```
- [ ] Test SSH connectivity (if applicable)
  ```bash
  ssh nao@<robot-ip>
  ```

**Documentation:**
- [ ] Network topology diagram
- [ ] IP address assignment table
- [ ] Firewall rules document
- [ ] Router configuration notes

---

## 2️⃣ Software Environment Setup

### 2.1 Development Machine Setup

**Operating System:**
- [ ] Linux (Ubuntu 22.04 LTS recommended) OR
- [ ] Windows with WSL2 with Ubuntu 22.04 OR
- [ ] macOS (limited support)

**Core Tools:**
```bash
# Ubuntu/WSL2
sudo apt update
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python-is-python3 \
    git \
    curl \
    wget \
    build-essential \
    cmake \
    pkg-config \
    libssl-dev
```

**Verification Checklist:**
- [ ] Python 3.10+ installed: `python3 --version`
- [ ] Git installed: `git --version`
- [ ] Pip upgraded: `pip install --upgrade pip`
- [ ] Virtual environment works: `python3 -m venv test_env`

### 2.2 GPU Setup (for AI models)

**NVIDIA GPU (Recommended):**
```bash
# Check driver
nvidia-smi

# Install CUDA Toolkit 12.1 (or latest compatible)
wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_530.30.02_linux.run
sudo sh cuda_12.1.0_530.30.02_linux.run

# Verify CUDA
nvcc --version
```

**Verification:**
- [ ] NVIDIA driver: `nvidia-smi`
- [ ] CUDA version: `nvcc --version`
- [ ] cuDNN installed (if needed for PyTorch)
- [ ] GPU memory available: `nvidia-smi` shows >12GB

**Fallback (CPU-only):**
- [ ] Machine has 64GB+ RAM
- [ ] SSD for model caching
- [ ] Understand slower inference times

### 2.3 Python Virtual Environment

**Create project environment:**
```bash
# Navigate to project
cd ~/Embodied_AI_NaoRobot

# Create virtual environment
python3.10 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Create requirements.txt (template)
# See section 2.4
```

**Verification:**
- [ ] Virtual env activated: `which python` shows venv path
- [ ] Can install packages: `pip install requests`
- [ ] Can import packages: `python -c "import requests"`

### 2.4 Dependencies Installation

**Create `requirements.txt` with base dependencies:**

```txt
# Core
python-dotenv==1.0.0
pydantic==2.0.0

# Robotics
naoqi>=2.8.6.23

# Web Framework
fastapi==0.104.0
uvicorn==0.24.0
python-socketio==5.9.0
python-engineio==4.7.0
aiofiles==23.2.0

# AI/ML
torch==2.1.0
transformers==4.35.0
numpy==1.24.3
scipy==1.11.0

# Speech
openai-whisper==20231117
piper-tts==1.2.0

# LLM
ollama==0.1.0
# Or: llama-cpp-python

# Database
sqlalchemy==2.0.0
psycopg2-binary==2.9.0

# RAG (Phase 7)
chromadb==0.4.0
sentence-transformers==2.2.2

# Development
pytest==7.4.0
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
mypy==1.7.0
pre-commit==3.5.0

# Documentation
sphinx==7.2.0
sphinx-rtd-theme==2.0.0
```

**Install:**
```bash
pip install -r requirements.txt
```

**Verification Checklist:**
- [ ] All packages install without errors
- [ ] Can import each major package
- [ ] PyTorch GPU support: `python -c "import torch; print(torch.cuda.is_available())"`

---

## 3️⃣ Project Repository Setup

### 3.1 Git Configuration

**Clone/Setup Repository:**
```bash
# Clone the repo
git clone https://github.com/SanketSalviNITK/Embodied_AI_NaoRobot.git
cd Embodied_AI_NaoRobot

# Configure git (already done, but verify)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Verify
git config --list
```

**Verification Checklist:**
- [ ] Repository cloned successfully
- [ ] Git user configured
- [ ] Remote points to GitHub: `git remote -v`

### 3.2 Branch Strategy

**Establish branching convention:**
```bash
# Main branch for releases
main

# Development branch for integration
develop

# Feature branches for each phase
feature/phase-0-robot-assessment
feature/phase-1-connectivity
feature/phase-2-dashboard
... etc
```

**Setup:**
- [ ] Create `develop` branch: `git checkout -b develop && git push -u origin develop`
- [ ] Document branch strategy in `CONTRIBUTING.md`
- [ ] Set up branch protection rules on GitHub (main branch)

### 3.3 GitHub Configuration

**Repository Settings:**
- [ ] Add `.gitignore` for Python/Node projects
- [ ] Add `CONTRIBUTING.md` with guidelines
- [ ] Add `CODE_OF_CONDUCT.md`
- [ ] Set up Issues templates
- [ ] Set up PR templates
- [ ] Enable branch protection on `main` (require PR review)
- [ ] Add collaborators with appropriate permissions
- [ ] Configure branch auto-delete on PR merge

---

## 4️⃣ Development Environment Configuration

### 4.1 IDE Setup (VSCode Recommended)

**Install Extensions:**
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension eamodio.gitlens
code --install-extension ms-vscode-remote.remote-containers
code --install-extension GitHub.Copilot
```

**Configure VSCode `.vscode/settings.json`:**
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "[python]": {
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

**Verification:**
- [ ] VSCode opens project without errors
- [ ] Python extension recognizes virtual env
- [ ] Linting and formatting work

### 4.2 Code Quality Tools

**Install and configure:**
```bash
pip install black flake8 mypy pytest

# Create .flake8 config
echo "[flake8]
max-line-length = 88
extend-ignore = E203, W503" > .flake8

# Create pyproject.toml for black
echo "[tool.black]
line-length = 88
target-version = ['py310']" >> pyproject.toml
```

**Pre-commit Hooks:**
```bash
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
EOF

# Install hooks
pre-commit install
```

**Verification:**
- [ ] `black --check src/` runs without errors
- [ ] `flake8 src/` runs without errors
- [ ] Pre-commit hooks execute on commit

### 4.3 Docker Setup (Optional but Recommended)

**Install Docker:**
```bash
# Ubuntu
sudo apt install -y docker.io docker-compose

# Verify
docker --version
docker-compose --version
```

**Create `Dockerfile` for project:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.ai_backend.main"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  ai-backend:
    build: .
    ports:
      - "8001:8001"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./src:/app/src
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Verification:**
- [ ] `docker --version` shows Docker installed
- [ ] `docker-compose --version` shows version
- [ ] Can build: `docker-compose build`

---

## 5️⃣ Model Downloads & Configuration

### 5.1 Download AI Models

**Whisper (Speech-to-Text):**
```bash
# Download will happen automatically on first use
# But pre-download to save time:
python3 << 'EOF'
import whisper
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
EOF
```

**Estimated sizes:**
- tiny: 39MB
- base: 140MB
- small: 466MB
- medium: 1.5GB
- large: 2.9GB

**Piper (Text-to-Speech):**
```bash
pip install piper-tts

# Download voice model
piper --download-dir ./models en_US-lessac-medium
```

**Mistral/Ollama (LLM):**
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download model
ollama pull mistral
# Or: ollama pull llama2
```

**Embedding Model:**
```bash
python3 << 'EOF'
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
EOF
```

**Verification Checklist:**
- [ ] Whisper model downloaded (~500MB for 'base')
- [ ] Piper voice model downloaded
- [ ] Ollama Mistral model available
- [ ] Embedding model cached
- [ ] Total disk space used: _____ GB

### 5.2 Configuration Files

**Create `config/` directory structure:**
```
config/
├── .env.example              # Template for environment variables
├── robot_config.yaml         # Robot connection settings
├── ai_config.yaml            # AI model settings
├── server_config.yaml        # Server settings
└── logging_config.yaml       # Logging configuration
```

**Create `.env.example`:**
```bash
# Robot Configuration
ROBOT_IP=192.168.1.100
ROBOT_PORT=9559
ROBOT_NAME=NAO_V4

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8001
SERVER_DEBUG=false

# AI Models
WHISPER_MODEL=base
PIPER_VOICE=en_US-lessac-medium
LLM_MODEL=mistral
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=512

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=embodied_ai
DB_USER=postgres
DB_PASSWORD=change_me

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

**Create `config/robot_config.yaml`:**
```yaml
robot:
  ip: "192.168.1.100"
  port: 9559
  name: "NAO_V4"
  naoqi_timeout: 5000

network:
  server_ip: "192.168.1.50"
  server_port: 8001
  heartbeat_interval: 1  # seconds

sensors:
  update_rate: 10  # Hz
  include_joints: true
  include_imu: true
  include_temperature: true

actuators:
  motion_speed: 0.5
  gesture_speed: 1.0
  max_joint_velocity: 1.0
```

**Verification:**
- [ ] `config/.env` created from `.env.example`
- [ ] All required env vars present
- [ ] Config files are valid YAML
- [ ] Can parse configs: `python -c "import yaml; yaml.safe_load(open('config/robot_config.yaml'))"`

---

## 6️⃣ Testing Infrastructure

### 6.1 Testing Framework Setup

**Create `tests/` directory structure:**
```
tests/
├── __init__.py
├── conftest.py                    # Pytest fixtures
├── test_robot_bridge.py
├── test_ai_backend.py
├── test_speech_pipeline.py
└── integration/
    ├── test_end_to_end.py
    └── test_robot_integration.py
```

**Create `tests/conftest.py`:**
```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def robot_mock():
    """Mock robot connection"""
    mock = Mock()
    mock.move_forward = Mock()
    mock.say = Mock()
    return mock

@pytest.fixture
def event_loop():
    """Event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

**Verification:**
- [ ] Can run: `pytest tests/`
- [ ] Can run specific test: `pytest tests/test_robot_bridge.py::test_connection`
- [ ] Test discovery works: `pytest --collect-only`

### 6.2 Test Configuration

**Create `pytest.ini`:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    -ra

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    robot: Requires robot hardware
```

**Verification:**
- [ ] `pytest --markers` shows custom markers
- [ ] Can filter tests: `pytest -m unit`

### 6.3 Continuous Integration (GitHub Actions)

**Create `.github/workflows/tests.yml`:**
```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-22.04
    strategy:
      matrix:
        python-version: ['3.10']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: flake8 src tests
    
    - name: Format check with black
      run: black --check src tests
    
    - name: Run tests
      run: pytest tests/ -m "not robot"
```

**Verification:**
- [ ] `.github/workflows/` created
- [ ] GitHub Actions workflow uploaded
- [ ] Can trigger test run via push to develop

---

## 7️⃣ Logging & Monitoring

### 7.1 Logging Setup

**Create `src/utils/logging_config.py`:**
```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app_name="embodied-ai", level=logging.INFO):
    """Configure logging for the application"""
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger(app_name)
    logger.setLevel(level)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        f"logs/{app_name}.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

**Verification:**
- [ ] Logging configured without errors
- [ ] Can create logger: `from src.utils.logging_config import setup_logging`
- [ ] Logs appear in `logs/` directory

### 7.2 Monitoring Tools (Optional)

**Health Check Endpoints:**
- [ ] `/health` - Basic health check
- [ ] `/metrics` - Prometheus metrics
- [ ] `/logs` - Recent logs view

---

## 8️⃣ Documentation & Communication

### 8.1 Project Documentation

**Ensure these exist:**
- [ ] `EMBODIED_AI_ROADMAP.md` - Project roadmap
- [ ] `README_PROJECT_STRUCTURE.md` - Project structure
- [ ] `docs/guides/Installation-Setup.md` - Setup instructions
- [ ] `CONTRIBUTING.md` - Contribution guidelines
- [ ] `API_REFERENCE.md` - API documentation
- [ ] `ARCHITECTURE.md` - System design

**Verification:**
- [ ] All docs can be read without errors
- [ ] Links between docs work
- [ ] Markdown formatting is correct

### 8.2 Team Communication Setup

**Establish channels:**
- [ ] Slack/Discord for team chat
- [ ] Weekly standup schedule
- [ ] GitHub Issues for tracking
- [ ] GitHub Discussions for questions

**Documentation:**
- [ ] Team member contact info
- [ ] On-call rotation (if applicable)
- [ ] Escalation procedures

---

## 9️⃣ Database Setup (for later phases)

### 9.1 PostgreSQL Setup (Phase 4+)

**For later use, but install now:**
```bash
# Ubuntu
sudo apt install -y postgresql postgresql-contrib

# Verify
psql --version

# Create database
sudo -u postgres createdb embodied_ai
sudo -u postgres createuser embodied_ai_user
```

**Configuration:**
- [ ] PostgreSQL installed and running
- [ ] Can connect: `psql -U embodied_ai_user -d embodied_ai`
- [ ] Backup strategy documented

### 9.2 Redis Setup (for caching, Phase 4+)

```bash
# Ubuntu
sudo apt install -y redis-server

# Verify
redis-cli ping
```

---

## 🔟 Phase 0 Specific Setup

### 10.1 Hardware Diagnostic Tools

**Create diagnostic scripts in `scripts/diagnostics/`:**
- [ ] `check_motors.py` - Test all 22 joints
- [ ] `check_audio.py` - Test microphones and speakers
- [ ] `check_cameras.py` - Test both cameras
- [ ] `check_sensors.py` - Test IMU and other sensors
- [ ] `network_test.py` - Test latency and connectivity

**Verification:**
- [ ] All diagnostic scripts created
- [ ] Can run: `python scripts/diagnostics/check_motors.py`
- [ ] Output is clear and actionable

### 10.2 Robot Connection Verification

**Test script `test_robot_connection.py`:**
```python
#!/usr/bin/env python3
"""Test robot connection and basic functionality"""

import sys
sys.path.insert(0, '.')

from src.robot_bridge import RobotBridge
import logging

logging.basicConfig(level=logging.INFO)

def test_connection():
    bridge = RobotBridge(
        robot_ip="192.168.1.100",
        robot_port=9559
    )
    
    # Test connection
    if bridge.connect():
        print("✓ Connected to robot")
    else:
        print("✗ Failed to connect")
        return False
    
    # Test basic functions
    # - Get joint angles
    # - Get battery status
    # - Test motion
    # - Test audio
    
    print("All tests passed!")
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
```

**Verification:**
- [ ] Connection test script works
- [ ] Can identify robot issues
- [ ] Can read and interpret output

---

## ✅ Pre-Development Checklist

### Must Complete Before Starting Phase 0

**Hardware:**
- [ ] Robot hardware assessed and documented
- [ ] Robot can power on and boot
- [ ] Network connectivity verified (<50ms latency)
- [ ] Server machine meets specs
- [ ] Server connected to same network as robot

**Software:**
- [ ] Development environment set up
- [ ] Python 3.10+ with virtual environment
- [ ] Git configured and repository cloned
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] GPU setup complete (if available)
- [ ] Can import torch/transformers/fastapi

**Infrastructure:**
- [ ] GitHub repository configured
- [ ] Branch strategy documented
- [ ] Testing framework set up
- [ ] Pre-commit hooks installed
- [ ] Logging configured

**Configuration:**
- [ ] `.env` file created with correct values
- [ ] Robot IP address configured
- [ ] Server hostname/IP configured
- [ ] Database credentials set (if using)

**Documentation:**
- [ ] All roadmap documents reviewed
- [ ] Architecture understood
- [ ] Phase 0 tasks understood
- [ ] Team roles assigned

**Models & Data:**
- [ ] Whisper model downloaded
- [ ] Piper voice model downloaded
- [ ] Ollama/Mistral available
- [ ] Embedding model cached
- [ ] Disk space verified (10GB+ free)

---

## Setup Verification Script

**Create `verify_setup.sh` to check everything:**

```bash
#!/bin/bash

echo "🔍 Verifying Embodied AI Project Setup..."
echo ""

# Python
echo "✓ Checking Python..."
python3 --version

# Virtual Env
echo "✓ Checking Virtual Environment..."
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated"
else
    echo "✓ Virtual environment: $VIRTUAL_ENV"
fi

# Dependencies
echo "✓ Checking Dependencies..."
python3 -c "import torch, transformers, fastapi, whisper" && echo "✓ All packages imported successfully"

# Git
echo "✓ Checking Git..."
git log --oneline -1

# Directory Structure
echo "✓ Checking Directory Structure..."
for dir in src tests config docs logs; do
    [ -d "$dir" ] && echo "  ✓ $dir/" || echo "  ✗ $dir/ missing"
done

# Configuration
echo "✓ Checking Configuration..."
[ -f ".env" ] && echo "  ✓ .env exists" || echo "  ✗ .env missing"
[ -f "config/robot_config.yaml" ] && echo "  ✓ robot_config.yaml exists" || echo "  ✗ robot_config.yaml missing"

# Models
echo "✓ Checking Models..."
# This would check for downloaded models

echo ""
echo "✅ Setup verification complete!"
```

---

## Next Steps

Once all items are checked:

1. **Commit setup** to git:
   ```bash
   git add -A
   git commit -m "setup: initial development environment configuration"
   git push origin develop
   ```

2. **Create GitHub Issues** for each phase:
   - Phase 0: Robot Assessment
   - Phase 1: Connectivity Layer
   - etc.

3. **Start Phase 0** with team
4. **Document any issues** found during setup

---

**Setup Status:** Ready for Phase 0  
**Last Updated:** 2026-06-13

For questions about setup, see `docs/guides/Installation-Setup.md` or check GitHub Discussions.
