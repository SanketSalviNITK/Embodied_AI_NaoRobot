#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Keyboard Control for NAO Robot
Real-time movement control using WASD keys
Press ESC or Ctrl+C to exit
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Platform-specific keyboard input
import msvcrt


def get_key():
    """Get keyboard input without blocking"""
    if msvcrt.kbhit():
        return msvcrt.getch().lower()
    return None


def main():
    """Main keyboard control loop"""
    from robot_bridge import MotionBridge
    from naoqi import ALProxy

    wifi_ip = '192.168.137.87'

    print("\n" + "=" * 70)
    print("NAO ROBOT - KEYBOARD CONTROL")
    print("=" * 70)
    print("\nConnecting to robot...")

    try:
        # Connect to robot
        bridge = MotionBridge(ip=wifi_ip)
        tts = ALProxy('ALTextToSpeech', wifi_ip, 9559)
        print("OK  Connected to robot at {}".format(wifi_ip))
        tts.say("Robot ready for control")
    except Exception as e:
        print("ERROR: Failed to connect - {}".format(str(e)))
        return False

    # Stand robot
    print("\nPreparing robot (standing)...")
    try:
        bridge.stand()
        time.sleep(1)
    except Exception as e:
        print("WARNING: Could not stand - {}".format(str(e)))

    print("\n" + "=" * 70)
    print("KEYBOARD CONTROLS:")
    print("=" * 70)
    print("  W - Walk FORWARD")
    print("  S - Walk BACKWARD")
    print("  A - Turn LEFT")
    print("  D - Turn RIGHT")
    print("  SPACE - Stop movement")
    print("  ESC or Ctrl+C - Exit program")
    print("=" * 70)
    print("\nStarting control loop (press a key)...\n")

    time.sleep(1)

    # Control loop
    try:
        while True:
            key = get_key()

            if key == 'w':  # Walk forward
                print(">> FORWARD")
                try:
                    bridge.walk_forward(distance=0.3, speed=0.3)
                except Exception as e:
                    print("   Error: {}".format(str(e)))

            elif key == 's':  # Walk backward
                print(">> BACKWARD")
                try:
                    bridge.walk_backward(distance=0.3, speed=0.3)
                except Exception as e:
                    print("   Error: {}".format(str(e)))

            elif key == 'a':  # Turn left
                print(">> TURN LEFT")
                try:
                    bridge.turn_left(angle=0.3, speed=0.3)
                except Exception as e:
                    print("   Error: {}".format(str(e)))

            elif key == 'd':  # Turn right
                print(">> TURN RIGHT")
                try:
                    bridge.turn_right(angle=0.3, speed=0.3)
                except Exception as e:
                    print("   Error: {}".format(str(e)))

            elif key == ' ':  # Stop
                print(">> STOP")
                try:
                    bridge.stop()
                except Exception as e:
                    print("   Error: {}".format(str(e)))

            elif key == '\x1b':  # ESC key
                print("\n>> EXIT (ESC pressed)")
                break

            # Small delay to prevent CPU spinning
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n\n>> EXIT (Ctrl+C pressed)")

    finally:
        # Cleanup
        print("\nCleaning up...")
        try:
            bridge.stop()
            bridge.stand()
            tts.say("Control ended")
            print("OK  Robot stopped and standing")
        except Exception:
            pass

    print("\nGoodbye!\n")
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print("\nFATAL ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
