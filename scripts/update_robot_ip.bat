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

REM Phase 0 test files
echo Updating Phase 0 tests...
echo.

for %%F in (test_phase0_joint_control.py test_phase0_motion.py test_phase0_sensors_detailed.py test_phase0_audio.py test_phase0_leds.py) do (
    if exist "..\tests\phase0\%%F" (
        echo Updating: ..\tests\phase0\%%F
        powershell -Command "(Get-Content '..\tests\phase0\%%F') -replace '%oldIP%', '%newIP%' | Set-Content '..\tests\phase0\%%F'"
        echo   OK
        set /a filesUpdated+=1
    )
)

REM Legacy test files
echo.
echo Updating legacy tests...
echo.

for %%F in (test_1_naoqi_basic_py27.py test_2_network_stability_py27.py test_3_robot_sensors_py27.py) do (
    if exist "..\tests\legacy\%%F" (
        echo Updating: ..\tests\legacy\%%F
        powershell -Command "(Get-Content '..\tests\legacy\%%F') -replace '%oldIP%', '%newIP%' | Set-Content '..\tests\legacy\%%F'"
        echo   OK
        set /a filesUpdated+=1
    )
)

REM Documentation files
echo.
echo Updating documentation...
echo.

for %%F in (WIFI_CONNECTION_GUIDE.md PHASE0_ASSESSMENT_GUIDE.md) do (
    if exist "..\docs\guides\%%F" (
        echo Updating: ..\docs\guides\%%F
        powershell -Command "(Get-Content '..\docs\guides\%%F') -replace '%oldIP%', '%newIP%' | Set-Content '..\docs\guides\%%F'"
        echo   OK
        set /a filesUpdated+=1
    ) else if exist "..\docs\phases\%%F" (
        echo Updating: ..\docs\phases\%%F
        powershell -Command "(Get-Content '..\docs\phases\%%F') -replace '%oldIP%', '%newIP%' | Set-Content '..\docs\phases\%%F'"
        echo   OK
        set /a filesUpdated+=1
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
