#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Walking Directions - Diagnose movement mapping
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def main():
    """Test each direction"""
    from robot_bridge import MotionBridge
    from naoqi import ALProxy

    wifi_ip = '192.168.137.87'

    print("\n" + "=" * 70)
    print("WALKING DIRECTION TEST")
    print("=" * 70)
    print("\nThis will test each direction separately")
    print("Watch the robot and note which direction it moves\n")

    # Initialize
    print("Connecting to robot...")
    bridge = MotionBridge(ip=wifi_ip)
    tts = ALProxy('ALTextToSpeech', wifi_ip, 9559)

    print("OK  Connected\n")

    # Stand first
    print("1. Standing robot...")
    tts.say("Standing up")
    bridge.stand()
    time.sleep(2)

    # Test 1: moveToward(0.1, 0, 0) - expect forward
    print("\n2. Testing moveToward(0.1, 0, 0)")
    print("   Expected: Move FORWARD")
    print("   Watch robot...")
    tts.say("Moving with parameters one zero zero")
    bridge.motion.moveToward(0.1, 0, 0)
    time.sleep(2)
    bridge.stop()
    time.sleep(1)

    # Back to stand
    print("   Back to standing")
    bridge.stand()
    time.sleep(2)

    # Test 2: moveToward(0, 0.1, 0) - expect sideways
    print("\n3. Testing moveToward(0, 0.1, 0)")
    print("   Expected: Move SIDEWAYS RIGHT")
    print("   Watch robot...")
    tts.say("Moving with parameters zero one zero")
    bridge.motion.moveToward(0, 0.1, 0)
    time.sleep(2)
    bridge.stop()
    time.sleep(1)

    # Back to stand
    print("   Back to standing")
    bridge.stand()
    time.sleep(2)

    # Test 3: moveToward(-0.1, 0, 0) - expect opposite of test 1
    print("\n4. Testing moveToward(-0.1, 0, 0)")
    print("   Expected: Move BACKWARD (opposite of test 1)")
    print("   Watch robot...")
    tts.say("Moving with parameters minus one zero zero")
    bridge.motion.moveToward(-0.1, 0, 0)
    time.sleep(2)
    bridge.stop()
    time.sleep(1)

    # Back to stand
    print("   Back to standing")
    bridge.stand()
    time.sleep(2)

    # Test 4: moveToward(0, -0.1, 0) - expect opposite of test 2
    print("\n5. Testing moveToward(0, -0.1, 0)")
    print("   Expected: Move SIDEWAYS LEFT (opposite of test 2)")
    print("   Watch robot...")
    tts.say("Moving with parameters zero minus one zero")
    bridge.motion.moveToward(0, -0.1, 0)
    time.sleep(2)
    bridge.stop()
    time.sleep(1)

    # Final stand
    print("\n6. Final stand")
    bridge.stand()
    time.sleep(1)

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print("\nTell me what each test did:")
    print("  Test 2 (0.1, 0, 0) moved: FORWARD / BACKWARD / LEFT / RIGHT")
    print("  Test 3 (0, 0.1, 0) moved: FORWARD / BACKWARD / LEFT / RIGHT")
    print("  Test 4 (-0.1, 0, 0) moved: FORWARD / BACKWARD / LEFT / RIGHT")
    print("  Test 5 (0, -0.1, 0) moved: FORWARD / BACKWARD / LEFT / RIGHT")
    print("\nBased on this, we can map the correct directions!")

    tts.say("Test complete")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
