#!/usr/bin/env python3
"""
Test 3: Robot Sensors
Tests all sensor inputs and data reading
"""

import sys
import time

def test_sensors():
    """Test all robot sensors"""

    robot_ip = "169.254.80.144"
    robot_port = 9559

    print("=" * 60)
    print("TEST 3: Robot Sensors")
    print("=" * 60)
    print(f"\nTesting sensors on robot at {robot_ip}:{robot_port}\n")

    results = {}

    try:
        from naoqi import ALProxy

        # Test Battery
        print("1. Testing Battery Sensor...")
        try:
            battery = ALProxy("ALBattery", robot_ip, robot_port)
            charge = battery.getBatteryCharge()
            health = battery.getBatteryHealth()
            print(f"   ✅ Battery charge: {charge}%")
            print(f"   ✅ Battery health: {health}")
            results["Battery"] = "✅"
        except Exception as e:
            print(f"   ❌ Battery sensor failed: {e}")
            results["Battery"] = "❌"

        # Test IMU/Accelerometer
        print("\n2. Testing IMU/Accelerometer...")
        try:
            memory = ALProxy("ALMemory", robot_ip, robot_port)

            # Get accelerometer data
            acc_x = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
            acc_y = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value")
            acc_z = memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")

            print(f"   ✅ Accelerometer X: {acc_x:.4f} g")
            print(f"   ✅ Accelerometer Y: {acc_y:.4f} g")
            print(f"   ✅ Accelerometer Z: {acc_z:.4f} g")
            results["Accelerometer"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Accelerometer failed: {e}")
            results["Accelerometer"] = "⚠️"

        # Test Gyroscope
        print("\n3. Testing Gyroscope...")
        try:
            gyr_x = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value")
            gyr_y = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value")
            gyr_z = memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value")

            print(f"   ✅ Gyroscope X: {gyr_x:.4f} rad/s")
            print(f"   ✅ Gyroscope Y: {gyr_y:.4f} rad/s")
            print(f"   ✅ Gyroscope Z: {gyr_z:.4f} rad/s")
            results["Gyroscope"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Gyroscope failed: {e}")
            results["Gyroscope"] = "⚠️"

        # Test FSR (Force Sensitive Resistors) - foot sensors
        print("\n4. Testing Foot Sensors (FSR)...")
        try:
            # Left foot
            lfoot_fl = memory.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
            lfoot_fr = memory.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
            lfoot_rl = memory.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
            lfoot_rr = memory.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

            print(f"   ✅ Left foot FSR Front-Left: {lfoot_fl:.2f}")
            print(f"   ✅ Left foot FSR Front-Right: {lfoot_fr:.2f}")
            print(f"   ✅ Left foot FSR Rear-Left: {lfoot_rl:.2f}")
            print(f"   ✅ Left foot FSR Rear-Right: {lfoot_rr:.2f}")
            results["Foot Sensors (FSR)"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Foot sensors failed: {e}")
            results["Foot Sensors (FSR)"] = "⚠️"

        # Test Joint Encoders
        print("\n5. Testing Joint Encoders...")
        try:
            motion = ALProxy("ALMotion", robot_ip, robot_port)

            # Sample a few joints
            test_joints = ["HeadYaw", "HeadPitch", "LShoulderPitch", "RShoulderPitch"]
            joint_data = []

            for joint in test_joints:
                angle = motion.getAngles(joint, False)[0]
                print(f"   ✅ {joint}: {angle:.4f} rad")
                joint_data.append(angle)

            results["Joint Encoders"] = "✅"
        except Exception as e:
            print(f"   ❌ Joint encoders failed: {e}")
            results["Joint Encoders"] = "❌"

        # Test Microphone
        print("\n6. Testing Microphone...")
        try:
            audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
            input_vol = audio.getInputVolume()
            print(f"   ✅ Microphone input volume: {input_vol}%")
            print(f"   ℹ️  Microphone is ready to record audio")
            results["Microphone"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Microphone test failed: {e}")
            results["Microphone"] = "⚠️"

        # Test Speaker
        print("\n7. Testing Speaker...")
        try:
            tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
            output_vol = audio.getOutputVolume()
            print(f"   ✅ Speaker output volume: {output_vol}%")
            print(f"   ℹ️  Speaker is ready for audio output")
            results["Speaker"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Speaker test failed: {e}")
            results["Speaker"] = "⚠️"

        # Test Cameras
        print("\n8. Testing Cameras...")
        try:
            video = ALProxy("ALVideoDevice", robot_ip, robot_port)
            cameras = video.getCameraList()
            print(f"   ✅ Available cameras: {cameras}")
            results["Cameras"] = "✅"
        except Exception as e:
            print(f"   ⚠️  Camera test (may not be available): {e}")
            results["Cameras"] = "⚠️"

        # Summary
        print("\n" + "=" * 60)
        print("SENSOR TEST SUMMARY:")
        print("=" * 60)

        passed = 0
        warning = 0
        failed = 0

        for sensor, status in results.items():
            print(f"  {status} {sensor}")
            if "✅" in status:
                passed += 1
            elif "⚠️" in status:
                warning += 1
            else:
                failed += 1

        print(f"\nTotal: {passed} passed, {warning} warning(s), {failed} failed")

        print("\n" + "=" * 60)
        if failed == 0:
            print("✅ SENSOR TEST COMPLETED!")
            print("\nAll critical sensors are responding.")
            print("Next test: Run test_4_motion_control.py")
        else:
            print("⚠️  SENSOR TEST COMPLETED WITH ISSUES")
            print(f"\nSome sensors failed. Check above for details.")

        print("=" * 60)

        return failed == 0

    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure NAOqi SDK is installed")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_sensors()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
