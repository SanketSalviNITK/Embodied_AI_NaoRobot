# Installation & Hardware Setup Guide

## Prerequisites

### Hardware Requirements

#### Server Machine
- **CPU:** Intel i7/i9 or AMD Ryzen 7/9 (8+ cores)
- **RAM:** Minimum 16GB (32GB recommended)
- **GPU:** NVIDIA GPU with 12GB+ VRAM (recommended)
  - Tested: GTX 1660, RTX 4070, RTX 4080
- **Storage:** 256GB+ SSD (for OS + models)
- **Network:** 1Gbps Ethernet connection

#### NAO Robot V4
- Hardware version: NAO V4.x
- Power supply and charging dock
- Network access (WiFi or Ethernet)
- All 22 joints functional

### Software Requirements

- **OS:** Linux (Ubuntu 22.04 LTS recommended) or Windows with WSL2
- **Python:** 3.9 or higher
- **Docker:** (optional but recommended)
- **Git:** For version control

## Step 1: Robot Hardware Setup

### 1.1 Physical Inspection
- [ ] Check all joints move freely
- [ ] Verify microphones are working
- [ ] Test cameras (front and bottom)
- [ ] Confirm battery installation
- [ ] Ensure all cables are connected

### 1.2 NAO Operating System
- [ ] Boot NAO robot
- [ ] Note NAO OS version: ___________
- [ ] Record NAO IP address: ___________
- [ ] Verify network connectivity

### 1.3 Network Configuration
```bash
# Connect to NAO via SSH
ssh nao@<NAO_IP_ADDRESS>
# Default password: nao

# Verify network
ping -c 5 8.8.8.8
```

### 1.4 Hardware Diagnostics
Run NAO diagnostics:
```bash
# Via Choregraphe IDE or command line
# Commands to verify sensors...
```

## Step 2: Server Environment Setup

### 2.1 Ubuntu/Linux Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    git \
    cmake \
    build-essential

# Install CUDA (if using NVIDIA GPU)
# Follow NVIDIA's official guide for your GPU
```

### 2.2 Python Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv ~/embodied_ai_env

# Activate environment
source ~/embodied_ai_env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 2.3 Clone Repository

```bash
git clone https://github.com/YourOrg/embodied-ai.git
cd embodied-ai

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Robot Bridge Setup

### 3.1 NAOqi SDK Installation

```bash
# Option 1: Using Ollama (Recommended)
curl https://ollama.ai/install.sh | sh

# Option 2: Manual NAOqi SDK
# Download from Aldebaran website
```

### 3.2 Configuration

Create `config/robot_config.yaml`:
```yaml
robot:
  ip: "192.168.1.100"  # Replace with your NAO IP
  port: 9559
  name: "NAO_V4"
  
network:
  server_ip: "0.0.0.0"
  server_port: 8080
```

### 3.3 Test Connection

```bash
python scripts/test_robot_connection.py
```

## Step 4: AI Backend Setup

### 4.1 Download Models

```bash
# Whisper (Speech-to-Text)
mkdir -p ~/models
# Model will be downloaded automatically on first use

# Piper (Text-to-Speech)
pip install piper-tts

# Mistral/Ollama (LLM)
ollama pull mistral
```

### 4.2 Start Services

```bash
# Start robot bridge
python -m src.robot_bridge.main

# In another terminal, start AI backend
python -m src.ai_backend.main

# In another terminal, start web dashboard
cd src/web_dashboard
npm install
npm run dev
```

### 4.3 Verify Setup

- [ ] Robot bridge running on http://localhost:8000
- [ ] AI backend accessible at http://localhost:8001
- [ ] Web dashboard at http://localhost:5173 (dev) or :3000 (prod)
- [ ] Robot responding to ping
- [ ] All services communicating

## Step 5: Development Environment

### 5.1 IDE Setup (VSCode recommended)

```bash
# Install extensions
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension dbaeumer.vscode-eslint
```

### 5.2 Development Tools

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

## Troubleshooting

### Robot Connection Issues
- Ensure NAO is on same network as server
- Check firewall settings
- Verify NAO IP with `arp-scan` or check router

### CUDA Issues
- Verify NVIDIA drivers: `nvidia-smi`
- Check CUDA version: `nvcc --version`
- Reinstall CUDA if needed

### Model Download Issues
- Check disk space: `df -h`
- Verify internet connection
- Try manual download if automatic fails

### Performance Issues
- Monitor GPU usage: `nvidia-smi -l 1`
- Check CPU/RAM: `top` or `htop`
- Profile components individually

## Next Steps

1. Complete [Phase 0: Robot Assessment](../phases/Phase-0-Robot-Assessment.md)
2. Move to [Phase 1: Robot Connectivity](../phases/Phase-1-Connectivity.md)
3. See [Development Environment Guide](Development-Environment.md) for advanced setup

## Support

For detailed troubleshooting, see [Troubleshooting Guide](Troubleshooting.md)

---

**Setup Version:** 1.0  
**Last Updated:** 2026-06-13  
**Tested On:** Ubuntu 22.04 LTS, NAO V4
