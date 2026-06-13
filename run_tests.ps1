# NAOqi Python 2.7 Test Runner for PowerShell
# This script sets PYTHONPATH and runs the tests

Write-Host ""
Write-Host "======================================================================"
Write-Host "NAOqi Python 2.7 Test Suite (PowerShell)" -ForegroundColor Green
Write-Host "======================================================================"
Write-Host ""

# Set PYTHONPATH to include NAOqi SDK
$naoqi_path = Join-Path $PSScriptRoot "pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\lib"
$env:PYTHONPATH = "$naoqi_path;$env:PYTHONPATH"

Write-Host "PYTHONPATH set to:" -ForegroundColor Cyan
Write-Host "  $env:PYTHONPATH" -ForegroundColor Gray
Write-Host ""

# Check if python2.7 is available
try {
    $python_version = python2.7 --version 2>&1
    Write-Host "Python version: $python_version" -ForegroundColor Green
} catch {
    Write-Host "ERROR: python2.7 not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure Python 2.7 is installed and available in PATH"
    Write-Host "Download Python 2.7 from: https://www.python.org/downloads/"
    Write-Host ""
    exit 1
}

# Check NAOqi SDK
Write-Host "Checking NAOqi SDK availability..." -ForegroundColor Cyan
try {
    $naoqi_check = python2.7 -c "from naoqi import ALProxy; print('NAOqi SDK: OK')" 2>&1
    Write-Host "  $naoqi_check" -ForegroundColor Green
} catch {
    Write-Host "ERROR: NAOqi SDK not properly installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "PYTHONPATH is set to: $env:PYTHONPATH"
    Write-Host ""
    Write-Host "If NAOqi is in a different location, edit this script."
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "======================================================================"
Write-Host "Running All Tests" -ForegroundColor Cyan
Write-Host "======================================================================"
Write-Host ""

# Run the master test script
python2.7 run_all_tests_py27.py
$test_result = $LASTEXITCODE

Write-Host ""
Write-Host "======================================================================"
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
Write-Host "======================================================================"
Write-Host ""

exit $test_result
