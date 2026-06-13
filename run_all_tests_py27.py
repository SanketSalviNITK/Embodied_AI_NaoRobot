#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Master Test Runner for Pre-Phase 0 Robot Validation (Python 2.7)
Executes all tests in sequence and generates a report
Compatible with NAOqi 2.8.6.23
"""

import sys
import subprocess
import time
from datetime import datetime

def run_test(test_number, test_name, test_file):
    """Run a single test and return result"""

    print("\n" + "=" * 70)
    print("RUNNING TEST {0}: {1}".format(test_number, test_name))
    print("=" * 70)
    print("File: {0}".format(test_file))
    print("Time: {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("=" * 70 + "\n")

    try:
        # Run test and capture output
        process = subprocess.Popen(
            [sys.executable, test_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        output, _ = process.communicate()
        result = process.returncode

        # Print the output
        print(output)

        success = result == 0

        if success:
            print("\nOK  Test {0} PASSED".format(test_number))
        else:
            print("\nERROR: Test {0} FAILED".format(test_number))

        return success, test_name, output

    except Exception as e:
        error_msg = "ERROR: Test {0} failed with error: {1}".format(test_number, str(e))
        print("\n" + error_msg)
        return False, test_name, error_msg

def main():
    """Run all tests"""

    print("\n" + "=" * 70)
    print("PRE-PHASE 0 COMPREHENSIVE ROBOT VALIDATION TEST SUITE (Python 2.7)")
    print("=" * 70 + "\n")

    print("Start time: {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("Robot IP: 169.254.80.144")
    print("System IP: 169.254.80.100")
    print("\nThis test suite will validate:")
    print("  OK  NAOqi connectivity and proxies")
    print("  OK  Network latency and stability")
    print("  OK  Robot sensors (IMU, battery, FSR, etc.)")
    print("  OK  Joint encoders and motion control")
    print("  OK  Audio system (speaker and microphone)")

    # Define tests
    tests = [
        (1, "NAOqi Basic Connection", "test_1_naoqi_basic_py27.py"),
        (2, "Network Stability", "test_2_network_stability_py27.py"),
        (3, "Robot Sensors", "test_3_robot_sensors_py27.py"),
    ]

    results = []
    test_outputs = []
    start_time = time.time()

    # Run all tests
    for test_number, test_name, test_file in tests:
        success, name, output = run_test(test_number, test_name, test_file)
        results.append((test_number, name, success))
        test_outputs.append((test_number, name, output))

        # Add delay between tests
        if test_number < len(tests):
            print("\nWaiting 2 seconds before next test...")
            time.sleep(2)

    end_time = time.time()
    duration = end_time - start_time

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70 + "\n")

    passed = sum(1 for _, _, success in results if success)
    failed = sum(1 for _, _, success in results if not success)
    total = len(results)

    print("Total tests: {0}".format(total))
    print("Passed: {0}".format(passed))
    print("Failed: {0}".format(failed))
    print("Duration: {0:.1f} seconds\n".format(duration))

    print("Detailed Results:")
    print("-" * 70)
    for test_num, test_name, success in results:
        status = "OK  PASSED" if success else "ERROR FAILED"
        print("  Test {0}: {1:<40} {2}".format(test_num, test_name, status))
    print("-" * 70)

    # Overall result
    print("\n" + "=" * 70)
    if failed == 0:
        print("OK  ALL TESTS PASSED!")
        print("\nYour robot is ready for Phase 0!")
        print("\nNext steps:")
        print("  1. Review the test results above")
        print("  2. Document any warnings or issues")
        print("  3. Create PRE_PHASE0_TESTS_REPORT.md with results")
        print("  4. Proceed to Phase 0: Robot Assessment")
        overall_success = True
    else:
        print("WARNING {0} test(s) failed!".format(failed))
        print("\nBefore proceeding to Phase 0:")
        print("  1. Review the failed test output above")
        print("  2. Check troubleshooting section in each test")
        print("  3. Fix identified issues")
        print("  4. Re-run the failed test(s)")
        overall_success = False

    print("=" * 70)
    print("End time: {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("=" * 70 + "\n")

    # Create summary file
    try:
        summary_file = "TEST_RESULTS_SUMMARY.txt"
        with open(summary_file, "w") as f:
            f.write("PRE-PHASE 0 TEST RESULTS (Python 2.7)\n")
            f.write("=" * 70 + "\n\n")
            f.write("Date: {0}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            f.write("Robot IP: 169.254.80.144\n")
            f.write("System IP: 169.254.80.100\n")
            f.write("NAOqi: 2.8.6.23 (Python 2.7)\n\n")
            f.write("Total Tests: {0}\n".format(total))
            f.write("Passed: {0}\n".format(passed))
            f.write("Failed: {0}\n".format(failed))
            f.write("Duration: {0:.1f} seconds\n\n".format(duration))
            f.write("Results:\n")
            f.write("-" * 70 + "\n")
            for test_num, test_name, success in results:
                status = "PASSED" if success else "FAILED"
                f.write("  Test {0}: {1:<40} {2}\n".format(test_num, test_name, status))
            f.write("-" * 70 + "\n\n")
            if overall_success:
                f.write("OK  ALL TESTS PASSED - Ready for Phase 0\n")
            else:
                f.write("WARNING {0} test(s) failed - See details below\n\n".format(failed))
                f.write("FAILED TEST DETAILS:\n")
                f.write("=" * 70 + "\n\n")
                for test_num, test_name, output in test_outputs:
                    test_result = next((r for r in results if r[0] == test_num), None)
                    if test_result and not test_result[2]:
                        f.write("TEST {0}: {1}\n".format(test_num, test_name))
                        f.write("-" * 70 + "\n")
                        f.write(output)
                        f.write("\n\n")

        print("OK  Results saved to: {0}\n".format(summary_file))
    except Exception as e:
        print("WARNING Could not save results file: {0}\n".format(e))

    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nWARNING: Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Fatal error: {0}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)
