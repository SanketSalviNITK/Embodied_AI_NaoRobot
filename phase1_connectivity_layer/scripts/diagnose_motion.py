#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Motion Bridge Diagnostic Script
Debug movement issues
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def main():
    """Run diagnostics"""
    print("\n" + "=" * 70)
    print("MOTION BRIDGE DIAGNOSTIC SCRIPT")
    print("=" * 70)

    wifi_ip = '192.168.137.87'

    # Step 1: Import check
    print("\n[STEP 1] Checking NAOqi import...")
    try:
        from naoqi import ALProxy
        print("OK  NAOqi SDK available")
    except ImportError as e:
        print("ERROR: NAOqi not found: {}".format(str(e)))
        return False

    # Step 2: Connection check
    print("\n[STEP 2] Checking WiFi connection to {}...".format(wifi_ip))
    try:
        motion = ALProxy('ALMotion', wifi_ip, 9559)
        print("OK  ALMotion connected")
    except Exception as e:
        print("ERROR: ALMotion failed: {}".format(str(e)))
        return False

    try:
        posture = ALProxy('ALRobotPosture', wifi_ip, 9559)
        print("OK  ALRobotPosture connected")
    except Exception as e:
        print("ERROR: ALRobotPosture failed: {}".format(str(e)))
        return False

    # Step 3: Robot config
    print("\n[STEP 3] Getting robot config...")
    try:
        config = motion.getRobotConfig()
        print("OK  Robot config retrieved")
        print("    Model: {}".format(config[0]))
    except Exception as e:
        print("ERROR: Config failed: {}".format(str(e)))

    # Step 4: Check if robot is moving
    print("\n[STEP 4] Checking if robot is moving...")
    try:
        is_moving = motion.isMoving()
        print("OK  Is moving: {}".format(is_moving))
    except Exception as e:
        print("ERROR: isMoving check failed: {}".format(str(e)))

    # Step 5: Check stiffness
    print("\n[STEP 5] Checking joint stiffness...")
    try:
        joint_names = ['HeadYaw', 'RShoulderPitch', 'RHipPitch']
        stiffness = motion.getStiffnesses(joint_names)
        for name, stiff in zip(joint_names, stiffness):
            print("    {}: {}".format(name, stiff))
    except Exception as e:
        print("ERROR: Stiffness check failed: {}".format(str(e)))

    # Step 6: Try to set stiffness
    print("\n[STEP 6] Attempting to set stiffness...")
    try:
        motion.setStiffnessesAbsolute(['HeadYaw'], [1.0])
        print("OK  Stiffness set successfully")
    except Exception as e:
        print("ERROR: Stiffness set failed: {}".format(str(e)))
        print("This might prevent movement")

    # Step 7: Try simple posture
    print("\n[STEP 7] Attempting to set posture (Stand)...")
    try:
        result = posture.goToPosture('Stand', 0.5)
        print("OK  Posture command sent: {}".format(result))
        print("    Note: Robot may take 5-10 seconds to reach posture")
        time.sleep(3)
    except Exception as e:
        print("ERROR: Posture failed: {}".format(str(e)))
        import traceback
        traceback.print_exc()

    # Step 8: Final status
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print("\n✓ If all steps passed, robot should be working")
    print("✗ If any step failed, that's the issue")
    print("\nCommon issues:")
    print("  - Robot stiffness can't be set → Motor problem")
    print("  - Posture fails → Joint control issue")
    print("  - Movement slow → WiFi latency")

    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\n\nFATAL ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
