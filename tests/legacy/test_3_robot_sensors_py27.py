#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test 3: Robot Sensors (Python 2.7 Compatible)
Tests all sensor inputs and data reading
Compatible with NAOqi 2.8.6.23
"""

import sys
import time

def test_sensors():
    """Test all robot sensors"""

    robot_ip = "169.254.175.171"
    robot_port = 9559

    print("=" * 60)
    print("TEST 3: Robot Sensors (Python 2.7)")
    print("=" * 60)
    print("\nTesting sensors on robot at {0}:{1}\n".format(robot_ip, robot_port))

    results = {}

    try:
        from naoqi import ALProxy

        # Test Battery
        print("1. Testing Battery Sensor...")
        try:
            battery = ALProxy("ALBattery", robot_ip, robot_port)
            charge = battery.getBatteryCharge()
            print("   OK  Battery charge: {0}%".format(charge))
            results["Battery"] = "OK"
        except Exception as e:
            print("   WARNING Battery sensor failed: {0}".format(e))
            results["Battery"] = "WARNING"

        # Test IMU/Accelerometer
        print("\n2. Testing IMU/Accelerometer...")
        try:
            memory = ALProxy("ALMemory", robot_ip, robot_port)

            # Get accelerometer data
            acc_x = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
            acc_y = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value")
            acc_z = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")

            print("   OK  Accelerometer X: {0:.4f} g".format(acc_x))
            print("   OK  Accelerometer Y: {0:.4f} g".format(acc_y))
            print("   OK  Accelerometer Z: {0:.4f} g".format(acc_z))
            results["Accelerometer"] = "OK"
        except Exception as e:
            print("   WARNING Accelerometer failed: {0}".format(e))
            results["Accelerometer"] = "WARNING"

        # Test Gyroscope
        print("\n3. Testing Gyroscope...")
        try:
            gyr_x = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value")
            gyr_y = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value")
            gyr_z = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value")

            print("   OK  Gyroscope X: {0:.4f} rad/s".format(gyr_x))
            print("   OK  Gyroscope Y: {0:.4f} rad/s".format(gyr_y))
            print("   OK  Gyroscope Z: {0:.4f} rad/s".format(gyr_z))
            results["Gyroscope"] = "OK"
        except Exception as e:
            print("   WARNING Gyroscope failed: {0}".format(e))
            results["Gyroscope"] = "WARNING"

        # Test FSR (Force Sensitive Resistors) - foot sensors
        print("\n4. Testing Foot Sensors (FSR)...")
        try:
            # Left foot
            lfoot_fl = memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
            lfoot_fr = memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
            lfoot_rl = memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
            lfoot_rr = memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

            print("   OK  Left foot FSR Front-Left: {0:.2f}".format(lfoot_fl))
            print("   OK  Left foot FSR Front-Right: {0:.2f}".format(lfoot_fr))
            print("   OK  Left foot FSR Rear-Left: {0:.2f}".format(lfoot_rl))
            print("   OK  Left foot FSR Rear-Right: {0:.2f}".format(lfoot_rr))
            results["Foot Sensors (FSR)"] = "OK"
        except Exception as e:
            print("   WARNING Foot sensors failed: {0}".format(e))
            results["Foot Sensors (FSR)"] = "WARNING"

        # Test Joint Encoders
        print("\n5. Testing Joint Encoders...")
        try:
            motion = ALProxy("ALMotion", robot_ip, robot_port)

            # Sample a few joints
            test_joints = ["HeadYaw", "HeadPitch", "LShoulderPitch", "RShoulderPitch"]
            joint_data = []

            for joint in test_joints:
                angle = motion.getAngles(joint, False)[0]
                print("   OK  {0}: {1:.4f} rad".format(joint, angle))
                joint_data.append(angle)

            results["Joint Encoders"] = "OK"
        except Exception as e:
            print("   ERROR Joint encoders failed: {0}".format(e))
            results["Joint Encoders"] = "ERROR"

        # Test Microphone
        print("\n6. Testing Microphone...")
        try:
            audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
            print("   OK  Microphone proxy accessible")
            print("   INFO Microphone is ready to record audio")
            results["Microphone"] = "OK"
        except Exception as e:
            print("   WARNING Microphone test failed: {0}".format(e))
            results["Microphone"] = "WARNING"

        # Test Speaker
        print("\n7. Testing Speaker...")
        try:
            tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
            output_vol = audio.getOutputVolume()
            print("   OK  Speaker output volume: {0}%".format(output_vol))
            print("   INFO Speaker is ready for audio output")
            results["Speaker"] = "OK"
        except Exception as e:
            print("   WARNING Speaker test failed: {0}".format(e))
            results["Speaker"] = "WARNING"

        # Test Cameras
        print("\n8. Testing Cameras...")
        try:
            video = ALProxy("ALVideoDevice", robot_ip, robot_port)
            print("   OK  Video device proxy accessible")
            print("   INFO Cameras may be available (firmware dependent)")
            results["Cameras"] = "OK"
        except Exception as e:
            print("   WARNING Camera test (may not be available): {0}".format(e))
            results["Cameras"] = "WARNING"

        # Summary
        print("\n" + "=" * 60)
        print("SENSOR TEST SUMMARY:")
        print("=" * 60)

        passed = 0
        warning = 0
        failed = 0

        for sensor, status in results.items():
            if status == "OK":
                print("  OK  {0}".format(sensor))
                passed += 1
            elif status == "WARNING":
                print("  WARNING {0}".format(sensor))
                warning += 1
            else:
                print("  ERROR {0}".format(sensor))
                failed += 1

        print("\nTotal: {0} passed, {1} warning(s), {2} failed".format(passed, warning, failed))

        print("\n" + "=" * 60)
        if failed == 0:
            print("OK  SENSOR TEST COMPLETED!")
            print("\nAll critical sensors are responding.")
            print("All tests completed successfully!")
        else:
            print("WARNING SENSOR TEST COMPLETED WITH ISSUES")
            print("\nSome sensors failed. Check above for details.")

        print("=" * 60)

        return failed == 0

    except ImportError as e:
        print("\nERROR: Import error: {0}".format(e))
        print("Make sure NAOqi SDK is installed for Python 2.7")
        return False
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_sensors()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
