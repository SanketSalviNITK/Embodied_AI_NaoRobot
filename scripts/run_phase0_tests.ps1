# Phase 0: Robot Assessment - Comprehensive Test Suite
# Tests all robot systems: motion, sensors, audio, LEDs

Write-Host ""
Write-Host "======================================================================"
Write-Host "Phase 0: Robot Assessment - Comprehensive Test Suite"
Write-Host "======================================================================"
Write-Host ""

# Get project directory
$ProjectDir = Split-Path -Parent -Path $PSScriptRoot
$venvPath = Join-Path $ProjectDir "venv_py27\Scripts\Activate.ps1"

# Activate Python 2.7 virtual environment
Write-Host "Activating Python 2.7 virtual environment..."
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "OK  Virtual environment activated"
} else {
    Write-Host "ERROR: Could not find virtual environment at $venvPath"
    Write-Host "Please run: scripts\setup_python_environments.bat"
    exit 1
}

Write-Host ""

# Check robot connectivity
Write-Host "Checking robot connectivity..."
try {
    python -c "from naoqi import ALProxy; ALProxy('ALMotion', '169.254.175.171', 9559); print('OK  Robot is reachable')" 2>$null
} catch {
    Write-Host "WARNING: Robot might not be reachable"
    Write-Host "Make sure robot is powered on and connected"
}

Write-Host ""

# Create results directory
$resultsDir = Join-Path $ProjectDir "results\phase0_results"
if (!(Test-Path $resultsDir)) {
    New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null
}

# Run all Phase 0 tests
$totalTests = 5
$passedTests = 0

Write-Host ""
Write-Host "======================================================================"
Write-Host "Running Phase 0 Tests"
Write-Host "======================================================================"
Write-Host ""

# Test 1: Joint Control
Write-Host "[1/5] Running Joint Control Test..."
$testPath = Join-Path $ProjectDir "tests\phase0\test_phase0_joint_control.py"
$logPath = Join-Path $resultsDir "test_1_joint_control.log"
python $testPath > $logPath 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "       PASSED"
    $passedTests++
} else {
    Write-Host "       FAILED"
}
Write-Host ""

# Test 2: Motion & Walking
Write-Host "[2/5] Running Motion Test..."
$testPath = Join-Path $ProjectDir "tests\phase0\test_phase0_motion.py"
$logPath = Join-Path $resultsDir "test_2_motion.log"
python $testPath > $logPath 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "       PASSED"
    $passedTests++
} else {
    Write-Host "       FAILED"
}
Write-Host ""

# Test 3: Detailed Sensors
Write-Host "[3/5] Running Sensor Analysis Test..."
$testPath = Join-Path $ProjectDir "tests\phase0\test_phase0_sensors_detailed.py"
$logPath = Join-Path $resultsDir "test_3_sensors.log"
python $testPath > $logPath 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "       PASSED"
    $passedTests++
} else {
    Write-Host "       FAILED"
}
Write-Host ""

# Test 4: Audio & Speech
Write-Host "[4/5] Running Audio Test..."
$testPath = Join-Path $ProjectDir "tests\phase0\test_phase0_audio.py"
$logPath = Join-Path $resultsDir "test_4_audio.log"
python $testPath > $logPath 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "       PASSED"
    $passedTests++
} else {
    Write-Host "       FAILED"
}
Write-Host ""

# Test 5: LED Control
Write-Host "[5/5] Running LED Test..."
$testPath = Join-Path $ProjectDir "tests\phase0\test_phase0_leds.py"
$logPath = Join-Path $resultsDir "test_5_leds.log"
python $testPath > $logPath 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "       PASSED"
    $passedTests++
} else {
    Write-Host "       FAILED"
}
Write-Host ""

# Print summary
Write-Host "======================================================================"
Write-Host "Phase 0 Test Results Summary"
Write-Host "======================================================================"
Write-Host ""
Write-Host "Total Tests: $totalTests"
Write-Host "Passed: $passedTests"
Write-Host "Failed: $($totalTests - $passedTests)"
Write-Host ""

if ($passedTests -eq $totalTests) {
    Write-Host "Status: ALL TESTS PASSED ✓"
} elseif ($passedTests -gt 0) {
    Write-Host "Status: Some tests passed"
} else {
    Write-Host "Status: ALL TESTS FAILED"
}

Write-Host ""
Write-Host "Detailed logs saved in: $resultsDir"
Write-Host ""
Write-Host "Test Results:"
Write-Host "   - test_1_joint_control.log"
Write-Host "   - test_2_motion.log"
Write-Host "   - test_3_sensors.log"
Write-Host "   - test_4_audio.log"
Write-Host "   - test_5_leds.log"
Write-Host ""
Write-Host "======================================================================"
Write-Host ""

Write-Host "Press Enter to continue..."
Read-Host
