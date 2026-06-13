# New Robot Setup Guide

**Robot IP:** 169.254.175.171  
**Date:** 2026-06-13  

---

## ✅ Quick Setup (5 minutes)

### Step 1: Update IP Address in All Files

**Option A: PowerShell (Recommended)**
```powershell
.\update_robot_ip.ps1
```

**Option B: Batch Script**
```bash
update_robot_ip.bat
```

Both scripts will:
- ✅ Find all Python test files
- ✅ Find all documentation files
- ✅ Replace old IP with new IP: 169.254.175.171
- ✅ Display update summary

---

### Step 2: Verify Robot Connection

**Test 1: Ping Robot**
```bash
ping 169.254.175.171
```

**Expected output:**
```
Pinging 169.254.175.171 with 32 bytes of data:
Reply from 169.254.175.171: bytes=32 time=5ms TTL=64
Reply from 169.254.175.171: bytes=32 time=4ms TTL=64
```

**Test 2: Test NAOqi Connection**
```bash
python -c "from naoqi import ALProxy; ALProxy('ALMotion', '169.254.175.171', 9559); print('OK')"
```

**Expected output:**
```
OK
```

---

### Step 3: Run Phase 0 Tests

```bash
run_phase0_tests.bat
```

**Expected Duration:** 30-45 minutes

**Expected Result:** All 5 tests pass ✅

---

## 📋 What Gets Updated

### Test Scripts (9 files)
- ✅ test_phase0_joint_control.py
- ✅ test_phase0_motion.py
- ✅ test_phase0_sensors_detailed.py
- ✅ test_phase0_audio.py
- ✅ test_phase0_leds.py
- ✅ test_1_naoqi_basic_py27.py
- ✅ test_2_network_stability_py27.py
- ✅ test_3_robot_sensors_py27.py
- ✅ run_all_tests_py27.py

### Documentation (2 files)
- ✅ WIFI_CONNECTION_GUIDE.md
- ✅ PHASE0_ASSESSMENT_GUIDE.md

---

## 🔍 Old vs New IP

| Aspect | Old Robot | New Robot |
|--------|-----------|-----------|
| **IP Address** | 169.254.80.144 | 169.254.175.171 |
| **Connection Type** | LAN (wired) | LAN (wired) |
| **NAOqi Version** | 2.8.6.23 | 2.8.6.23 (assumed) |
| **All Tests** | ✅ Working | ✅ Should work |

---

## ✅ Verification Checklist

- [ ] IP update scripts run successfully
- [ ] `ping 169.254.175.171` responds
- [ ] NAOqi connection test returns "OK"
- [ ] run_phase0_tests.bat starts successfully
- [ ] All 5 tests pass
- [ ] Results saved to phase0_results/

---

## 🚀 Next Steps

1. ✅ Run update script
2. ✅ Verify connectivity
3. ✅ Run Phase 0 tests
4. ✅ Document baseline
5. ✅ Proceed to Phase 1

---

## 📞 If Issues Occur

**Problem: Ping fails**
- Check robot is powered on
- Check network cable connected
- Try static IP assignment

**Problem: NAOqi connection fails**
- Verify ping works first
- Check port 9559 is accessible
- Try power cycling robot (off 30s, on 60s)

**Problem: Tests fail with old IP**
- Confirm update scripts completed
- Check test files for old IP manually
- Search for "169.254.80" in test files

---

## 🎯 Summary

**Old Robot:** 169.254.80.144 ❌  
**New Robot:** 169.254.175.171 ✅  

**All files updated automatically:**
```bash
.\update_robot_ip.ps1
# OR
update_robot_ip.bat
```

**Verify:**
```bash
ping 169.254.175.171
python -c "from naoqi import ALProxy; ALProxy('ALMotion', '169.254.175.171', 9559); print('OK')"
```

**Run tests:**
```bash
run_phase0_tests.bat
```

---

Ready to proceed with Phase 0! 🚀

