@echo off
REM NAOqi Python 2.7 Test Runner for Windows (Using Virtual Environment)
REM This script activates venv_py27 and runs the tests

echo.
echo ======================================================================
echo NAOqi Python 2.7 Test Suite (Using Virtual Environment)
echo ======================================================================
echo.

REM Check if venv_py27 exists
if not exist "%CD%\venv_py27" (
    echo ERROR: Python 2.7 virtual environment not found!
    echo.
    echo Virtual environment not found at: %CD%\venv_py27
    echo.
    echo Please run setup_python_environments.bat first to create the environment:
    echo   %CD%\setup_python_environments.bat
    echo.
    pause
    exit /b 1
)

echo Activating Python 2.7 virtual environment...
call "%CD%\venv_py27\Scripts\activate.bat"

REM Verify activation by checking if python exists in venv
if not exist "%CD%\venv_py27\Scripts\python.exe" (
    echo ERROR: Failed to activate virtual environment!
    echo.
    echo Python executable not found in venv_py27
    echo.
    pause
    exit /b 1
)

echo OK  Virtual environment activated successfully!
echo.
echo Verifying NAOqi SDK availability...
python -c "from naoqi import ALProxy; print('NAOqi SDK: OK')"
if errorlevel 1 (
    echo.
    echo ERROR: NAOqi SDK not properly installed in virtual environment!
    echo.
    echo Please run setup_python_environments.bat to reinstall dependencies:
    echo   %CD%\setup_python_environments.bat
    echo.
    call "%CD%\venv_py27\Scripts\deactivate.bat"
    pause
    exit /b 1
)

echo OK  NAOqi SDK verified successfully!
echo.

REM Check robot connectivity
echo Checking robot connectivity...
ping -n 1 169.254.80.144 >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot ping robot at 169.254.80.144
    echo.
    echo Make sure:
    echo   1. Robot is powered on
    echo   2. Robot is connected via LAN
    echo   3. Your system IP is 169.254.80.100
    echo.
    echo Tests may fail if robot is not accessible.
    echo.
) else (
    echo OK  Robot is reachable at 169.254.80.144
    echo.
)

echo ======================================================================
echo Running All Tests
echo ======================================================================
echo.

REM Run the master test script
python run_all_tests_py27.py

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

REM Deactivate virtual environment
echo Deactivating Python 2.7 virtual environment...
call "%CD%\venv_py27\Scripts\deactivate.bat"

echo.
pause
exit /b %TEST_RESULT%
