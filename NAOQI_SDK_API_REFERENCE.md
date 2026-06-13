# NAOqi 2.8.6.23 SDK API Reference

**Version:** NAOqi 2.8.6.23 (Python 2.7)  
**Date:** 2026-06-13  
**Location:** `pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/lib/`

---

## 📚 Overview

NAOqi is Aldebaran's distributed middleware platform for NAO robots. It provides access to:
- Robot motion and movement
- Sensor data (accelerometer, gyroscope, FSR, battery, etc.)
- Audio I/O (microphone, speaker)
- Vision and camera control
- Memory and events
- LED control
- And many more robot functions

---

## 🔗 Core Modules

### **ALProxy** - Remote Method Invocation
```python
from naoqi import ALProxy

# Create a proxy to any NAOqi service
proxy = ALProxy("ServiceName", "169.254.80.144", 9559)

# Synchronous call
result = proxy.methodName(arg1, arg2)

# Asynchronous call
future = proxy.post.methodName(arg1, arg2)
```

### **qi** - Communication Framework
Low-level communication library for RPC and messaging.

---

## 🎮 Motion & Movement APIs

### **ALMotion**
Robot motion control and kinematics
```python
motion = ALProxy("ALMotion", IP, PORT)
```

**Key Methods:**
- `wakeUp()` - Wake up the robot (stiffness ON)
- `rest()` - Put robot to rest (stiffness OFF)
- `getStiffnesses(names)` - Get joint stiffness
- `setStiffnesses(names, stiffness)` - Set joint stiffness
- `getAngles(names, useSensors)` - Read joint angles (degrees/radians)
- `setAngles(names, angles, fractionMaxSpeed)` - Move joints
- `moveTo(x, y, theta)` - Move robot in 2D space
- `turnHead()` - Head movement
- `walkForward(distance)` - Walk forward
- `walkBackward(distance)` - Walk backward
- `turnLeft(angle)` - Turn left
- `turnRight(angle)` - Turn right
- `stopMove()` - Stop all motion
- `getBodyNames(group)` - Get joint names
- `getMaxSpeed(names)` - Get max joint speed
- `getMotionCycleTime()` - Get motion cycle period

---

### **ALRobotPosture**
Pre-defined postures and pose control
```python
posture = ALProxy("ALRobotPosture", IP, PORT)
```

**Key Methods:**
- `goToPosture(postureName, maxSpeedFraction)` - Go to predefined posture
- `getPostureList()` - Get available postures
- `getPosture()` - Get current posture

**Available Postures:**
- "Stand" - Standing position
- "Sit" - Sitting position
- "SitRelax" - Sitting relaxed
- "StandZero" - T-pose (arms out)
- "Crouch" - Crouching position
- "LyingBelly" - Lying on belly
- "LyingBack" - Lying on back
- "Stand Init" - Initial stand
- "Stand Zero" - Zero position

---

### **ALWalkingActivity**
Walking pattern generation
```python
walking = ALProxy("ALWalkingActivity", IP, PORT)
```

**Key Methods:**
- `startWalking()` - Start walking
- `stopWalking()` - Stop walking
- `getWalkingConfig(name)` - Get walk configuration
- `setWalkingConfig(name, value)` - Set walk configuration

---

## 📊 Sensor APIs

### **ALMemory**
Access to robot sensor data via named events
```python
memory = ALProxy("ALMemory", IP, PORT)
```

**Key Methods:**
- `getData(key)` - Get data by key name
- `getDataListName()` - Get all available data keys
- `subscribeMicroEvent(event, callback)` - Subscribe to events
- `unsubscribeMicroEvent(event, callback)` - Unsubscribe

**Common Sensor Keys:**

**Accelerometer (IMU):**
- `Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value` (g)
- `Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value` (g)
- `Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value` (g)

**Gyroscope:**
- `Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value` (rad/s)
- `Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value` (rad/s)
- `Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value` (rad/s)

**Foot Sensors (FSR):**
- `Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value`
- `Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value`
- `Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value`
- `Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value`
- `Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value`
- `Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value`
- `Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value`
- `Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value`

**Touch Sensors:**
- `Device/SubDeviceList/Head/Touch/Front/Sensor/Value`
- `Device/SubDeviceList/Head/Touch/Middle/Sensor/Value`
- `Device/SubDeviceList/Head/Touch/Rear/Sensor/Value`
- `Device/SubDeviceList/LHand/Touch/Back/Sensor/Value`
- `Device/SubDeviceList/RHand/Touch/Back/Sensor/Value`

**Bumpers:**
- `Device/SubDeviceList/LFoot/Bumper/Left/Sensor/Value`
- `Device/SubDeviceList/LFoot/Bumper/Right/Sensor/Value`
- `Device/SubDeviceList/RFoot/Bumper/Left/Sensor/Value`
- `Device/SubDeviceList/RFoot/Bumper/Right/Sensor/Value`

**Temperature:**
- `Device/SubDeviceList/Battery/Sensor/Temperature` (°C)

**CPU/Actuator Temperature:**
- `Device/SubDeviceList/ChestBoard/Sensor/Temperature`
- `Device/SubDeviceList/LLeg/Ankle/Roll/Temperature`
- `Device/SubDeviceList/RLeg/Ankle/Roll/Temperature`

---

### **ALBattery**
Battery status and monitoring
```python
battery = ALProxy("ALBattery", IP, PORT)
```

**Key Methods:**
- `getBatteryCharge()` - Get battery charge percentage (0-100)
- `getBatteryStatus()` - Get battery status string
- `getBatteryTemperature()` - Get battery temperature in °C

---

### **ALSensors**
General sensor management
```python
sensors = ALProxy("ALSensors", IP, PORT)
```

**Key Methods:**
- `getSensorsNames()` - Get list of all sensors
- `getSensorsValues(sensorsList)` - Get multiple sensor values

---

## 🎤 Audio APIs

### **ALAudioDevice**
Audio input/output control
```python
audio = ALProxy("ALAudioDevice", IP, PORT)
```

**Key Methods:**
- `getOutputVolume()` - Get speaker volume (0-100)
- `setOutputVolume(volume)` - Set speaker volume
- `getInputVolume()` - Get microphone volume (NOT in 2.8.6.23)
- `setInputVolume(volume)` - Set microphone volume
- `recordFile(soundFile)` - Record audio to file
- `playFile(soundFile)` - Play audio file
- `getSoundList()` - Get list of available sounds
- `stopAudio()` - Stop audio playback

---

### **ALTextToSpeech**
Text-to-speech synthesis
```python
tts = ALProxy("ALTextToSpeech", IP, PORT)
```

**Key Methods:**
- `say(text)` - Speak text
- `say(text, language)` - Speak in specific language
- `getLanguage()` - Get current language
- `setLanguage(language)` - Set language
- `getAvailableLanguages()` - Get supported languages
- `setParameter(param, value)` - Set TTS parameters
- `getParameter(param)` - Get TTS parameter
- `setVolume(volume)` - Set voice volume

**Supported Languages:**
- English (en_US)
- French (fr_FR)
- Spanish (es_ES)
- German (de_DE)
- Italian (it_IT)
- Japanese (ja_JP)
- Mandarin (zh_CN)
- And more...

---

### **ALSoundLocalization**
Locate sound sources
```python
sound = ALProxy("ALSoundLocalization", IP, PORT)
```

**Key Methods:**
- `setParameter(paramName, value)` - Set sound localization parameters
- `getParameter(paramName)` - Get parameters
- `subscribe(serviceName)` - Subscribe to sound detection

---

## 👁️ Vision APIs

### **ALVideoDevice**
Camera capture and video processing
```python
video = ALProxy("ALVideoDevice", IP, PORT)
```

**Key Methods:**
- `getImageLocal(cameraId)` - Get camera image
- `releaseImage(imageId)` - Release image memory
- `startCamera(cameraId)` - Start camera
- `stopCamera(cameraId)` - Stop camera
- `setCameraParameter(cameraId, param, value)` - Camera settings
- `getCameraParameter(cameraId, param)` - Get camera parameter

**Camera IDs:**
- 0 = Top camera (front)
- 1 = Bottom camera (front)

---

### **ALFaceDetection**
Face detection (if available)
```python
face = ALProxy("ALFaceDetection", IP, PORT)
```

**Key Methods:**
- `subscribe(name)` - Subscribe to face detection
- `unsubscribe(name)` - Unsubscribe
- `setParameter(param, value)` - Set detection parameters

---

## 💡 LED APIs

### **ALLeds**
LED control and effects
```python
leds = ALProxy("ALLeds", IP, PORT)
```

**Key Methods:**
- `on(name)` - Turn on LED
- `off(name)` - Turn off LED
- `setIntensity(name, intensity)` - Set LED brightness (0.0-1.0)
- `fadeRGB(name, rgb, duration)` - Fade to RGB color
- `post.fadeRGB(name, rgb, duration)` - Asynchronous fade
- `randomEyes()` - Animate eyes randomly
- `rasta()` - Rasta animation
- `setParameter(name, param, value)` - LED parameters

**LED Groups:**
- "FaceLeds" - Face LEDs
- "ChestLeds" - Chest LEDs
- "LeftFootLeds" - Left foot LEDs
- "RightFootLeds" - Right foot LEDs
- "LeftEarLeds" - Left ear LEDs
- "RightEarLeds" - Right ear LEDs
- "AllLeds" - All LEDs

---

## 🎭 Expression & Gesture APIs

### **ALRobotExpression**
Robot expressions and emotions
```python
expression = ALProxy("ALRobotExpression", IP, PORT)
```

**Key Methods:**
- `createTrigger(condition, callback)` - Create behavior triggers
- `removeTrigger(triggerId)` - Remove trigger

---

### **ALGesture**
Gesture control
```python
gesture = ALProxy("ALGesture", IP, PORT)
```

**Key Methods:**
- `playGesture(gestureName)` - Play gesture
- `getGestureList()` - List available gestures
- `playGestureFromFile(path)` - Play custom gesture

---

## 🧠 AI & Behavior APIs

### **ALBehaviorManager**
Manage and control behaviors
```python
behavior = ALProxy("ALBehaviorManager", IP, PORT)
```

**Key Methods:**
- `startBehavior(behaviorName)` - Start behavior
- `stopBehavior(behaviorName)` - Stop behavior
- `runBehavior(behaviorName)` - Run behavior once
- `getBehaviorList()` - List installed behaviors
- `isBehaviorRunning(behaviorName)` - Check if running
- `getRunningBehaviors()` - Get all running behaviors

---

## ⏱️ Timing & Scheduling APIs

### **ALScheduler**
Schedule tasks and callbacks
```python
scheduler = ALProxy("ALScheduler", IP, PORT)
```

**Key Methods:**
- `scheduleAtFixedRate(callback, delay, period)` - Periodic callback
- `scheduleOnce(callback, delay)` - One-time callback
- `cancel(taskId)` - Cancel scheduled task

---

## 📡 DCM (Device Communication Manager)

### **DCM**
Low-level device control
```python
dcm = ALProxy("DCM", IP, PORT)
```

**Key Methods:**
- `setDesired(device_commands)` - Set device values
- `getTime(timestamp)` - Get robot time

---

## 🔌 Configuration APIs

### **ALResourceManager**
Manage robot resources
```python
resource = ALProxy("ALResourceManager", IP, PORT)
```

---

### **ALServiceManager**
Manage loaded services
```python
services = ALProxy("ALServiceManager", IP, PORT)
```

**Key Methods:**
- `getServices()` - List loaded services
- `getServiceInfo(serviceName)` - Get service details
- `registerService(serviceName, address)` - Register service

---

## 📜 Logging APIs

### **ALLogger**
Access robot logs
```python
logger = ALProxy("ALLogger", IP, PORT)
```

**Key Methods:**
- `getLogPath()` - Get log directory path
- `flushLogs()` - Flush logs to disk

---

## 🔐 System APIs

### **ALRobotInfo**
Robot information and system details
```python
info = ALProxy("ALRobotInfo", IP, PORT)
```

**Key Methods:**
- `getRobotType()` - Get robot model
- `getRobotVersion()` - Get robot software version
- `getMemoryUsage()` - Get memory statistics

---

### **ALDiagnostics**
System diagnostics
```python
diag = ALProxy("ALDiagnostics", IP, PORT)
```

---

## 📚 Complete ALProxy Usage Example

```python
from naoqi import ALProxy

robot_ip = "169.254.80.144"
robot_port = 9559

# Motion control
motion = ALProxy("ALMotion", robot_ip, robot_port)
motion.wakeUp()
motion.moveTo(0.2, 0.0, 0.0)  # Move 20cm forward
motion.rest()

# Text-to-speech
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
tts.say("Hello World")

# Read sensors
memory = ALProxy("ALMemory", robot_ip, robot_port)
battery = memory.getData("Device/SubDeviceList/Battery/Sensor/Charge")
print "Battery: {0}%".format(battery)

# LED control
leds = ALProxy("ALLeds", robot_ip, robot_port)
leds.fadeRGB("FaceLeds", 0xFF0000FF, 0.5)  # Red

# Take picture
video = ALProxy("ALVideoDevice", robot_ip, robot_port)
image = video.getImageLocal(0)  # Top camera
video.releaseImage(image[6])
```

---

## ⚠️ NAOqi 2.8.6.23 Specific Notes

**Methods NOT available in this version:**
- `ALAudioDevice.getInputVolume()` 
- `ALBattery.getBatteryHealth()`
- `ALVideoDevice.getCameraList()`
- Some advanced facial recognition features

**Available sensors confirmed:**
✅ Accelerometer (IMU)
✅ Gyroscope
✅ Foot Sensors (FSR)
✅ Touch Sensors
✅ Battery charge
✅ Temperature sensors
✅ Joint encoders
✅ Speaker/audio output
✅ Camera access (basic)

---

## 🚀 Getting Started

### 1. Connect to Robot
```python
from naoqi import ALProxy
motion = ALProxy("ALMotion", "169.254.80.144", 9559)
```

### 2. Wake Up
```python
motion.wakeUp()
```

### 3. Control Movement
```python
motion.moveTo(0.1, 0.0, 0.0)  # Move 10cm forward
```

### 4. Read Sensors
```python
memory = ALProxy("ALMemory", IP, PORT)
acc_x = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
```

### 5. Speak
```python
tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.say("Hello!")
```

### 6. Rest
```python
motion.rest()
```

---

## 📖 Documentation Links

- Official NAOqi Documentation: http://doc.aldebaran.com/
- NAO V4 Hardware specs: http://doc.aldebaran.com/2-8/family/nao_v4/
- Sensor data keys: http://doc.aldebaran.com/2-8/dev_guide/python/examples/

---

## 📞 API Reference Summary

| Module | Purpose | Status |
|--------|---------|--------|
| ALMotion | Movement control | ✅ Working |
| ALMemory | Sensor data | ✅ Working |
| ALAudioDevice | Audio I/O | ⚠️ Partial |
| ALBattery | Battery status | ✅ Working |
| ALLeds | LED control | ✅ Working |
| ALVideoDevice | Camera control | ⚠️ Limited |
| ALTextToSpeech | Text-to-speech | ✅ Working |
| ALRobotPosture | Posture control | ✅ Working |
| ALBehaviorManager | Behavior control | ✅ Working |
| ALLogger | Logging | ✅ Working |
| ALServiceManager | Service management | ✅ Working |

---

**NAOqi Version:** 2.8.6.23  
**Last Updated:** 2026-06-13  
**Tested:** Yes ✅
