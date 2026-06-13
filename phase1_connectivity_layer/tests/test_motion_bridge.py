#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Motion Bridge Unit Tests
Tests all motion control functionality
"""

import sys
import time


def test_connection():
    """Test: Connect to robot"""
    print("\n[TEST 1] Connection Test")
    print("-" * 70)

    try:
        from robot_bridge import MotionBridge

        # Try WiFi first, fall back to LAN
        ips = ['192.168.137.87', '169.254.175.171']

        bridge = None
        for ip in ips:
            try:
                print("Attempting connection to {}...".format(ip))
                bridge = MotionBridge(ip=ip)
                print("OK  Connected to robot at {}".format(ip))
                break
            except Exception:
                continue

        if bridge is None:
            print("ERROR: Could not connect to robot")
            return False

        return True

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def test_postures():
    """Test: Posture control"""
    print("\n[TEST 2] Posture Control Test")
    print("-" * 70)

    try:
        from robot_bridge import MotionBridge

        bridge = MotionBridge()

        postures = [
            ('stand', 'Standing'),
            ('sit', 'Sitting'),
            ('crouch', 'Crouching'),
            ('stand', 'Return to standing')
        ]

        for posture_name, description in postures:
            print("Testing {}: {}...".format(posture_name, description))
            method = getattr(bridge, posture_name)
            method()
            print("  OK  {}".format(description))
            time.sleep(1)

        return True

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def test_walking():
    """Test: Walking"""
    print("\n[TEST 3] Walking Test")
    print("-" * 70)

    try:
        from robot_bridge import MotionBridge

        bridge = MotionBridge()

        # Ensure standing
        print("Preparing: Standing...")
        bridge.stand()
        time.sleep(1)

        tests = [
            (lambda: bridge.walk_forward(0.3, 0.3), "Walk forward 30cm"),
            (lambda: bridge.stop(), "Stop"),
            (lambda: bridge.turn_left(0.3, 0.3), "Turn left"),
            (lambda: bridge.stop(), "Stop"),
            (lambda: bridge.turn_right(0.3, 0.3), "Turn right"),
            (lambda: bridge.stop(), "Stop"),
        ]

        for test_func, description in tests:
            print("Testing: {}...".format(description))
            test_func()
            print("  OK  {}".format(description))
            time.sleep(0.5)

        return True

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def test_joint_control():
    """Test: Joint control"""
    print("\n[TEST 4] Joint Control Test")
    print("-" * 70)

    try:
        from robot_bridge import MotionBridge
        import math

        bridge = MotionBridge()

        print("Testing: Head movement...")

        # Turn head left
        print("  Turning head left...")
        bridge.set_joint_angle('HeadYaw', math.radians(30), speed=0.5)
        time.sleep(0.5)

        # Turn head right
        print("  Turning head right...")
        bridge.set_joint_angle('HeadYaw', math.radians(-30), speed=0.5)
        time.sleep(0.5)

        # Return to center
        print("  Return to center...")
        bridge.set_joint_angle('HeadYaw', 0, speed=0.5)
        time.sleep(0.5)

        print("OK  Joint control working")

        # Get current angles
        print("\nTesting: Get joint angles...")
        angles = bridge.get_joint_angles()
        print("OK  Retrieved {} joint angles".format(len(angles)))

        return True

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def test_stiffness():
    """Test: Stiffness control"""
    print("\n[TEST 5] Stiffness Control Test")
    print("-" * 70)

    try:
        from robot_bridge import MotionBridge

        bridge = MotionBridge()

        print("Testing: Set stiffness to 1.0 (stiff)...")
        bridge.stiffen()
        print("OK  Robot stiffened")
        time.sleep(1)

        print("Testing: Get stiffness values...")
        stiffness = bridge.get_stiffness()
        print("OK  Retrieved {} stiffness values".format(len(stiffness)))

        print("Testing: Relax robot...")
        bridge.relax()
        print("OK  Robot relaxed")

        return True

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def test_status():
    """Test: Robot status"""
    print("\n[TEST 6] Robot Status Test")
    print("-" * 70)

    try:
        from robot_bridge import MotionBridge

        bridge = MotionBridge()

        print("Testing: Get robot status...")
        status = bridge.get_robot_status()

        print("OK  Robot Status:")
        print("  IP: {}".format(status['ip']))
        print("  Moving: {}".format(status['moving']))
        print("  Joints: {} degrees of freedom".format(len(status['joints'])))

        return True

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("MOTION BRIDGE TEST SUITE")
    print("=" * 70)

    tests = [
        ('Connection', test_connection),
        ('Postures', test_postures),
        ('Walking', test_walking),
        ('Joint Control', test_joint_control),
        ('Stiffness', test_stiffness),
        ('Status', test_status),
    ]

    results = {}
    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print("FATAL ERROR in {}: {}".format(test_name, str(e)))
            results[test_name] = False
            failed += 1

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print("{}: {}".format(test_name, status))

    print("\nTotal: {}/{} tests passed".format(passed, passed + failed))

    if failed == 0:
        print("\nOK  All motion bridge tests passed!")
        return 0
    else:
        print("\nERROR: {} test(s) failed".format(failed))
        return 1


if __name__ == "__main__":
    sys.exit(main())
