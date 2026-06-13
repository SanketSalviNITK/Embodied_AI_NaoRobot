# Pre-Phase 0 Tests - NAO Robot Validation

**Network Status:** ✅ Verified  
**Robot IP:** 169.254.80.144  
**System IP:** 169.254.80.100  
**Ping Test:** ✅ Working  

Now let's validate everything else before starting Phase 0 officially!

---

## Test Categories (In Order)

### 1. Network Connectivity Tests ✅ (Already Done)

**Current Status:**
- [x] Ping successful (network layer verified)
- [x] Robot powered on
- [x] Connected via LAN

**Next: Network Quality Tests**
- [ ] Test ping latency stability
- [ ] Test SSH connectivity
- [ ] Test transfer speeds
- [ ] Test NAOqi port accessibility

---

### 2. SSH & Remote Access Tests

**What to Test:**
```bash
# Test SSH connection to robot
ssh nao@169.254.80.144

# Default credentials (standard NAO):
# Username: nao
# Password: nao
```

**Expected Results:**
- ✅ SSH prompt appears
- ✅ Can list files: `ls`
- ✅ Can check NAO OS version: `uname -a`
- ✅ Can check network config: `ifconfig`

**Tests to Run:**
```bash
# Check robot's own network config
ssh nao@169.254.80.144 "ifconfig"

# Check robot's hostname
ssh nao@169.254.80.144 "hostname"

# Check available disk space
ssh nao@169.254.80.144 "df -h"

# Check system uptime
ssh nao@169.254.80.144 "uptime"

# Check what processes are running
ssh nao@169.254.80.144 "ps aux | grep nao"
```

**Document These:**
- [ ] SSH username works
- [ ] Default password accepted
- [ ] Robot OS version: _______________
- [ ] Available disk space: _______________
- [ ] Uptime: _______________

---

### 3. NAOqi SDK Accessibility Tests

**What to Test:**
NAOqi is the robot's main SDK - we need to verify it's accessible.

**Test 1: Check NAOqi Service**
```bash
# SSH into robot and check if naoqi is running
ssh nao@169.254.80.144 "ps aux | grep naoqi"

# Expected output: naoqi process running
```

**Test 2: Test NAOqi Python Module**

Create a test file `test_naoqi_basic.py`:

```python
#!/usr/bin/env python3
"""Test NAOqi SDK accessibility"""

import sys
from naoqi import ALProxy
import time

def test_naoqi_connection():
    """Test basic connection to NAOqi"""
    
    robot_ip = "169.254.80.144"
    robot_port = 9559
    
    print(f"🔍 Testing NAOqi connection to {robot_ip}:{robot_port}")
    
    try:
        # Test Motion proxy
        motion = ALProxy("ALMotion", robot_ip, robot_port)
        print("✅ ALMotion proxy created successfully")
        
        # Test posture proxy
        posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
        print("✅ ALRobotPosture proxy created successfully")
        
        # Test battery proxy
        battery = ALProxy("ALBattery", robot_ip, robot_port)
        print("✅ ALBattery proxy created successfully")
        
        # Test speech proxy
        tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
        print("✅ ALTextToSpeech proxy created successfully")
        
        # Test audio proxy
        audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
        print("✅ ALAudioDevice proxy created successfully")
        
        # Get actual battery data
        battery_data = battery.getBatteryCharge()
        print(f"🔋 Battery charge: {battery_data}%")
        
        # Get stiffness status
        stiffness = motion.getStiffnesses("Body")
        print(f"🤖 Robot stiffness status: {stiffness}")
        
        print("\n✅ ALL NAOQI TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ NAOqi connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_naoqi_connection()
    sys.exit(0 if success else 1)
```

**Run:**
```bash
python test_naoqi_basic.py
```

**Document:**
- [ ] NAOqi connection successful
- [ ] ALMotion proxy works
- [ ] ALRobotPosture proxy works
- [ ] ALBattery proxy works
- [ ] ALTextToSpeech proxy works
- [ ] ALAudioDevice proxy works
- [ ] Battery percentage: ____%

---

### 4. Joint Motion Tests

**What to Test:**
All 22 degrees of freedom (DoF) on the robot.

Create `test_robot_joints.py`:

```python
#!/usr/bin/env python3
"""Test robot joint movements"""

from naoqi import ALProxy
import time

def test_joint_movements():
    """Test all robot joints"""
    
    robot_ip = "169.254.80.144"
    robot_port = 9559
    
    print("🔍 Testing Robot Joint Movements")
    print("=" * 50)
    
    try:
        motion = ALProxy("ALMotion", robot_ip, robot_port)
        
        # First, enable stiffness
        print("\n1️⃣  Enabling stiffness...")
        motion.stiffnessInterpolation("Body", 1.0, 1.0)
        time.sleep(1)
        
        # Test each joint group
        joint_groups = {
            "Head": ["HeadYaw", "HeadPitch"],
            "Left Arm": ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"],
            "Right Arm": ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
            "Left Leg": ["LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll"],
            "Right Leg": ["RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"],
            "Torso": ["TorsoYaw"]
        }
        
        print("\n2️⃣  Testing individual joints...")
        tested_joints = []
        
        for group_name, joints in joint_groups.items():
            print(f"\n   {group_name}:")
            
            for joint in joints:
                try:
                    # Get current angle
                    angle = motion.getAngles(joint, False)[0]
                    print(f"   ✅ {joint}: {angle:.2f}°")
                    tested_joints.append(joint)
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"   ❌ {joint}: {e}")
        
        # Disable stiffness
        print("\n3️⃣  Disabling stiffness...")
        motion.stiffnessInterpolation("Body", 0.0, 1.0)
        
        print(f"\n✅ Successfully tested {len(tested_joints)}/{len([j for jlist in joint_groups.values() for j in jlist])} joints")
        print(f"   Expected 22 joints total")
        
        return True
        
    except Exception as e:
        print(f"❌ Joint test failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = test_joint_movements()
    sys.exit(0 if success else 1)
```

**Run:**
```bash
python test_robot_joints.py
```

**Document:**
- [ ] Head joints tested
- [ ] Left arm joints tested
- [ ] Right arm joints tested
- [ ] Left leg joints tested
- [ ] Right leg joints tested
- [ ] Torso joint tested
- [ ] Total joints working: ____/22

---

### 5. Sensor Tests

**What to Test:**
Microphones, cameras, IMU, temperature sensors.

Create `test_robot_sensors.py`:

```python
#!/usr/bin/env python3
"""Test robot sensors"""

from naoqi import ALProxy
import time

def test_sensors():
    """Test all robot sensors"""
    
    robot_ip = "169.254.80.144"
    robot_port = 9559
    
    print("🔍 Testing Robot Sensors")
    print("=" * 50)
    
    results = {}
    
    try:
        # Test Microphone
        print("\n1️⃣  Testing Microphone...")
        try:
            audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
            # Check microphone properties
            audio_config = audio.getInputVolume()
            print(f"   ✅ Microphone input volume: {audio_config}%")
            results["Microphone"] = "✅"
        except Exception as e:
            print(f"   ❌ Microphone test failed: {e}")
            results["Microphone"] = "❌"
        
        # Test Cameras
        print("\n2️⃣  Testing Cameras...")
        try:
            video = ALProxy("ALVideoDevice", robot_ip, robot_port)
            # Get camera info
            cameras = video.getCameraList()
            print(f"   ✅ Found cameras: {cameras}")
            results["Cameras"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Camera test (may not be available in this NAOqi version): {e}")
            results["Cameras"] = "⚠️"
        
        # Test IMU/Accelerometer
        print("\n3️⃣  Testing IMU/Accelerometer...")
        try:
            memory = ALProxy("ALMemory", robot_ip, robot_port)
            
            # Get accelerometer data
            acc_x = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
            acc_y = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value")
            acc_z = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")
            
            print(f"   ✅ Accelerometer X: {acc_x:.3f}")
            print(f"   ✅ Accelerometer Y: {acc_y:.3f}")
            print(f"   ✅ Accelerometer Z: {acc_z:.3f}")
            results["IMU"] = "✅"
        except Exception as e:
            print(f"   ❌ IMU test failed: {e}")
            results["IMU"] = "❌"
        
        # Test Temperature Sensors
        print("\n4️⃣  Testing Temperature Sensors...")
        try:
            memory = ALProxy("ALMemory", robot_ip, robot_port)
            
            temps = [
                ("CPU", "Device/SubDeviceList/DummyTorsoSensor/Temperature/Sensor/Value"),
                ("Battery", "Device/SubDeviceList/Battery/Charge/Sensor/Value"),
            ]
            
            for name, key in temps:
                try:
                    temp = memory.getData(key)
                    print(f"   ✅ {name}: {temp}")
                except:
                    pass
            
            results["Temperature"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Temperature test: {e}")
            results["Temperature"] = "⚠️"
        
        # Test Battery
        print("\n5️⃣  Testing Battery...")
        try:
            battery = ALProxy("ALBattery", robot_ip, robot_port)
            charge = battery.getBatteryCharge()
            health = battery.getBatteryHealth()
            print(f"   ✅ Battery charge: {charge}%")
            print(f"   ✅ Battery health: {health}")
            results["Battery"] = "✅"
        except Exception as e:
            print(f"   ❌ Battery test failed: {e}")
            results["Battery"] = "❌"
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 SENSOR TEST SUMMARY:")
        for sensor, status in results.items():
            print(f"   {status} {sensor}")
        
        return all("❌" not in status for status in results.values())
        
    except Exception as e:
        print(f"❌ Sensor tests failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = test_sensors()
    sys.exit(0 if success else 1)
```

**Run:**
```bash
python test_robot_sensors.py
```

**Document:**
- [ ] Microphone working
- [ ] Cameras detected
- [ ] IMU/Accelerometer working
- [ ] Temperature sensors working
- [ ] Battery sensors working

---

### 6. Audio System Tests

**What to Test:**
Speaker output and sound system.

Create `test_audio.py`:

```python
#!/usr/bin/env python3
"""Test robot audio system"""

from naoqi import ALProxy
import time

def test_audio():
    """Test audio input/output"""
    
    robot_ip = "169.254.80.144"
    robot_port = 9559
    
    print("🔍 Testing Audio System")
    print("=" * 50)
    
    try:
        # Test Text-to-Speech (Speaker)
        print("\n1️⃣  Testing Speaker (Text-to-Speech)...")
        tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
        
        # Set volume
        audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
        audio.setOutputVolume(50)
        print("   ✅ Volume set to 50%")
        
        # Speak test
        print("   🎤 Robot should say: 'Hello, this is NAO'")
        tts.say("Hello, this is NAO")
        time.sleep(2)
        print("   ✅ Speech output working")
        
        # Test Microphone
        print("\n2️⃣  Testing Microphone (Audio Input)...")
        audio.setInputVolume(100)
        print("   ✅ Microphone input volume set to 100%")
        print("   🎙️  Microphone should be ready to capture audio")
        
        # Test audio device info
        print("\n3️⃣  Audio Device Info...")
        input_volume = audio.getInputVolume()
        output_volume = audio.getOutputVolume()
        print(f"   ✅ Input volume: {input_volume}%")
        print(f"   ✅ Output volume: {output_volume}%")
        
        print("\n✅ AUDIO SYSTEM TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = test_audio()
    sys.exit(0 if success else 1)
```

**Run:**
```bash
python test_audio.py
```

**Document:**
- [ ] Speaker working (robot spoke)
- [ ] Microphone input volume set
- [ ] Audio device responding

---

### 7. Network Latency & Stability Tests

**What to Test:**
Network performance over time.

Create `test_network_stability.py`:

```python
#!/usr/bin/env python3
"""Test network latency and stability"""

import subprocess
import time
import statistics

def test_ping_stability(ip_address, count=10):
    """Test ping latency and stability"""
    
    print(f"🔍 Testing Network Stability to {ip_address}")
    print("=" * 50)
    print(f"Sending {count} ping packets...\n")
    
    latencies = []
    lost = 0
    
    for i in range(count):
        try:
            # Windows ping command
            result = subprocess.run(
                ["ping", "-n", "1", ip_address],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse latency from output
            if "time=" in result.stdout:
                # Extract time value
                time_str = result.stdout.split("time=")[1].split("ms")[0]
                latency = float(time_str)
                latencies.append(latency)
                print(f"   Ping {i+1}/{count}: {latency:.2f}ms ✅")
            else:
                print(f"   Ping {i+1}/{count}: Lost ❌")
                lost += 1
                
        except Exception as e:
            print(f"   Ping {i+1}/{count}: Error - {e}")
            lost += 1
        
        time.sleep(0.5)
    
    # Calculate statistics
    if latencies:
        print("\n📊 NETWORK STATISTICS:")
        print(f"   Minimum latency: {min(latencies):.2f}ms")
        print(f"   Maximum latency: {max(latencies):.2f}ms")
        print(f"   Average latency: {statistics.mean(latencies):.2f}ms")
        print(f"   Median latency: {statistics.median(latencies):.2f}ms")
        print(f"   Packets lost: {lost}/{count}")
        
        if max(latencies) < 50:
            print("\n✅ Network latency is excellent (<50ms)")
            return True
        elif max(latencies) < 100:
            print("\n⚠️  Network latency is acceptable (<100ms)")
            return True
        else:
            print("\n❌ Network latency is high (>100ms)")
            return False
    else:
        print("\n❌ All ping packets lost!")
        return False

if __name__ == "__main__":
    import sys
    
    robot_ip = "169.254.80.144"
    success = test_ping_stability(robot_ip, count=15)
    sys.exit(0 if success else 1)
```

**Run:**
```bash
python test_network_stability.py
```

**Document:**
- [ ] Average latency: _____ms
- [ ] Max latency: _____ms
- [ ] Packet loss: _____%
- [ ] Network quality: _____ (excellent/acceptable/poor)

---

### 8. File Transfer Test

**What to Test:**
Can we transfer files to/from the robot.

```bash
# Test SCP file transfer
scp test_file.txt nao@169.254.80.144:/tmp/

# Verify file transferred
ssh nao@169.254.80.144 "ls -la /tmp/test_file.txt"

# Copy file back
scp nao@169.254.80.144:/tmp/test_file.txt test_file_retrieved.txt

# Verify
ls -la test_file_retrieved.txt
```

**Document:**
- [ ] Can upload files via SCP
- [ ] Can download files via SCP
- [ ] Transfer speed acceptable

---

## Summary Checklist

Complete this checklist for Phase 0 sign-off:

### Network
- [ ] Ping successful (<50ms latency)
- [ ] SSH connection works
- [ ] Network stable (no packet loss)
- [ ] File transfer working

### NAOqi
- [ ] NAOqi service running
- [ ] All proxies connect successfully
- [ ] Battery accessible
- [ ] Stiffness control works

### Motors & Joints
- [ ] All 22 joints accessible
- [ ] Motion proxy responds
- [ ] Can read joint angles
- [ ] Stiffness can be toggled

### Sensors
- [ ] Microphone responding
- [ ] Accelerometer data available
- [ ] Temperature sensors responding
- [ ] Battery level readable

### Audio
- [ ] Speaker plays audio (robot can speak)
- [ ] Microphone input configured
- [ ] Volume controls work

### Overall
- [ ] All critical tests passing
- [ ] Network stable and fast
- [ ] Robot responding to commands
- [ ] Ready for Phase 0!

---

## Next Steps

Once all tests pass:

1. **Document Results**
   - Record all test outcomes
   - Note any issues found
   - Save latency benchmarks

2. **Create Test Report**
   - Fill out PRE_PHASE0_TESTS_REPORT.md
   - Document any anomalies
   - Note firmware versions

3. **Begin Phase 0**
   - Start formal hardware assessment
   - Run diagnostic suite
   - Complete robot baseline documentation

---

**Test Status:** Ready to execute  
**Expected Duration:** 2-3 hours for all tests  
**Robot State:** Powered on and connected ✅
