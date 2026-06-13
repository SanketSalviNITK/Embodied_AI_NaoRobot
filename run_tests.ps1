# NAOqi Python 2.7 Test Runner for PowerShell (Using Virtual Environment)
# This script activates venv_py27 and runs the tests

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "NAOqi Python 2.7 Test Suite (Using Virtual Environment)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""

# Get current directory
$ProjectDir = Get-Location
$Py27VenvPath = Join-Path $ProjectDir "venv_py27"

# Check if venv_py27 exists
if (-not (Test-Path $Py27VenvPath)) {
    Write-Host "ERROR: Python 2.7 virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Virtual environment not found at: $Py27VenvPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run setup_python_environments.ps1 first to create the environment:" -ForegroundColor Yellow
    Write-Host "  $ProjectDir\setup_python_environments.ps1" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Activating Python 2.7 virtual environment..." -ForegroundColor Cyan
& "$Py27VenvPath\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment!" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Verifying NAOqi SDK availability..." -ForegroundColor Cyan
try {
    $naoqi_check = python -c "from naoqi import ALProxy; print('NAOqi SDK: OK')" 2>&1
    Write-Host "  $naoqi_check" -ForegroundColor Green
} catch {
    Write-Host "ERROR: NAOqi SDK not properly installed in virtual environment!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run setup_python_environments.ps1 to reinstall dependencies:" -ForegroundColor Yellow
    Write-Host "  $ProjectDir\setup_python_environments.ps1" -ForegroundColor Gray
    Write-Host ""
    deactivate
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check robot connectivity
Write-Host "Checking robot connectivity..." -ForegroundColor Cyan
$ping_result = Test-Connection -ComputerName "169.254.80.144" -Count 1 -Quiet
if (-not $ping_result) {
    Write-Host "WARNING: Cannot ping robot at 169.254.80.144" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. Robot is powered on"
    Write-Host "  2. Robot is connected via LAN"
    Write-Host "  3. Your system IP is 169.254.80.100"
    Write-Host ""
    Write-Host "Tests may fail if robot is not accessible." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "OK  Robot is reachable" -ForegroundColor Green
    Write-Host ""
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Running All Tests" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Run the master test script
python run_all_tests_py27.py
$test_result = $LASTEXITCODE

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
if ($test_result -eq 0) {
    Write-Host "SUCCESS: All tests passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your robot is ready for Phase 0!"
    Write-Host "Review TEST_RESULTS_SUMMARY.txt for details."
} else {
    Write-Host "FAILURE: Some tests failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the output above for details."
    Write-Host "See PYTHON27_TEST_GUIDE.md for troubleshooting."
}
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Deactivate virtual environment
Write-Host "Deactivating Python 2.7 virtual environment..." -ForegroundColor Cyan
deactivate

Write-Host ""
Read-Host "Press Enter to exit"
exit $test_result
