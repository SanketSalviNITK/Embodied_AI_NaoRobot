#!/usr/bin/env python3
"""
Test 1: Basic NAOqi Connection
Tests if we can connect to the robot and access basic proxies
"""

import sys
import time

def test_naoqi_connection():
    """Test basic connection to NAOqi"""

    robot_ip = "169.254.80.144"
    robot_port = 9559

    print("=" * 60)
    print("TEST 1: Basic NAOqi Connection")
    print("=" * 60)
    print(f"\nConnecting to robot at {robot_ip}:{robot_port}...\n")

    try:
        # Import NAOqi
        from naoqi import ALProxy
        print("✅ NAOqi module imported successfully")

        # Test Motion proxy
        print("\n1. Testing ALMotion proxy...")
        motion = ALProxy("ALMotion", robot_ip, robot_port)
        print("   ✅ ALMotion proxy created successfully")

        # Test posture proxy
        print("\n2. Testing ALRobotPosture proxy...")
        posture = ALProxy("ALRobotPosture", robot_ip, robot_port)
        print("   ✅ ALRobotPosture proxy created successfully")

        # Test battery proxy
        print("\n3. Testing ALBattery proxy...")
        battery = ALProxy("ALBattery", robot_ip, robot_port)
        print("   ✅ ALBattery proxy created successfully")

        # Test speech proxy
        print("\n4. Testing ALTextToSpeech proxy...")
        tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
        print("   ✅ ALTextToSpeech proxy created successfully")

        # Test audio proxy
        print("\n5. Testing ALAudioDevice proxy...")
        audio = ALProxy("ALAudioDevice", robot_ip, robot_port)
        print("   ✅ ALAudioDevice proxy created successfully")

        # Test memory proxy
        print("\n6. Testing ALMemory proxy...")
        memory = ALProxy("ALMemory", robot_ip, robot_port)
        print("   ✅ ALMemory proxy created successfully")

        # Get actual data
        print("\n" + "=" * 60)
        print("GETTING ROBOT DATA:")
        print("=" * 60)

        # Battery data
        print("\n🔋 Battery Information:")
        try:
            battery_charge = battery.getBatteryCharge()
            battery_health = battery.getBatteryHealth()
            print(f"   Battery Charge: {battery_charge}%")
            print(f"   Battery Health: {battery_health}")
        except Exception as e:
            print(f"   ⚠️  Could not get battery data: {e}")

        # Stiffness status
        print("\n🤖 Robot Stiffness Status:")
        try:
            stiffness = motion.getStiffnesses("Body")
            print(f"   Stiffness values: {stiffness}")
            if isinstance(stiffness, list) and len(stiffness) > 0:
                if stiffness[0] > 0:
                    print("   ⚠️  Robot is currently stiff (high stiffness)")
                else:
                    print("   ✅ Robot is relaxed (low stiffness)")
        except Exception as e:
            print(f"   ⚠️  Could not get stiffness: {e}")

        # Posture
        print("\n👤 Robot Posture:")
        try:
            current_posture = posture.getPosture()
            print(f"   Current posture: {current_posture}")
        except Exception as e:
            print(f"   ⚠️  Could not get posture: {e}")

        # NAOqi version
        print("\n📊 System Information:")
        try:
            naoqi_version = memory.getData("NAOqiVersion")
            print(f"   NAOqi version: {naoqi_version}")
        except:
            try:
                # Try alternative method
                version = motion.robotName()
                print(f"   Robot name: {version}")
            except:
                print("   ⚠️  Could not get NAOqi version")

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nRobot is responding correctly and all proxies are accessible.")
        print("\nNext test: Run test_2_network_stability.py")
        print("=" * 60)

        return True

    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        print("\nMake sure NAOqi SDK is installed:")
        print("   pip install naoqi")
        return False

    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print(f"\nCould not connect to robot at {robot_ip}:{robot_port}")
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
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
