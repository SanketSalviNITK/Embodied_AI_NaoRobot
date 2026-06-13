# Motion Bridge - User Guide

**Status:** ✅ Phase 1.1 - Implemented  
**Components:** 22 DOF robot motion control  
**Supported Connections:** LAN & WiFi

---

## 📖 Overview

The **Motion Bridge** provides a simple, clean Python interface to control all robot movement and joints.

### Key Features
- ✅ Posture control (stand, sit, crouch, etc.)
- ✅ Walking (forward, backward, left, right, turning)
- ✅ Joint control (all 22 joints)
- ✅ Stiffness management
- ✅ Both LAN and WiFi support
- ✅ Error handling and recovery

---

## 🚀 Quick Start

### Installation

Activate Python 2.7 environment:
```bash
cd phase1_connectivity_layer
venv_py27\Scripts\activate.bat
```

### Basic Usage

```python
from robot_bridge import MotionBridge

# Connect to robot (WiFi IP)
bridge = MotionBridge(ip='192.168.137.87')

# Or use LAN IP
bridge = MotionBridge(ip='169.254.175.171')

# Simple commands
bridge.stand()              # Stand up
bridge.say("Hello")         # Say something (requires audio bridge)
bridge.walk_forward(1.0)    # Walk 1 meter forward
bridge.turn_left(0.5)       # Turn left
bridge.sit()                # Sit down
```

---

## 📋 API Reference

### Posture Control

```python
bridge.stand()              # Stand up
bridge.sit()                # Sit down
bridge.crouch()             # Crouch position
bridge.lie_on_belly()       # Lie on belly
bridge.lie_on_back()        # Lie on back
```

### Walking

```python
# Forward/Backward
bridge.walk_forward(distance=0.5, speed=0.5)   # meters, 0-1
bridge.walk_backward(distance=0.5, speed=0.5)

# Sideways
bridge.walk_left(distance=0.3, speed=0.5)
bridge.walk_right(distance=0.3, speed=0.5)

# Turning
bridge.turn_left(angle=0.5, speed=0.5)    # radians
bridge.turn_right(angle=0.5, speed=0.5)

# Movement control
bridge.stop()               # Stop immediately
bridge.is_moving()          # Check if moving
```

### Joint Control

```python
import math

# Single joint
bridge.set_joint_angle('HeadYaw', math.radians(30), speed=0.5)

# Multiple joints
bridge.set_joint_angles({
    'HeadYaw': 0.5,
    'HeadPitch': -0.3,
    'LShoulderPitch': 1.0
}, speed=0.3)

# Get joint angles
angles = bridge.get_joint_angles()
print(angles['HeadYaw'])    # Get specific joint
```

### Stiffness Control

```python
bridge.stiffen()            # Stiffness = 1.0 (stiff)
bridge.relax()              # Stiffness = 0.0 (relaxed)
bridge.set_stiffness(0.5)   # Custom stiffness 0-1

# Get current stiffness
stiffness = bridge.get_stiffness()
```

### Status & Utilities

```python
bridge.is_moving()          # True if moving
bridge.get_robot_config()   # Robot configuration
bridge.get_robot_status()   # Full status dict
```

---

## 🎮 Complete Example - Dance Routine

```python
from robot_bridge import MotionBridge
import time
import math

# Connect to robot
bridge = MotionBridge(ip='192.168.137.87')

# Stand
bridge.stand()
time.sleep(1)

# Dance sequence
for i in range(3):
    # Move head
    bridge.set_joint_angle('HeadYaw', math.radians(30), speed=0.5)
    time.sleep(0.5)
    bridge.set_joint_angle('HeadYaw', math.radians(-30), speed=0.5)
    time.sleep(0.5)
    
    # Turn
    bridge.turn_left(angle=0.3, speed=0.5)
    time.sleep(0.5)
    bridge.turn_right(angle=0.3, speed=0.5)
    time.sleep(0.5)

# Return to normal
bridge.set_joint_angle('HeadYaw', 0, speed=0.3)
bridge.stand()
```

---

## 🔌 Connection Options

### WiFi Connection (Recommended)
```python
bridge = MotionBridge(ip='192.168.137.87')
```

**Advantages:**
- Mobile and flexible
- No cables
- Wireless operation

### LAN Connection (Stable)
```python
bridge = MotionBridge(ip='169.254.175.171')
```

**Advantages:**
- Lower latency
- More stable
- Faster response

---

## 📊 Joint Reference

### All 22 Joints (4 DOF arms, 6 DOF legs each)

**Head (2 DOF):**
- `HeadYaw` - Head rotation left/right
- `HeadPitch` - Head tilt up/down

**Left Arm (5 DOF):**
- `LShoulderPitch` - Shoulder forward/back
- `LShoulderRoll` - Shoulder up/down
- `LElbowYaw` - Elbow rotation
- `LElbowRoll` - Elbow bend
- `LWristYaw` - Wrist rotation

**Right Arm (5 DOF):**
- `RShoulderPitch`, `RShoulderRoll`
- `RElbowYaw`, `RElbowRoll`
- `RWristYaw`

**Left Leg (6 DOF):**
- `LHipYawPitch`, `LHipRoll`, `LHipPitch`
- `LKneePitch`, `LAnklePitch`, `LAnkleRoll`

**Right Leg (6 DOF):**
- `RHipYawPitch`, `RHipRoll`, `RHipPitch`
- `RKneePitch`, `RAnklePitch`, `RAnkleRoll`

---

## ⚠️ Safety Guidelines

1. **Clear Space:** Ensure 2-3 meters of clear space around robot
2. **Speed:** Keep speed 0.3-0.7 for safety
3. **Stiffness:** Always stiffen before movement
4. **Supervision:** Supervise robot during tests
5. **Falls:** Watch for balance issues

---

## 🐛 Troubleshooting

### "Failed to connect"
- Check robot power
- Verify IP address (ping test)
- Ensure NAOqi is running
- Check firewall settings

### "Movement too slow"
- Increase speed parameter (max 1.0)
- Reduce distance
- Check robot stiffness

### "Robot not responding"
- Relax and stiffen: `bridge.relax()`, `bridge.stiffen()`
- Try stop: `bridge.stop()`
- Reconnect: `bridge = MotionBridge()`

---

## 📚 Related Documentation

- **Robot Config:** `robot_config.json`
- **Test Suite:** `tests/test_motion_bridge.py`
- **Phase 1 README:** `README.md`
- **NAOqi Reference:** `/docs/references/NAOQI_SDK_API_REFERENCE.md`

---

## 🎯 Next Phases

After Motion Bridge:
- **Phase 1.2:** Sensor Bridge (read accelerometer, battery, etc.)
- **Phase 1.3:** Audio Bridge (text-to-speech, microphone)
- **Phase 1.4:** LED Bridge (RGB colors, animations)
- **Phase 2:** REST API (expose bridges via HTTP)
- **Phase 3:** WebSocket (real-time streaming)

---

**Status:** ✅ Ready to Use  
**Last Updated:** 2026-06-13
