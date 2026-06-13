# Phase 0: Robot Assessment Guide

**Duration:** 1 week  
**Status:** ✅ Ready to Execute  
**Date Started:** 2026-06-13  

---

## 📋 Overview

Phase 0 is the **Robot Assessment & Baseline Documentation** phase. It involves:

1. ✅ Running comprehensive tests on all robot systems
2. ✅ Documenting hardware baseline
3. ✅ Identifying any issues or limitations
4. ✅ Creating performance benchmarks
5. ✅ Preparing for Phase 1 development

---

## 🎯 Phase 0 Goals

### Primary Goals
- [ ] Verify all 22 joints are functional
- [ ] Test sensor accuracy and stability
- [ ] Validate motion control systems
- [ ] Confirm audio and speech capabilities
- [ ] Verify LED control systems
- [ ] Document hardware baseline

### Secondary Goals
- [ ] Identify hardware limitations
- [ ] Note any sensor drift or calibration needs
- [ ] Test maximum speeds and ranges
- [ ] Verify safety limits are in place
- [ ] Create performance benchmarks

---

## 🚀 Getting Started

### Prerequisites
- ✅ Robot powered on and connected
- ✅ Network connection verified (169.254.80.144)
- ✅ NAOqi 2.8.6.23 operational
- ✅ Python 2.7 environment set up
- ✅ Test scripts prepared

### Estimated Timeline
- Test execution: 30-45 minutes
- Analysis & documentation: 1-2 hours
- Total Phase 0 time: 4-6 hours

---

## 📝 Phase 0 Test Checklist

### Pre-Test
- [ ] Robot is powered on
- [ ] Robot is connected via LAN
- [ ] System can ping robot (169.254.80.144)
- [ ] NAOqi service is responsive
- [ ] Virtual environment activated
- [ ] Clear floor space for movement tests
- [ ] Video camera ready (optional, for documentation)

### During Tests
- [ ] Test 1: Joint Control (22 DOF)
- [ ] Test 2: Motion & Walking
- [ ] Test 3: Detailed Sensor Analysis
- [ ] Test 4: Audio & Speech
- [ ] Test 5: LED Control

### Post-Test
- [ ] Save all test results
- [ ] Document any failures
- [ ] Note any unusual behavior
- [ ] Compare with baseline expectations
- [ ] Create assessment report

---

## 🔬 Detailed Phase 0 Tests

### Test 1: Joint Control & Movement
**Duration:** 5-7 minutes  
**Purpose:** Verify all 22 DOF joints are operational

**What's Tested:**
- Joint angle reading (current position)
- Predefined postures (Stand, Sit, Crouch, etc.)
- Head movement (left/right/up/down)
- Arm movement (shoulders, elbows)
- Stiffness control (soft/stiff)
- Joint speed capabilities
- Motion range limits

**Expected Results:**
- ✅ All joints respond to commands
- ✅ Position angles readable with <1° error
- ✅ Posture transitions smooth
- ✅ Stiffness adjustable 0.0-1.0

**Failure Cases:**
- ❌ Joint doesn't move
- ❌ Angle reading inaccurate (>5° error)
- ❌ Posture transition fails
- ❌ Stiffness doesn't change

**Run Test:**
```bash
python test_phase0_joint_control.py
```

---

### Test 2: Motion & Walking
**Duration:** 8-10 minutes  
**Purpose:** Validate locomotion and movement

**What's Tested:**
- Forward walking (20cm)
- Backward walking (20cm)
- Lateral movement (side stepping)
- Rotation in place (turning)
- Balance maintenance
- Motion cycle time
- Walking configuration parameters

**Expected Results:**
- ✅ Robot walks smoothly forward/backward
- ✅ Lateral movement stable
- ✅ Rotation accurate (±5°)
- ✅ Balance maintained during movement
- ✅ Motion cycle <50ms

**Failure Cases:**
- ❌ Robot stumbles or falls
- ❌ Movement jerky or uncontrolled
- ❌ Rotation overshoots target
- ❌ Unstable balance

**Run Test:**
```bash
python test_phase0_motion.py
```

---

### Test 3: Detailed Sensor Analysis
**Duration:** 5-7 minutes  
**Purpose:** Verify sensor accuracy and stability

**What's Tested:**
- Accelerometer readings (gravity vector)
- Gyroscope stability (no rotation)
- Foot pressure sensors (FSR) - all 8 sensors
- Touch sensors (head front/middle/rear)
- Battery charge and temperature
- Temperature monitoring
- Sensor reading stability (variance <5%)

**Expected Readings:**
- **Accelerometer:** 
  - Z axis ~1.0g (gravity) when standing
  - X, Y axes ~0.0g when stable
  
- **Gyroscope:**
  - X, Y, Z axes ~0.0 rad/s when stationary
  
- **FSR:**
  - Values 0-1.0 scale (normalized pressure)
  - Front sensors higher when upright
  
- **Battery:**
  - Charge >20% for safe operation
  - Temperature 20-40°C normal

**Failure Cases:**
- ❌ Accelerometer drifting >0.1g
- ❌ Gyroscope noise >0.01 rad/s
- ❌ FSR values inconsistent
- ❌ Battery charge <10%
- ❌ Temperature >50°C

**Run Test:**
```bash
python test_phase0_sensors_detailed.py
```

---

### Test 4: Audio & Speech
**Duration:** 5-8 minutes  
**Purpose:** Validate audio system

**What's Tested:**
- Text-to-speech synthesis
- Multiple language support (en_US, fr_FR, es_ES)
- Volume control (0-100%)
- Speech parameter adjustment
- Microphone system availability
- Audio quality and clarity

**Expected Results:**
- ✅ Speech synthesis produces clear audio
- ✅ Multiple languages supported
- ✅ Volume adjustable
- ✅ Speech parameters responsive
- ✅ Microphone accessible

**Failure Cases:**
- ❌ No audio output
- ❌ Speech distorted or garbled
- ❌ Volume doesn't change
- ❌ Language switching fails

**Run Test:**
```bash
python test_phase0_audio.py
```

---

### Test 5: LED Control
**Duration:** 3-5 minutes  
**Purpose:** Validate LED systems

**What's Tested:**
- LED on/off control
- Brightness adjustment (0-100%)
- RGB color control
- LED groups (chest, face, feet, ears)
- Eye animations
- Fade effects
- Synchronized LED control

**Expected Results:**
- ✅ All LEDs respond to commands
- ✅ Brightness smooth gradient
- ✅ Colors accurate
- ✅ Animations smooth
- ✅ All LED groups functional

**Failure Cases:**
- ❌ LED doesn't light
- ❌ Color doesn't match expected
- ❌ Animation jerky or slow
- ❌ LED group unresponsive

**Run Test:**
```bash
python test_phase0_leds.py
```

---

## 🏃 Running All Tests at Once

```bash
run_phase0_tests.bat
```

This will:
1. ✅ Activate Python 2.7 environment
2. ✅ Verify robot connectivity
3. ✅ Run all 5 tests sequentially
4. ✅ Save logs to `phase0_results/`
5. ✅ Display summary report

**Expected Time:** 30-40 minutes

---

## 📊 Analyzing Results

### Test Results Files
```
phase0_results/
├── test_1_joint_control.log
├── test_2_motion.log
├── test_3_sensors.log
├── test_4_audio.log
└── test_5_leds.log
```

### What to Look For

**Passing Indicators:**
- ✅ "OK" status messages
- ✅ All tests return exit code 0
- ✅ Readings within expected ranges
- ✅ Smooth, responsive movement

**Warning Indicators:**
- ⚠️ "WARNING" status in logs
- ⚠️ Non-critical failures
- ⚠️ Out-of-range readings
- ⚠️ Slow response times

**Failure Indicators:**
- ❌ "ERROR" or "FAILED" status
- ❌ Tests return non-zero exit code
- ❌ No response from robot systems
- ❌ Critical sensor failures

---

## 📋 Documentation Template

Use `PHASE0_BASELINE_TEMPLATE.md` to document:

1. **Hardware Inventory**
   - Robot model (NAO V4)
   - NAOqi version (2.8.6.23)
   - Number of operational joints
   - Functional sensors

2. **Baseline Measurements**
   - Joint angles (neutral position)
   - Sensor readings (stationary)
   - Battery charge & temperature
   - Motor speeds

3. **Issues Found**
   - Failed joints or sensors
   - Limitations discovered
   - Calibration needs
   - Hardware damage

4. **Performance Metrics**
   - Motion smoothness
   - Sensor accuracy
   - Audio quality
   - Response times

5. **Recommendations**
   - Maintenance needed
   - Calibration procedures
   - Safe operation limits
   - Next steps

---

## ⚠️ Safety Guidelines

### Before Running Tests
- [ ] Clear all obstacles from robot's path
- [ ] Ensure adequate space (2m x 2m minimum)
- [ ] Check battery level (>20%)
- [ ] Verify stable power connection
- [ ] Be prepared to stop robot if needed

### During Tests
- [ ] Stay alert and watchful
- [ ] Keep hands near power button
- [ ] Don't interfere with robot movement
- [ ] Monitor for overheating (>50°C)
- [ ] Stop immediately if safety risk detected

### After Tests
- [ ] Return robot to standing position
- [ ] Allow robot to rest (stiffness OFF)
- [ ] Check for any damage
- [ ] Document any issues
- [ ] Charge battery if needed

---

## 🔧 Troubleshooting

### Robot Not Responding
```
Problem: Tests fail with connection error
Solution:
1. Check robot power (should have white light)
2. Ping robot: ping 169.254.80.144
3. Power cycle robot (off 30s, on 60s)
4. Check NAOqi service: ssh nao@169.254.80.144
```

### Joint Not Moving
```
Problem: Specific joint doesn't respond
Solution:
1. Check joint name spelling
2. Verify joint stiffness is enabled
3. Check for mechanical obstruction
4. Try moving a different joint to isolate issue
5. Document which joint is affected
```

### Sensor Reading Errors
```
Problem: Sensor returns NaN or out-of-range
Solution:
1. Verify robot is in stable standing position
2. Check sensor availability (some may be disabled)
3. Compare with other sensors' readings
4. Check temperature (sensors drift when hot)
5. Try power cycle if persistent
```

### Audio Not Working
```
Problem: No speech output or distorted audio
Solution:
1. Check speaker volume: getOutputVolume()
2. Verify language is set correctly
3. Try simple phrase first: "hello"
4. Check for network latency
5. Restart NAOqi service if needed
```

---

## 📈 Success Criteria

### Phase 0 Completion
**All of the following must be true:**

✅ At least 4 of 5 tests pass  
✅ No critical system failures  
✅ Baseline documentation complete  
✅ Issues identified and documented  
✅ Robot is stable and responsive  

### Ready for Phase 1
**Phase 1 can start when:**

✅ All Phase 0 tests pass  
✅ Hardware baseline documented  
✅ Safety limits verified  
✅ Issues resolved or documented  
✅ Team approves to proceed  

---

## 📝 Next Steps After Phase 0

### If All Tests Pass ✅
1. Archive test results
2. Create baseline report
3. Document any findings
4. Proceed to Phase 1: Robot Connectivity Layer
5. Start implementing ROS2/bridge service

### If Some Tests Fail ⚠️
1. Investigate failed tests
2. Document issues clearly
3. Schedule maintenance if needed
4. Retest after fixes
5. Get approval before Phase 1

### If Critical Failure ❌
1. Stop all operations
2. Power down robot safely
3. Document complete error details
4. Contact robot manufacturer support
5. Do not proceed until resolved

---

## 📞 Support & References

**Test Script Documentation:**
- `NAOQI_SDK_API_REFERENCE.md` - All available APIs
- `PYTHON27_TEST_GUIDE.md` - Python 2.7 specific guidance
- `PYTHON_ENVIRONMENT_GUIDE.md` - Environment setup

**Robot Hardware:**
- NAO V4 specifications
- Joint DOF breakdown (22 total)
- Sensor capabilities
- Safety limits

**Next Phase:**
- Phase 1: Robot Connectivity Layer
- ROS2 integration
- Bridge service implementation

---

## ✅ Checklist for Phase 0 Completion

- [ ] All prerequisite checks completed
- [ ] Run all 5 Phase 0 tests
- [ ] Review test results
- [ ] Document findings in baseline template
- [ ] Identify any issues
- [ ] Create Phase 0 assessment report
- [ ] Archive all test logs
- [ ] Get team approval
- [ ] Proceed to Phase 1

---

**Phase 0 Status:** 🚀 **READY TO START**

**Estimated Completion:** 4-6 hours  
**Next Phase:** Phase 1 - Robot Connectivity Layer  

---

Created: 2026-06-13  
Last Updated: 2026-06-13  
