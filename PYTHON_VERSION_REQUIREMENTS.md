# Python Version Requirements & NAOqi Compatibility

**⚠️ IMPORTANT:** Python version compatibility with NAOqi is critical!

---

## NAOqi Python Compatibility

### NAOqi 2.8.x (Most Common for NAO V4)

| NAOqi Version | Python 2.7 | Python 3.5 | Python 3.6 | Python 3.7 | Python 3.8+ |
|---|---|---|---|---|---|
| 2.8.5 | ✅ Yes | ⚠️ Maybe | ⚠️ Maybe | ❌ No | ❌ No |
| 2.8.6 | ✅ Yes | ⚠️ Maybe | ⚠️ Maybe | ❌ No | ❌ No |
| 2.8.7 | ✅ Yes | ⚠️ Partial | ❌ No | ❌ No | ❌ No |

**Legend:**
- ✅ Fully supported
- ⚠️ Partial/experimental support
- ❌ Not supported

---

## What's the NAOqi Version on Your Robot?

**Check your robot's NAOqi version:**

```bash
# Via SSH to robot
ssh nao@169.254.80.144
naoqi --version

# Or check from Windows/Linux
ssh nao@169.254.80.144 "naoqi --version"
```

**Record your version:** _______________

---

## Python Version on Your Development Machine

**Check your current Python version:**

```bash
python --version
python3 --version
```

**Current versions:**
- `python`: _______________
- `python3`: _______________

---

## ⚠️ Critical Issue with My Test Scripts

I created the test scripts with:
```python
#!/usr/bin/env python3
```

**This assumes Python 3.x, BUT:**
- NAOqi 2.8.x is primarily built for **Python 2.7**
- Python 3 support is **limited/experimental**
- Using Python 3 may cause import errors

---

## RECOMMENDED SOLUTIONS

### Solution 1: Check NAOqi Version First (RECOMMENDED)

```bash
# SSH into robot
ssh nao@169.254.80.144

# Check NAOqi version
naoqi --version

# Check Python on robot
python --version
python3 --version
```

**If output shows:**
- Python 2.7 only → Use Python 2.7 for NAOqi tests
- Python 3.x available → Can try Python 3.x but may have issues
- Both available → Use Python 2.7 for compatibility

### Solution 2: Use Python 2.7 (Safest Option)

If your robot runs NAOqi 2.8.x and you have Python 2.7 available:

```bash
# Install NAOqi for Python 2.7
pip2 install naoqi

# Run tests with Python 2.7
python2 test_1_naoqi_basic.py
python2 test_2_network_stability.py
python2 test_3_robot_sensors.py

# Or master runner
python2 run_all_tests.py
```

### Solution 3: Create Python 2.7 Compatible Scripts

I can update the test scripts to be compatible with Python 2.7 if needed.

Changes needed:
```python
# Instead of:
#!/usr/bin/env python3

# Use:
#!/usr/bin/env python2.7

# Or (more compatible):
#!/usr/bin/env python

# Avoid Python 3-only syntax:
# - f-strings (use .format() instead)
# - Type hints
# - Print function (already done in my code)
```

---

## Immediate Action Required

**Before running ANY tests:**

1. **Determine your NAOqi version:**
   ```bash
   ssh nao@169.254.80.144 "naoqi --version"
   ```

2. **Document the version:**
   NAOqi version: _______________
   NAOqi Python support: _______________

3. **Check available Python versions:**
   ```bash
   python --version
   python2 --version
   python2.7 --version
   python3 --version
   ```

4. **Report back with:**
   - NAOqi version
   - Available Python versions
   - Which Python version should we target

---

## If You're Not Sure

**Safest approach:**

1. **Keep Python 2.7 installation** (if you have it)
   ```bash
   python2.7 --version
   ```

2. **Install NAOqi for Python 2.7:**
   ```bash
   pip2 install naoqi
   ```

3. **Update test scripts** to use Python 2.7 (I can do this)

4. **Run tests with Python 2.7:**
   ```bash
   python2.7 run_all_tests.py
   ```

---

## Python 2.7 vs Python 3.x Considerations

### Why Python 2.7?
- ✅ Full NAOqi 2.8.x compatibility
- ✅ NAOqi SDK officially built for Python 2.7
- ✅ Most reliable for robot communication
- ❌ Deprecated (EOL January 2020)

### Why Python 3.x?
- ✅ Modern, actively maintained
- ✅ Better performance
- ✅ More libraries available
- ❌ Limited NAOqi compatibility
- ❌ May require older NAOqi versions

---

## Recommendations

### For NAO V4 with NAOqi 2.8.x

**Use Python 2.7 for:**
- Direct robot communication (NAOqi proxies)
- Motion control
- Sensor reading
- Any NAOqi-dependent code

**Use Python 3.x for:**
- AI backend (separate from robot communication)
- Web dashboard
- Machine learning components
- Future-looking code

**Hybrid Approach (BEST):**
```
Test Scripts (Python 2.7) ←→ Robot via NAOqi
                    ↓
REST API Bridge (Python 3.x) ←→ AI Backend (Python 3.x)
```

---

## If My Test Scripts Don't Work

**They might fail because:**
1. Python 3.x incompatibility with NAOqi
2. Wrong Python version used
3. NAOqi SDK not installed for that Python version

**To fix:**
1. Check NAOqi version (see above)
2. Check Python version
3. I'll update scripts if needed

---

## What You Should Do NOW

1. **Check robot NAOqi version:**
   ```bash
   ssh nao@169.254.80.144 "naoqi --version"
   ```

2. **Check available Python:**
   ```bash
   python --version
   python2.7 --version
   python3 --version
   ```

3. **Install correct NAOqi version:**
   ```bash
   # For Python 2.7
   pip2 install naoqi
   
   # For Python 3.x (if NAOqi supports it)
   pip3 install naoqi
   ```

4. **Run appropriate test:**
   ```bash
   # If Python 2.7
   python2.7 run_all_tests.py
   
   # If Python 3.x
   python3 run_all_tests.py
   ```

5. **Report results** to confirm everything works

---

## Quick Checklist

Before running tests:

- [ ] Know your NAOqi version
- [ ] Know available Python versions on development machine
- [ ] NAOqi SDK installed for correct Python version
- [ ] Python version matches NAOqi compatibility
- [ ] Can import NAOqi successfully:
  ```bash
  python -c "from naoqi import ALProxy; print('✅ NAOqi imported successfully')"
  ```
- [ ] Robot ping still working: `ping 169.254.80.144`

---

## Need Help?

If you encounter Python compatibility issues:

1. **Share your NAOqi version and Python versions**
2. **I'll update scripts to be compatible**
3. **We can create version-specific test scripts**

---

**Status:** Awaiting your NAOqi version and Python version info  
**Action Required:** Check versions as outlined above

Please reply with:
- Your NAOqi version (from robot)
- Your Python 2.7 version (if available)
- Your Python 3.x version (if available)

Then I'll ensure all scripts are compatible! ✅
