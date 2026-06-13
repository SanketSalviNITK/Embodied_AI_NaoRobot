#!/usr/bin/env python3
"""
Master Test Runner for Pre-Phase 0 Robot Validation
Executes all tests in sequence and generates a report
"""

import sys
import subprocess
import time
from datetime import datetime

def run_test(test_number, test_name, test_file):
    """Run a single test and return result"""

    print("\n" + "=" * 70)
    print(f"RUNNING TEST {test_number}: {test_name}")
    print("=" * 70)
    print(f"File: {test_file}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=False,
            timeout=120
        )

        success = result.returncode == 0

        if success:
            print(f"\n✅ Test {test_number} PASSED")
        else:
            print(f"\n❌ Test {test_number} FAILED")

        return success, test_name

    except subprocess.TimeoutExpired:
        print(f"\n⏱️  Test {test_number} TIMEOUT (exceeded 2 minutes)")
        return False, test_name
    except FileNotFoundError:
        print(f"\n❌ Test file not found: {test_file}")
        return False, test_name
    except Exception as e:
        print(f"\n❌ Test {test_number} ERROR: {e}")
        return False, test_name

def main():
    """Run all tests"""

    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  PRE-PHASE 0 COMPREHENSIVE ROBOT VALIDATION TEST SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝\n")

    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Robot IP: 169.254.80.144")
    print("System IP: 169.254.80.100")
    print("\nThis test suite will validate:")
    print("  ✓ NAOqi connectivity and proxies")
    print("  ✓ Network latency and stability")
    print("  ✓ Robot sensors (IMU, battery, FSR, etc.)")
    print("  ✓ Joint encoders and motion control")
    print("  ✓ Audio system (speaker and microphone)")

    # Define tests
    tests = [
        (1, "NAOqi Basic Connection", "test_1_naoqi_basic.py"),
        (2, "Network Stability", "test_2_network_stability.py"),
        (3, "Robot Sensors", "test_3_robot_sensors.py"),
    ]

    results = []
    start_time = time.time()

    # Run all tests
    for test_number, test_name, test_file in tests:
        success, name = run_test(test_number, test_name, test_file)
        results.append((test_number, name, success))

        # Add delay between tests
        if test_number < len(tests):
            print(f"\n⏳ Waiting 2 seconds before next test...")
            time.sleep(2)

    end_time = time.time()
    duration = end_time - start_time

    # Print summary
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  TEST SUMMARY".ljust(70).center(70) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝\n")

    passed = sum(1 for _, _, success in results if success)
    failed = sum(1 for _, _, success in results if not success)
    total = len(results)

    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration:.1f} seconds\n")

    print("Detailed Results:")
    print("-" * 70)
    for test_num, test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  Test {test_num}: {test_name:<40} {status}")
    print("-" * 70)

    # Overall result
    print("\n" + "=" * 70)
    if failed == 0:
        print("✅ ALL TESTS PASSED!")
        print("\nYour robot is ready for Phase 0!")
        print("\nNext steps:")
        print("  1. Review the test results above")
        print("  2. Document any warnings or issues")
        print("  3. Create PRE_PHASE0_TESTS_REPORT.md with results")
        print("  4. Proceed to Phase 0: Robot Assessment")
        overall_success = True
    else:
        print(f"⚠️  {failed} test(s) failed!")
        print("\nBefore proceeding to Phase 0:")
        print("  1. Review the failed test output above")
        print("  2. Check troubleshooting section in each test")
        print("  3. Fix identified issues")
        print("  4. Re-run the failed test(s)")
        overall_success = False

    print("=" * 70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    # Create summary file
    try:
        summary_file = "TEST_RESULTS_SUMMARY.txt"
        with open(summary_file, "w") as f:
            f.write("PRE-PHASE 0 TEST RESULTS\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Robot IP: 169.254.80.144\n")
            f.write(f"System IP: 169.254.80.100\n\n")
            f.write(f"Total Tests: {total}\n")
            f.write(f"Passed: {passed}\n")
            f.write(f"Failed: {failed}\n")
            f.write(f"Duration: {duration:.1f} seconds\n\n")
            f.write("Results:\n")
            f.write("-" * 70 + "\n")
            for test_num, test_name, success in results:
                status = "PASSED" if success else "FAILED"
                f.write(f"  Test {test_num}: {test_name:<40} {status}\n")
            f.write("-" * 70 + "\n\n")
            if overall_success:
                f.write("✅ ALL TESTS PASSED - Ready for Phase 0\n")
            else:
                f.write(f"⚠️  {failed} test(s) failed - See details above\n")

        print(f"✅ Results saved to: {summary_file}\n")
    except Exception as e:
        print(f"⚠️  Could not save results file: {e}\n")

    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
