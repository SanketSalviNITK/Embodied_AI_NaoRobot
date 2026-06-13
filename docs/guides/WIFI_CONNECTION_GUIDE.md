# WiFi Connection Guide for NAO V4

**Enable wireless connectivity** while maintaining full programming and testing capabilities

---

## 🌐 Overview

### Current Setup
- **Connection:** LAN (wired ethernet)
- **Robot IP:** 169.254.80.144
- **System IP:** 169.254.80.100
- **Network:** Direct point-to-point

### WiFi Setup
- **Connection:** WiFi (wireless)
- **Robot IP:** [DHCP or Static - TBD]
- **System IP:** [Router IP range]
- **Network:** Standard WiFi router

---

## ✅ WiFi Capabilities

NAO V4 **fully supports WiFi:**
- ✅ 2.4GHz wireless (standard)
- ✅ 5GHz wireless (with compatible router)
- ✅ Full NAOqi functionality over WiFi
- ✅ Same programming/testing capability as LAN
- ✅ Multiple connections supported

---

## 📋 Prerequisites

### Hardware Needed
- ✅ WiFi router (2.4GHz minimum, 5GHz recommended)
- ✅ Router within range of robot (10-30m typical)
- ✅ Network SSID (WiFi name)
- ✅ Network password

### Robot Requirements
- ✅ NAO V4 with WiFi module
- ✅ Fully charged battery
- ✅ NAOqi 2.8.6.23 (already installed)
- ✅ Access to robot settings

---

## 🔧 Step 1: Connect Robot to WiFi

### Option A: Via Web Interface (Easiest)

**Step 1: Find Robot IP on Current LAN**
```
Current: 169.254.80.144
```

**Step 2: Open Web Browser**
```
URL: http://169.254.80.144:8080/
```

**Step 3: Navigate to Network Settings**
```
Settings → Network → WiFi
```

**Step 4: Select Your WiFi Network**
- Look for your SSID (WiFi name)
- Enter WiFi password
- Select "Connect"

**Step 5: Wait for Connection**
- Robot will connect to WiFi
- Page will show new IP address
- Note the new IP (format: 192.168.x.x or similar)

---

### Option B: Via SSH (Advanced)

**Step 1: SSH into Robot (Current LAN)**
```bash
ssh nao@169.254.80.144
```

**Step 2: Edit Network Configuration**
```bash
sudo nano /etc/network/interfaces
```

**Step 3: Add WiFi Configuration**
```
auto wlan0
iface wlan0 inet dhcp
    wpa-ssid "YOUR_WIFI_NAME"
    wpa-psk "YOUR_WIFI_PASSWORD"
```

**Step 4: Save and Restart Network**
```bash
sudo service networking restart
```

**Step 5: Get New IP**
```bash
ifconfig
# Look for wlan0 inet addr: xxx.xxx.xxx.xxx
```

---

### Option C: Via Physical Robot Menu

**If robot has display:**
1. Use head touch to navigate menu
2. Select "Network Settings"
3. Choose "WiFi"
4. Select SSID
5. Enter password
6. Confirm connection

---

## 🔍 Step 2: Find Robot's WiFi IP Address

### Method 1: From Web Interface
- Robot will show new IP after WiFi connection
- Format: `192.168.x.x` (depends on your router)

### Method 2: Via Router Admin Panel
```
1. Go to router web interface
2. Look for "Connected Devices"
3. Find "NAO" or check MAC address
4. Note the IP address
```

### Method 3: Via Command Line
```bash
# From your computer, find NAO on network
ping nao.local  # May work on some networks

# Or scan network for 169.254.x.x devices
arp -a  # Shows all connected devices
```

### Method 4: SSH from LAN
```bash
# While still connected via LAN
ssh nao@169.254.80.144

# Inside robot
ifconfig
# Look for wlan0 section, find "inet addr:"
```

---

## 🖥️ Step 3: Update Test Scripts

Once you have the new WiFi IP, update your test scripts:

### Find & Replace
In all test files, replace:
```python
robot_ip = "169.254.80.144"
```

With your new WiFi IP:
```python
robot_ip = "192.168.x.x"  # Your WiFi IP
```

### Files to Update
- `test_phase0_joint_control.py`
- `test_phase0_motion.py`
- `test_phase0_sensors_detailed.py`
- `test_phase0_audio.py`
- `test_phase0_leds.py`
- `run_all_tests_py27.py`
- `test_1_naoqi_basic_py27.py`
- `test_2_network_stability_py27.py`
- `test_3_robot_sensors_py27.py`

### Quick Update Script
```bash
# PowerShell (replace all IPs in Python files)
(Get-Content test_phase0_*.py) -replace '169.254.80.144', '192.168.x.x' | Set-Content test_phase0_*.py
```

---

## ✅ Step 4: Verify WiFi Connection

### Test 1: Ping Robot
```bash
ping 192.168.x.x
```

**Expected output:**
```
Pinging 192.168.x.x with 32 bytes of data:
Reply from 192.168.x.x: bytes=32 time=5ms TTL=64
Reply from 192.168.x.x: bytes=32 time=4ms TTL=64
```

### Test 2: Test NAOqi Connection
```bash
python -c "from naoqi import ALProxy; ALProxy('ALMotion', '192.168.x.x', 9559); print('OK')"
```

**Expected output:**
```
OK
```

### Test 3: Run Pre-Phase0 Tests
```bash
python test_1_naoqi_basic_py27.py
```

Should complete successfully with all tests passing.

---

## 🔄 Switching Between LAN and WiFi

### Keep Both Connections

**Option 1: Both Cables & WiFi Active**
- Robot can be connected to both
- LAN takes priority (usually)
- Keep LAN cable in place as backup

**Option 2: Switch as Needed**
- Disconnect ethernet cable to force WiFi
- Robot will use WiFi when LAN unavailable
- Easy to switch back by plugging cable in

**Option 3: Disable One**
Via web interface or SSH:
- Disable LAN: Removes ethernet configuration
- Disable WiFi: Removes WiFi configuration
- Only one active at a time

---

## 📊 LAN vs WiFi Comparison

| Aspect | LAN | WiFi |
|--------|-----|------|
| **Speed** | 100 Mbps | 20-54 Mbps |
| **Latency** | 1-5ms | 5-20ms |
| **Stability** | Very stable | Generally stable |
| **Range** | ~1m (cable) | 10-30m |
| **Reliability** | Excellent | Good |
| **Setup** | Plug & play | Config needed |
| **Mobility** | Fixed location | Flexible |

---

## ⚠️ Important Notes

### Latency Impact
WiFi adds slight latency (~10-15ms more):
- ✅ **Still fine for:** Testing, development, real-time AI
- ⚠️ **May affect:** High-speed network tests, millisecond-critical operations

### Network Stability
- WiFi can have drops: Always keep LAN as backup
- Robot auto-reconnects to WiFi if connection drops
- LAN reconnection is instant (if cable plugged)

### IP Address Changes
- **Static IP recommended:** Set in router DHCP settings
- **Dynamic IP:** Get new IP each reconnection
- **Save new IP:** Once confirmed stable

### Firewall/Router
- Some routers block devices by default
- May need to whitelist robot MAC address
- Check router admin panel if connection issues

---

## 🚀 Running Tests Over WiFi

### Before Running Tests
1. ✅ Confirm WiFi connection: `ping 192.168.x.x`
2. ✅ Update IP in all test scripts
3. ✅ Verify NAOqi works: Test basic connection
4. ✅ Check battery level >20%
5. ✅ Clear robot's movement space

### Run Tests
```bash
# Now using WiFi IP instead of LAN
run_phase0_tests.bat

# Or individual test
python test_phase0_joint_control.py
```

### Monitor Stability
- Watch for timeouts or connection drops
- Check robot's WiFi signal strength
- If issues, check router logs
- Switch back to LAN if needed

---

## 🔧 Troubleshooting WiFi

### Robot Won't Connect to WiFi

**Check 1: WiFi Credentials**
```
Verify SSID and password are correct
Make sure WiFi is enabled on router
```

**Check 2: WiFi Compatibility**
```
NAO V4 supports: 802.11 b/g/n
Frequency: 2.4GHz (5GHz if supported)
```

**Check 3: Robot Restart**
```
Power off robot for 30 seconds
Power on and wait 60 seconds
Try WiFi connection again
```

---

### Connected but Can't Communicate

**Check 1: Find IP Address**
```bash
# SSH via LAN first
ssh nao@169.254.80.144

# Check wlan0 IP
ifconfig | grep "inet addr" -A 1 -B 1
```

**Check 2: Test Connectivity**
```bash
# From your computer
ping <WiFi_IP>

# From robot
ping 8.8.8.8  # Google DNS
```

**Check 3: NAOqi Port**
```bash
# Check if port 9559 is open
telnet <WiFi_IP> 9559
```

---

### Slow or Unstable Connection

**Check 1: WiFi Signal**
```
Get closer to router
Check for interference (microwaves, cordless phones)
Switch to 5GHz if available
```

**Check 2: Network Congestion**
```
Reduce other device usage
Avoid heavy downloads
Test at quiet network time
```

**Check 3: Keep LAN Backup**
```
Connect ethernet cable too
Switch to LAN if WiFi unstable
Use LAN for critical tests
```

---

## 📝 Setup Checklist

### Pre-WiFi
- [ ] Robot powered on
- [ ] Connected via LAN (169.254.80.144)
- [ ] Router available with SSID/password
- [ ] Clear line of sight to router
- [ ] NAOqi 2.8.6.23 running

### WiFi Configuration
- [ ] Accessed robot web interface (http://169.254.80.144:8080/)
- [ ] Navigated to Network/WiFi settings
- [ ] Selected WiFi SSID
- [ ] Entered password correctly
- [ ] Clicked "Connect"

### Post-WiFi Setup
- [ ] Found robot's new WiFi IP address
- [ ] Pinged robot: `ping <WiFi_IP>`
- [ ] Tested NAOqi connection
- [ ] Updated IP in test scripts
- [ ] Ran Phase 0 tests over WiFi

### Verification
- [ ] Robot responds to NAOqi calls over WiFi
- [ ] All 5 Phase 0 tests pass over WiFi
- [ ] Network latency acceptable (<50ms)
- [ ] WiFi connection stable
- [ ] LAN cable kept as backup

---

## 🎯 After WiFi Setup

### Recommended Configuration
```
┌─────────────────┐
│   WiFi Router   │
└────────┬────────┘
         │
    ┌────┴────┐
    │          │
   NAO      Your PC
 (WiFi)    (WiFi or LAN)
```

### Keep LAN Available
- Leave ethernet cable connected
- Switch to LAN if WiFi unstable
- Use LAN for critical tests
- WiFi for development/testing

### Run Phase 0 Again
```bash
run_phase0_tests.bat  # All tests run over WiFi
```

**Expected Results:**
- ✅ All 5 tests pass
- ⚠️ Slightly higher latency (still acceptable)
- ✅ Full functionality maintained

---

## 📚 Additional Resources

### More Information
- NAO WiFi setup: Search "NAO V4 WiFi configuration"
- NAOqi over network: http://doc.aldebaran.com/
- Router configuration: Check your router manual

### Common Issues
- See "Troubleshooting WiFi" section above
- Most issues resolve with proper IP configuration
- Keep LAN as fallback for stable operation

### Next Steps
1. ✅ Set up WiFi connection
2. ✅ Verify connectivity
3. ✅ Update test scripts with new IP
4. ✅ Run Phase 0 tests over WiFi
5. ✅ Document baseline with WiFi IP
6. ✅ Proceed to Phase 1 development

---

**WiFi Setup Ready to Begin!**

Once complete, you'll have:
- ✅ Wireless connectivity to robot
- ✅ Same full programming capability
- ✅ Flexibility to move robot around
- ✅ LAN backup for stability

---

Created: 2026-06-13  
Status: Ready to implement

