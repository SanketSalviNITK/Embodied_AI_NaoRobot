#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnostic Motion Logger for NAO Robot
Captures complete sensor data during movement for analysis
"""

from __future__ import print_function

import sys
import os
import time
import csv
import msvcrt
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class DiagnosticLogger(object):
    """Log comprehensive motion data for diagnostics"""

    def __init__(self, ip='192.168.137.87'):
        """Initialize logger"""
        from robot_bridge import MotionBridge
        from naoqi import ALProxy

        self.ip = ip
        self.bridge = MotionBridge(ip=ip)
        self.motion = self.bridge.motion
        self.memory = ALProxy('ALMemory', ip, 9559)
        self.tts = ALProxy('ALTextToSpeech', ip, 9559)

        # All joint names
        self.all_joints = [
            'HeadYaw', 'HeadPitch',
            'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw',
            'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw',
            'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
            'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'
        ]

        # FSR sensor keys (foot pressure sensors)
        self.fsr_keys = [
            'Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value',
            'Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value',
            'Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value',
            'Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value',
            'Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value',
            'Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value',
            'Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value',
            'Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value',
        ]

        # IMU sensor keys
        self.imu_keys = {
            'accel_x': 'Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value',
            'accel_y': 'Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value',
            'accel_z': 'Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value',
            'gyro_x': 'Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value',
            'gyro_y': 'Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value',
            'gyro_z': 'Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value',
        }

        # Log file setup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.log_file = os.path.join(self.log_dir, 'diagnostic_log_{}.csv'.format(timestamp))
        self.command_log_file = os.path.join(self.log_dir, 'command_log_{}.txt'.format(timestamp))

        # CSV headers
        self.csv_headers = ['timestamp', 'time_sec', 'command'] + \
                          self.all_joints + \
                          ['FSR_LFL', 'FSR_LFR', 'FSR_LRL', 'FSR_LRR', 'FSR_RFL', 'FSR_RFR', 'FSR_RRL', 'FSR_RRR'] + \
                          ['IMU_AccelX', 'IMU_AccelY', 'IMU_AccelZ', 'IMU_GyroX', 'IMU_GyroY', 'IMU_GyroZ']

        # Initialize CSV file
        with open(self.log_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.csv_headers)

        self.start_time = time.time()
        self.is_logging = False
        self.current_command = ""

        print("OK  Diagnostic logger initialized")
        print("Log file: {}".format(self.log_file))
        print("Command log: {}".format(self.command_log_file))

    def get_all_sensor_data(self):
        """Get all sensor data"""
        data = {}

        # Joint angles
        try:
            angles = self.motion.getAngles(self.all_joints, False)
            for joint, angle in zip(self.all_joints, angles):
                data[joint] = angle
        except Exception:
            for joint in self.all_joints:
                data[joint] = 0.0

        # FSR sensors
        try:
            fsr_values = []
            for key in self.fsr_keys:
                val = self.memory.getData(key)
                fsr_values.append(val if val else 0.0)
            for i, val in enumerate(fsr_values):
                data['FSR_{}'.format(i)] = val
        except Exception:
            for i in range(8):
                data['FSR_{}'.format(i)] = 0.0

        # IMU sensors
        try:
            for name, key in self.imu_keys.items():
                val = self.memory.getData(key)
                data['IMU_{}'.format(name)] = val if val else 0.0
        except Exception:
            for name in self.imu_keys.keys():
                data['IMU_{}'.format(name)] = 0.0

        return data

    def log_sample(self):
        """Log one sample of sensor data"""
        if not self.is_logging:
            return

        try:
            elapsed = time.time() - self.start_time
            data = self.get_all_sensor_data()

            # Prepare row
            row = [datetime.now().isoformat(), elapsed, self.current_command]
            for header in self.all_joints:
                row.append(data.get(header, 0.0))
            for i in range(8):
                row.append(data.get('FSR_{}'.format(i), 0.0))
            for name in ['AccelX', 'AccelY', 'AccelZ', 'GyroX', 'GyroY', 'GyroZ']:
                row.append(data.get('IMU_{}'.format(name), 0.0))

            # Write to CSV
            with open(self.log_file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row)

        except Exception as e:
            print("Log error: {}".format(str(e)))

    def execute_command(self, cmd, duration=2.0):
        """Execute command and log"""
        self.current_command = cmd
        self.is_logging = True

        print("\n>> {} (logging...)".format(cmd))

        # Log command
        with open(self.command_log_file, 'a') as f:
            f.write("[{:.2f}] COMMAND: {}\n".format(time.time() - self.start_time, cmd))

        start = time.time()

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

            # Log samples during movement
            while time.time() - start < duration:
                self.log_sample()
                time.sleep(0.05)  # 20 Hz sampling

            # Stop movement
            self.motion.stopWalk()
            self.motion.stopMove()

            # Log stop
            with open(self.command_log_file, 'a') as f:
                f.write("[{:.2f}] STOPPED\n".format(time.time() - self.start_time))

        except Exception as e:
            print("Error: {}".format(str(e)))
            self.motion.stopWalk()
            self.motion.stopMove()

        finally:
            self.is_logging = False
            self.current_command = ""
            time.sleep(0.5)

    def run(self):
        """Main control loop"""
        print("\n" + "=" * 70)
        print("DIAGNOSTIC MOTION LOGGER")
        print("=" * 70)
        print("\nKEYBOARD CONTROLS:")
        print("  W - FORWARD (log)")
        print("  S - BACKWARD (log)")
        print("  A - LEFT (log)")
        print("  D - RIGHT (log)")
        print("  SPACE - STOP (log)")
        print("  ESC or Ctrl+C - EXIT")
        print("\nDATA LOGGED:")
        print("  ✓ All 22 joint angles")
        print("  ✓ 8 foot pressure sensors (FSR)")
        print("  ✓ 6-axis IMU (accel + gyro)")
        print("  ✓ Timestamps")
        print("  ✓ Commands")
        print("\nOUTPUT FILES:")
        print("  1. {}".format(self.log_file))
        print("  2. {}".format(self.command_log_file))
        print("\n" + "=" * 70 + "\n")

        time.sleep(1)

        try:
            print("Standing robot...")
            self.bridge.stand()
            time.sleep(1)
            print("Ready! Start issuing commands...\n")

            self.tts.say("Diagnostic logging ready")

            while True:
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

                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\n\nEXIT (Ctrl+C pressed)")

        finally:
            print("\nCleaning up...")
            try:
                self.motion.stopWalk()
                self.motion.stopMove()
                self.bridge.stand()
                self.tts.say("Logging complete")
                print("OK  Logging complete")
                print("\nFiles saved:")
                print("  Data: {}".format(self.log_file))
                print("  Commands: {}".format(self.command_log_file))
                print("\nAnalyze with: pandas, matplotlib, or Excel\n")
            except Exception:
                pass


def main():
    """Main entry point"""
    try:
        logger = DiagnosticLogger(ip='192.168.137.87')
        logger.run()
        return True
    except Exception as e:
        print("\nFATAL ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
