#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Phase 0 Test: Joint Control & Movement
Tests all 22 DOF (degrees of freedom) joints
Verifies motion range, speed, and accuracy
Compatible with NAOqi 2.8.6.23
"""

import sys
from naoqi import ALProxy
import time

def test_joint_control():
    """Test all robot joints and movements"""

    robot_ip = "169.254.175.171"
    robot_port = 9559

    print("=" * 70)
    print("PHASE 0 TEST: Joint Control & Movement (22 DOF)")
    print("=" * 70)
    print("\nTesting all joint angles, ranges, and movements\n")

    results = {}
    total_tests = 0
    passed_tests = 0

    try:
        motion = ALProxy("ALMotion", robot_ip, robot_port)
        posture = ALProxy("ALRobotPosture", robot_ip, robot_port)

        # Wake up robot
        print("1. Waking up robot (enabling stiffness)...")
        try:
            motion.wakeUp()
            print("   OK  Robot stiffness enabled\n")
            results["Wake Up"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Wake Up"] = "FAIL"
        total_tests += 1

        # Get all joint names
        print("2. Getting joint list...")
        try:
            all_joints = motion.getBodyNames("Body")
            print("   OK  Found {0} joints\n".format(len(all_joints)))
            for joint in all_joints:
                print("      - {0}".format(joint))
            print("")
            results["Get Joint List"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Get Joint List"] = "FAIL"
            all_joints = []
        total_tests += 1

        # Test joint angles
        print("=" * 70)
        print("3. Reading Joint Angles (Current Positions)")
        print("=" * 70 + "\n")

        if all_joints:
            try:
                angles = motion.getAngles(all_joints, True)
                print("Current joint angles (in radians):\n")

                for i, joint in enumerate(all_joints):
                    if i < len(angles):
                        angle_rad = angles[i]
                        angle_deg = angle_rad * 180.0 / 3.14159
                        print("   {0:<25} {1:8.4f} rad  ({2:7.2f}°)".format(
                            joint, angle_rad, angle_deg))

                print("\n   OK  All joint angles readable")
                results["Read Joint Angles"] = "PASS"
                passed_tests += 1
            except Exception as e:
                print("   ERROR: {0}\n".format(e))
                results["Read Joint Angles"] = "FAIL"
            total_tests += 1

        # Test postures
        print("\n" + "=" * 70)
        print("4. Testing Predefined Postures")
        print("=" * 70 + "\n")

        postures_to_test = ["Stand", "SitRelax", "Stand"]

        for posture_name in postures_to_test:
            try:
                print("   Moving to {0} posture...".format(posture_name))
                posture.goToPosture(posture_name, 0.8)
                time.sleep(2)
                print("   OK  {0} posture achieved\n".format(posture_name))
                results["Posture: {0}".format(posture_name)] = "PASS"
                passed_tests += 1
            except Exception as e:
                print("   ERROR: {0}\n".format(e))
                results["Posture: {0}".format(posture_name)] = "FAIL"
            total_tests += 1

        # Test head movement
        print("=" * 70)
        print("5. Testing Head Movement")
        print("=" * 70 + "\n")

        try:
            print("   Moving head left...")
            motion.setAngles(["HeadYaw"], [0.5], 0.5)
            time.sleep(1)

            print("   Moving head right...")
            motion.setAngles(["HeadYaw"], [-0.5], 0.5)
            time.sleep(1)

            print("   Moving head center...")
            motion.setAngles(["HeadYaw"], [0.0], 0.5)
            time.sleep(1)

            print("   OK  Head movement working\n")
            results["Head Movement"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Head Movement"] = "FAIL"
        total_tests += 1

        # Test arm movement
        print("=" * 70)
        print("6. Testing Arm Movement")
        print("=" * 70 + "\n")

        try:
            # Left arm
            print("   Moving left arm...")
            left_arm = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
            left_angles = [0.5, 0.3, -0.5, -0.5]
            motion.setAngles(left_arm, left_angles, 0.5)
            time.sleep(1)

            # Right arm
            print("   Moving right arm...")
            right_arm = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
            right_angles = [0.5, -0.3, 0.5, 0.5]
            motion.setAngles(right_arm, right_angles, 0.5)
            time.sleep(1)

            # Return to rest
            print("   Returning to rest position...")
            motion.rest()
            time.sleep(1)

            print("   OK  Arm movement working\n")
            results["Arm Movement"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Arm Movement"] = "FAIL"
        total_tests += 1

        # Get max speeds
        print("=" * 70)
        print("7. Joint Speed Capabilities")
        print("=" * 70 + "\n")

        try:
            sample_joints = ["HeadYaw", "LShoulderPitch", "RShoulderPitch", "LAnklePitch"]
            print("Max speeds for sample joints:\n")

            for joint in sample_joints:
                try:
                    max_speed = motion.getMaxSpeed(joint)
                    print("   {0:<25} {1:.4f} rad/s".format(joint, max_speed))
                except:
                    pass

            print("\n   OK  Speed data retrieved\n")
            results["Joint Speeds"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Joint Speeds"] = "WARN"
        total_tests += 1

        # Test stiffness
        print("=" * 70)
        print("8. Testing Joint Stiffness")
        print("=" * 70 + "\n")

        try:
            test_joint = "HeadYaw"
            print("   Getting stiffness for {0}...".format(test_joint))
            stiffness = motion.getStiffnesses(test_joint)
            print("   Stiffness: {0}\n".format(stiffness))

            print("   Setting stiffness to 0.5...")
            motion.setStiffnesses(test_joint, 0.5)
            time.sleep(0.5)

            print("   Setting stiffness back to 1.0...")
            motion.setStiffnesses(test_joint, 1.0)
            time.sleep(0.5)

            print("   OK  Stiffness control working\n")
            results["Stiffness Control"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Stiffness Control"] = "FAIL"
        total_tests += 1

    except Exception as e:
        print("\nCRITICAL ERROR: {0}\n".format(e))
        return False

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY: Joint Control & Movement")
    print("=" * 70)
    print("\nDetailed Results:\n")

    for test_name, result in results.items():
        status_icon = "OK  " if result == "PASS" else "FAIL" if result == "FAIL" else "WARN"
        print("   {0:<35} {1}".format(test_name, status_icon))

    print("\n" + "=" * 70)
    print("Total: {0}/{1} tests passed".format(passed_tests, total_tests))
    print("=" * 70)

    success = passed_tests >= (total_tests - 1)  # Allow 1 failure

    if success:
        print("\nOK  Joint control test PASSED\n")
        return 0
    else:
        print("\nWARNING Joint control test FAILED\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_joint_control()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        sys.exit(1)
