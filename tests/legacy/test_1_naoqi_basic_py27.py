#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test 1: Basic NAOqi Connection (Python 2.7 Compatible)
Tests if we can connect to the robot and access basic proxies
Compatible with NAOqi 2.8.6.23
"""

import sys
import time

def test_naoqi_connection():
    """Test basic connection to NAOqi"""

    robot_ip = "169.254.80.144"
    robot_port = 9559

    print("=" * 60)
    print("TEST 1: Basic NAOqi Connection (Python 2.7)")
    print("=" * 60)
    print("\nConnecting to robot at {0}:{1}...\n".format(robot_ip, robot_port))

    try:
        # Import NAOqi
        from naoqi import ALProxy
        print("OK  NAOqi module imported successfully")

        # Test Motion proxy
        print("\n1. Testing ALMotion proxy...")
        motion = ALProxy("ALMotion", robot_ip, robot_port)
        print("   OK  ALMotion proxy created successfully")

        # Test posture proxy
        print("\n2. Testing ALRobotPosture proxy...")
        posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
        print("   OK  ALRobotPosture proxy created successfully")

        # Test battery proxy
        print("\n3. Testing ALBattery proxy...")
        battery = ALProxy("ALBattery", robot_ip, robot_port)
        print("   OK  ALBattery proxy created successfully")

        # Test speech proxy
        print("\n4. Testing ALTextToSpeech proxy...")
        tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
        print("   OK  ALTextToSpeech proxy created successfully")

        # Test audio proxy
        print("\n5. Testing ALAudioDevice proxy...")
        audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
        print("   OK  ALAudioDevice proxy created successfully")

        # Test memory proxy
        print("\n6. Testing ALMemory proxy...")
        memory = ALProxy("ALMemory", robot_ip, robot_port)
        print("   OK  ALMemory proxy created successfully")

        # Get actual data
        print("\n" + "=" * 60)
        print("GETTING ROBOT DATA:")
        print("=" * 60)

        # Battery data
        print("\nBattery Information:")
        try:
            battery_charge = battery.getBatteryCharge()
            battery_health = battery.getBatteryHealth()
            print("   Battery Charge: {0}%".format(battery_charge))
            print("   Battery Health: {0}".format(battery_health))
        except Exception as e:
            print("   WARNING: Could not get battery data: {0}".format(e))

        # Stiffness status
        print("\nRobot Stiffness Status:")
        try:
            stiffness = motion.getStiffnesses("Body")
            print("   Stiffness values: {0}".format(stiffness))
            if isinstance(stiffness, list) and len(stiffness) > 0:
                if stiffness[0] > 0:
                    print("   WARNING: Robot is currently stiff (high stiffness)")
                else:
                    print("   OK  Robot is relaxed (low stiffness)")
        except Exception as e:
            print("   WARNING: Could not get stiffness: {0}".format(e))

        # Posture
        print("\nRobot Posture:")
        try:
            current_posture = posture.getPosture()
            print("   Current posture: {0}".format(current_posture))
        except Exception as e:
            print("   WARNING: Could not get posture: {0}".format(e))

        # NAOqi version
        print("\nSystem Information:")
        try:
            naoqi_version = memory.getData("NAOqiVersion")
            print("   NAOqi version: {0}".format(naoqi_version))
        except:
            try:
                # Try alternative method
                version = motion.robotName()
                print("   Robot name: {0}".format(version))
            except:
                print("   WARNING: Could not get NAOqi version")

        print("\n" + "=" * 60)
        print("OK  ALL TESTS PASSED!")
        print("=" * 60)
        print("\nRobot is responding correctly and all proxies are accessible.")
        print("\nNext test: Run test_2_network_stability_py27.py")
        print("=" * 60)

        return True

    except ImportError as e:
        print("\nERROR: Import failed: {0}".format(e))
        print("\nMake sure NAOqi SDK is installed for Python 2.7:")
        print("   The folder in your project: pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649")
        print("   You may need to add it to PYTHONPATH")
        return False

    except Exception as e:
        print("\nERROR: Connection failed: {0}".format(e))
        print("\nCould not connect to robot at {0}:{1}".format(robot_ip, robot_port))
        print("\nChecklist:")
        print("  - Is the robot powered on?")
        print("  - Is the robot connected to the network?")
        print("  - Is the IP address correct? (current: 169.254.80.144)")
        print("  - Is the port correct? (current: 9559)")
        print("  - Can you ping the robot? (run: ping 169.254.80.144)")
        return False

if __name__ == "__main__":
    try:
        success = test_naoqi_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        sys.exit(1)
