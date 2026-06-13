# Python 2.7 Test Guide (NAOqi 2.8.6.23)

**CRITICAL:** Your NAOqi version is **2.8.6.23-Python2.7 compatible ONLY**

You MUST use Python 2.7, NOT Python 3.x!

---

## ✅ Files Created for Python 2.7

```
run_all_tests_py27.py          ← Use this! (Master runner)
test_1_naoqi_basic_py27.py     ← NAOqi connectivity test
test_2_network_stability_py27.py ← Network quality test
test_3_robot_sensors_py27.py    ← Sensor validation test
```

All are compatible with:
- Python 2.7
- NAOqi 2.8.6.23-win64-vs2015

---

## 🚀 How to Run Tests

### Option 1: Run All Tests At Once (RECOMMENDED)

```bash
python2.7 run_all_tests_py27.py
```

Or if you have Python 2.7 in your PATH as just `python`:

```bash
python run_all_tests_py27.py
```

**This will:**
1. Test NAOqi connectivity
2. Test network stability
3. Test robot sensors
4. Generate automatic report: `TEST_RESULTS_SUMMARY.txt`

**Duration:** 15-20 minutes

### Option 2: Run Individual Tests

```bash
# Test 1: NAOqi connectivity
python2.7 test_1_naoqi_basic_py27.py

# Test 2: Network quality
python2.7 test_2_network_stability_py27.py

# Test 3: Sensor validation
python2.7 test_3_robot_sensors_py27.py
```

---

## ⚠️ Prerequisites

### 1. Python 2.7 Installed

**Check:**
```bash
python2.7 --version
```

Should output something like:
```
Python 2.7.x
```

### 2. NAOqi SDK for Python 2.7

**Check:**
```bash
python2.7 -c "from naoqi import ALProxy; print('OK')"
```

Should output: `OK`

**If not installed:**

You have this folder in your project:
```
pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649
```

**Add it to PYTHONPATH:**

On Windows (Command Prompt):
```bash
set PYTHONPATH=%PYTHONPATH%;C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\lib
```

Or add to Python path directly in your script (already handled in test files).

### 3. Robot is Powered On and Connected

```bash
ping 169.254.80.144
```

Should see responses (not "Unreachable").

---

## 📋 What You'll See

### Good Output Example

```
======================================================================
TEST 1: NAOqi Basic Connection (Python 2.7)
======================================================================

Connecting to robot at 169.254.80.144:9559...

OK  NAOqi module imported successfully

1. Testing ALMotion proxy...
   OK  ALMotion proxy created successfully

2. Testing ALRobotPosture proxy...
   OK  ALRobotPosture proxy created successfully

... (more tests)

======================================================================
OK  ALL TESTS PASSED!
======================================================================

Robot is responding correctly and all proxies are accessible.

Next test: Run test_2_network_stability_py27.py
```

### If Tests Fail

**Error: "ImportError: No module named naoqi"**
- NAOqi SDK not properly installed for Python 2.7
- Need to add SDK to PYTHONPATH (see Prerequisites section)

**Error: "Connection refused"**
- Robot not powered on
- Wrong IP address
- NAOqi service not running on robot

**Error: "Timeout"**
- Network issue
- Robot disconnected
- Firewall blocking

---

## 📊 Success Criteria

### Test 1 - PASS if:
✅ All proxies created successfully  
✅ Battery data accessible  
✅ No connection errors  

### Test 2 - PASS if:
✅ Max latency <50ms (excellent)  
✅ 0% packet loss  
✅ Consistent response times  

### Test 3 - PASS if:
✅ Most sensors responding  
✅ No critical failures  
✅ Data values reasonable  

### Overall - READY FOR PHASE 0 if:
✅ All 3 tests pass OR  
✅ Tests 1&2 pass + minimal warnings in Test 3  

---

## 🔧 Troubleshooting

### "python2.7: command not found"

**Windows:**
```bash
# Check if Python 2.7 is in PATH
python --version

# If that shows Python 2.7, use:
python run_all_tests_py27.py

# Or find full path:
where python2.7

# Use full path if needed:
C:\Python27\python.exe run_all_tests_py27.py
```

**Fallback:**
```bash
# Just use python if it's Python 2.7
python run_all_tests_py27.py
```

---

### NAOqi SDK Not Found

**Check where it is:**
```bash
ls -la pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649/
```

**Add to path (Windows Command Prompt):**
```bash
set PYTHONPATH=%cd%\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\lib;%PYTHONPATH%
```

**Or (PowerShell):**
```powershell
$env:PYTHONPATH = "$pwd\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\lib;$env:PYTHONPATH"
```

**Then run tests:**
```bash
python2.7 run_all_tests_py27.py
```

---

### Robot Won't Connect

```bash
# Test 1: Can you ping it?
ping 169.254.80.144

# Test 2: Is NAOqi running on robot?
ssh nao@169.254.80.144 "ps aux | grep naoqi"

# Test 3: Can you SSH?
ssh nao@169.254.80.144

# Test 4: Check NAOqi port
# Should be listening on port 9559
ssh nao@169.254.80.144 "netstat -an | grep 9559"
```

If you can't SSH or port 9559 isn't open:
- Power cycle the robot
- Wait 60 seconds for full boot
- Try again

---

## ✅ Complete Step-by-Step

```bash
# 1. Check Python 2.7
python2.7 --version

# 2. Check NAOqi can be imported
python2.7 -c "from naoqi import ALProxy; print('NAOqi OK')"

# 3. Check robot is reachable
ping 169.254.80.144

# 4. Run all tests
python2.7 run_all_tests_py27.py

# 5. Review results
type TEST_RESULTS_SUMMARY.txt
```

---

## 📝 Expected Duration

- Test 1: 2-3 minutes
- Test 2: 5-10 minutes (15 pings)
- Test 3: 3-5 minutes
- **Total: 15-20 minutes**

---

## 📊 Key Differences from Python 3 Version

These scripts are Python 2.7 compatible because:

❌ NO f-strings (removed, use .format() instead)  
❌ NO type hints (not supported in Python 2.7)  
✅ Uses subprocess.Popen instead of subprocess.run  
✅ Manual statistics calculation (no statistics module)  
✅ Compatible print function syntax  

---

## 🎯 Next Steps After Tests Pass

1. ✅ Save `TEST_RESULTS_SUMMARY.txt`
2. ✅ Review results for any warnings
3. ✅ Proceed to Phase 0: Robot Assessment
4. ✅ Follow docs/phases/Phase-0-Robot-Assessment.md

---

## ❌ If Tests Fail

1. Review error messages carefully
2. Check troubleshooting section above
3. Fix identified issues
4. Re-run the specific failed test:
   ```bash
   python2.7 test_1_naoqi_basic_py27.py
   ```
5. If still failing, check:
   - NAOqi SDK installation
   - Python 2.7 version compatibility
   - Network connectivity
   - Robot power and response

---

## 💡 Tips

- Make sure you use `python2.7` NOT `python3`
- If `python2.7` doesn't work, try just `python` (if it's Python 2.7)
- Keep robot powered on during all tests
- Close other programs using network bandwidth
- Use wired Ethernet if possible (not WiFi)

---

**NAOqi Version:** 2.8.6.23-Python2.7  
**Python Required:** 2.7.x  
**Test Files:** _py27 suffix  
**Created:** 2026-06-13

Go! 🚀
