# Quick Pre-Phase 0 Test Guide

**Current Status:** Robot powered on, network connected, ping working ✅

---

## 🚀 Quick Start

### Option 1: Run All Tests At Once (Recommended)

```bash
python run_all_tests.py
```

This will:
- Run test 1: NAOqi connection
- Run test 2: Network stability
- Run test 3: Robot sensors
- Generate a summary report

**Expected Duration:** 10-15 minutes  
**Difficulty:** Easy - just one command!

---

### Option 2: Run Individual Tests

If you want to run tests one by one:

```bash
# Test 1: Basic NAOqi connectivity
python test_1_naoqi_basic.py

# Test 2: Network latency and stability
python test_2_network_stability.py

# Test 3: Sensor data reading
python test_3_robot_sensors.py
```

---

## ✅ Prerequisites

Before running tests, verify:

1. **Robot is powered on**
   ```bash
   # Should see robot moving or responding
   ```

2. **Network connectivity**
   ```bash
   ping 169.254.80.144
   # Should see responses
   ```

3. **NAOqi SDK installed**
   ```bash
   pip install naoqi
   ```

4. **Python 3 available**
   ```bash
   python --version
   # Should show Python 3.x
   ```

---

## 📊 What Each Test Does

### Test 1: NAOqi Basic Connection
**Purpose:** Verify robot is accessible via NAOqi SDK  
**Duration:** 2-3 minutes  
**Tests:**
- Can import NAOqi module
- Can create proxy connections
- Can read battery level
- Can read robot stiffness status

**Success Indicator:** ✅ All proxies created successfully

---

### Test 2: Network Stability
**Purpose:** Measure network quality for real-time control  
**Duration:** 5-10 minutes  
**Tests:**
- Ping latency (15 pings)
- Packet loss rate
- Latency consistency

**Success Indicator:** ✅ Max latency <50ms, 0% packet loss

---

### Test 3: Robot Sensors
**Purpose:** Verify all sensors are working  
**Duration:** 3-5 minutes  
**Tests:**
- Battery sensor
- Accelerometer (IMU)
- Gyroscope
- Foot sensors (FSR)
- Joint encoders
- Microphone
- Speaker
- Cameras

**Success Indicator:** ✅ Most sensors responding

---

## 📋 Test Results Checklist

After running tests, you should have:

- [ ] `TEST_RESULTS_SUMMARY.txt` - Automatic summary file
- [ ] All test outputs in console
- [ ] Network latency measurements
- [ ] Sensor data readings
- [ ] Battery percentage
- [ ] Robot stiffness status

---

## ✨ Expected Results Summary

### Good Results ✅
```
✅ All 3 tests PASSED
✅ Network max latency: <50ms
✅ Battery charge: >20%
✅ All sensors responding
✅ Robot stiffness accessible
✅ NAOqi proxies created
```

### Warning Results ⚠️
```
⚠️ Some sensors unavailable (depends on NAO version)
⚠️ Network latency 50-100ms (acceptable)
⚠️ Battery charge <20% (charge robot)
```

### Bad Results ❌
```
❌ Cannot connect to robot via NAOqi
❌ Network latency >100ms
❌ Ping packet loss >5%
❌ Critical sensors not responding
```

---

## 🔧 Troubleshooting

### "Connection refused" or "Cannot connect to 169.254.80.144"

**Check:**
1. Is robot powered on?
2. Can you ping the robot?
   ```bash
   ping 169.254.80.144
   ```
3. Is NAOqi running on robot?
   ```bash
   ssh nao@169.254.80.144 "ps aux | grep naoqi"
   ```

**Fix:**
- Power cycle the robot
- Check network cable
- Wait 30-60 seconds for robot to boot

---

### "ImportError: No module named naoqi"

**Fix:**
```bash
pip install naoqi
```

**Alternative:** Use NAOqi SDK from robot package

---

### "Ping successful but NAOqi fails"

**Check:**
1. NAOqi port 9559 is open
   ```bash
   # From Windows, try telnet
   telnet 169.254.80.144 9559
   ```

2. NAOqi version compatibility
   ```bash
   ssh nao@169.254.80.144 "naoqi --version"
   ```

**Fix:**
- Restart NAOqi service on robot
- Check firewall rules

---

### "Network latency too high (>100ms)"

**Check:**
1. Network congestion
2. WiFi interference (if using WiFi)
3. Cable quality (if using Ethernet)

**Fix:**
- Use wired Ethernet instead of WiFi
- Reduce other network traffic
- Move closer to WiFi access point

---

## 📊 Sample Good Output

```
TEST 1: NAOqi Basic Connection
✅ NAOqi module imported successfully
✅ ALMotion proxy created successfully
✅ ALRobotPosture proxy created successfully
✅ ALBattery proxy created successfully
✅ ALTextToSpeech proxy created successfully
✅ ALAudioDevice proxy created successfully
✅ ALMemory proxy created successfully

Robot Data:
🔋 Battery Charge: 85%
🔋 Battery Health: Good
🤖 Stiffness values: [0.5, 0.5, 0.5, 0.5, ...]
👤 Current posture: Stand

TEST 2: Network Stability
Ping 1/15:    2.34ms ✅
Ping 2/15:    2.45ms ✅
Ping 3/15:    2.51ms ✅
...
Network Statistics:
  Minimum:    2.34ms
  Maximum:    3.21ms
  Average:    2.67ms
  Packet loss: 0%

✅ Network quality is EXCELLENT for real-time robotics!

TEST 3: Robot Sensors
✅ Battery charge: 85%
✅ Battery health: Good
✅ Accelerometer X: 0.0043 g
✅ Accelerometer Y: -0.0012 g
✅ Accelerometer Z: 9.8104 g (gravity)
✅ Gyroscope data available
✅ Foot sensors responding
✅ Joint encoders working
✅ Microphone ready
✅ Speaker ready

✅ ALL TESTS PASSED!
Your robot is ready for Phase 0!
```

---

## 🎯 Next Steps After Tests

### If All Tests Passed ✅

1. **Document Results**
   - Save `TEST_RESULTS_SUMMARY.txt`
   - Note any warnings or observations

2. **Begin Phase 0**
   - Read: `docs/phases/Phase-0-Robot-Assessment.md`
   - Follow robot assessment checklist
   - Document hardware baseline

3. **Expected Timeline**
   - Phase 0: 1 week
   - Then proceed to Phase 1: Robot Connectivity

### If Some Tests Failed ⚠️

1. **Review Failures**
   - Read error messages carefully
   - Check troubleshooting section above

2. **Fix Issues**
   - Address network issues first
   - Check robot power and connections
   - Verify NAOqi installation

3. **Re-run Failed Tests**
   ```bash
   python test_1_naoqi_basic.py  # Or specific test
   ```

4. **If Still Failing**
   - Check `PRE_PHASE0_TESTS.md` for detailed troubleshooting
   - Consult team / GitHub Issues

---

## 📝 Example Command Sequence

Here's exactly what to type:

```bash
# 1. Navigate to project directory
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI

# 2. Verify ping still works
ping 169.254.80.144

# 3. Run all tests
python run_all_tests.py

# 4. Check results
type TEST_RESULTS_SUMMARY.txt
```

---

## ⏱️ Time Estimate

- **Quick test (just connectivity):** 5 minutes
- **Full test suite:** 15 minutes
- **With troubleshooting:** 30-60 minutes

---

## ✅ Sign-Off Checklist

After tests complete, verify:

- [ ] NAOqi connection successful
- [ ] Network latency <100ms
- [ ] Battery >15%
- [ ] Sensors responding
- [ ] Results saved to file
- [ ] Ready to start Phase 0

---

## 📞 Support

If tests fail:

1. Check this guide's troubleshooting section
2. Review `PRE_PHASE0_TESTS.md` for detailed tests
3. Check GitHub Issues for similar problems
4. Ask team in Slack/Discord

---

## 🚀 Ready?

```bash
python run_all_tests.py
```

Go! 🎉

---

**Test Suite Version:** 1.0  
**Created:** 2026-06-13  
**Robot IP:** 169.254.80.144  
**System IP:** 169.254.80.100
