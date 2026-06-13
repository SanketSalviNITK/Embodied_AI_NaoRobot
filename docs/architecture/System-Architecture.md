# System Architecture

## Overview

The Embodied AI system is designed with clear separation of concerns across five architectural layers:

1. **Physical Robot** (NAO V4)
2. **Robot Middleware** (Bridge Service)
3. **AI Backend** (Intelligence & Processing)
4. **Web Dashboard** (User Interface)
5. **Integration Layer** (Future Extensions)

## Detailed Architecture

### Layer 1: Physical Robot (NAO V4)

**Responsibilities:**
- Speech capture via microphones
- Audio output via speakers
- Motion execution (22 DoF)
- Sensor data acquisition
- Camera feeds
- Status reporting (battery, temperature)

**Key Systems:**
- Locomotion (walking, standing, sitting)
- Manipulation (arm and hand movements)
- Head movements (gaze control)
- Audio I/O (dual-mic array)
- Vision (2 cameras)
- IMU and accelerometer

### Layer 2: Robot Middleware

**Responsibilities:**
- Standardized robot API abstraction
- Motion command queuing and execution
- Sensor data streaming and aggregation
- Audio/video streaming with compression
- Connection state management
- Safety monitoring and emergency stop

**Technology Options:**
- **Recommended:** ROS2 Humble
- **Alternative:** Custom Python + WebSocket/MQTT
- **Communication:** TCP/UDP, binary protocol for real-time data

**Key Components:**
```
┌─────────────────────────────────────┐
│      ROS2 Bridge / Python Service   │
├─────────────────────────────────────┤
│  Motion   │ Sensors │ Audio  │ Video│
│  Executor │ Streamer│ Bridge │ Comp │
├─────────────────────────────────────┤
│      NAOqi SDK / Hardware API       │
└─────────────────────────────────────┘
```

### Layer 3: AI Backend

**Core Subsystems:**

#### 3a. Conversational AI
- **LLM:** Mistral 7B (default) or Llama 13B (higher quality)
- **Inference:** Ollama or llama.cpp
- **Memory:** Short-term (conversation buffer) + Long-term (database)
- **Context:** User profiles, interaction history

#### 3b. Speech Processing
- **STT:** Whisper (OpenAI) - accurate, multilingual
- **TTS:** Piper - lightweight, natural-sounding
- **VAD:** Voice activity detection
- **Audio I/O:** Bridge to robot speaker/microphone

#### 3c. Motion Control
- **Gesture Synthesis:** Gesture library + executor
- **Animation:** Coordinated arm/head/torso movements
- **Synchronization:** Motion timed to speech output
- **Emotion Mapping:** Gesture selection based on conversational context

#### 3d. Memory System
- **Short-term:** Current conversation context (in-memory)
- **Long-term:** SQLite or PostgreSQL for persistence
- **User Models:** Preferences, interaction history, learning profile
- **Session Management:** Isolated conversation contexts

#### 3e. RAG System (Phase 7+)
- **Embedding Model:** all-MiniLM-L6-v2
- **Vector Database:** ChromaDB (embedded) or Qdrant (distributed)
- **Document Processing:** PDF, DOCX, TXT extraction
- **Semantic Search:** k-NN in embedding space
- **Context Integration:** Retrieved documents inform LLM prompts

**Architecture Diagram:**
```
User Input (Text/Speech)
    ↓
[Speech-to-Text] (Whisper)
    ↓
[Intent Recognition] & [Memory Lookup]
    ↓
[LLM Engine] (Mistral/Llama)
    ├─→ [RAG Retrieval] (ChromaDB)
    └─→ [Context Building] (User profile + history)
    ↓
[Response Generation]
    ├─→ [Gesture Selection]
    ├─→ [Emotion Mapping]
    └─→ [Text-to-Speech] (Piper)
    ↓
[Output Synchronization]
    ├─→ Robot Motion
    ├─→ Robot Speech
    └─→ LED Control
```

### Layer 4: Web Dashboard

**Components:**

#### 4a. Robot Control
- Live camera feed display
- Manual motion controls (sliders, buttons)
- Teleoperation mode
- Emergency stop interface
- Robot state indicator

#### 4b. Monitoring & Analytics
- Real-time sensor display (joint angles, temperature, battery)
- Performance metrics (latency, CPU, memory)
- Connection status
- Historical logs

#### 4c. AI Interface
- Text/voice chat interface
- Conversation history display
- Session management
- Context visibility

#### 4d. Document Intelligence (Phase 8+)
- Document upload interface
- Q&A on documents
- Source attribution
- Document browser

#### 4e. Digital Twin (Phase 6+)
- Real-time 3D robot model
- Joint angle visualization
- Motion playback and replay
- Multiple camera angles

**Technology Stack:**
- **Frontend:** React 18 + Vite
- **3D Graphics:** Three.js
- **Communication:** WebSocket + REST API
- **Styling:** Tailwind CSS

### Layer 5: Integration & Research Extensions

**Future Capabilities:**
- Multi-agent coordination
- Autonomous navigation (LiDAR + SLAM)
- Vision-language models (object detection, scene understanding)
- Campus integration (calendar, room booking)
- Learning analytics
- Federated learning

## Data Flow Diagrams

### Conversation Flow
```
User Voice Input
    ↓ [Capture via Robot Mic]
Audio Stream (16kHz PCM)
    ↓ [Network → Server]
Whisper (STT)
    ↓ [Transcription]
LLM Input Processing
    ├─→ User Profile Lookup
    ├─→ Conversation History
    └─→ RAG Retrieval
    ↓
LLM Response Generation
    ├─→ Gesture Selection
    ├─→ Emotion Detection
    └─→ Piper TTS
    ↓
Output Synchronization
    ├─→ Speech Output [Robot Speaker]
    └─→ Motion Execution [Robot Joints]
```

### Sensor Streaming Flow
```
Robot Sensors (10Hz)
    ├─→ Joint Angles [22 joints]
    ├─→ IMU Data [3-axis]
    ├─→ Temperature
    ├─→ Battery Voltage
    └─→ CPU Usage
    ↓
Sensor Aggregation Service
    ↓
Local Cache (Redis or in-memory)
    ↓
Web Dashboard (WebSocket push)
    ↓
Real-time Visualization
```

## API Boundaries

### Robot Bridge API
**Input:** Motion commands, gesture requests  
**Output:** Sensor data, status, acknowledgment  
**Protocol:** ROS2 services/topics or REST API  

### AI Backend API
**Input:** User text/speech, document queries  
**Output:** Text response, gesture sequence, audio  
**Protocol:** REST API + WebSocket for streaming  

### Web Dashboard API
**Input:** User interactions, queries  
**Output:** Real-time updates, control commands  
**Protocol:** WebSocket (real-time), REST (static)  

## Scalability Considerations

### Current Design (Single Robot)
- Monolithic Python backend
- Embedded vector database
- Single-machine inference

### Future Scaling (Multiple Robots)
- Microservices architecture
- Distributed vector database (Qdrant)
- Inference service (vLLM)
- Message broker (Redis/RabbitMQ)
- Kubernetes orchestration

## Security & Safety

### Safety Mechanisms
- Motion command validation (joint limits, velocity limits)
- Emergency stop (software + hardware)
- Timeout watchdog (robot auto-disables after 5s inactivity)
- Temperature monitoring

### Security Considerations
- Local-only deployment (no external cloud)
- User data encryption at rest
- Network isolation (local network only)
- Input validation and sanitization
- Rate limiting on API endpoints

## Performance Targets

| Component | Metric | Target |
|-----------|--------|--------|
| **Response Latency** | User input → Robot response | <3 seconds |
| **Speech Recognition** | Transcription accuracy | >85% |
| **Motion Execution** | Command → Physical movement | <200ms |
| **Sensor Update Rate** | Joint data streaming | >5Hz |
| **Video Streaming** | Camera feed FPS | ≥15fps |
| **System Uptime** | Availability | >95% |

## Architecture Evolution

### Phase-wise Architecture Growth

```
Phase 0-1: Core Infrastructure
  Robot ←→ Bridge ←→ Backend

Phase 2-3: User Interface + Speech
  Robot ←→ Bridge ←→ Backend ←→ Dashboard
                          ↓
                        Speech

Phase 4-5: Intelligent Interaction
  Robot ←→ Bridge ←→ Backend ←→ Dashboard
                      ↓    ↓
                      LLM  Motion

Phase 6-10: Enhanced Capabilities
  Add: Digital Twin, RAG, Emotions, Learning
  
Phase 11+: Research Platform
  Add: Microservices, APIs, Community extensions
```

## Referenced Documents
- [EMBODIED_AI_ROADMAP.md](../../EMBODIED_AI_ROADMAP.md) - Implementation details
- [Technology-Stack.md](Technology-Stack.md) - Detailed tech choices
- [Robot-Bridge-API.md](../api-reference/Robot-Bridge-API.md) - API specs

---

**Version:** 1.0  
**Last Updated:** 2026-06-13
