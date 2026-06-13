#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Safe Keyboard Control for NAO Robot
With motor encoder feedback and movement blocking
"""

import sys
import os
import time
import msvcrt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class SafeRobotController(object):
    """Robot controller with safety mechanisms"""

    def __init__(self, ip='192.168.137.87'):
        """Initialize robot controller"""
        from robot_bridge import MotionBridge
        from naoqi import ALProxy

        self.ip = ip
        self.bridge = MotionBridge(ip=ip)
        self.motion = self.bridge.motion
        self.tts = ALProxy('ALTextToSpeech', ip, 9559)

        # Safety state
        self.is_moving = False
        self.last_command_time = 0
        self.movement_timeout = 5.0  # Max 5 seconds per movement
        self.min_command_interval = 0.1  # Min 0.1s between commands

        # Joint names for encoder reading
        self.leg_joints = [
            'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
            'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'
        ]

        print("OK  Robot controller initialized")
        self.tts.say("Ready for control")

    def get_joint_angles(self):
        """Get current joint angles"""
        try:
            angles = self.motion.getAngles(self.leg_joints, False)
            return dict(zip(self.leg_joints, angles))
        except Exception:
            return {}

    def display_status(self, command=""):
        """Display robot status"""
        angles = self.get_joint_angles()

        if command:
            status = "Command: {} | ".format(command)
        else:
            status = ""

        if self.is_moving:
            status += "MOVING (blocking new input)"
        else:
            status += "Ready"

        print("\r[{}] Hip angles: L={:.2f}/{:.2f} R={:.2f}/{:.2f}".format(
            status,
            angles.get('LHipPitch', 0),
            angles.get('LHipRoll', 0),
            angles.get('RHipPitch', 0),
            angles.get('RHipRoll', 0)
        ), end='')
        sys.stdout.flush()

    def can_accept_command(self):
        """Check if robot can accept new command"""
        # Block if currently moving
        if self.is_moving:
            return False

        # Block if too soon after last command
        if time.time() - self.last_command_time < self.min_command_interval:
            return False

        return True

    def execute_command(self, cmd, duration=3.0):
        """Execute command with blocking"""
        if not self.can_accept_command():
            print("\r[BLOCKED] Previous movement still in progress...  ", end='')
            sys.stdout.flush()
            return False

        self.is_moving = True
        self.last_command_time = time.time()
        start_time = time.time()

        print("\r[EXECUTING] {}".format(cmd), end='')
        sys.stdout.flush()

        try:
            if cmd == "FORWARD":
                self.motion.setWalkTargetVelocity(0.5, 0.0, 0.0, 1.0)

            elif cmd == "BACKWARD":
                self.motion.setWalkTargetVelocity(-0.5, 0.0, 0.0, 1.0)

            elif cmd == "LEFT":
                self.motion.setWalkTargetVelocity(0.0, 0.0, 0.5, 1.0)

            elif cmd == "RIGHT":
                self.motion.setWalkTargetVelocity(0.0, 0.0, -0.5, 1.0)

            elif cmd == "STOP":
                self.motion.stopWalk()
                self.motion.stopMove()
                self.is_moving = False
                return True

            # Monitor movement with timeout
            while time.time() - start_time < duration:
                self.display_status(cmd)

                # Check for timeout
                if time.time() - start_time > self.movement_timeout:
                    print("\r[TIMEOUT] Movement timeout! Stopping...", end='')
                    self.motion.stopWalk()
                    self.motion.stopMove()
                    break

                time.sleep(0.1)

            # Always stop after command completes
            self.motion.stopWalk()
            self.motion.stopMove()

            return True

        except Exception as e:
            print("\r[ERROR] {}: {}".format(cmd, str(e)), end='')
            self.motion.stopWalk()
            self.motion.stopMove()
            return False

        finally:
            self.is_moving = False
            time.sleep(0.2)  # Small delay before accepting next command

    def run(self):
        """Main control loop"""
        print("\n" + "=" * 70)
        print("SAFE NAO ROBOT KEYBOARD CONTROL")
        print("=" * 70)
        print("\nKEYBOARD CONTROLS:")
        print("  W - Walk FORWARD")
        print("  S - Walk BACKWARD")
        print("  A - Turn LEFT")
        print("  D - Turn RIGHT")
        print("  SPACE - STOP")
        print("  ESC or Ctrl+C - EXIT")
        print("\nSAFETY FEATURES:")
        print("  ✓ Movement blocking (prevents concurrent commands)")
        print("  ✓ Motor encoder feedback (joint angle monitoring)")
        print("  ✓ Timeout protection (5 second auto-stop)")
        print("  ✓ Command interval protection (min 0.1s between commands)")
        print("\n" + "=" * 70)
        print("\nStarting control loop...\n")

        time.sleep(1)

        try:
            # Stand
            print("Standing robot...")
            self.bridge.stand()
            time.sleep(1)
            print("Ready!\n")

            # Control loop
            while True:
                # Non-blocking key input
                if msvcrt.kbhit():
                    key = msvcrt.getch().lower()

                    if key == 'w':
                        self.execute_command("FORWARD", duration=2.0)

                    elif key == 's':
                        self.execute_command("BACKWARD", duration=2.0)

                    elif key == 'a':
                        self.execute_command("LEFT", duration=2.0)

                    elif key == 'd':
                        self.execute_command("RIGHT", duration=2.0)

                    elif key == ' ':
                        self.execute_command("STOP")

                    elif key == '\x1b':  # ESC
                        print("\n\nEXIT requested")
                        break

                else:
                    # Show status even when no input
                    self.display_status()
                    time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\nEXIT (Ctrl+C pressed)")

        finally:
            print("\nCleaning up...")
            try:
                self.motion.stopWalk()
                self.motion.stopMove()
                self.bridge.stand()
                self.tts.say("Control ended")
                print("OK  Robot stopped and standing\n")
            except Exception:
                pass


def main():
    """Main entry point"""
    try:
        controller = SafeRobotController(ip='192.168.137.87')
        controller.run()
        return True
    except Exception as e:
        print("\nFATAL ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
