@echo off
REM NAOqi Python 2.7 Test Runner for Windows
REM This script sets PYTHONPATH and runs the tests

echo.
echo ======================================================================
echo NAOqi Python 2.7 Test Suite
echo ======================================================================
echo.

REM Set PYTHONPATH to include NAOqi SDK
set PYTHONPATH=%CD%\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\lib;%PYTHONPATH%

echo Python Path: %PYTHONPATH%
echo.

REM Check if python2.7 is available
python2.7 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: python2.7 not found!
    echo.
    echo Please ensure Python 2.7 is installed and available in PATH
    echo You can download Python 2.7 from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Checking NAOqi SDK availability...
python2.7 -c "from naoqi import ALProxy; print('NAOqi SDK: OK')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: NAOqi SDK not properly installed!
    echo.
    echo PYTHONPATH is set to:
    echo %PYTHONPATH%
    echo.
    echo If NAOqi is in a different location, edit this script.
    echo.
    pause
    exit /b 1
)

echo NAOqi SDK verified successfully!
echo.
echo ======================================================================
echo Running All Tests
echo ======================================================================
echo.

REM Run the master test script
python2.7 run_all_tests_py27.py

REM Capture the exit code
set TEST_RESULT=%ERRORLEVEL%

echo.
echo ======================================================================
if %TEST_RESULT% equ 0 (
    echo SUCCESS: All tests passed!
    echo.
    echo Your robot is ready for Phase 0!
    echo Review TEST_RESULTS_SUMMARY.txt for details.
) else (
    echo FAILURE: Some tests failed!
    echo.
    echo Check the output above for details.
    echo See PYTHON27_TEST_GUIDE.md for troubleshooting.
)
echo ======================================================================
echo.

pause
exit /b %TEST_RESULT%
