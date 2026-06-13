# Update Robot IP Address Across All Test Scripts
# OLD IP: 169.254.80.144 (or other previous IPs)
# NEW IP: 169.254.175.171

$oldIPs = @("169.254.80.144", "192.168.")  # Old IPs to replace
$newIP = "169.254.175.171"

Write-Host "======================================================================" -ForegroundColor Green
Write-Host "Robot IP Update Script" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Old IP(s): $oldIPs" -ForegroundColor Yellow
Write-Host "New IP: $newIP" -ForegroundColor Yellow
Write-Host ""

# Files to update
$filesToUpdate = @(
    "test_phase0_joint_control.py",
    "test_phase0_motion.py",
    "test_phase0_sensors_detailed.py",
    "test_phase0_audio.py",
    "test_phase0_leds.py",
    "test_1_naoqi_basic_py27.py",
    "test_2_network_stability_py27.py",
    "test_3_robot_sensors_py27.py",
    "run_all_tests_py27.py",
    "WIFI_CONNECTION_GUIDE.md",
    "PHASE0_ASSESSMENT_GUIDE.md"
)

$filesUpdated = 0

foreach ($file in $filesToUpdate) {
    $filePath = Join-Path (Get-Location) $file

    if (Test-Path $filePath) {
        Write-Host "Updating: $file" -ForegroundColor Cyan

        $content = Get-Content $filePath -Raw
        $originalContent = $content

        # Replace old IPs with new IP
        foreach ($oldIP in $oldIPs) {
            if ($oldIP -ne "192.168.") {
                $content = $content -replace [regex]::Escape($oldIP), $newIP
            }
        }

        # Check if changes were made
        if ($content -ne $originalContent) {
            Set-Content $filePath $content -NoNewline
            Write-Host "  ✓ Updated" -ForegroundColor Green
            $filesUpdated++
        } else {
            Write-Host "  - No changes needed" -ForegroundColor Gray
        }
    } else {
        Write-Host "  ✗ File not found: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "Update Complete!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Files updated: $filesUpdated" -ForegroundColor Yellow
Write-Host "New Robot IP: $newIP" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify connection: ping $newIP" -ForegroundColor Gray
Write-Host "  2. Test NAOqi: python -c `"from naoqi import ALProxy; ALProxy('ALMotion', '$newIP', 9559)`"" -ForegroundColor Gray
Write-Host "  3. Run Phase 0 tests: run_phase0_tests.bat" -ForegroundColor Gray
Write-Host ""
