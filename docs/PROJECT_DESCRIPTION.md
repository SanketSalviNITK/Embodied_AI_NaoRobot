# Embodied AI Platform - NAO Robot V4

## Project Overview

This repository contains the complete implementation of an **Embodied AI Platform** built on a NAO Robot V4. The project transforms a used NAO robot into a modern, locally-hosted AI system that serves as a physical interface for conversational AI, research, and educational applications.

## Vision

Convert a NAO Robot V4 into a modern Embodied AI platform powered by locally hosted AI models, creating a physical interface to an intelligent system running on a local server. All intelligence resides on the server while the robot acts as:

- **Audio input/output device** - Capture user speech and output synthesized responses
- **Sensor platform** - Provide real-time sensor data (IMU, temperature, joint angles)
- **Actuator platform** - Execute motion commands and gestures
- **Physical embodiment of AI** - Make the AI tangible and interactive

## Key Features

### Phase 1-5 (MVP - 6-8 weeks)
- ✅ Robot hardware assessment and validation
- ✅ Remote robot control via web dashboard
- ✅ Speech-to-text and text-to-speech pipeline
- ✅ Conversational AI with local LLM (Mistral/Llama)
- ✅ Synchronized gestures and motion control

### Phase 6-10 (Extended Platform - 18-21 weeks)
- Digital twin visualization (3D real-time model)
- Retrieval-Augmented Generation (RAG) for document Q&A
- Presentation assistant capabilities
- Advanced embodied AI with emotion recognition
- Learning from user interactions

### Phase 11+ (Research Platform)
- Open-source community platform
- Multi-agent coordination
- Autonomous navigation
- Vision-language integration
- Campus-wide deployment

## System Architecture

```
┌─────────────────────────────────────────────┐
│   WEB DASHBOARD (React + Three.js)          │
│   ├─ Robot Control & Teleoperation          │
│   ├─ Live Camera Feed & Sensor Monitoring   │
│   ├─ Digital Twin (3D Visualization)        │
│   └─ AI Chat Interface                      │
└──────────────┬──────────────────────────────┘
               │ HTTP/WebSocket
┌──────────────▼──────────────────────────────┐
│   LOCAL AI SERVER (FastAPI Backend)         │
│   ├─ LLM Engine (Mistral 7B)                │
│   ├─ Speech Pipeline (Whisper + Piper)     │
│   ├─ Motion Controller & Gesture Synthesis  │
│   ├─ Memory System (Short & Long-term)      │
│   ├─ RAG System (ChromaDB)                  │
│   └─ Intent Recognition                     │
└──────────────┬──────────────────────────────┘
               │ ROS2/TCP/WebSocket
┌──────────────▼──────────────────────────────┐
│   ROBOT MIDDLEWARE (ROS2/Python Bridge)     │
│   ├─ Motion Command Execution               │
│   ├─ Sensor Data Streaming                  │
│   ├─ Audio/Video I/O                        │
│   └─ Connection Management                  │
└──────────────┬──────────────────────────────┘
               │ NAOqi SDK
┌──────────────▼──────────────────────────────┐
│   NAO ROBOT V4 (Physical Platform)          │
│   ├─ 22 Degrees of Freedom                  │
│   ├─ Dual Microphones & Speakers            │
│   ├─ 2 HD Cameras                           │
│   ├─ IMU & Accelerometer                    │
│   └─ Battery & Motor Control                │
└─────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Robot Bridge** | ROS2 Humble | Industry standard for robotics |
| **Speech-to-Text** | OpenAI Whisper | Accurate, multilingual, runs locally |
| **Text-to-Speech** | Piper | Lightweight, natural-sounding |
| **Local LLM** | Mistral 7B | Best speed/quality balance for real-time interaction |
| **LLM Server** | Ollama | Simple deployment, excellent performance |
| **Vector Database** | ChromaDB | Lightweight, embedded, good for RAG |
| **Web Framework** | FastAPI | Modern, high-performance, excellent tooling |
| **Frontend** | React 18 + Vite | Standard, large community, good performance |
| **3D Graphics** | Three.js | Mature, good WebGL support, NAO examples available |

## Project Structure

```
Embodied_AI_NaoRobot/
├── EMBODIED_AI_ROADMAP.md           ← Complete implementation plan
├── README_PROJECT_STRUCTURE.md      ← Navigation guide
├── GETTING_STARTED_CHECKLIST.md     ← Onboarding checklist
├── docs/                            ← All documentation
│   ├── architecture/                ← System design
│   ├── phases/                      ← Phase-by-phase specs (0-11)
│   ├── guides/                      ← Setup and how-to guides
│   ├── api-reference/               ← API specifications
│   ├── technical-specs/             ← Deep technical dives
│   └── research/                    ← Research resources
├── src/                             ← Source code (to be developed)
│   ├── robot_bridge/
│   ├── ai_backend/
│   ├── web_dashboard/
│   └── rag_system/
├── tests/                           ← Test suite
├── config/                          ← Configuration files
├── examples/                        ← Example scripts
├── scripts/                         ← Utility scripts
└── notebooks/                       ← Jupyter notebooks for research
```

## Getting Started

### Quick Start (30 minutes)
1. Read: `EMBODIED_AI_ROADMAP.md` → Executive Summary
2. Review: `README_PROJECT_STRUCTURE.md` → Your role section
3. Check: `docs/INDEX.md` → Navigation hub

### Full Onboarding (1 week)
1. Follow: `GETTING_STARTED_CHECKLIST.md`
2. Complete: All 6 onboarding phases
3. Start: Phase 0 - Robot Assessment

### Setup & Installation
1. Follow: `docs/guides/Installation-Setup.md`
2. Install dependencies (Python, ROS2, models)
3. Test robot connectivity
4. Deploy services locally

## Development Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| 0 | Robot Assessment | 1 week | 📋 Planning |
| 1 | Connectivity Layer | 2 weeks | 📋 Planning |
| 2 | Remote Dashboard | 2 weeks | 📋 Planning |
| 3 | Speech Pipeline | 2 weeks | 📋 Planning |
| 4 | LLM Integration | 3 weeks | 📋 Planning |
| 5 | Embodied Behaviors | 3 weeks | 📋 Planning |
| 6 | Digital Twin | 2 weeks | 📋 Planning |
| 7 | RAG System | 2 weeks | 📋 Planning |
| 8 | Document UI | 2 weeks | 📋 Planning |
| 9 | Presentation Assistant | 2 weeks | 📋 Planning |
| 10 | Advanced AI | 3 weeks | 📋 Planning |
| 11 | Research Platform | Ongoing | 📋 Planning |

**MVP Timeline:** 6-8 weeks (Phases 0-5)  
**Full Platform:** 18-21 weeks (Phases 0-10)

## Research Applications

This platform enables cutting-edge research in:

- **Embodied AI** - How physical embodiment affects AI behavior
- **Human-Robot Interaction** - Natural conversation and gesture synthesis
- **Educational Robotics** - AI-powered teaching assistants
- **Digital Twins** - Real-time robot simulation and control
- **Local LLMs** - Deploying large models on resource-constrained hardware
- **Retrieval-Augmented Generation** - Grounded AI responses using documents
- **Agentic AI** - Autonomous decision-making and planning
- **Robotics Dashboards** - Real-time monitoring and control interfaces

## Hardware Requirements

### Robot
- NAO Robot V4 (or compatible)
- Network access (WiFi or Ethernet)
- Power supply and charging dock

### Server Machine
- **CPU:** Intel i7/i9 or AMD Ryzen 7/9 (8+ cores)
- **RAM:** 32GB (minimum 16GB)
- **GPU:** NVIDIA GPU with 12GB+ VRAM (RTX 4070/4080 recommended)
- **Storage:** 256GB+ SSD
- **OS:** Linux (Ubuntu 22.04 LTS) or Windows with WSL2

## Team & Contribution

### Recommended Team Composition
- 2–5 full-time developers
- Mix of: Robotics, AI/ML, Frontend, Systems Engineering
- Academic research focus

### Contributing
See individual phase documentation for contribution guidelines.

## References

- **Main Roadmap:** `EMBODIED_AI_ROADMAP.md`
- **Documentation Hub:** `docs/INDEX.md`
- **Architecture:** `docs/architecture/System-Architecture.md`
- **Installation:** `docs/guides/Installation-Setup.md`

## License

(To be determined - MIT/Apache 2.0/Custom)

## Contact

**Project Owner:** Sanket Salvi  
**GitHub:** [@SanketSalviNITK](https://github.com/SanketSalviNITK)  
**Repository:** [Embodied_AI_NaoRobot](https://github.com/SanketSalviNITK/Embodied_AI_NaoRobot)

---

**Project Status:** Documentation & Planning Phase ✅ Complete  
**Ready to Start:** Phase 0 - Robot Assessment  
**Last Updated:** 2026-06-13

**Start here:** [EMBODIED_AI_ROADMAP.md](EMBODIED_AI_ROADMAP.md)
