# 🚀 Getting Started Checklist

Use this checklist to guide you through the onboarding process and ensure you have everything needed to start contributing to the Embodied AI project.

## 📋 Phase 1: Documentation Review (Est. 2 hours)

### Understanding the Project
- [ ] **Read Main Roadmap Executive Summary** (5-10 min)
  - File: `EMBODIED_AI_ROADMAP.md`
  - Section: "Executive Summary"
  - ✓ Goal: Understand project vision and phases

- [ ] **Understand Project Structure** (10-15 min)
  - File: `README_PROJECT_STRUCTURE.md`
  - ✓ Goal: Know how to navigate documentation

- [ ] **Review Documentation Index** (5 min)
  - File: `docs/INDEX.md`
  - ✓ Goal: Know what docs exist

- [ ] **Learn System Architecture** (30-45 min)
  - File: `docs/architecture/System-Architecture.md`
  - ✓ Goal: Understand technical design

### Role-Specific Reading
Choose one based on your role:

**For Software Engineers:**
- [ ] Development Environment Setup (20 min)
  - File: `docs/guides/Installation-Setup.md`
- [ ] Phase 1: Connectivity Details (30 min)
  - File: `docs/phases/Phase-1-Connectivity.md`
- [ ] Robot Bridge API (20 min)
  - File: `docs/api-reference/Robot-Bridge-API.md`

**For Hardware/Robotics Engineers:**
- [ ] Robot Assessment Instructions (20 min)
  - File: `docs/phases/Phase-0-Robot-Assessment.md`
- [ ] Installation & Hardware Setup (30 min)
  - File: `docs/guides/Installation-Setup.md`
- [ ] NAO Hardware Specifications (20 min)
  - File: `docs/technical-specs/NAO-Hardware-Specs.md`

**For AI/ML Engineers:**
- [ ] Phase 4: LLM Integration (30 min)
  - File: `docs/phases/Phase-4-LLM-Integration.md`
- [ ] Speech Pipeline Details (30 min)
  - File: `docs/technical-specs/Speech-Pipeline.md`

**For Project Managers:**
- [ ] Timeline & Resources (20 min)
  - File: `EMBODIED_AI_ROADMAP.md` → "Timeline & Resource Allocation"
- [ ] Risk Assessment (15 min)
  - File: `EMBODIED_AI_ROADMAP.md` → "Risk Assessment & Mitigation"

---

## 💻 Phase 2: Environment Setup (Est. 2-4 hours)

### Prerequisites Check
- [ ] **Verify System Requirements**
  - [ ] OS: Linux (Ubuntu 22.04) or Windows with WSL2
  - [ ] RAM: Minimum 16GB
  - [ ] Disk: 256GB+ SSD
  - [ ] Python 3.9+
  - [ ] Git installed

- [ ] **Network Setup**
  - [ ] Have NAO robot IP address: _______________
  - [ ] Robot on same network as development machine
  - [ ] Can ping robot successfully

### Installation
- [ ] **Follow Installation Guide**
  - File: `docs/guides/Installation-Setup.md`
  - [ ] Complete Step 1: Robot Hardware Setup
  - [ ] Complete Step 2: Server Environment Setup
  - [ ] Complete Step 3: Robot Bridge Setup
  - [ ] Complete Step 4: AI Backend Setup
  - [ ] Complete Step 5: Development Environment

- [ ] **Verify Installation**
  - [ ] Robot bridge running on `http://localhost:8000`
  - [ ] AI backend accessible on `http://localhost:8001`
  - [ ] Web dashboard accessible on `http://localhost:5173` (dev)
  - [ ] Robot responding to ping
  - [ ] All services communicating

### Optional: IDE Setup
- [ ] Install VSCode or preferred IDE
- [ ] Install Python extensions
- [ ] Install ESLint/Prettier for JavaScript
- [ ] Configure for this project

---

## 🏗️ Phase 3: Project Familiarization (Est. 1 hour)

### Code Structure Exploration
- [ ] Explore `src/` directory structure
- [ ] Check `config/` for configuration templates
- [ ] Review `tests/` directory setup
- [ ] Look at `examples/` for sample code

### Tool Familiarity
- [ ] [ ] Understand git workflow
  - [ ] Know how to create feature branches
  - [ ] Know how to submit pull requests
- [ ] [ ] Familiarize with this project's conventions
  - [ ] Review any `.claude.md` files
  - [ ] Check Python/JavaScript style guides
- [ ] [ ] Set up communication channels
  - [ ] Join team Slack/Discord
  - [ ] Review team documentation wiki

### Git Setup
- [ ] Configure git user (if not done)
  ```bash
  git config user.name "Your Name"
  git config user.email "your.email@example.com"
  ```
- [ ] Create feature branch for your work
  ```bash
  git checkout -b feature/your-feature-name
  ```

---

## 📊 Phase 4: Assigned Phase Documentation (Est. 1-2 hours)

### Read Your Current Phase
Based on project status (currently Phase 0), read:

**Phase 0: Robot Assessment** (1 week)
- [ ] Read: `docs/phases/Phase-0-Robot-Assessment.md`
- [ ] Understand: All success criteria
- [ ] Know: Required deliverables
- [ ] Check: Task checklist

**If assigned to Phase 1: Connectivity** (2 weeks)
- [ ] Read: `docs/phases/Phase-1-Connectivity.md`
- [ ] Review: Robot Bridge API
- [ ] Understand: Communication protocol
- [ ] Note: Dependencies and blockers

**For Other Phases:**
- [ ] Read: `docs/phases/Phase-X-Name.md`
- [ ] Review: Related API documentation
- [ ] Note: Phase dependencies
- [ ] Understand: Technical architecture for phase

### Understanding Deliverables
- [ ] List all deliverables for your phase
- [ ] Note success criteria
- [ ] Identify external dependencies
- [ ] Plan timeline and milestones

---

## 🔧 Phase 5: Quick Reference Setup (Est. 15 min)

### Bookmark Important Links
- [ ] Main Roadmap: `EMBODIED_AI_ROADMAP.md`
- [ ] Navigation: `README_PROJECT_STRUCTURE.md`
- [ ] Your Phase: `docs/phases/Phase-X.md`
- [ ] Relevant API: `docs/api-reference/X-API.md`

### Create Personal Documentation
- [ ] Create `SETUP_NOTES.md` in your workspace with:
  - Your local IP addresses
  - NAO robot configuration
  - Custom environment variables
  - Personal bookmarks

### Join Communication
- [ ] [ ] Slack/Discord channel
- [ ] [ ] Regular team meetings
- [ ] [ ] Pair programming sessions (if applicable)

---

## ✅ Phase 6: First Task Verification (Est. 30 min)

### Confirm Readiness
- [ ] [ ] Can you describe the 5 architectural layers?
- [ ] [ ] Can you identify your assigned phase?
- [ ] [ ] Can you access all three main services (bridge, backend, dashboard)?
- [ ] [ ] Do you know who to ask for help?

### First Task
- [ ] [ ] Assigned a task for your phase
- [ ] [ ] Have a GitHub issue/ticket
- [ ] [ ] Created a feature branch
- [ ] [ ] Ready to start coding

### Last Check
- [ ] [ ] Have all prerequisites installed
- [ ] [ ] Can run your phase's tests
- [ ] [ ] Environment variables configured
- [ ] [ ] Can build/run the code

---

## 🎯 Your First Week

### Daily Tasks
- [ ] **Day 1:** Complete Phases 1-2 of this checklist
- [ ] **Day 2:** Complete Phase 3 (Familiarization)
- [ ] **Day 3:** Complete Phase 4 (Phase Documentation)
- [ ] **Day 4:** Complete Phase 5 (Quick Reference)
- [ ] **Day 5:** Complete Phase 6 & begin first task

### Weekly Goals
- [ ] [ ] Understand overall system architecture
- [ ] [ ] Know your assigned phase inside-out
- [ ] [ ] Environment fully set up and tested
- [ ] [ ] First task started
- [ ] [ ] Made first commit to feature branch

### Questions to Answer by End of Week
1. What are the 5 architectural layers?
2. What is your assigned phase?
3. What is the main deliverable of your phase?
4. How do you start the development environment?
5. Who is your point of contact for questions?

---

## 🆘 Getting Help

### If You're Stuck
1. **Check these first:**
   - [ ] `docs/guides/Troubleshooting.md`
   - [ ] Search existing documentation
   - [ ] Check GitHub issues/discussions

2. **Ask the team:**
   - [ ] Post in Slack/Discord
   - [ ] Create a GitHub discussion
   - [ ] Schedule pair programming session

3. **Escalate if needed:**
   - [ ] Reach out to tech lead
   - [ ] Check project manager

### Documentation to Troubleshoot
- [ ] Installation issues → `docs/guides/Installation-Setup.md`
- [ ] Development setup → `docs/guides/Development-Environment.md`
- [ ] Phase-specific questions → `docs/phases/Phase-X.md`
- [ ] Architecture questions → `docs/architecture/System-Architecture.md`
- [ ] API questions → `docs/api-reference/`

---

## 📈 Onboarding Progress Tracker

### Week 1
- [ ] Documentation review completed
- [ ] Environment setup complete
- [ ] Code base explored
- [ ] First task understood

### Week 2
- [ ] First task in progress
- [ ] Contributing to codebase
- [ ] Understanding team workflows
- [ ] Comfortable with phase documentation

### Week 3
- [ ] First pull request submitted
- [ ] Code review feedback received
- [ ] Contributing regularly
- [ ] Understanding overall architecture

### Week 4+
- [ ] Contributing independently
- [ ] Unblocking own tasks
- [ ] Helping newer team members
- [ ] Planning next phase

---

## 📝 Sign-Off Checklist

Once you've completed all items above, you're ready to contribute!

- [ ] **I have read** the main roadmap
- [ ] **I understand** the project vision and architecture
- [ ] **I have set up** my development environment
- [ ] **I can run** the robot bridge, AI backend, and dashboard
- [ ] **I know** my assigned phase
- [ ] **I have read** my phase documentation
- [ ] **I understand** the success criteria
- [ ] **I know** where to get help
- [ ] **I am ready** to start my first task

**Date Completed:** _______________  
**Name:** _______________  
**Assigned Phase:** _______________  
**Point of Contact:** _______________  

---

## 🚀 You're Ready!

Congratulations on completing the onboarding checklist! You're now ready to contribute to the Embodied AI project.

**Next Step:** Start working on your assigned phase!

### Your First Commit
```bash
git add .
git commit -m "docs: complete onboarding checklist"
git push origin feature/your-feature-name
```

### Share Your Progress
- Let the team know you're ready
- Join your first team meeting
- Start contributing!

---

**Questions?** Refer back to the relevant documentation files, or ask your point of contact.

Good luck! 🎉
