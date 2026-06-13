@echo off
REM Phase 0: Robot Assessment - Comprehensive Test Suite
REM Tests all robot systems: motion, sensors, audio, LEDs

echo.
echo ======================================================================
echo Phase 0: Robot Assessment - Comprehensive Test Suite
echo ======================================================================
echo.

REM Activate Python 2.7 virtual environment
call "%CD%\venv_py27\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo OK  Virtual environment activated
echo.

REM Check robot connectivity
echo Checking robot connectivity...
python -c "from naoqi import ALProxy; ALProxy('ALMotion', '169.254.80.144', 9559); print('OK  Robot is reachable')" 2>nul

if errorlevel 1 (
    echo WARNING: Robot might not be reachable
    echo Make sure robot is powered on and connected
    echo.
)

REM Create results directory
if not exist "phase0_results" mkdir phase0_results

REM Run all Phase 0 tests
set TOTAL_TESTS=5
set PASSED_TESTS=0

echo.
echo ======================================================================
echo Running Phase 0 Tests
echo ======================================================================
echo.

REM Test 1: Joint Control
echo [1/5] Running Joint Control Test...
python test_phase0_joint_control.py > phase0_results\test_1_joint_control.log 2>&1
if errorlevel 1 (
    echo       FAILED
) else (
    echo       PASSED
    set /a PASSED_TESTS+=1
)
echo.

REM Test 2: Motion & Walking
echo [2/5] Running Motion Test...
python test_phase0_motion.py > phase0_results\test_2_motion.log 2>&1
if errorlevel 1 (
    echo       FAILED
) else (
    echo       PASSED
    set /a PASSED_TESTS+=1
)
echo.

REM Test 3: Detailed Sensors
echo [3/5] Running Sensor Analysis Test...
python test_phase0_sensors_detailed.py > phase0_results\test_3_sensors.log 2>&1
if errorlevel 1 (
    echo       FAILED
) else (
    echo       PASSED
    set /a PASSED_TESTS+=1
)
echo.

REM Test 4: Audio & Speech
echo [4/5] Running Audio Test...
python test_phase0_audio.py > phase0_results\test_4_audio.log 2>&1
if errorlevel 1 (
    echo       FAILED
) else (
    echo       PASSED
    set /a PASSED_TESTS+=1
)
echo.

REM Test 5: LED Control
echo [5/5] Running LED Test...
python test_phase0_leds.py > phase0_results\test_5_leds.log 2>&1
if errorlevel 1 (
    echo       FAILED
) else (
    echo       PASSED
    set /a PASSED_TESTS+=1
)
echo.

REM Print summary
echo ======================================================================
echo Phase 0 Test Results Summary
echo ======================================================================
echo.
echo Total Tests: %TOTAL_TESTS%
echo Passed: %PASSED_TESTS%
echo Failed: %TOTAL_TESTS - PASSED_TESTS%
echo.

if %PASSED_TESTS% equ %TOTAL_TESTS% (
    echo Status: ALL TESTS PASSED ✓
) else if %PASSED_TESTS% gtr 0 (
    echo Status: Some tests passed
) else (
    echo Status: ALL TESTS FAILED
)

echo.
echo Detailed logs saved in: phase0_results\
echo.
echo Test Results:
echo   - test_1_joint_control.log
echo   - test_2_motion.log
echo   - test_3_sensors.log
echo   - test_4_audio.log
echo   - test_5_leds.log
echo.
echo ======================================================================
echo.

REM Deactivate virtual environment
call "%CD%\venv_py27\Scripts\deactivate.bat"

pause
