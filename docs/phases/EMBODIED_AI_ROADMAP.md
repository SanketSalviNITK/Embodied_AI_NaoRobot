# Embodied AI Platform: NAO Robot V4 Modernization Roadmap

**Project Vision:** Convert a used NAO Robot V4 into a modern Embodied AI platform powered by locally hosted AI models, creating a physical interface to an intelligent system running on a local server.

**Document Version:** 1.0  
**Last Updated:** 2026-06-13  
**Target Audience:** R&D Team, Project Stakeholders, Academic Partners

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Phase-wise Roadmap Overview](#phase-wise-roadmap-overview)
4. [Detailed Phase Breakdown](#detailed-phase-breakdown)
5. [Technology Stack Recommendations](#technology-stack-recommendations)
6. [Risk Assessment & Mitigation](#risk-assessment--mitigation)
7. [MVP Definition](#mvp-definition)
8. [Development Prioritization](#development-prioritization)
9. [Timeline & Resource Allocation](#timeline--resource-allocation)
10. [Future Research Extensions](#future-research-extensions)

---

## Executive Summary

### Project Objectives

This roadmap outlines a phased approach to transform a NAO Robot V4 into a research platform for embodied AI applications. The system architecture separates the robot (perception and actuation) from intelligence (local AI server), enabling:

- **Immediate Value:** Interactive robot control and teleoperation capabilities
- **Near-term Research:** Conversational AI, gesture synthesis, and human-robot interaction
- **Long-term Platform:** Foundation for multi-agent systems, autonomous navigation, and campus-wide AI deployment

### Key Principles

- **Incremental Delivery:** Each phase produces a working system with demonstrable value
- **Separation of Concerns:** Robot hardware, middleware, AI backend, and UI layers are decoupled
- **Local-First Deployment:** All computation on-premise for privacy and control
- **Research-Grade Infrastructure:** Extensible architecture for emerging AI techniques

### Target Team

- Small university research lab with 2–5 full-time developers
- Skill set: Robotics, Python backend, React frontend, Linux systems
- Timeline: 12–18 months to full platform maturity

### Expected Outcomes

- **Working System:** Interactive embodied AI that converses, gestures, and responds to user input
- **Research Capabilities:** Framework for studying human-robot interaction and embodied AI
- **Educational Value:** Teaching assistant for campus courses and demonstrations
- **Community Contribution:** Open-source platform for roboticists and AI researchers

---

## System Architecture

### High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB DASHBOARD (Layer 4)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Robot Ctrl   │  │ AI Chat UI   │  │ Digital Twin (3D)    │ │
│  │ Teleoperation│  │ Voice/Text   │  │ Real-time Viz        │ │
│  │ Emergency    │  │ Session Logs │  │ Joint Visualization │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└──────────────────────────┬───────────────────────────────────────┘
                           │
            HTTP/WebSocket │ JSON API
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                     LOCAL AI SERVER (Layer 3)                    │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐ │
│  │ LLM Engine     │  │ Speech Pipeline │  │ Motion Controller│ │
│  │ (Llama/Qwen)   │  │ (Whisper/Piper) │  │ Gesture Synth    │ │
│  │ Memory System  │  │ Audio I/O       │  │ Animation Ctrl   │ │
│  └────────────────┘  └─────────────────┘  └──────────────────┘ │
│                                                                  │
│  ┌────────────────┐  ┌─────────────────┐                       │
│  │ RAG System     │  │ Intent Resolver │                       │
│  │ (ChromaDB)     │  │ State Manager   │                       │
│  └────────────────┘  └─────────────────┘                       │
└──────────────────────────┬───────────────────────────────────────┘
                           │
         TCP/UDP/WebSocket │ Binary Protocol
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│               ROBOT MIDDLEWARE (Layer 2)                          │
│            Robot Bridge Service (ROS2 / Python)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Motion Cmd   │  │ Sensor Stream│  │ Audio I/O Bridge     │  │
│  │ Execution    │  │ Aggregator   │  │ (Mic/Speaker)        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                    ROS API│ / NAOqi SDK
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                   NAO ROBOT V4 (Layer 1)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Microphone   │  │ Speaker      │  │ Joint Actuators      │  │
│  │ Cameras      │  │ Head LEDs    │  │ (22 DoF)             │  │
│  │ Accelerometer│  │ Tactile      │  │ Motion Control       │  │
│  │ Gyroscope    │  │ Sensors      │  │ Battery Monitor      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Architectural Layers

| Layer | Component | Role | Technologies |
|-------|-----------|------|---------------|
| **1** | NAO Robot V4 | Physical I/O | Sensors, Actuators, Network |
| **2** | Robot Middleware | Hardware Abstraction | ROS2 / Python Bridge |
| **3** | AI Backend | Intelligence & Control | LLM, Speech, Motion Synthesis |
| **4** | Web Dashboard | User Interface & Control | React, Three.js, WebSocket |
| **5** | Future Extensions | Research Capabilities | Multi-agent, Vision-Language, Nav |

---

## Phase-wise Roadmap Overview

### Quick Reference Table

| Phase | Name | Duration | Core Focus | Deliverable | Team Size |
|-------|------|----------|------------|-------------|-----------|
| 0 | Robot Recovery & Assessment | 1 week | Hardware validation | Working NAO unit | 1 person |
| 1 | Robot Connectivity Layer | 2 weeks | Network communication | Robot bridge service | 2 people |
| 2 | Remote Control Dashboard | 2 weeks | Web UI & teleoperation | Control interface | 2 people |
| 3 | Speech Pipeline | 2 weeks | Audio I/O | STT & TTS integration | 2 people |
| 4 | Local LLM Integration | 3 weeks | Conversational AI | Chat interface + memory | 2–3 people |
| 5 | Embodied AI Behaviors | 3 weeks | Gesture + speech sync | Gesture library & executor | 2–3 people |
| 6 | Digital Twin | 2 weeks | 3D visualization | Real-time pose sync | 2 people |
| 7 | RAG System | 2 weeks | Document intelligence | Embeddings & retrieval | 2 people |
| 8 | Document Intelligence UI | 2 weeks | Document upload & QA | PDF/PPT ingestion | 2 people |
| 9 | Presentation Assistant | 2 weeks | Slide generation | Presentation mode | 2 people |
| 10 | Advanced Embodied AI | 3 weeks | Emotion, context awareness | Emotional responses | 2–3 people |
| 11 | Research Platform | Ongoing | Community & extensions | APIs, documentation | 1–2 people |

**Total Estimated Duration:** 12–18 months (consecutive development)

---

## Detailed Phase Breakdown

### Phase 0: Robot Recovery & Assessment

**Duration:** 1 week  
**Team:** 1 person (robotics engineer)  
**Status:** Foundation

#### Objective
Recover, diagnose, and validate the NAO Robot V4 hardware. Establish baseline functionality and identify any physical/software issues before integration.

#### User Value
- Confidence in hardware readiness
- Understanding of current NAO software stack
- Documentation of hardware state

#### Features Implemented
- Physical inspection and repairs
- NAO operating system validation
- Network connectivity testing
- Sensor calibration checks
- Battery condition assessment
- Motion control verification

#### Technical Architecture
- Direct NAO access via Choregraphe or command line
- Initial NAOqi SDK exploration
- Hardware diagnostic scripts

#### Technology Stack
- NAOqi SDK (existing on robot)
- Choregraphe IDE
- Python 2.7 / Python 3.x bridge
- Network diagnostics tools (ping, SSH)

#### Detailed Tasks

1. **Physical Inspection**
   - Check mechanical integrity (joints, servos)
   - Inspect cables and connectors
   - Verify LED/actuator responsiveness
   - Clean and stabilize base

2. **Software Baseline**
   - Boot NAO and confirm OS version
   - Check installed packages
   - Verify NAOqi Python SDK
   - Test basic motion commands

3. **Network Setup**
   - Configure static IP address
   - Set up SSH access
   - Verify WiFi/Ethernet connectivity
   - Test ping latency (<50ms target)

4. **Hardware Diagnostics**
   - Run joint motion tests (all 22 degrees of freedom)
   - Test sensors (microphone, cameras, accelerometer, gyro)
   - Check battery capacity
   - Monitor temperature sensors

5. **Documentation**
   - Record hardware inventory
   - Document any repairs made
   - Create hardware baseline report
   - Note software version numbers

#### Dependencies
- Physical robot unit
- NAOqi SDK documentation
- Network infrastructure

#### Estimated Duration
- 3–5 days

#### Team Skills Required
- Robotics fundamentals
- Linux system administration
- Hardware troubleshooting
- NAOqi SDK basics

#### Risks
- **Hardware Degradation:** Old robot may have motor or sensor issues
  - *Mitigation:* Perform full diagnostics; consider replacement servos if needed
- **Software Incompatibility:** NAOqi may not work on modern systems
  - *Mitigation:* Use Docker container or VM with compatible OS
- **Network Connectivity:** Robot may not connect reliably
  - *Mitigation:* Use wired Ethernet for initial setup

#### Success Criteria
✓ Robot can perform basic motion sequences  
✓ All 4 microphones and 2 cameras functional  
✓ Network latency <50ms to server  
✓ Battery holds charge for ≥2 hours  
✓ Hardware diagnostic report complete  

#### Demonstration Scenario
- Robot boots successfully
- Perform a pre-recorded motion sequence (e.g., wave hand)
- Streams camera feed over network
- Responds to verbal wake word

---

### Phase 1: Robot Connectivity Layer

**Duration:** 2 weeks  
**Team:** 2 people (backend + systems engineer)  
**Builds on:** Phase 0  
**Status:** Core Infrastructure

#### Objective
Create an abstraction layer that decouples the robot hardware from the AI backend. Establish bidirectional communication (commands to robot, sensor/audio streams from robot).

#### User Value
- Robot can be controlled remotely from any network-connected server
- Sensor data and audio streams available to AI system
- Foundation for all future AI interactions

#### Features Implemented
- Robot API abstraction service
- Motion command execution
- Sensor data aggregation (joint angles, IMU, temperature)
- Audio streaming (microphone → server, server → speaker)
- Video streaming (cameras → server)
- Heartbeat & connection monitoring
- Emergency stop mechanism

#### Technical Architecture

```
Robot ←→ Bridge Service ←→ AI Backend
    (NAOqi API)         (Standardized API)
    
NAO provides raw HAL  →  Bridge normalizes  →  AI receives clean
Choregraphe commands     and packages data      event stream
```

#### Technology Stack

**Robot Side:**
- NAOqi SDK (Python)
- ROS2 (Humble distribution) - recommended for modern robotics
- Or: Custom Python service with WebSocket/MQTT

**Server Side:**
- Python 3.9+ with async support (asyncio, FastAPI)
- WebSocket or gRPC for real-time bidirectional communication
- Redis for command queueing and state cache
- Protocol Buffers for efficient serialization

**Recommendation:** Start with ROS2 for flexibility; fallback to custom Python if team unfamiliar with ROS.

#### Detailed Tasks

1. **ROS2 Bridge Development (Recommended Path)**
   - Set up ROS2 Humble on server and robot
   - Create ROS2 node wrappers for NAOqi
   - Define custom ROS2 message types for NAO sensors
   - Implement motion command subscribers
   - Bridge ROS publishers to HTTP/WebSocket API

2. **Alternative: Custom Python Bridge**
   - Create FastAPI server on local machine
   - Implement NAOqi Python client connection
   - Define REST endpoints for motion commands
   - Implement WebSocket handlers for real-time data
   - Create middleware for state synchronization

3. **Motion Command Execution**
   - Implement synchronous motion execution
   - Add queue for sequential commands
   - Create gesture templates (wave, point, nod, etc.)
   - Add safety limits (joint velocity, temperature)

4. **Sensor Data Streaming**
   - Aggregate joint angle data (22 sensors @ 10Hz)
   - Stream IMU data (accelerometer, gyroscope @ 100Hz)
   - Monitor battery voltage and temperature
   - Collect CPU and memory usage metrics

5. **Audio Pipeline**
   - Capture microphone input (16kHz, mono)
   - Stream to server via WebSocket or MQTT
   - Receive audio output from server
   - Play through robot speakers with volume control

6. **Video Pipeline**
   - Stream front camera (640x480 @ 30fps)
   - Stream bottom camera (640x480 @ 30fps)
   - Implement H.264 compression to reduce bandwidth
   - Add timestamp and sync markers

7. **Connection Management**
   - Heartbeat mechanism (1Hz ping-pong)
   - Automatic reconnection with exponential backoff
   - State cache to handle temporary disconnections
   - Connection status indicator in logs

8. **Safety Systems**
   - E-stop handler (immediate motion halt)
   - Temperature threshold monitoring
   - Joint limit enforcement
   - Watchdog timer (timeout = autonomous disable)

#### Dependencies
- Phase 0 completion (working robot)
- ROS2 Humble (or equivalent)
- Network infrastructure with <100ms latency

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- Python 3 proficiency
- ROS2 fundamentals (or network programming)
- Linux systems administration
- Understanding of real-time systems

#### Risks

- **ROS2 Learning Curve:** Adds complexity if team unfamiliar
  - *Mitigation:* Use custom Python bridge initially; migrate to ROS2 later if needed
  
- **NAOqi Compatibility:** Old NAOqi SDK may have bugs
  - *Mitigation:* Pin to known working version; use Docker for isolation
  
- **Network Latency:** Wireless dropout causing command loss
  - *Mitigation:* Implement command queueing and ACKs; use wired connection for initial setup

#### Success Criteria
✓ Robot responds to motion commands from remote server  
✓ All sensors stream data at >5Hz to server  
✓ Audio captured from microphone and sent to server  
✓ Server can play audio through robot speaker  
✓ Video feeds available at ≥15fps  
✓ Connection state monitored with heartbeat  
✓ Emergency stop halts all motion within 100ms  

#### Demonstration Scenario
- Server sends motion command ("raise left arm")
- Robot executes movement
- Server displays real-time joint angles on console
- User speaks into robot mic; audio appears in server logs
- Server plays pre-recorded audio; robot speaker outputs sound
- Server receives video frames from both cameras

---

### Phase 2: Remote Control Dashboard

**Duration:** 2 weeks  
**Team:** 2 people (frontend + fullstack)  
**Builds on:** Phase 1  
**Status:** First User Interface

#### Objective
Create a web-based control center for teleoperation and monitoring. Provide operators with real-time robot state visualization and manual control capabilities.

#### User Value
- Easy-to-use interface for non-technical operators
- Real-time robot state monitoring
- Safe teleoperation with visual feedback
- Foundation for future autonomous behaviors

#### Features Implemented
- Web dashboard UI (React)
- Live camera feed display
- Robot status panel (battery, temperature, joint angles)
- Manual motion controls (sliders, buttons)
- Emergency stop button
- Motion history log
- Connection status indicator

#### Technical Architecture

```
Web Browser (React)
    ↓ HTTP/WebSocket
FastAPI/Express Server
    ↓ ROS2/Python Bridge
NAO Robot
```

#### Technology Stack

**Frontend:**
- React 18+ with hooks
- Vite.js for bundling
- Socket.io or native WebSocket for real-time updates
- Tailwind CSS for styling
- Chart.js for sensor visualization

**Backend:**
- FastAPI (Python) or Express (Node.js)
- CORS handling for web requests
- Session management for operator logs

#### Detailed Tasks

1. **Project Setup**
   - Initialize React + Vite project
   - Set up routing (Home, Control, Monitoring, Logs)
   - Configure build pipeline
   - Set up environment variables for API endpoint

2. **Robot Connection Panel**
   - Connect/disconnect buttons
   - Connection status indicator (green/red/yellow)
   - Robot IP address input
   - Last heartbeat timestamp
   - Network latency display

3. **Camera View Component**
   - Real-time video stream from front camera
   - Fullscreen toggle
   - Frame rate display
   - Timestamp overlay
   - Record video option (future)

4. **Status Monitor**
   - Battery percentage and voltage graph
   - Temperature gauge (with color coding)
   - CPU/memory usage (if available)
   - Network status (ping, packet loss)
   - Uptime counter

5. **Manual Control Panel**
   - Motion control buttons (forward, backward, turn, stand, sit)
   - Joint sliders for fine control (head pitch/yaw, arm angles)
   - Speed/power adjustment slider
   - Gesture buttons (wave, point, dance)
   - Animation selector with preview

6. **Emergency Stop**
   - Large red button (CSS styled)
   - High-visibility design
   - Confirm dialog to prevent accidental clicks
   - Broadcasts immediate halt command
   - Logs E-stop event with timestamp

7. **Sensor Dashboard**
   - Real-time joint angle visualization (line chart)
   - 3D joint diagram (static, shows current positions)
   - Temperature graph over time
   - Accelerometer readings (3-axis)
   - Gyroscope readings (3-axis)

8. **Log Viewer**
   - Timeline of all commands sent
   - Timestamp, command type, parameters
   - Result status (success/fail)
   - Export logs to CSV
   - Filter by command type

#### Dependencies
- Phase 1 completion (working bridge service)
- Node.js 18+ and npm
- Modern web browser (Chrome, Firefox, Safari)

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- React / JavaScript proficiency
- Web UI/UX design
- CSS and responsive design
- REST API integration
- WebSocket basics

#### Risks

- **Browser WebSocket Restrictions:** CORS or self-signed cert issues
  - *Mitigation:* Use proper certificates; test in multiple browsers
  
- **Real-time Performance:** Latency from network or rendering
  - *Mitigation:* Throttle updates; use efficient rendering (React.memo, virtualization)

#### Success Criteria
✓ Dashboard loads and connects to robot  
✓ Live camera feed displays at ≥15fps  
✓ All sensor readings update in real-time  
✓ Motion commands execute within 100ms of button click  
✓ Emergency stop works from any screen  
✓ Log shows all commands with timestamps  
✓ Responsive design works on tablet (future prep)  

#### Demonstration Scenario
- Open dashboard in web browser
- See live camera feed from robot
- Click "Wave" button; robot waves
- Drag joint slider; robot joint moves smoothly
- Monitor battery voltage dropping in real-time
- Press emergency stop; robot freezes
- View command history in log panel

---

### Phase 3: Speech Pipeline

**Duration:** 2 weeks  
**Team:** 2 people (audio engineer + backend)  
**Builds on:** Phase 1  
**Status:** Audio I/O Complete

#### Objective
Implement bidirectional speech processing: capture voice from user (STT), send to AI backend, and convert AI responses back to speech (TTS).

#### User Value
- Robot can listen and respond to spoken commands
- Natural voice-based interaction without text input
- Foundation for conversational AI

#### Features Implemented
- Speech-to-Text (STT) pipeline
- Text-to-Speech (TTS) synthesis
- Wake word detection (optional)
- Audio input/output level control
- Voice activity detection (VAD)
- Noise handling

#### Technical Architecture

```
Robot Microphone
    ↓ (PCM 16kHz)
Audio Capture Service
    ↓ (WebSocket)
Whisper (STT)
    ↓ (Text)
[AI Backend receives transcription]
    ↓ (Response text)
Piper (TTS)
    ↓ (MP3/WAV)
Audio Playback Service
    ↓ (PCM via NAOqi)
Robot Speaker
```

#### Technology Stack

**Speech-to-Text:**
- OpenAI Whisper (Recommended) - accurate, multilingual, runs locally
- Faster-Whisper (faster variant)
- PocketSphinx (lightweight alternative)

**Text-to-Speech:**
- Piper (ONNX-based, lightweight, natural-sounding)
- Coqui TTS (slower but higher quality)
- XTTS (multi-lingual, expressive)

**Recommendation:** Whisper + Piper for balance of quality and performance.

#### Detailed Tasks

1. **Audio Capture Service**
   - Connect to robot microphone via NAOqi
   - Implement continuous audio streaming (16kHz, 16-bit, mono)
   - Apply noise reduction (optional, may hurt transcription)
   - Implement voice activity detection (VAD) to detect speech
   - Buffer audio chunks and send to STT service

2. **Whisper STT Integration**
   - Download Whisper model (small or medium, ~500MB–1.5GB)
   - Set up inference pipeline
   - Implement batching for multiple audio frames
   - Add confidence scoring
   - Handle multilingual input
   - Cache model in memory for low latency

3. **Whisper Configuration**
   - Choose model size (tiny, base, small, medium, large)
   - Recommendation: **medium** for accuracy without extreme latency
   - Set language explicitly for faster inference
   - Configure temperature for beam search

4. **Text-to-Speech Pipeline**
   - Download Piper model (lightweight ONNX)
   - Set up TTS inference
   - Handle text preprocessing (punctuation, numbers, abbreviations)
   - Support multiple voices (male, female, different accents)
   - Generate audio at robot speaker sample rate (16kHz or higher)

5. **Audio Output Service**
   - Convert TTS output to NAOqi audio format
   - Control speaker volume (0–100%)
   - Play audio without blocking
   - Queue multiple audio outputs
   - Handle simultaneous speech and motion

6. **Wake Word Detection (Optional, Phase 3.5)**
   - Use lightweight wake word detector (Porcupine, Snowboy, or PocketSphinx)
   - Only send audio to Whisper when wake word detected
   - Reduces bandwidth and latency
   - Customizable wake word

7. **Latency Optimization**
   - Measure STT latency (target: <500ms for phrase)
   - Measure TTS latency (target: <1s for sentence)
   - Profile GPU utilization
   - Cache common responses if needed
   - Streaming STT output if available (Faster-Whisper)

8. **Error Handling**
   - Handle no-speech detection (silence)
   - Manage low confidence transcriptions
   - Fallback responses ("I didn't understand")
   - Log failed transcriptions for debugging

#### Dependencies
- Phase 1 completion (audio streaming from bridge)
- GPU or sufficiently fast CPU (Whisper inference)
- Disk space for models (~2–3GB)

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- Audio signal processing basics
- Python proficiency
- Understanding of speech recognition/synthesis
- Linux/CUDA setup

#### Risks

- **Whisper Latency:** Inference may be slow on CPU
  - *Mitigation:* Use smaller model; enable GPU acceleration; cache outputs
  
- **Noisy Environment:** Robot microphones pick up motor noise
  - *Mitigation:* Apply noise reduction or use directional microphone
  
- **TTS Quality:** Piper voices may sound robotic
  - *Mitigation:* Evaluate multiple models; tune prosody parameters

#### Success Criteria
✓ User speaks; robot captures audio and sends to server  
✓ Whisper transcribes with >80% accuracy in quiet room  
✓ Server receives transcription within 1 second  
✓ Text responses converted to speech via Piper  
✓ Robot plays audio with natural-sounding voice  
✓ Average end-to-end latency <2 seconds  
✓ Handles background noise reasonably well  

#### Demonstration Scenario
- Start speech pipeline
- User says "Hello"
- Robot's microphone captures audio
- Server transcribes: "Hello"
- Server generates response: "Hi there!"
- Piper converts to speech
- Robot speaker says: "Hi there!"
- Process completes within 2 seconds

---

### Phase 4: Local LLM Integration

**Duration:** 3 weeks  
**Team:** 2–3 people (AI engineer + backend)  
**Builds on:** Phase 3  
**Status:** Conversational AI Online

#### Objective
Integrate a locally-hosted Large Language Model to provide intelligent conversational capabilities. Build memory system to maintain context across interactions.

#### User Value
- Robot engages in meaningful conversations
- Remembers context and prior exchanges
- Can answer questions about provided knowledge
- Foundation for embodied AI reasoning

#### Features Implemented
- Local LLM deployment
- Conversation memory (short-term and long-term)
- Session-based context management
- User profiles
- Response generation with personality
- Temperature and sampling control

#### Technical Architecture

```
User Speech → Transcription → LLM with Memory → Response Generation → TTS
                                      ↓
                            ChromaDB (future: embeddings)
```

#### Technology Stack

**Language Model:**
- **Llama 2 (13B)** - Recommended starting point
  - Strong performance, good community support
  - ~26GB VRAM required (or CPU with 64GB RAM)
  
- **Mistral 7B** - Lightweight alternative
  - Faster inference, good quality
  - ~16GB VRAM required
  
- **Qwen 1.5 (7B–14B)** - Excellent for conversations
  - Chinese + English support
  - Strong instruction-following
  
- **Recommendation:** Start with Mistral 7B for speed; upgrade to Llama 13B for quality

**Inference Engine:**
- Ollama (simplest, recommended for prototyping)
- llama.cpp (optimized C++ implementation)
- vLLM (high-performance serving with batching)
- LM Studio (GUI-based, beginner-friendly)

**Memory Storage:**
- In-memory Python dict (session-based)
- SQLite (persistent storage, lightweight)
- PostgreSQL (scalable, full-featured)
- Recommendation: SQLite initially, migrate to PostgreSQL if scaling

**Memory Management:**
- Prompt-based context (summary of prior messages)
- Sliding window of recent messages
- User-specific prompts and personality
- Session isolation

#### Detailed Tasks

1. **LLM Deployment with Ollama**
   - Install Ollama on server
   - Download and load Mistral 7B model
   - Verify inference works and measure latency
   - Configure GPU or CPU offloading
   - Create inference wrapper in Python

2. **Inference Pipeline**
   - Build FastAPI endpoint for text generation
   - Implement streaming responses for lower latency
   - Add temperature and top_k controls
   - Handle long sequences (context window ~2000 tokens)
   - Add timeout protection (max 30s per response)

3. **Memory System - Short-term**
   - Store current conversation in memory
   - Keep last 5–10 exchanges (user + bot)
   - Implement as list of dictionaries
   - Clear on session end

4. **Memory System - Long-term**
   - Create SQLite schema for conversations
   - Store session metadata (timestamp, user, topic)
   - Log all exchanges with context
   - Implement message retrieval by session

5. **User Profiles**
   - Define user schema (name, preferences, interaction history)
   - Implement user lookup/creation
   - Store personality traits and communication style
   - Adapt responses based on user profile

6. **Prompt Engineering**
   - Design system prompt for robot personality
   - Create context injection format
   - Include conversation history in prompt
   - Add safety guardrails (prevent harmful responses)
   - Template for different conversational modes

7. **Conversation Manager**
   - Accept transcribed text as input
   - Build prompt with context and history
   - Call LLM with streaming
   - Stream response back to speech synthesis
   - Log exchange to database

8. **Response Quality Improvements**
   - Implement response truncation (max length)
   - Add postprocessing (clean up formatting)
   - Handle edge cases (empty response, malformed output)
   - Add retry logic for failures
   - Implement response caching for common queries

9. **Performance Optimization**
   - Measure inference latency (target: <3s per response)
   - Profile memory usage
   - Implement batch inference if needed
   - Cache embeddings for fast retrieval (Phase 7)

#### Dependencies
- Phase 3 completion (speech pipeline)
- GPU with ≥12GB VRAM (or CPU with 64GB RAM)
- 50GB+ disk space for models
- ~30GB RAM total system memory

#### Estimated Duration
- 15–21 days

#### Team Skills Required
- LLM fundamentals and prompt engineering
- Python FastAPI or Flask
- Database design (SQL)
- Performance profiling
- Understanding of inference optimization

#### Risks

- **Inference Latency:** Model may be too slow for real-time conversation
  - *Mitigation:* Start with Mistral 7B; use quantization (4-bit); implement streaming
  
- **VRAM Requirements:** Model may not fit in GPU memory
  - *Mitigation:* Use smaller model or CPU offloading; quantize weights
  
- **Hallucination:** LLM may generate plausible but false information
  - *Mitigation:* Implement confidence scoring; add information retrieval (Phase 7)
  
- **Safety:** Model may produce inappropriate responses
  - *Mitigation:* Add content filters; review logs; tune system prompt

#### Success Criteria
✓ User can have multi-turn conversation with robot  
✓ Robot responds to at least 5 consecutive exchanges  
✓ Conversation memory maintained across 10+ turns  
✓ Average response time <3 seconds  
✓ Responses are contextually relevant  
✓ Robot maintains consistent "personality"  
✓ No hallucinations on factual claims (yet)  

#### Demonstration Scenario
1. **Turn 1:**
   - User: "What's your name?"
   - Robot: "I'm NAO, a friendly research robot."

2. **Turn 2:**
   - User: "What can you do?"
   - Robot: "I can listen, speak, move, and learn about the world. I can answer questions and have conversations."

3. **Turn 3:**
   - User: "My name is Alice. Nice to meet you."
   - Robot: "Nice to meet you too, Alice!"

4. **Turn 4:**
   - User: "Who am I?"
   - Robot: "You're Alice! We just met a moment ago."

5. **Turn 5:**
   - User: "Can you tell me a joke?"
   - Robot: "Why did the robot go to school? To improve its AI-Q!"

---

### Phase 5: Embodied AI Behaviors

**Duration:** 3 weeks  
**Team:** 2–3 people (motion engineer + AI engineer)  
**Builds on:** Phase 4  
**Status:** Motion-Aware AI

#### Objective
Synchronize robot motion with conversational AI. Create gesture library and intelligent gesture selection based on conversational context.

#### User Value
- Robot gestures naturally while speaking
- Movements reinforce emotional content
- More engaging and human-like interaction
- Demonstrates embodied cognition research

#### Features Implemented
- Gesture library (20+ gestures)
- Gesture synthesis system
- Motion-speech synchronization
- Emotion-based gesture selection
- Idle behaviors and micro-expressions
- Animation blending

#### Technical Architecture

```
LLM Response
    ↓
Intent Analysis (Question? Statement? Command?)
    ↓
Emotion Extraction (Happy, Sad, Confused, Excited?)
    ↓
Gesture Selector (What gesture fits?)
    ↓
Gesture Executor + TTS
    ↓
Robot Motion + Speech (Synchronized)
```

#### Technology Stack

- **Gesture Authoring:** Choregraphe (for pre-built NAO behaviors) or Python API
- **Motion Executor:** Motion command queuing system
- **Synchronization:** Frame-based timing with TTS output duration
- **Animation Library:** Pre-recorded sequences stored as JSON/YAML

#### Detailed Tasks

1. **Gesture Library Definition**
   - Catalog NAO's natural movement capabilities
   - Record 20–30 distinct gestures:
     - **Affirmative:** nod, wave, thumbs up
     - **Negative:** shake head, shrug, raise hands
     - **Emotional:** smile (LED), sad, excited, confused
     - **Pointing:** point left/right/down/up
     - **Greeting:** wave, bow, dance
     - **Listening:** lean in, tilt head
     - **Thinking:** hand on chin, look up
   - Capture motion as joint angle sequences
   - Add timing information (duration in seconds)

2. **Gesture Executor Service**
   - Create gesture playback engine
   - Implement smooth motion interpolation between joints
   - Handle simultaneous head and arm motions
   - Queue multiple gestures
   - Add speed/intensity scaling

3. **Gesture-Response Mapping**
   - Define rules for when to use each gesture
   - Examples:
     - Question detected → head tilt, "listening" posture
     - Affirmative response → nod, positive energy
     - Explanation given → open-hand gesture, forward lean
     - Greeting → wave with smile (LED)
   - Implement mapping in decision system

4. **Motion-Speech Synchronization**
   - Receive TTS duration before playing audio
   - Select gesture that completes within audio duration
   - Blend gestures if multiple needed
   - Start gesture before speech begins
   - Idle position by speech end

5. **Emotion Extraction from LLM**
   - Add emotion classification to LLM response
   - Classify: neutral, positive, negative, curious, excited
   - Use either:
     - Separate emotion classification call
     - Prompt engineering (ask LLM for emotion)
     - Zero-shot sentiment analysis (small transformer)
   - Map emotion to gesture intensity and LED color

6. **LED Control**
   - Control head LEDs (RGB)
   - Map emotions to colors:
     - Happy → yellow/gold
     - Sad → blue
     - Thinking → white
     - Excited → flashing green
   - Blink patterns for attention

7. **Idle Behaviors**
   - Implement subtle movements when not speaking
   - Head micro-movements (±5 degrees)
   - Breathing motion (gentle torso sway)
   - Blink simulation (LED pulses)
   - Frequency: 1–2 per minute

8. **Gesture Blending**
   - Create smooth transitions between gestures
   - Avoid jerky movements
   - Implement fade-in/fade-out for overlapping gestures
   - Joint velocity limits (safety)

9. **Performance Optimization**
   - Pre-compute gesture joint sequences
   - Store as efficient binary format
   - Load all gestures at startup
   - Execution at ≥30Hz for smooth motion

#### Dependencies
- Phase 4 completion (LLM integration)
- Phase 1 completion (motion control)
- Choregraphe or Python NAOqi docs
- Gesture motion capture data

#### Estimated Duration
- 15–21 days

#### Team Skills Required
- Robotics motion planning
- Gesture design and kinesthetics
- Python with asyncio for concurrent motion/speech
- Understanding of natural human gestures

#### Risks

- **Gesture Library Capture:** Time-consuming to record many gestures
  - *Mitigation:* Start with 10 core gestures; expand incrementally
  
- **Synchronization Complexity:** Audio and motion may drift
  - *Mitigation:* Use frame-based timing; test with various speeds
  
- **Uncanny Valley:** Jerky or unnatural gestures may be off-putting
  - *Mitigation:* Smooth motion curves; test with real users; iterate

#### Success Criteria
✓ Robot performs at least 10 distinct gestures  
✓ Gestures complete within expected time  
✓ Gesture selection matches conversation type  
✓ Motion synchronized with speech (±200ms)  
✓ Smooth, natural-looking movements  
✓ LEDs change color with emotion  
✓ Idle behaviors visible when not speaking  

#### Demonstration Scenario
1. **Question:**
   - User: "What is the capital of France?"
   - Robot tilts head, leans forward (listening pose)
   - Response: "The capital of France is Paris."
   - Robot nods while speaking

2. **Explanation:**
   - User: "Explain photosynthesis."
   - Robot opens arms (receptive pose)
   - Provides detailed explanation
   - Gestures with hand movements during explanation

3. **Greeting:**
   - User: "Hi NAO, how are you?"
   - Robot waves enthusiastically
   - LED lights up yellow (happy)
   - Response: "Hi! I'm doing great!"

---

### Phase 6: Digital Twin

**Duration:** 2 weeks  
**Team:** 2 people (3D graphics + backend)  
**Builds on:** Phase 5  
**Status:** Visualization Layer

#### Objective
Create a real-time 3D representation of the NAO robot in a web browser. Visualize robot state and demonstrate motion synchronously with physical robot.

#### User Value
- Understand robot state at a glance
- Verify motion before/after execution
- Educational visualization of robotics
- Debugging tool for motion issues

#### Features Implemented
- Real-time 3D model of NAO robot
- Joint angle synchronization
- Motion replay functionality
- Multiple camera angles
- Wireframe and shaded rendering modes
- Performance metrics overlay

#### Technical Architecture

```
Robot Bridge
    ↓ (Joint angles @ 10Hz)
WebSocket / HTTP
    ↓
Web Dashboard
    ↓ (Three.js rendering)
3D Digital Twin
    ↓ (WebGL canvas)
Browser Display
```

#### Technology Stack

**3D Rendering:**
- **Three.js** (Recommended) - most popular, good NAO community examples
- **Babylon.js** - alternative with similar features
- **Cesium.js** - more complex, better for larger scenes

**NAO Model:**
- URDF (Unified Robot Description Format) - standard for ROS
- Export NAO URDF from Choregraphe or NAOqi
- Convert to Three.js-compatible format (glTF or OBJ)
- Or: Use community NAO model from GitHub

**Physics (Optional):**
- Cannon.js (for future collision detection)
- Not needed for visualization-only phase

#### Detailed Tasks

1. **Obtain NAO 3D Model**
   - Source options:
     - Aldebaran/SoftBank official STL files (if available)
     - Community models from GitHub
     - Create from scratch using Blender (fallback)
   - Convert to glTF format for Three.js
   - Verify joint alignment with physical robot

2. **Three.js Scene Setup**
   - Create 3D scene with proper lighting
   - Add ground plane
   - Position camera with orbit controls
   - Implement zoom/pan/rotate
   - Add lighting (directional + ambient)

3. **Robot Model Loading**
   - Load glTF model into scene
   - Verify visual appearance
   - Test joint naming convention
   - Confirm scale (physical coordinates)

4. **Joint Synchronization**
   - Parse incoming joint angle data
   - Update Three.js joint rotations
   - Handle kinematic chain correctly
   - Interpolate between frames for smooth animation
   - Support 22 NAO joints (head, arms, legs, torso)

5. **Real-time Update Loop**
   - Receive joint data at 10Hz
   - Update Three.js transforms
   - Render at 60Hz (decoupled from data rate)
   - Implement interpolation for smooth display

6. **Multiple Camera Views**
   - Implement preset camera angles:
     - Front view
     - Side view
     - Top view
     - Isometric view
     - Free orbit
   - Allow user to switch between views

7. **Rendering Modes**
   - Shaded (default, realistic colors)
   - Wireframe (shows skeleton)
   - Joint-only (debugging)
   - Heatmap (joint speed or temperature)

8. **Motion Recording & Replay**
   - Record joint trajectory over time
   - Store as JSON (time, joint angles)
   - Implement playback controls (play, pause, rewind)
   - Timeline scrubber for frame-by-frame review

9. **Performance Optimization**
   - Target 60 FPS rendering
   - LOD (level-of-detail) for complex geometry
   - Frustum culling (only render visible parts)
   - Monitor GPU/CPU usage
   - Profile rendering bottlenecks

10. **Debugging Features**
    - Display joint angles as text overlay
    - Show target vs. actual angles
    - Joint velocity indicators
    - Temperature color coding
    - Latency indicator

#### Dependencies
- Phase 5 completion (working robot motion)
- NAO 3D model (STL/glTF files)
- React web dashboard infrastructure

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- 3D graphics and Three.js
- WebGL and shader basics
- Robotics kinematics
- JavaScript and React
- Blender (optional, for model conversion)

#### Risks

- **Model Accuracy:** 3D model may not match physical robot
  - *Mitigation:* Calibrate model with physical measurements; compare side-by-side
  
- **Performance:** 3D rendering may be slow on older browsers
  - *Mitigation:* Optimize geometry; test across browsers; implement LOD

#### Success Criteria
✓ NAO 3D model displays in web browser  
✓ Joint angles update in real-time (≥30fps)  
✓ Digital twin matches physical robot pose  
✓ Can orbit camera around model  
✓ Motion replay works correctly  
✓ Performance stable for 5+ minute sessions  

#### Demonstration Scenario
1. Open dashboard
2. See 3D robot model in center of screen
3. Issue a motion command (e.g., "Raise left arm")
4. Physical robot moves
5. Digital twin updates in sync, showing same pose
6. User rotates view to see motion from different angle
7. Pause motion and examine digital twin from all sides

---

### Phase 7: RAG System

**Duration:** 2 weeks  
**Team:** 2 people (backend + data engineer)  
**Builds on:** Phase 4  
**Status:** Knowledge Integration

#### Objective
Implement Retrieval-Augmented Generation (RAG) to allow the AI to cite sources and answer questions based on uploaded documents.

#### User Value
- Robot can answer questions about provided knowledge
- Reduces hallucinations through grounded responses
- Foundation for educational use cases
- Supports domain-specific knowledge

#### Features Implemented
- Document ingestion pipeline
- Embedding generation
- Vector search capability
- Context retrieval and ranking
- Integration with LLM for grounded responses

#### Technical Architecture

```
Documents (PDF, DOCX, TXT)
    ↓
Text Extraction & Chunking
    ↓
Embedding Model (nomic-embed-text)
    ↓
Vector Database (ChromaDB)
    ↓
Query
    ↓
Semantic Search
    ↓
Retrieved Context + LLM Prompt
    ↓
Grounded Response
```

#### Technology Stack

**Embedding Model:**
- **all-MiniLM-L6-v2** (Recommended) - lightweight, good quality
  - 22MB model size
  - 384-dimensional embeddings
  - Fast inference
  
- **nomic-embed-text** - specifically trained for retrieval
  
- **jina-base-en** - longer context window

**Vector Database:**
- **ChromaDB** (Recommended) - simple, good for <1M vectors
  - Can run in-process or as separate service
  - Persistent storage
  - Good for prototyping
  
- **Qdrant** - more robust, better for scale
  - Binary quantization support
  - Better performance at scale
  
- **FAISS** - ultra-lightweight, CPU-only

**Document Processing:**
- PyPDF for PDF extraction
- python-docx for DOCX
- Langchain for unified interface

#### Detailed Tasks

1. **Environment Setup**
   - Install ChromaDB and dependencies
   - Initialize vector database
   - Set up persistent storage directory
   - Test embedding model loading

2. **Document Ingestion Pipeline**
   - Implement document upload endpoint
   - Extract text from PDF (PyPDF2 or pdfplumber)
   - Extract text from DOCX (python-docx)
   - Plain text file support
   - Create metadata (filename, upload date, source)

3. **Text Chunking Strategy**
   - Split documents into ~512-token chunks
   - Maintain sentence boundaries
   - Overlap chunks by ~50 tokens for context
   - Preserve paragraph structure
   - Add source markers for citation

4. **Embedding Generation**
   - Load sentence-transformer model (all-MiniLM-L6-v2)
   - Generate embeddings for all chunks
   - Cache embeddings to avoid recomputation
   - Batch processing for efficiency
   - Monitor memory usage

5. **Vector Database Integration**
   - Store embeddings in ChromaDB
   - Include chunk text and metadata
   - Implement persistent storage
   - Create indices for fast retrieval
   - Support multiple collections (documents/corpora)

6. **Semantic Search**
   - Query encoding using same embedding model
   - k-NN search in vector space (k=3–5)
   - Implement similarity threshold (filter poor matches)
   - Return ranked results with scores
   - Handle edge cases (empty query, no results)

7. **Context Building**
   - Retrieve top-K relevant chunks
   - Sort by relevance score
   - Concatenate into context string
   - Add source attribution (filename, page number)
   - Manage context length to fit LLM window

8. **LLM Integration with RAG**
   - Modify system prompt to use retrieval context
   - Instruct LLM to cite sources
   - Format: "According to [source], ..."
   - Fallback if no relevant documents found
   - Handle conflicting information

9. **Citation and Attribution**
   - Track which documents provided context
   - Display citations in web UI
   - Implement "source link" feature
   - Show relevance scores
   - Audit trail of retrieved documents

10. **Performance Optimization**
    - Profile embedding generation speed
    - Optimize vector search
    - Cache frequent queries
    - Async document processing
    - Monitor database size

#### Dependencies
- Phase 4 completion (LLM integration)
- Sentence-transformers library
- ChromaDB library
- Document parsing libraries

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- Information retrieval fundamentals
- Vector databases and embeddings
- Document processing
- NLP and semantic search
- Python data pipeline development

#### Risks

- **Retrieval Quality:** Irrelevant documents retrieved
  - *Mitigation:* Fine-tune embedding model; adjust chunk size; test with real documents
  
- **Hallucination Despite RAG:** LLM may ignore retrieved context
  - *Mitigation:* Use stronger instruction prompts; filter low-confidence results
  
- **Scalability:** Slow with many documents
  - *Mitigation:* Migrate to Qdrant; implement batching; optimize embeddings

#### Success Criteria
✓ Users can upload PDF/DOCX documents  
✓ Documents are indexed and searchable  
✓ Queries retrieve relevant context chunks  
✓ LLM provides answers citing sources  
✓ Citations are accurate and traceable  
✓ Search latency <500ms  
✓ Supports 100+ documents  

#### Demonstration Scenario
1. Upload PDF: "Introduction to Machine Learning"
2. Ask robot: "What is a neural network?"
3. System retrieves relevant chunks
4. Robot responds: "According to your learning materials, a neural network is a computing system inspired by biological neural networks..."
5. User asks: "Where did you find that?"
6. Dashboard shows source document and highlighted passage

---

### Phase 8: Document Intelligence UI

**Duration:** 2 weeks  
**Team:** 2 people (frontend + backend)  
**Builds on:** Phase 7  
**Status:** Document Management Interface

#### Objective
Create a web interface for document upload, browsing, and interactive question-answering with visual feedback.

#### User Value
- Easy document management
- Interactive learning through Q&A
- Transparent information retrieval
- Support for multiple document types

#### Features Implemented
- Document upload interface
- Document list and browser
- Metadata display (upload date, size, chunk count)
- Document-specific Q&A
- Source highlighting
- Delete/manage documents

#### Technical Architecture

```
Web UI (React)
    ↓
FastAPI Backend
    ↓
Document Management Service
    ↓
ChromaDB
    ↓
Vector Search
```

#### Technology Stack

- React components for file upload
- Drag-and-drop interface
- PDF.js for PDF preview
- Table components for document list
- Modal dialogs for Q&A

#### Detailed Tasks

1. **Document Upload Component**
   - File input with drag-and-drop
   - Support for PDF, DOCX, TXT, PPT
   - Progress indicator during upload
   - Error handling with user feedback
   - File size validation

2. **Document List View**
   - Table showing all uploaded documents
   - Columns: filename, upload date, size, chunk count
   - Search/filter functionality
   - Sort by name/date/size
   - Actions: View, Q&A, Delete

3. **Document Preview**
   - PDF.js integration for PDF preview
   - Page-by-page navigation
   - Highlight retrieved chunks
   - Show chunk boundaries
   - Zoom controls

4. **Q&A Interface**
   - Text input for questions
   - "Ask Document" button
   - Results panel showing:
     - Answer text
     - Retrieved chunks
     - Relevance scores
     - Source page/location
   - History of asked questions

5. **Source Highlighting**
   - Visual indication of which chunks provided answer
   - Color-coding for relevance
   - Click to jump to source in document
   - Side-by-side view (question + answer + source)

6. **Document Management**
   - Delete document with confirmation
   - Update document metadata
   - Re-index document if needed
   - Bulk operations (delete multiple)
   - Export chunk list to CSV

7. **Integration with Chat**
   - Option to include specific documents in conversation
   - Scope RAG to specific documents
   - Display which document is being referenced
   - Easy navigation between chat and documents

#### Dependencies
- Phase 7 completion (RAG system)
- React dashboard
- FastAPI backend with document endpoints

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- React component development
- File upload handling
- REST API design
- PDF.js or similar
- UI/UX design

#### Success Criteria
✓ Users can upload documents via drag-and-drop  
✓ Document list displays all uploaded files  
✓ Can ask questions about specific documents  
✓ Retrieved chunks highlighted in source  
✓ Search and filter work correctly  
✓ Delete removes document and embeddings  
✓ UI responsive on desktop and tablet  

#### Demonstration Scenario
1. Open "Document Intelligence" tab
2. Drag PDF into upload area
3. Document appears in list
4. Click "Ask" on document
5. Type: "What are the main topics?"
6. Robot summarizes document
7. Click on highlighted chunk
8. View source PDF at that location

---

### Phase 9: Presentation Assistant

**Duration:** 2 weeks  
**Team:** 2 people (frontend + backend)  
**Builds on:** Phase 8  
**Status:** Educational Presentation Mode

#### Objective
Enable the robot to act as a presentation assistant. Convert documents into slides and have the robot present content with synchronized gestures.

#### User Value
- Robot becomes interactive teaching tool
- Transforms documents into engaging presentations
- Suitable for educational demos and lectures
- Novel application of embodied AI

#### Features Implemented
- Slide generation from documents
- Presentation mode interface
- Speaker notes generation
- Synchronized robot presentation
- Next/previous slide control
- Slide preview and editing

#### Technical Architecture

```
Document → LLM Slide Generation → Slides + Speaker Notes
                                            ↓
                                    Presentation Mode
                                            ↓
                                   Robot Presentation
                                   (Motion + Speech)
```

#### Technology Stack

- Reveal.js or Slidy for presentation framework
- react-reveal or custom carousel for slide display
- LLM for slide generation (existing Llama/Mistral)

#### Detailed Tasks

1. **Slide Generation Pipeline**
   - Receive document content
   - Call LLM with prompt: "Create 5-10 educational slides about..."
   - Parse LLM output to extract:
     - Slide title
     - Bullet points
     - Key concepts
   - Structure as JSON array
   - Store generated presentation

2. **Slide Format Definition**
   ```json
   {
     "slides": [
       {
         "title": "Introduction to AI",
         "content": [
           "Artificial Intelligence is the field of computer science...",
           "Key applications: ...",
           "Future potential: ..."
         ],
         "notes": "Talk about historical context..."
       }
     ]
   }
   ```

3. **Presentation Mode UI**
   - Large slide display area
   - Title and content visible
   - Current slide number
   - Previous/next buttons
   - Fullscreen toggle
   - Speaker notes (hidden from audience, visible to presenter)

4. **Speaker Notes**
   - Auto-generated or custom notes
   - Appear only in presenter view
   - Include timing suggestions
   - Talking points
   - Transitions to next slide

5. **Robot Presentation Control**
   - Synchronize robot speech with slides
   - Robot reads speaker notes out loud
   - Robot gestures during presentation
   - Gesture selection based on content
   - Button to have robot advance slides

6. **Interactive Elements (Phase 9.5)**
   - Pause for questions
   - Answer questions using RAG context
   - Robot can return to previous slide if asked
   - Real-time Q&A during presentation

7. **Presentation History**
   - Save generated presentations
   - List of past presentations
   - Replay functionality
   - Edit slides after generation
   - Share presentations (export to PDF)

8. **Voice Control (Optional)**
   - Voice commands to advance slides
   - "Next slide", "Previous slide", "Show speaker notes"
   - Voice-controlled Q&A

#### Dependencies
- Phase 8 completion (document UI)
- Phase 5 completion (embodied behaviors)
- LLM for slide generation

#### Estimated Duration
- 10–14 days

#### Team Skills Required
- Frontend design for presentations
- LLM prompt engineering
- Speech synchronization
- React component state management

#### Risks

- **Slide Quality:** LLM-generated slides may lack visual appeal
  - *Mitigation:* Implement slide editing; use templates; review before presentation
  
- **Synchronization:** Robot speech may not align with gesture timing
  - *Mitigation:* Test extensively; use explicit timing markers

#### Success Criteria
✓ Can generate presentation from document  
✓ Display slides in presentation mode  
✓ Robot reads speaker notes out loud  
✓ Advance slides with button clicks  
✓ Robot performs gestures during presentation  
✓ At least 5-10 slides generated reliably  

#### Demonstration Scenario
1. Upload document: "Climate Change 101"
2. Click "Generate Presentation"
3. 8 slides created with title and talking points
4. Click "Present with NAO"
5. Robot displays first slide and begins:
   - "Welcome to Climate Change 101."
   - Gestures to indicate greeting
6. Click "Next Slide"
7. Robot transitions and explains next topic
8. Continue through presentation
9. Finish and save presentation

---

### Phase 10: Advanced Embodied AI

**Duration:** 3 weeks  
**Team:** 2–3 people (AI engineer + systems)  
**Builds on:** Phase 5, 4  
**Status:** Enhanced Interaction

#### Objective
Implement advanced AI capabilities: emotional awareness, multi-turn context understanding, persistent learning, and adaptive responses.

#### User Value
- Robot responses adapt to user mood and context
- Learning from interactions improves future responses
- More natural, dynamic conversations
- Research platform for embodied cognition

#### Features Implemented
- Emotion detection and expression
- Long-term user learning (preferences, habits)
- Context persistence across sessions
- Adaptive response generation
- Confidence scoring and uncertainty expressions
- Multi-agent coordination (future prep)

#### Technical Architecture

```
User Input → Emotion Analysis → LLM with Adaptive Prompt → Response
                                    ↓
                            User Profile Update
                                    ↓
                        Database (persistent memory)
```

#### Technology Stack

- Emotion classification model (transformer-based)
- User database (PostgreSQL or SQLite)
- Enhanced prompt templates with user context
- Confidence estimation module

#### Detailed Tasks

1. **Emotion Classification**
   - Integrate sentiment/emotion model
   - Options:
     - Distilbert-base-uncased-finetuned-emotion
     - goEmotions model
     - Fine-tune on domain-specific data
   - Classify user input into: happy, sad, angry, neutral, confused
   - Also detect robot's emotional state based on context

2. **User Profile System**
   - Schema: user ID, name, preferences, interaction history
   - Track:
     - Favorite topics
     - Communication style (formal/casual)
     - Preferred gesture styles
     - Technical level (novice/advanced)
   - Update profile based on interactions

3. **Persistent User Memory**
   - Store long-term facts about user
   - Examples:
     - "User is interested in machine learning"
     - "User prefers technical explanations"
     - "User has interacted 50+ times"
   - Retrieve and include in context
   - Limit to top 5–10 most relevant facts

4. **Adaptive Prompt Engineering**
   - Dynamic system prompt based on:
     - User emotion
     - User preferences
     - Current topic
     - Interaction count
   - Examples:
     - Sad user → more empathetic responses
     - New user → simpler explanations
     - Technical user → deeper technical content

5. **Confidence Scoring**
   - Measure LLM confidence in response
   - Implement through:
     - Token probability averaging
     - Ensemble methods
     - Semantic consistency checks
   - Express uncertainty in language:
     - High confidence: "I'm sure..."
     - Medium: "I think..."
     - Low: "I'm not certain, but..."

6. **Learning from Feedback**
   - User provides positive/negative feedback
   - Store as: user ID, context, response, feedback
   - Use to improve future responses
   - Implement simple online learning

7. **Emotional Expression**
   - Map detected emotions to:
     - Speech prosody (pitch, speed, emotion in voice)
     - Gestures (exaggerated for emotions)
     - LED colors and patterns
     - Tone of language (matching user mood)

8. **Multi-turn Context Management**
   - Enhance context window with:
     - User emotion over time
     - Topic continuity
     - User preferences
     - Prior corrections/feedback
   - Maintain conversation coherence over 20+ turns

9. **Uncertainty Expressions**
   - Robot admits when uncertain
   - Offers to search documents
   - Asks clarifying questions
   - Suggests relevant topics

10. **Performance Profiling**
    - Measure response quality
    - Log user satisfaction
    - Track improvement over time
    - Identify common failure modes

#### Dependencies
- Phase 4 completion (LLM integration)
- Phase 5 completion (embodied behaviors)
- User database infrastructure
- Emotion classification model

#### Estimated Duration
- 15–21 days

#### Team Skills Required
- NLP and sentiment/emotion classification
- User modeling and personalization
- Database design
- Prompt engineering expertise
- Learning from human feedback

#### Risks

- **Bias in Emotion Detection:** Model may misclassify emotions
  - *Mitigation:* Use robust models; test across demographics; add manual override
  
- **User Privacy:** Storing user data requires consent and care
  - *Mitigation:* Clear privacy policy; implement data retention limits; anonymization

#### Success Criteria
✓ Emotion detected from user input  
✓ User profiles created and updated  
✓ Robot adapts response tone to emotion  
✓ Long-term facts about user remembered  
✓ Confidence expressed appropriately  
✓ Learning from feedback improves responses  

#### Demonstration Scenario
1. **Session 1:**
   - New user approaches robot
   - Robot: "Hi! I'm NAO. I don't think we've met. What's your name?"
   - Learns user is interested in AI

2. **Session 2 (next day):**
   - Same user returns, seems happy
   - Robot: "Hi Sarah! Great to see you again! You mentioned you were interested in AI yesterday. Want to continue learning?"
   - User: "Sure, but I'm confused about transformers."
   - Robot detects sadness/confusion
   - Responds with extra explanation and encouraging gesture

3. **Session 3 (week later):**
   - User appears sad
   - Robot detects emotion
   - Responds: "Hi Sarah. I notice you seem a bit down today. Would you like to talk about something, or would some uplifting conversation help?"
   - Adopts more empathetic tone
   - User mentions frustration with work
   - Robot offers supportive gestures and understanding

---

### Phase 11: Research Platform

**Duration:** Ongoing (1–2 people)  
**Builds on:** Phase 10  
**Status:** Community & Extension

#### Objective
Stabilize the platform, create comprehensive documentation, establish APIs for researchers, and enable community contributions.

#### User Value
- Reusable platform for embodied AI research
- Reference implementation for robotics education
- Integration point for emerging AI techniques
- Community contributions and improvements

#### Features Implemented
- Public GitHub repository
- API documentation (OpenAPI/Swagger)
- Research publication examples
- Extension framework for modules
- Contribution guidelines
- Academic citing information

#### Technical Architecture

```
Public API ← Stable Core ← Community Extensions
    ↓
Research Projects
    ↓
Papers and Publications
```

#### Technology Stack

- Sphinx or MkDocs for documentation
- OpenAPI specification
- GitHub Actions for CI/CD
- Docker containerization

#### Detailed Tasks

1. **Code Organization & Cleanup**
   - Refactor code into modules
   - Remove temporary/debug code
   - Establish code style standards (Black, flake8)
   - Add comprehensive docstrings
   - Create configuration management

2. **API Specification**
   - Document all endpoints
   - Use OpenAPI 3.0 spec
   - Generate Swagger UI
   - Provide example requests/responses
   - Version API (v1, v2, etc.)

3. **Documentation**
   - Installation guide (Docker + bare metal)
   - Quick start tutorial
   - Architecture documentation
   - Component API reference
   - Configuration options
   - Troubleshooting guide
   - Paper/publication guide

4. **Example Notebooks**
   - Jupyter notebooks showing:
     - How to control robot
     - How to use RAG system
     - How to create custom gestures
     - How to train emotion classifier
   - Runnable code samples

5. **Extension Framework**
   - Define plugin architecture
   - Examples:
     - Custom LLM models
     - Custom gesture libraries
     - Custom sensors
   - Plugin registration and discovery
   - Dependency management

6. **Docker Support**
   - Multi-stage Dockerfile
   - Separate images for components
   - Docker Compose for full stack
   - Instructions for GPU support
   - Registry (Docker Hub, GitHub)

7. **CI/CD Pipeline**
   - GitHub Actions for testing
   - Automated linting and formatting
   - Build checks on every PR
   - Documentation build verification
   - Release automation

8. **Contribution Guidelines**
   - Code of conduct
   - Contributing.md with instructions
   - Issue/PR templates
   - Review process
   - Community communication channels

9. **Research Support**
   - Templates for research projects
   - Data collection frameworks
   - Analysis tools
   - Publication guide
   - Open dataset repository

10. **Community Management**
    - GitHub Discussions for Q&A
    - Issues triaging
    - Release notes and changelog
    - Roadmap transparency
    - Quarterly demos/webinars

#### Dependencies
- All prior phases completed
- GitHub repository setup
- Documentation infrastructure

#### Estimated Duration
- 2–3 weeks initial setup
- Ongoing 1–2 people for maintenance

#### Team Skills Required
- Software engineering best practices
- Technical writing
- Community management
- DevOps and CI/CD
- Open-source experience

#### Success Criteria
✓ Code passes linting and tests  
✓ API documentation complete and accurate  
✓ Installation works on clean machine  
✓ At least 3 example notebooks  
✓ Plugin system allows extensions  
✓ GitHub Stars >100 within 6 months  
✓ At least 2 research papers using platform  

---

## Technology Stack Recommendations

### Tier 1: Proven & Recommended

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Robot Communication** | ROS2 Humble | Industry standard, good NAO support, long-term maintenance |
| **Speech-to-Text** | Whisper Medium | Accurate (>80%), multilingual, runs locally, active community |
| **Text-to-Speech** | Piper | Lightweight, natural-sounding, easy to deploy, multiple voices |
| **Local LLM** | Mistral 7B | Best speed/quality balance, good instruction following, <16GB VRAM |
| **LLM Serving** | Ollama | Simple, Mistral integration, good performance, easy setup |
| **Embeddings** | all-MiniLM-L6-v2 | Lightweight, good quality, 22MB model size |
| **Vector Database** | ChromaDB | Simple, embedded option, good for prototyping, persistent storage |
| **Web Framework** | FastAPI | Modern Python, excellent performance, auto OpenAPI docs |
| **Frontend** | React 18 + Vite | Standard, large community, good tooling, performance |
| **3D Graphics** | Three.js | Mature, NAO examples available, good WebGL support |
| **Containerization** | Docker | Standard industry practice, excellent reproducibility |

### Tier 2: Alternative Options (If Tier 1 Unavailable)

| Component | Alternative | Trade-off |
|-----------|-------------|----------|
| **Robot Communication** | Custom Python + WebSocket | More code, but simpler if ROS unfamiliar |
| **Speech-to-Text** | Faster-Whisper | 2–3x faster, slightly lower accuracy |
| **Text-to-Speech** | Coqui TTS | Higher quality, slower inference |
| **Local LLM** | Llama 2 13B | Better quality, needs 26GB VRAM |
| **Vector Database** | Qdrant | Better scale, more complex deployment |
| **Frontend** | Vue.js 3 or Svelte | Smaller learning curve, similar capabilities |
| **3D Graphics** | Babylon.js | Similar capabilities to Three.js |

### Recommended Hardware Specs

```
Minimum Viable:
- CPU: Intel i7 / AMD Ryzen 7 (8 cores)
- RAM: 16GB
- GPU: NVIDIA GTX 1660 (6GB VRAM) or AMD RX 6600
- Storage: 256GB SSD (OS + models)
- Network: 1Gbps Ethernet

Recommended (Optimal):
- CPU: Intel i9 / AMD Ryzen 9 (16 cores)
- RAM: 32GB
- GPU: NVIDIA RTX 4070 (12GB VRAM) or RTX 4080 (16GB)
- Storage: 1TB NVMe SSD
- Network: WiFi 6 (802.11ax) + Ethernet backup

Budget Alternative:
- Use cloud GPU (RunPod, Lambda Labs) for LLM inference
- Keep smaller local models for real-time responses
- Stream large model predictions
```

---

## Risk Assessment & Mitigation

### Critical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| **NAO Hardware Failure** | Entire project blocked | Medium (old hardware) | Phase 0 diagnostics; maintain spare parts; document repairs |
| **Network Latency** | Poor user experience; unsafe motion | Medium | Use wired Ethernet; implement robust queuing; set safety timeouts |
| **LLM VRAM Exhaustion** | System crashes; unusable | High (Llama 13B) | Start with Mistral 7B; implement quantization; use cloud inference fallback |
| **Inference Latency** | Conversation feels sluggish | Medium-High | Profile bottlenecks; optimize pipeline; implement caching and batching |

### Major Risks

| Risk | Mitigation |
|------|-----------|
| **Integration Complexity** | Modular architecture with clear interfaces; comprehensive testing at each phase |
| **Gesture Uncanny Valley** | User testing early; iterate on gesture library; smooth motion curves |
| **RAG Hallucination** | Source citation; confidence scoring; human review of high-stakes responses |
| **Privacy Concerns** | Clear data retention policies; encrypt user data; local-only deployment |

### Minor Risks

| Risk | Mitigation |
|------|-----------|
| **Library Dependency Updates** | Pin versions; use Docker for reproducibility; regular security scanning |
| **Browser Compatibility** | Test on Chrome, Firefox, Safari; use polyfills if needed |
| **Model Download Failures** | Cache models locally; implement retry logic; document download links |

---

## MVP Definition

### Minimum Viable Product (MVP)

**Scope:** Phases 0–5  
**Duration:** 6–8 weeks  
**Team:** 2–3 people  

**Capabilities:**
- Interactive robot controlled remotely
- Speech-based conversation (listen and respond)
- Synchronized gestures with speech
- Teleoperation dashboard
- Working conversation memory

**Success Metric:** User can have a 5-turn conversation with robot; robot responds to voice commands; motion is synchronized with speech.

### Extended MVP (Phases 0–7)

**Scope:** Phases 0–7  
**Duration:** 12 weeks  
**Team:** 3–4 people  

**Adds:**
- Document upload and retrieval
- Grounded responses with source citation
- Digital twin visualization

**Success Metric:** Robot can answer questions about uploaded documents; responses are grounded in sources.

---

## Development Prioritization

### Critical Path (Do First)

```
Phase 0 (1 week)
    ↓
Phase 1 (2 weeks) ← Foundation for everything
    ↓
Phase 3 (2 weeks) ← Speech is key for user interaction
    ↓
Phase 4 (3 weeks) ← Core conversational AI
    ↓
Phase 5 (3 weeks) ← Embodied AI differentiates project
```

**Dependencies:** 3 → 4 → 5 are tightly coupled.  
**Parallel Work:** Phase 2 (dashboard) can happen in parallel with Phase 3 (speech).

### Recommended Parallel Workstreams

```
Workstream A (Backend):          Workstream B (Frontend):
Phase 1 (Connectivity)           Phase 2 (Dashboard UI)
    ↓                                ↓
Phase 3 (Speech)            +    Phase 6 (Digital Twin)
    ↓                                ↓
Phase 4 (LLM)               +    Phase 8 (Document UI)
    ↓                                ↓
Phase 5 (Behaviors)         ←─── Integrate
    ↓
Phase 7 (RAG)

Total: 18–22 person-weeks with 2 developers
Can be achieved in 12–15 weeks with parallel work
```

---

## Timeline & Resource Allocation

### Summary Timeline

```
Weeks:    1-1    3-4    5-6    7-8    9-11   12-14  15-16  17-18  19-21  22-24  25+
         ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌───┐  ┌───┐  ┌──┐  ┌───┐  ┌───┐  ┌───┐  ┌────┐
Phase:   │0 │→ │1 │→ │2 │→ │3 │→ │ 4 │→ │ 5 │→ │6 │→ │ 7 │→ │ 8 │→ │ 9 │→ │10+ │
         └──┘  └──┘  └──┘  └──┘  └───┘  └───┘  └──┘  └───┘  └───┘  └───┘  └────┘
                │ ├──────────────────────────────┤ │
                │ Phase 2 (Dashboard UI) - Parallel │
                └────────────────────────────────────┘

MVP Completion: Week 8 (Phase 0–4)
Extended MVP: Week 12 (Phase 0–7)
Full Platform: Week 21 (Phase 0–10)
Community-Ready: Week 24+ (Phase 11 ongoing)
```

### Resource Allocation (Per Phase)

| Phase | Developers | Weeks | Person-Weeks | Key Role |
|-------|-----------|-------|--------------|----------|
| 0 | 1 | 1 | 1 | Roboticist |
| 1 | 2 | 2 | 4 | Backend Engineer |
| 2 | 2 | 2 | 4 | Frontend Engineer |
| 3 | 2 | 2 | 4 | Audio Engineer |
| 4 | 2 | 3 | 6 | AI/ML Engineer |
| 5 | 2 | 3 | 6 | Motion Engineer |
| 6 | 2 | 2 | 4 | Graphics Engineer |
| 7 | 2 | 2 | 4 | Data Engineer |
| 8 | 2 | 2 | 4 | Frontend Engineer |
| 9 | 2 | 2 | 4 | AI Engineer |
| 10 | 3 | 3 | 9 | ML Engineer |
| 11 | 1–2 | Ongoing | TBD | DevOps Engineer |
| **TOTAL** | **2–3 avg** | **26 weeks** | **54 PW** | — |

**Interpretation:**
- With 2 full-time developers: 26–27 weeks (6 months)
- With 3 full-time developers: 18–20 weeks (4.5 months)
- With 4 full-time developers: 13–16 weeks (3.5 months)

---

## Future Research Extensions

### Autonomous Navigation (Post-Phase 11)

**Vision:** NAO autonomously navigates campus while performing AI tasks.

**Technologies:**
- LiDAR for mapping (RPLIDAR)
- ROS2 Nav2 stack
- Visual odometry from cameras
- SLAM (Simultaneous Localization and Mapping)

**Use Case:** Autonomous teaching assistant visiting classrooms.

### Vision-Language Models (Post-Phase 11)

**Vision:** Robot "sees" and understands objects, people, scenes.

**Technologies:**
- CLIP or LLaVA for image understanding
- Real-time object detection (YOLOv8)
- Face recognition (with privacy controls)

**Use Case:** Robot describes what it sees; recognizes students.

### Multi-Agent AI (Post-Phase 11)

**Vision:** Multiple NAO robots coordinate and collaborate.

**Technologies:**
- LlamaIndex for agent orchestration
- AutoGen for agent frameworks
- Message passing between robots

**Use Case:** Team of robots co-teaching a classroom.

### Smart Campus Integration (Post-Phase 11)

**Vision:** NAO integrates with building automation, calendar, student records.

**Technologies:**
- REST APIs to campus systems
- Calendar integration (Microsoft 365, Google Calendar)
- Room booking systems
- Student information systems (SIS)

**Use Case:** Robot knows schedule and location; meets students on time.

### Learning Analytics (Post-Phase 11)

**Vision:** Track learning outcomes and robot effectiveness as educator.

**Technologies:**
- Learning management system (LMS) integration
- Pedagogical analytics
- Student engagement metrics

**Use Case:** Measure and improve teaching effectiveness.

### Federated Learning (Post-Phase 11)

**Vision:** Multiple institutions share model improvements without sharing data.

**Technologies:**
- Federated learning frameworks
- Secure aggregation
- Differential privacy

**Use Case:** Collective intelligence across research labs.

---

## Appendix: Key Decisions & Rationale

### Why Not Use Cloud AI?

**Decision:** Keep all computation local.

**Rationale:**
- **Privacy:** Educational institution requires data residency
- **Latency:** Real-time conversation requires <1s round-trip
- **Cost:** Lower long-term cost for continuous operation
- **Reliability:** No internet dependency
- **Control:** Full transparency and customization

### Why ROS2 Over Custom Framework?

**Decision:** Use ROS2 for robot middleware.

**Rationale:**
- **Maturity:** 10+ years of development
- **Community:** Large robotics community; many resources
- **Standardization:** Future researchers familiar with ROS2
- **Extensibility:** Ecosystem of packages (Navigation, Manipulation, Perception)
- **Cost:** Open source and free

**If ROS Unfamiliar:** Custom Python with WebSocket is viable fallback with less time investment.

### Why Mistral 7B Over Llama 13B?

**Decision:** Start with Mistral 7B.

**Rationale:**
- **Speed:** 2x faster inference
- **VRAM:** 16GB vs 26GB requirement
- **Quality:** Sufficient for conversational AI
- **Cost:** Lower hardware requirements

**Upgrade Path:** Easy to migrate to Llama 13B later if needed.

### Why ChromaDB Over Qdrant?

**Decision:** Start with ChromaDB; upgrade to Qdrant if scaling needed.

**Rationale:**
- **Simplicity:** Embed in Python process; no separate service
- **Prototyping:** Faster to get working
- **Data Size:** Sufficient for 100–1000 documents
- **Cost:** No infrastructure overhead

**Scaling Path:** Qdrant offers better performance at scale (1M+ vectors).

---

## Success Metrics & KPIs

### Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Response Latency** | <3 seconds | Average time from user speech end to robot response start |
| **Transcription Accuracy** | >85% | Word error rate in English, quiet environment |
| **Motion Smoothness** | >30 FPS | Frame rate of joint interpolation |
| **System Uptime** | >95% | Percentage of time system available during testing |
| **Speech Naturalness** | >4/5 | User rating of TTS voice quality |
| **Gesture Appropriateness** | >80% | Percentage of gestures rated as fitting by users |

### Research Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Platform Adoption** | >10 research groups | Universities using platform within 12 months |
| **Publications** | 3+ peer-reviewed papers | Using platform or citing work |
| **Code Quality** | Grade A | CodeClimate or SonarQube score |
| **Documentation Coverage** | >90% | Code documented with docstrings |
| **Community Engagement** | 100+ GitHub stars | Community interest indicator |

### Educational Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Student Engagement** | >85% positive | Post-interaction surveys |
| **Learning Outcomes** | Grade improvement | Pre/post test scores (if used as tutor) |
| **Classroom Adoption** | 3+ courses | Courses using robot for teaching |

---

## Conclusion

This roadmap provides a realistic, phased approach to building a modern Embodied AI platform using the NAO Robot V4. The incremental delivery model ensures continuous value and allows for course corrections based on learnings.

**Key Success Factors:**

1. **Small, focused team:** 2–3 full-time developers can achieve all goals in 12–18 months
2. **Incremental delivery:** Each phase produces a working system
3. **Community-first mindset:** Documented, shareable, extensible architecture
4. **Research relevance:** Foundation for cutting-edge embodied AI research
5. **Practical constraints:** Realistic assessment of hardware limitations and timelines

**Next Steps:**

1. Form core team (2–3 developers)
2. Start Phase 0: Robot Assessment (1 week)
3. Proceed to Phases 1–5 for MVP (8 weeks total)
4. Gather feedback from early users
5. Plan extended feature set (Phases 6+) based on priorities

**Expected Outcome:**

By month 6–9, you will have a functional Embodied AI platform suitable for:
- University research projects
- Educational demonstrations
- Technology showcases
- Foundation for future embodied AI research

---

**Document Prepared By:** Embodied AI Project Team  
**Version:** 1.0  
**Last Reviewed:** 2026-06-13  
**Next Review:** 2026-09-13 (after MVP completion)
