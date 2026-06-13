@echo off
REM Update Robot IP Address Script
REM NEW IP: 169.254.175.171

echo.
echo ======================================================================
echo Robot IP Update Script
echo ======================================================================
echo.
echo Old IP: 169.254.80.144 (or similar)
echo New IP: 169.254.175.171
echo.

setlocal enabledelayedexpansion

set oldIP=169.254.80.144
set newIP=169.254.175.171
set filesUpdated=0

REM Files to update
set files=^
  test_phase0_joint_control.py ^
  test_phase0_motion.py ^
  test_phase0_sensors_detailed.py ^
  test_phase0_audio.py ^
  test_phase0_leds.py ^
  test_1_naoqi_basic_py27.py ^
  test_2_network_stability_py27.py ^
  test_3_robot_sensors_py27.py ^
  run_all_tests_py27.py ^
  WIFI_CONNECTION_GUIDE.md ^
  PHASE0_ASSESSMENT_GUIDE.md

echo Updating files...
echo.

for %%F in (%files%) do (
    if exist "%%F" (
        echo Updating: %%F
        powershell -Command "(Get-Content '%%F') -replace '%oldIP%', '%newIP%' | Set-Content '%%F'"
        echo   ^OK
        set /a filesUpdated+=1
    ) else (
        echo Skipping: %%F (not found)
    )
)

echo.
echo ======================================================================
echo Update Complete!
echo ======================================================================
echo.
echo Files updated: !filesUpdated!
echo New Robot IP: %newIP%
echo.
echo Next steps:
echo   1. Verify connection: ping %newIP%
echo   2. Test NAOqi: python -c "from naoqi import ALProxy; ALProxy('ALMotion', '%newIP%', 9559)"
echo   3. Run Phase 0 tests: run_phase0_tests.bat
echo.

pause
