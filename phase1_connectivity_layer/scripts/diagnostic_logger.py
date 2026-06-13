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

        # Safety state
        self.is_executing = False
        self.last_command_time = 0
        self.min_command_interval = 0.2  # Prevent rapid commands

        # CSV headers
        self.csv_headers = ['timestamp', 'time_sec', 'command'] + \
                          self.all_joints + \
                          ['FSR_LFL', 'FSR_LFR', 'FSR_LRL', 'FSR_LRR', 'FSR_RFL', 'FSR_RFR', 'FSR_RRL', 'FSR_RRR'] + \
                          ['IMU_AccelX', 'IMU_AccelY', 'IMU_AccelZ', 'IMU_GyroX', 'IMU_GyroY', 'IMU_GyroZ'] + \
                          ['FSR_TotalLeft', 'FSR_TotalRight', 'FSR_BalancePoint', 'IsMoving', 'IsBalanced',
                           'LHipPitch_Vel', 'RHipPitch_Vel', 'LKneePitch_Vel', 'RKneePitch_Vel',
                           'LeftFootLift', 'RightFootLift', 'StepDetected', 'AccelMagnitude']

        # Previous joint angles for velocity calculation
        self.prev_angles = {joint: 0.0 for joint in self.all_joints}
        self.prev_timestamp = time.time()

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
        """Get all sensor data with derived metrics"""
        data = {}
        current_time = time.time()

        # Joint angles
        try:
            angles = self.motion.getAngles(self.all_joints, False)
            for joint, angle in zip(self.all_joints, angles):
                data[joint] = angle
        except Exception:
            for joint in self.all_joints:
                data[joint] = 0.0

        # FSR sensors
        fsr_values = []
        try:
            for key in self.fsr_keys:
                val = self.memory.getData(key)
                fsr_values.append(val if val else 0.0)
            for i, val in enumerate(fsr_values):
                data['FSR_{}'.format(i)] = val
        except Exception:
            for i in range(8):
                data['FSR_{}'.format(i)] = 0.0
                fsr_values.append(0.0)

        # IMU sensors
        imu_values = {}
        try:
            for name, key in self.imu_keys.items():
                val = self.memory.getData(key)
                imu_values[name] = val if val else 0.0
                data['IMU_{}'.format(name)] = imu_values[name]
        except Exception:
            for name in self.imu_keys.keys():
                imu_values[name] = 0.0
                data['IMU_{}'.format(name)] = 0.0

        # ===== DERIVED METRICS FOR DIAGNOSIS =====

        # FSR balance analysis
        left_total = sum(fsr_values[0:4])  # Left foot (4 sensors)
        right_total = sum(fsr_values[4:8])  # Right foot (4 sensors)
        data['FSR_TotalLeft'] = left_total
        data['FSR_TotalRight'] = right_total

        # Balance point (center of pressure)
        total_pressure = left_total + right_total
        if total_pressure > 0:
            balance_point = (left_total - right_total) / total_pressure  # -1 (left) to 1 (right)
        else:
            balance_point = 0.0
        data['FSR_BalancePoint'] = balance_point

        # Is robot moving (based on FSR change)?
        data['IsMoving'] = 1 if (left_total > 0.1 or right_total > 0.1) else 0

        # Is robot balanced (roughly equal pressure)?
        pressure_diff = abs(left_total - right_total)
        data['IsBalanced'] = 1 if pressure_diff < 1.0 else 0

        # Joint velocities (to detect if joints are actually moving)
        dt = current_time - self.prev_timestamp if self.prev_timestamp else 0.05
        if dt > 0:
            data['LHipPitch_Vel'] = (data.get('LHipPitch', 0) - self.prev_angles.get('LHipPitch', 0)) / dt
            data['RHipPitch_Vel'] = (data.get('RHipPitch', 0) - self.prev_angles.get('RHipPitch', 0)) / dt
            data['LKneePitch_Vel'] = (data.get('LKneePitch', 0) - self.prev_angles.get('LKneePitch', 0)) / dt
            data['RKneePitch_Vel'] = (data.get('RKneePitch', 0) - self.prev_angles.get('RKneePitch', 0)) / dt
        else:
            data['LHipPitch_Vel'] = 0.0
            data['RHipPitch_Vel'] = 0.0
            data['LKneePitch_Vel'] = 0.0
            data['RKneePitch_Vel'] = 0.0

        # Step detection (knee bend = leg lifting)
        data['LeftFootLift'] = 1 if data.get('LKneePitch', 0) > 0.1 else 0
        data['RightFootLift'] = 1 if data.get('RKneePitch', 0) > 0.1 else 0
        data['StepDetected'] = data['LeftFootLift'] or data['RightFootLift']

        # Acceleration magnitude (overall movement)
        accel_x = imu_values.get('accel_x', 0)
        accel_y = imu_values.get('accel_y', 0)
        accel_z = imu_values.get('accel_z', 0)
        data['AccelMagnitude'] = (accel_x**2 + accel_y**2 + accel_z**2) ** 0.5

        # Update for next iteration
        self.prev_angles = {joint: data.get(joint, 0) for joint in self.all_joints}
        self.prev_timestamp = current_time

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

            # Joint angles
            for header in self.all_joints:
                row.append(data.get(header, 0.0))

            # FSR values
            for i in range(8):
                row.append(data.get('FSR_{}'.format(i), 0.0))

            # IMU values
            for name in ['AccelX', 'AccelY', 'AccelZ', 'GyroX', 'GyroY', 'GyroZ']:
                row.append(data.get('IMU_{}'.format(name), 0.0))

            # Derived metrics (DIAGNOSTICS!)
            row.append(data.get('FSR_TotalLeft', 0.0))
            row.append(data.get('FSR_TotalRight', 0.0))
            row.append(data.get('FSR_BalancePoint', 0.0))
            row.append(data.get('IsMoving', 0))
            row.append(data.get('IsBalanced', 0))
            row.append(data.get('LHipPitch_Vel', 0.0))
            row.append(data.get('RHipPitch_Vel', 0.0))
            row.append(data.get('LKneePitch_Vel', 0.0))
            row.append(data.get('RKneePitch_Vel', 0.0))
            row.append(data.get('LeftFootLift', 0))
            row.append(data.get('RightFootLift', 0))
            row.append(data.get('StepDetected', 0))
            row.append(data.get('AccelMagnitude', 0.0))

            # Write to CSV
            with open(self.log_file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row)

        except Exception as e:
            print("Log error: {}".format(str(e)))

    def execute_command(self, cmd, duration=2.0):
        """Execute command and log with safety blocking"""
        # Prevent concurrent commands (safety)
        if self.is_executing:
            print("\r[BLOCKED] Previous command still executing...", end='')
            sys.stdout.flush()
            return False

        if time.time() - self.last_command_time < self.min_command_interval:
            return False

        self.is_executing = True
        self.current_command = cmd
        self.is_logging = True
        self.last_command_time = time.time()

        print("\n>> EXECUTING: {} (logging 20 samples/sec)".format(cmd))

        # Log command
        with open(self.command_log_file, 'a') as f:
            f.write("[{:.2f}] COMMAND: {}\n".format(time.time() - self.start_time, cmd))

        start = time.time()
        samples = 0
        max_values = {}

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

                # Track key metrics for summary
                data = self.get_all_sensor_data()
                if data.get('IsMoving', 0):
                    max_values['IsMoving'] = 1
                if data.get('StepDetected', 0):
                    max_values['StepDetected'] = 1
                if abs(data.get('FSR_BalancePoint', 0)) > max_values.get('MaxImbalance', 0):
                    max_values['MaxImbalance'] = abs(data.get('FSR_BalancePoint', 0))

                samples += 1
                time.sleep(0.05)  # 20 Hz sampling

            # Stop movement
            self.motion.stopWalk()
            self.motion.stopMove()

            # Log stop
            with open(self.command_log_file, 'a') as f:
                elapsed = time.time() - self.start_time
                f.write("[{:.2f}] STOPPED\n".format(elapsed))
                f.write("  Samples: {}\n".format(samples))
                f.write("  Movement: {}\n".format("Yes" if max_values.get('IsMoving') else "No"))
                f.write("  Steps: {}\n".format("Yes" if max_values.get('StepDetected') else "No"))
                f.write("  Max Imbalance: {:.3f}\n\n".format(max_values.get('MaxImbalance', 0)))

            # Print summary
            print("\n   [RESULTS]")
            print("   - Samples logged: {}".format(samples))
            print("   - Movement detected: {}".format("YES ✓" if max_values.get('IsMoving') else "NO ✗"))
            print("   - Steps detected: {}".format("YES ✓" if max_values.get('StepDetected') else "NO ✗"))
            print("   - Max imbalance: {:.3f} {}".format(
                max_values.get('MaxImbalance', 0),
                ("(stable)" if max_values.get('MaxImbalance', 0) < 0.5 else "(WARNING: unstable)")
            ))

            return True

        except Exception as e:
            print("Error: {}".format(str(e)))
            self.motion.stopWalk()
            self.motion.stopMove()
            return False

        finally:
            self.is_executing = False
            self.is_logging = False
            self.current_command = ""
            time.sleep(0.3)

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
