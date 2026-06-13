# NAO Robot V4 - Coordinate System & Joint Orientations

**Reference:** NAO V4 Joint Schematics and Right-Hand Coordinate System

---

## 🤖 NAO Body-Relative Coordinate System

NAO uses a **standard right-hand coordinate system** aligned with its body:

```
        HEAD (facing forward)
          |
          | Z (UP)
          |
    L     |     R
    E  ---|--- A
    F   Y |   R
    T     |   M
          |
         GROUND
         
X-axis: Forward/Backward (robot's forward direction)
Y-axis: Left/Right (from robot's perspective)
Z-axis: Up/Down (vertical)
```

---

## 📐 Movement Parameters (moveToward)

```python
motion.moveToward(x, y, theta)
```

### Parameters:
- **x**: Forward/Backward velocity
  - `x > 0`: Move FORWARD
  - `x < 0`: Move BACKWARD
  
- **y**: Left/Right velocity
  - `y > 0`: Move LEFT
  - `y < 0`: Move RIGHT
  
- **theta**: Rotational velocity
  - `theta > 0`: Turn LEFT (counter-clockwise)
  - `theta < 0`: Turn RIGHT (clockwise)

---

## 🦵 Leg Joint Orientations (6 DOF per leg)

### Left Leg (L prefix):
- `LHipYawPitch`: Hip rotation (connects L & R legs)
- `LHipRoll`: Hip roll (abduction/adduction)
- `LHipPitch`: Hip pitch (forward/backward rotation)
- `LKneePitch`: Knee pitch (bending)
- `LAnklePitch`: Ankle pitch (forward/backward tilt)
- `LAnkleRoll`: Ankle roll (inversion/eversion)

### Right Leg (R prefix):
- `RHipYawPitch`: Hip rotation (same as left, connects both legs)
- `RHipRoll`: Hip roll
- `RHipPitch`: Hip pitch
- `RKneePitch`: Knee pitch
- `RAnklePitch`: Ankle pitch
- `RAnkleRoll`: Ankle roll

---

## 💪 Arm Joint Orientations (5 DOF per arm)

### Left Arm (L prefix):
- `LShoulderPitch`: Shoulder forward/backward
- `LShoulderRoll`: Shoulder up/down (abduction)
- `LElbowYaw`: Elbow rotation
- `LElbowRoll`: Elbow bending
- `LWristYaw`: Wrist rotation

### Right Arm (R prefix):
- `RShoulderPitch`: Shoulder forward/backward
- `RShoulderRoll`: Shoulder up/down
- `RElbowYaw`: Elbow rotation
- `RElbowRoll`: Elbow bending
- `RWristYaw`: Wrist rotation

---

## 🗣️ Head Joint Orientations (2 DOF)

- `HeadYaw`: Head rotation left/right
  - Positive: Turn LEFT
  - Negative: Turn RIGHT
  
- `HeadPitch`: Head tilt up/down
  - Positive: Tilt DOWN
  - Negative: Tilt UP

---

## 📏 Example: Walking Forward

To make robot walk forward:
```python
# Walk forward 1 meter at half speed
motion.moveToward(0.5, 0, 0)  # x > 0 = forward
```

This activates the leg joints in sequence:
1. Hip joints shift weight
2. Knee bends to lift leg
3. Hip/ankle rotate to step forward
4. Process repeats for other leg

---

## 📐 Complete Movement Examples

```python
# Forward
moveToward(0.5, 0, 0)      # x positive

# Backward
moveToward(-0.5, 0, 0)     # x negative

# Left
moveToward(0, 0.5, 0)      # y positive

# Right
moveToward(0, -0.5, 0)     # y negative

# Turn left (counter-clockwise)
moveToward(0, 0, 0.5)      # theta positive

# Turn right (clockwise)
moveToward(0, 0, -0.5)     # theta negative

# Diagonal: Forward + Left
moveToward(0.3, 0.3, 0)    # x positive, y positive

# Diagonal: Backward + Right
moveToward(-0.3, -0.3, 0)  # x negative, y negative
```

---

## 🎯 Walking Test Mapping

Based on NAO's right-hand coordinate system:

| Test | moveToward() | Expected Direction |
|------|--------------|-------------------|
| 1 | (0.1, 0, 0) | FORWARD |
| 2 | (0, 0.1, 0) | LEFT |
| 3 | (-0.1, 0, 0) | BACKWARD |
| 4 | (0, -0.1, 0) | RIGHT |

---

## 📚 References

- NAO V4 Joint Schematics
- NAOqi 2.8.6.23 ALMotion Documentation
- Standard Right-Hand Coordinate System
- Robot Kinematics Conventions

---

**Status:** ✅ Coordinate System Documented  
**Last Updated:** 2026-06-13
