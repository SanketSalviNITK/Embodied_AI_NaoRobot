# Test Runner Update - Now Using Virtual Environments

The test runners (`run_tests.bat` and `run_tests.ps1`) have been updated to work with the new virtual environments.

---

## What Changed

### Before (Old Method)
```
run_tests.bat
├── Manually set PYTHONPATH environment variable
├── Check for Python 2.7 in system PATH
├── Import NAOqi from system Python
└── Run tests
```

### After (New Method - Better!)
```
run_tests.bat
├── Activate venv_py27 virtual environment
├── Verify venv_py27 exists
├── Verify NAOqi SDK in virtual environment
├── Check robot connectivity
├── Run tests with isolated environment
└── Deactivate virtual environment
```

---

## Why This Is Better

✅ **Isolated Environment**
- All dependencies contained in venv_py27
- No conflicts with system Python

✅ **Cleaner Setup**
- No manual PYTHONPATH configuration
- Virtual environment handles all paths automatically

✅ **Better Error Detection**
- Checks for environment existence first
- Helpful error messages point to setup script
- Robot connectivity check included

✅ **Reproducible**
- Same environment everywhere
- Easy to recreate if needed
- Team members get identical setup

---

## How to Use

### Command Prompt (Batch)

```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
run_tests.bat
```

### PowerShell

```powershell
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
.\run_tests.ps1
```

---

## What the Script Does (Step by Step)

### Step 1: Check Virtual Environment
```
Checking: C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\venv_py27

❌ If missing:
   ERROR: Python 2.7 virtual environment not found!
   → Run: setup_python_environments.bat
   
✅ If found:
   Proceed to next step
```

### Step 2: Activate Environment
```
Activating Python 2.7 virtual environment...
(venv_py27) C:\...>  ← You'll see this in PowerShell
```

The prompt shows `(venv_py27)` to indicate active environment.

### Step 3: Verify NAOqi SDK
```
Verifying NAOqi SDK availability...

❌ If missing:
   ERROR: NAOqi SDK not properly installed!
   → Run: setup_python_environments.bat
   
✅ If found:
   NAOqi SDK: OK
```

### Step 4: Check Robot Connectivity
```
Checking robot connectivity...

✅ If reachable:
   OK  Robot is reachable
   
⚠️ If not reachable:
   WARNING: Cannot ping robot at 169.254.80.144
   → Power on robot, check LAN connection
   → Tests may still run but will fail at robot communication
```

### Step 5: Run Tests
```
======================================================================
Running All Tests
======================================================================

Test 1: NAOqi Basic Connection...
Test 2: Network Stability...
Test 3: Robot Sensors...

(Full output shown)
```

### Step 6: Display Results
```
======================================================================
SUCCESS: All tests passed!

Your robot is ready for Phase 0!
Review TEST_RESULTS_SUMMARY.txt for details.
======================================================================
```

### Step 7: Cleanup
```
Deactivating Python 2.7 virtual environment...
(back to normal prompt)
```

---

## Troubleshooting

### "Python 2.7 virtual environment not found!"

**Solution:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
setup_python_environments.bat
```

This creates the virtual environment.

---

### "NAOqi SDK not properly installed!"

**Solution:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
setup_python_environments.bat
```

This reinstalls NAOqi SDK in the virtual environment.

---

### "WARNING: Cannot ping robot"

**Robot not reachable - check:**
1. Robot is powered on
2. Robot is connected via LAN to your computer
3. Your system IP is 169.254.80.100
4. Robot IP is 169.254.80.144

**Test connectivity:**
```bash
ping 169.254.80.144
```

Should see responses like:
```
Pinging 169.254.80.144 with 32 bytes of data:
Reply from 169.254.80.144: bytes=32 time=5ms TTL=64
```

---

### Tests fail but robot is reachable

**Check:**
1. NAOqi service is running on robot
2. No firewall blocking port 9559
3. Review error output in console

**See:** `PYTHON27_TEST_GUIDE.md` for detailed troubleshooting

---

## File Structure

```
C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\
├── venv_py27/                    ← Virtual environment (created by setup script)
│   ├── Scripts/
│   │   ├── activate.bat          ← Used by run_tests.bat
│   │   ├── Activate.ps1          ← Used by run_tests.ps1
│   │   └── python.exe
│   └── Lib/
│       └── site-packages/
│           └── naoqi/            ← NAOqi SDK installed here
│
├── venv_py3/                     ← Python 3 environment (for future AI work)
│   └── (same structure)
│
├── setup_python_environments.bat  ← Creates both environments
├── setup_python_environments.ps1  ← PowerShell version
├── run_tests.bat                 ← Run Phase 0 tests
├── run_tests.ps1                 ← PowerShell version
└── (other project files)
```

---

## Comparison: Run Test Workflows

### Old Way (Manual PYTHONPATH)
```
1. Set PYTHONPATH in script
2. Hope system Python is available
3. Hope NAOqi path is correct
4. Run tests
5. Hope no conflicts with other packages
```

### New Way (Virtual Environment)
```
1. ✅ Activate venv_py27
2. ✅ Verify it exists
3. ✅ Verify NAOqi is there
4. ✅ Check robot is reachable
5. ✅ Run tests in isolated environment
6. ✅ Deactivate cleanly
```

---

## When to Regenerate Virtual Environment

**Regenerate if:**
- You broke package installations
- You want fresh install
- Setup script had errors previously

**How to regenerate:**
```bash
cd C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI
setup_python_environments.bat
# Answer 'y' when asked if you want to delete venv_py27
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Create environments | `setup_python_environments.bat` |
| Run tests | `run_tests.bat` |
| View test results | `TEST_RESULTS_SUMMARY.txt` |
| Troubleshoot Python 2.7 | `PYTHON27_TEST_GUIDE.md` |
| Understand environments | `PYTHON_ENVIRONMENT_GUIDE.md` |
| Check environment setup | `ENVIRONMENT_SETUP_README.md` |

---

## Summary

**Old:** Manual PYTHONPATH + system Python  
**New:** Virtual environment management

**Result:** Cleaner, safer, more reliable testing workflow

**Status:** ✅ Ready for Phase 0 testing

**Next:** Run `run_tests.bat` to begin Phase 0 assessment

---

**Updated:** 2026-06-13  
**Files:** `run_tests.bat`, `run_tests.ps1`
