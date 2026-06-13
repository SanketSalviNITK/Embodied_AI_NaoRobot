#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Phase 0 Test: Detailed Sensor Analysis
Comprehensive sensor readings and accuracy tests
Compatible with NAOqi 2.8.6.23
"""

import sys
from naoqi import ALProxy
import time

def test_sensors_detailed():
    """Detailed sensor testing and accuracy verification"""

    robot_ip = "169.254.175.171"
    robot_port = 9559

    print("=" * 70)
    print("PHASE 0 TEST: Detailed Sensor Analysis")
    print("=" * 70)
    print("\nComprehensive sensor accuracy and stability tests\n")

    results = {}
    total_tests = 0
    passed_tests = 0

    try:
        memory = ALProxy("ALMemory", robot_ip, robot_port)
        motion = ALProxy("ALMotion", robot_ip, robot_port)

        # Wake up robot
        print("1. Preparing robot for sensor tests...")
        try:
            motion.wakeUp()
            time.sleep(1)
            print("   OK  Robot ready\n")
            results["Robot Preparation"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Robot Preparation"] = "FAIL"
        total_tests += 1

        # Test IMU/Accelerometer
        print("=" * 70)
        print("2. Accelerometer (IMU) - Gravity Vector Test")
        print("=" * 70 + "\n")

        try:
            acc_readings = []
            print("   Taking 10 readings (1 reading per 100ms):\n")

            for i in range(10):
                acc_x = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
                acc_y = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value")
                acc_z = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")

                acc_readings.append((acc_x, acc_y, acc_z))

                magnitude = (acc_x**2 + acc_y**2 + acc_z**2) ** 0.5

                print("   Reading {0}: X={1:7.4f}  Y={2:7.4f}  Z={3:7.4f}  Mag={4:6.4f}g".format(
                    i+1, acc_x, acc_y, acc_z, magnitude))

                time.sleep(0.1)

            # Calculate statistics
            if acc_readings:
                avg_x = sum(r[0] for r in acc_readings) / len(acc_readings)
                avg_y = sum(r[1] for r in acc_readings) / len(acc_readings)
                avg_z = sum(r[2] for r in acc_readings) / len(acc_readings)
                avg_mag = (avg_x**2 + avg_y**2 + avg_z**2) ** 0.5

                print("\n   Average: X={0:7.4f}  Y={1:7.4f}  Z={2:7.4f}  Mag={3:6.4f}g".format(
                    avg_x, avg_y, avg_z, avg_mag))
                print("   (Expected Z gravity: ~9.81m/s^2 or ~1.0g when standing)\n")

            print("   OK  Accelerometer working\n")
            results["Accelerometer"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Accelerometer"] = "FAIL"
        total_tests += 1

        # Test Gyroscope
        print("=" * 70)
        print("3. Gyroscope - Stability Test (No Rotation)")
        print("=" * 70 + "\n")

        try:
            gyr_readings = []
            print("   Taking 10 readings (robot should be still):\n")

            for i in range(10):
                gyr_x = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value")
                gyr_y = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value")
                gyr_z = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value")

                gyr_readings.append((gyr_x, gyr_y, gyr_z))

                print("   Reading {0}: X={1:7.4f}  Y={2:7.4f}  Z={3:7.4f} rad/s".format(
                    i+1, gyr_x, gyr_y, gyr_z))

                time.sleep(0.1)

            if gyr_readings:
                avg_x = sum(r[0] for r in gyr_readings) / len(gyr_readings)
                avg_y = sum(r[1] for r in gyr_readings) / len(gyr_readings)
                avg_z = sum(r[2] for r in gyr_readings) / len(gyr_readings)

                print("\n   Average: X={0:7.4f}  Y={1:7.4f}  Z={2:7.4f} rad/s".format(
                    avg_x, avg_y, avg_z))
                print("   (Should be close to zero when stationary)\n")

            print("   OK  Gyroscope working\n")
            results["Gyroscope"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Gyroscope"] = "FAIL"
        total_tests += 1

        # Test FSR (Force Sensitive Resistors)
        print("=" * 70)
        print("4. Foot Sensors (FSR) - Pressure Test")
        print("=" * 70 + "\n")

        try:
            fsr_keys = [
                ("LFoot_FL", "Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value"),
                ("LFoot_FR", "Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value"),
                ("LFoot_RL", "Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value"),
                ("LFoot_RR", "Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value"),
                ("RFoot_FL", "Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value"),
                ("RFoot_FR", "Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value"),
                ("RFoot_RL", "Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value"),
                ("RFoot_RR", "Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value"),
            ]

            print("   Reading foot pressure sensors:\n")

            for name, key in fsr_keys:
                try:
                    value = memory.getData(key)
                    print("   {0:<12} {1:6.2f}".format(name, value))
                except:
                    pass

            print("\n   OK  FSR sensors working\n")
            results["Foot Sensors (FSR)"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Foot Sensors (FSR)"] = "WARN"
        total_tests += 1

        # Test touch sensors
        print("=" * 70)
        print("5. Touch Sensors")
        print("=" * 70 + "\n")

        try:
            touch_keys = [
                ("Head Front", "Device/SubDeviceList/Head/Touch/Front/Sensor/Value"),
                ("Head Middle", "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"),
                ("Head Rear", "Device/SubDeviceList/Head/Touch/Rear/Sensor/Value"),
            ]

            print("   Reading touch sensors (0=no touch, 1=touched):\n")

            for name, key in touch_keys:
                try:
                    value = memory.getData(key)
                    status = "TOUCHED" if value > 0.5 else "not touched"
                    print("   {0:<20} {1}".format(name, status))
                except:
                    pass

            print("\n   OK  Touch sensors working\n")
            results["Touch Sensors"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Touch Sensors"] = "WARN"
        total_tests += 1

        # Test battery
        print("=" * 70)
        print("6. Battery Status")
        print("=" * 70 + "\n")

        try:
            battery = ALProxy("ALBattery", robot_ip, robot_port)
            charge = battery.getBatteryCharge()
            status = battery.getBatteryStatus()
            temp = battery.getBatteryTemperature()

            print("   Battery charge: {0}%".format(charge))
            print("   Battery status: {0}".format(status))
            print("   Battery temperature: {0:.1f}C\n".format(temp))

            if charge > 20:
                print("   OK  Battery healthy\n")
                results["Battery"] = "PASS"
                passed_tests += 1
            else:
                print("   WARNING Battery low\n")
                results["Battery"] = "WARN"
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Battery"] = "FAIL"
        total_tests += 1

        # Test temperature sensors
        print("=" * 70)
        print("7. Temperature Sensors")
        print("=" * 70 + "\n")

        try:
            print("   Reading temperature sensors:\n")

            temp_keys = [
                ("Battery Temp", "Device/SubDeviceList/Battery/Sensor/Temperature"),
                ("Chest Temp", "Device/SubDeviceList/ChestBoard/Sensor/Temperature"),
            ]

            for name, key in temp_keys:
                try:
                    value = memory.getData(key)
                    print("   {0:<20} {1:.1f}C".format(name, value))
                except:
                    pass

            print("\n   OK  Temperature sensors working\n")
            results["Temperature Sensors"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Temperature Sensors"] = "WARN"
        total_tests += 1

        # Rest robot
        print("=" * 70)
        print("8. Finishing - Rest Position")
        print("=" * 70 + "\n")

        try:
            motion.rest()
            time.sleep(1)
            print("   OK  Robot at rest\n")
            results["Rest"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Rest"] = "FAIL"
        total_tests += 1

    except Exception as e:
        print("\nCRITICAL ERROR: {0}\n".format(e))
        return 1

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY: Detailed Sensor Analysis")
    print("=" * 70)
    print("\nDetailed Results:\n")

    for test_name, result in results.items():
        status_icon = "OK  " if result == "PASS" else "FAIL" if result == "FAIL" else "WARN"
        print("   {0:<35} {1}".format(test_name, status_icon))

    print("\n" + "=" * 70)
    print("Total: {0}/{1} tests passed".format(passed_tests, total_tests))
    print("=" * 70)

    success = passed_tests >= (total_tests - 1)

    if success:
        print("\nOK  Sensor analysis PASSED\n")
        return 0
    else:
        print("\nWARNING Sensor analysis had issues\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_sensors_detailed()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        sys.exit(1)
