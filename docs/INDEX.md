# Embodied AI Project Documentation Index

Welcome to the Embodied AI documentation hub. This directory contains all technical documentation, guides, and specifications for the NAO Robot V4 modernization project.

## Quick Navigation

### 📋 Main Roadmap
- **[EMBODIED_AI_ROADMAP.md](../EMBODIED_AI_ROADMAP.md)** - Complete phased implementation plan with phases 0-11

### 🏗️ Architecture & Design
Navigate to `docs/architecture/` for detailed technical specifications:
- **System Architecture Overview**
- **Layer Descriptions** (Robot, Middleware, AI Backend, Web UI)
- **Data Flow Diagrams**
- **Technology Stack Comparison**
- **Integration Points**

### 📚 Phase Documentation
Each phase has detailed specifications in `docs/phases/`:
- `Phase-0-Robot-Assessment.md`
- `Phase-1-Connectivity.md`
- `Phase-2-Dashboard.md`
- `Phase-3-Speech-Pipeline.md`
- `Phase-4-LLM-Integration.md`
- `Phase-5-Embodied-Behaviors.md`
- `Phase-6-Digital-Twin.md`
- `Phase-7-RAG-System.md`
- `Phase-8-Document-UI.md`
- `Phase-9-Presentation-Assistant.md`
- `Phase-10-Advanced-AI.md`
- `Phase-11-Research-Platform.md`

### 📖 User Guides
Step-by-step guides in `docs/guides/`:
- **Installation & Setup**
- **Robot Hardware Setup**
- **Development Environment**
- **Running Each Component**
- **Troubleshooting**
- **Contributing Guide**

### 🔌 API Reference
Technical API specifications in `docs/api-reference/`:
- **Robot Bridge API** - Motion commands, sensor data
- **AI Backend API** - LLM, speech, memory
- **Web Dashboard API** - Control and monitoring
- **RAG System API** - Document retrieval
- **WebSocket Events** - Real-time updates

### 🔬 Research & Technical Specs
In-depth technical information in `docs/technical-specs/`:
- **NAO V4 Hardware Specifications**
- **ROS2 Message Definitions**
- **Embedding & Vector Database Design**
- **Speech Processing Pipeline**
- **Motion Synthesis Algorithms**
- **Model Quantization & Optimization**

### 📊 Research Resources
Research papers, benchmarks, and evaluation in `docs/research/`:
- **Embodied AI Literature Review**
- **Human-Robot Interaction Studies**
- **Benchmark Results**
- **Performance Metrics**
- **Publication List**

## Folder Structure Overview

```
EmbodiedAI/
├── EMBODIED_AI_ROADMAP.md          ← Start here!
├── docs/
│   ├── INDEX.md                     ← You are here
│   ├── architecture/
│   │   ├── System-Architecture.md
│   │   ├── Layer-Descriptions.md
│   │   ├── Data-Flow.md
│   │   └── Technology-Stack.md
│   ├── phases/
│   │   ├── Phase-0-Robot-Assessment.md
│   │   ├── Phase-1-Connectivity.md
│   │   ├── Phase-2-Dashboard.md
│   │   └── ... (Phase 3-11)
│   ├── guides/
│   │   ├── Installation-Setup.md
│   │   ├── Development-Environment.md
│   │   ├── Running-Components.md
│   │   └── Troubleshooting.md
│   ├── api-reference/
│   │   ├── Robot-Bridge-API.md
│   │   ├── AI-Backend-API.md
│   │   ├── Web-Dashboard-API.md
│   │   └── RAG-System-API.md
│   ├── technical-specs/
│   │   ├── NAO-Hardware-Specs.md
│   │   ├── ROS2-Messages.md
│   │   ├── Embedding-Design.md
│   │   └── Model-Optimization.md
│   └── research/
│       ├── Literature-Review.md
│       ├── HRI-Studies.md
│       ├── Benchmarks.md
│       └── Performance-Metrics.md
├── src/                             ← Source code
│   ├── robot_bridge/
│   ├── ai_backend/
│   ├── web_dashboard/
│   └── rag_system/
├── tests/                           ← Test suites
├── config/                          ← Configuration files
├── examples/                        ← Example scripts & demos
├── scripts/                         ← Utility scripts
└── notebooks/                       ← Jupyter notebooks for research
```

## Getting Started

### For New Team Members
1. Read **[EMBODIED_AI_ROADMAP.md](../EMBODIED_AI_ROADMAP.md)** (Executive Summary + your relevant phase)
2. Read **[docs/guides/Installation-Setup.md](guides/Installation-Setup.md)**
3. Read **[docs/architecture/System-Architecture.md](architecture/System-Architecture.md)**
4. Choose a phase and dive into `docs/phases/Phase-X.md`

### For Project Managers
1. Review **EMBODIED_AI_ROADMAP.md** → Timeline & Resource Allocation section
2. Check **[docs/phases/](phases/)** for detailed breakdowns
3. Review **[docs/research/Performance-Metrics.md](research/Performance-Metrics.md)**

### For Researchers
1. Read **[docs/research/Literature-Review.md](research/Literature-Review.md)**
2. Check **[docs/technical-specs/](technical-specs/)** for implementation details
3. Review **[docs/research/Benchmarks.md](research/Benchmarks.md)**

### For Hardware Engineers
1. Read **[docs/technical-specs/NAO-Hardware-Specs.md](technical-specs/NAO-Hardware-Specs.md)**
2. Check **[docs/phases/Phase-0-Robot-Assessment.md](phases/Phase-0-Robot-Assessment.md)**
3. Review **[docs/guides/Troubleshooting.md](guides/Troubleshooting.md)**

### For Software Engineers
1. Read **[docs/guides/Development-Environment.md](guides/Development-Environment.md)**
2. Check **[docs/architecture/](architecture/)** for system design
3. Review **[docs/api-reference/](api-reference/)** for interface specs

## Key Documents to Complete

The following files are templates/placeholders and need detailed content:

### Priority 1 (Critical - Complete in Phase 0)
- [ ] `docs/guides/Installation-Setup.md` - Hardware setup instructions
- [ ] `docs/guides/Development-Environment.md` - Software environment setup
- [ ] `docs/technical-specs/NAO-Hardware-Specs.md` - Hardware inventory

### Priority 2 (Important - Complete by Phase 2)
- [ ] `docs/architecture/System-Architecture.md` - Detailed diagrams
- [ ] `docs/guides/Running-Components.md` - Step-by-step guides
- [ ] `docs/api-reference/Robot-Bridge-API.md` - Bridge API spec

### Priority 3 (Ongoing)
- [ ] Phase-specific documentation (as each phase is completed)
- [ ] `docs/research/` - Research findings and results
- [ ] `docs/api-reference/` - Additional API specs as implemented

## Contributing to Documentation

### Standards
- Use Markdown format (.md files)
- Include code examples where applicable
- Add diagrams (ASCII or embedded images)
- Update this INDEX when adding new files
- Link to related documents

### Template Structure
Each document should include:
```markdown
# Document Title

## Overview
Brief description of what this document covers.

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1
Content with examples.

## Section 2
Content with diagrams.

## References
Links to related documents.

## Revision History
- 2026-06-13: Initial version (Name)
```

## Communication & Resources

- **Main Roadmap:** [EMBODIED_AI_ROADMAP.md](../EMBODIED_AI_ROADMAP.md)
- **GitHub Repository:** (Link to be added)
- **Issue Tracker:** (GitHub Issues)
- **Team Wiki:** (Link to be added)
- **Slack Channel:** #embodied-ai (or equivalent)

## Version Control

- **Current Version:** 1.0
- **Last Updated:** 2026-06-13
- **Next Review:** 2026-09-13 (after MVP completion)

---

**Navigation Tips:**
- Use browser's "Find" (Ctrl+F / Cmd+F) to search within documents
- Click document links to jump between related files
- Check the Revision History at bottom of each document for change log

**Questions?** See [docs/guides/Troubleshooting.md](guides/Troubleshooting.md) or start an issue on GitHub.

Happy documenting! 🚀
