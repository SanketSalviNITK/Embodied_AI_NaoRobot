#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test WiFi Connection to NAO Robot
Verifies connectivity via both LAN and WiFi
"""

import sys
import time
import json

# Robot IPs
ROBOT_IPS = {
    'lan': '169.254.175.171',
    'wifi': '192.168.137.87'
}

NAOQI_PORT = 9559

def test_connection(ip, connection_type):
    """Test connection to robot at given IP"""
    print("\n" + "=" * 70)
    print("Testing {} Connection: {}".format(connection_type.upper(), ip))
    print("=" * 70)

    try:
        # Try to import naoqi
        print("1. Checking NAOqi SDK...")
        try:
            from naoqi import ALProxy
            print("   OK  NAOqi SDK available")
        except ImportError as e:
            print("   ERROR: NAOqi SDK not found: {}".format(str(e)))
            print("   Make sure to activate venv_py27 first")
            return False

        # Try to connect
        print("2. Attempting connection to {}:{}...".format(ip, NAOQI_PORT))
        try:
            motion = ALProxy('ALMotion', ip, NAOQI_PORT)
            print("   OK  Connected to ALMotion proxy")
        except Exception as e:
            print("   ERROR: Failed to connect: {}".format(str(e)))
            return False

        # Test basic functionality
        print("3. Testing basic functionality...")
        try:
            # Get robot version
            motion.getRobotConfig()
            print("   OK  Robot responded to command")
        except Exception as e:
            print("   ERROR: Robot command failed: {}".format(str(e)))
            return False

        # Get some sensor data
        print("4. Reading sensor data...")
        try:
            from naoqi import ALProxy
            memory = ALProxy('ALMemory', ip, NAOQI_PORT)
            battery = memory.getData('Device/SubDeviceList/Battery/Current/Sensor/Value')
            print("   OK  Battery level: {}%".format(int(battery)))
        except Exception as e:
            print("   WARNING: Could not read battery: {}".format(str(e)))

        print("\n✓ {} Connection Test PASSED".format(connection_type.upper()))
        return True

    except Exception as e:
        print("\n✗ {} Connection Test FAILED: {}".format(connection_type.upper(), str(e)))
        return False

def main():
    """Main test runner"""
    print("\n" + "=" * 70)
    print("NAO Robot WiFi & LAN Connection Test")
    print("=" * 70)
    print("\nRobot Configuration:")
    print("  LAN IP:  {}".format(ROBOT_IPS['lan']))
    print("  WiFi IP: {}".format(ROBOT_IPS['wifi']))
    print("  Port:    {}".format(NAOQI_PORT))

    results = {}

    # Test LAN
    results['lan'] = test_connection(ROBOT_IPS['lan'], 'LAN')
    time.sleep(2)

    # Test WiFi
    results['wifi'] = test_connection(ROBOT_IPS['wifi'], 'WiFi')

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print("\nLAN Connection:  {}".format("✓ PASSED" if results['lan'] else "✗ FAILED"))
    print("WiFi Connection: {}".format("✓ PASSED" if results['wifi'] else "✗ FAILED"))

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print("\nTotal: {}/{} connections working".format(passed, total))

    if all(results.values()):
        print("\n✓ Both LAN and WiFi connections are working!")
        print("\nYou can now use either IP for robot control:")
        print("  - LAN for stable, wired connection")
        print("  - WiFi for mobile, wireless operation")
        return 0
    elif results['lan']:
        print("\n⚠ LAN connection working, WiFi has issues")
        print("Check WiFi network and connection status")
        return 1
    elif results['wifi']:
        print("\n⚠ WiFi connection working, LAN has issues")
        print("Check LAN cable and network configuration")
        return 1
    else:
        print("\n✗ No connections working!")
        print("Check robot power and network configuration")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\n\nFATAL ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
