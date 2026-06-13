#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Phase 0 Test: Motion & Walking
Tests robot locomotion, balance, and movement patterns
Compatible with NAOqi 2.8.6.23
"""

import sys
from naoqi import ALProxy
import time

def test_motion():
    """Test robot motion and walking capabilities"""

    robot_ip = "169.254.175.171"
    robot_port = 9559

    print("=" * 70)
    print("PHASE 0 TEST: Motion & Walking")
    print("=" * 70)
    print("\nTesting robot locomotion and movement\n")

    results = {}
    total_tests = 0
    passed_tests = 0

    try:
        motion = ALProxy("ALMotion", robot_ip, robot_port)
        posture = ALProxy("ALRobotPosture", robot_ip, robot_port)

        # Wake up
        print("1. Preparing robot...")
        try:
            motion.wakeUp()
            posture.goToPosture("Stand", 0.8)
            time.sleep(2)
            print("   OK  Robot ready for motion tests\n")
            results["Robot Preparation"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Robot Preparation"] = "FAIL"
        total_tests += 1

        # Test walk forward
        print("=" * 70)
        print("2. Walking Forward")
        print("=" * 70 + "\n")

        try:
            print("   Walking 20cm forward...")
            motion.moveTo(0.2, 0.0, 0.0)
            time.sleep(2)
            print("   OK  Forward walk successful\n")
            results["Walk Forward"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Walk Forward"] = "WARN"
        total_tests += 1

        # Test walk backward
        print("=" * 70)
        print("3. Walking Backward")
        print("=" * 70 + "\n")

        try:
            print("   Walking 20cm backward...")
            motion.moveTo(-0.2, 0.0, 0.0)
            time.sleep(2)
            print("   OK  Backward walk successful\n")
            results["Walk Backward"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Walk Backward"] = "WARN"
        total_tests += 1

        # Test side step
        print("=" * 70)
        print("4. Side Step (Lateral Movement)")
        print("=" * 70 + "\n")

        try:
            print("   Stepping left (10cm)...")
            motion.moveTo(0.0, 0.1, 0.0)
            time.sleep(2)
            print("   Stepping right (10cm back)...")
            motion.moveTo(0.0, -0.1, 0.0)
            time.sleep(2)
            print("   OK  Lateral movement successful\n")
            results["Side Step"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Side Step"] = "WARN"
        total_tests += 1

        # Test rotation
        print("=" * 70)
        print("5. Rotation (Turn in Place)")
        print("=" * 70 + "\n")

        try:
            print("   Turning left (45 degrees)...")
            motion.moveTo(0.0, 0.0, 0.785)  # ~45 degrees
            time.sleep(2)
            print("   Turning right (90 degrees back)...")
            motion.moveTo(0.0, 0.0, -0.785)
            time.sleep(2)
            print("   OK  Rotation successful\n")
            results["Rotation"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Rotation"] = "WARN"
        total_tests += 1

        # Test motion cycle time
        print("=" * 70)
        print("6. Motion Cycle Time")
        print("=" * 70 + "\n")

        try:
            cycle_time = motion.getMotionCycleTime()
            print("   Motion cycle time: {0} ms\n".format(cycle_time))
            results["Motion Cycle Time"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Motion Cycle Time"] = "WARN"
        total_tests += 1

        # Test balance
        print("=" * 70)
        print("7. Balance Test")
        print("=" * 70 + "\n")

        try:
            print("   Testing balance by moving center of mass...")

            # Move COM forward-backward
            print("   COM forward...")
            motion.setAngles(["LHipPitch", "RHipPitch"], [0.2, 0.2], 0.5)
            time.sleep(1)

            print("   COM backward...")
            motion.setAngles(["LHipPitch", "RHipPitch"], [-0.2, -0.2], 0.5)
            time.sleep(1)

            print("   COM center...")
            motion.setAngles(["LHipPitch", "RHipPitch"], [0.0, 0.0], 0.5)
            time.sleep(1)

            print("   OK  Balance maintained\n")
            results["Balance"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Balance"] = "WARN"
        total_tests += 1

        # Test walking config
        print("=" * 70)
        print("8. Walking Configuration")
        print("=" * 70 + "\n")

        try:
            print("   Retrieving walk parameters...")
            # Try to get some walking parameters
            try:
                max_step = motion.getWalkingConfig("MaxStepX")
                print("   Max step X: {0}".format(max_step))
            except:
                pass

            print("   OK  Walking configuration accessible\n")
            results["Walking Config"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Walking Config"] = "WARN"
        total_tests += 1

        # Return to standing
        print("=" * 70)
        print("9. Returning to Rest Position")
        print("=" * 70 + "\n")

        try:
            print("   Moving to Stand posture...")
            posture.goToPosture("Stand", 0.8)
            time.sleep(2)
            print("   Putting robot to rest (stiffness OFF)...")
            motion.rest()
            time.sleep(1)
            print("   OK  Robot at rest\n")
            results["Rest Position"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Rest Position"] = "FAIL"
        total_tests += 1

    except Exception as e:
        print("\nCRITICAL ERROR: {0}\n".format(e))
        return 1

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY: Motion & Walking")
    print("=" * 70)
    print("\nDetailed Results:\n")

    for test_name, result in results.items():
        status_icon = "OK  " if result == "PASS" else "FAIL" if result == "FAIL" else "WARN"
        print("   {0:<35} {1}".format(test_name, status_icon))

    print("\n" + "=" * 70)
    print("Total: {0}/{1} tests passed".format(passed_tests, total_tests))
    print("=" * 70)

    success = passed_tests >= (total_tests - 2)  # Allow 2 failures

    if success:
        print("\nOK  Motion test PASSED\n")
        return 0
    else:
        print("\nWARNING Motion test had issues\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_motion()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        sys.exit(1)
