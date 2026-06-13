#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Empirical Walking Test - Determine actual moveToward() behavior
Tests which parameter controls which direction
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_movement(motion, x, y, theta, description):
    """Test a single movement"""
    print("\n" + "-" * 70)
    print("TEST: moveToward({}, {}, {})".format(x, y, theta))
    print("Description: {}".format(description))
    print("-" * 70)
    print("Watch robot and note direction of movement...")
    time.sleep(1)

    try:
        motion.moveToward(float(x), float(y), float(theta))
        print("Command sent: moveToward({}, {}, {})".format(x, y, theta))
        time.sleep(3)
        motion.stopMove()
        print("Movement completed")
    except Exception as e:
        print("ERROR: {}".format(str(e)))

    time.sleep(1)


def main():
    """Run empirical tests"""
    from naoqi import ALProxy

    wifi_ip = '192.168.137.87'

    print("\n" + "=" * 70)
    print("EMPIRICAL WALKING DIRECTION TEST")
    print("=" * 70)
    print("\nThis test will determine actual moveToward() parameter mapping")
    print("by testing each parameter individually with small movements\n")

    # Connect
    print("Connecting...")
    motion = ALProxy('ALMotion', wifi_ip, 9559)
    tts = ALProxy('ALTextToSpeech', wifi_ip, 9559)
    print("OK  Connected\n")

    # Stand
    print("Standing robot...")
    posture = ALProxy('ALRobotPosture', wifi_ip, 9559)
    posture.goToPosture('Stand', 0.5)
    time.sleep(2)

    # Test series 1: X parameter only
    print("\n" + "=" * 70)
    print("SERIES 1: Testing X parameter (first value)")
    print("=" * 70)

    tts.say("Testing X parameter. Positive value first")
    test_movement(motion, 0.2, 0, 0, "X=0.2, Y=0, Theta=0 (what direction?)")

    posture.goToPosture('Stand', 0.5)
    time.sleep(1)

    tts.say("Testing X parameter. Negative value")
    test_movement(motion, -0.2, 0, 0, "X=-0.2, Y=0, Theta=0 (opposite direction?)")

    posture.goToPosture('Stand', 0.5)
    time.sleep(1)

    # Test series 2: Y parameter only
    print("\n" + "=" * 70)
    print("SERIES 2: Testing Y parameter (second value)")
    print("=" * 70)

    tts.say("Testing Y parameter. Positive value first")
    test_movement(motion, 0, 0.2, 0, "X=0, Y=0.2, Theta=0 (what direction?)")

    posture.goToPosture('Stand', 0.5)
    time.sleep(1)

    tts.say("Testing Y parameter. Negative value")
    test_movement(motion, 0, -0.2, 0, "X=0, Y=-0.2, Theta=0 (opposite direction?)")

    posture.goToPosture('Stand', 0.5)
    time.sleep(1)

    # Test series 3: Theta parameter only
    print("\n" + "=" * 70)
    print("SERIES 3: Testing Theta parameter (third value)")
    print("=" * 70)

    tts.say("Testing rotation. Positive value first")
    test_movement(motion, 0, 0, 0.2, "X=0, Y=0, Theta=0.2 (turn which way?)")

    posture.goToPosture('Stand', 0.5)
    time.sleep(1)

    tts.say("Testing rotation. Negative value")
    test_movement(motion, 0, 0, -0.2, "X=0, Y=0, Theta=-0.2 (opposite direction?)")

    # Return to stand
    print("\n" + "=" * 70)
    posture.goToPosture('Stand', 0.5)
    time.sleep(1)

    print("\n" + "=" * 70)
    print("RESULTS NEEDED")
    print("=" * 70)
    print("\nPlease report what direction the robot moved for each test:")
    print("\nSERIES 1 (X parameter):")
    print("  Test 1 (X=0.2):  Robot moved [FORWARD/BACKWARD/LEFT/RIGHT/NONE]")
    print("  Test 2 (X=-0.2): Robot moved [FORWARD/BACKWARD/LEFT/RIGHT/NONE]")
    print("\nSERIES 2 (Y parameter):")
    print("  Test 3 (Y=0.2):  Robot moved [FORWARD/BACKWARD/LEFT/RIGHT/NONE]")
    print("  Test 4 (Y=-0.2): Robot moved [FORWARD/BACKWARD/LEFT/RIGHT/NONE]")
    print("\nSERIES 3 (Theta parameter):")
    print("  Test 5 (T=0.2):  Robot rotated [LEFT/RIGHT/NONE]")
    print("  Test 6 (T=-0.2): Robot rotated [LEFT/RIGHT/NONE]")
    print("\nBased on your observations, we can determine the correct mapping!")

    tts.say("Test complete")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
