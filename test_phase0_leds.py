#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Phase 0 Test: LED Control
Tests LED functionality and color control
Compatible with NAOqi 2.8.6.23
"""

import sys
from naoqi import ALProxy
import time

def test_leds():
    """Test LED control and effects"""

    robot_ip = "169.254.80.144"
    robot_port = 9559

    print("=" * 70)
    print("PHASE 0 TEST: LED Control")
    print("=" * 70)
    print("\nTesting LED functionality and effects\n")

    results = {}
    total_tests = 0
    passed_tests = 0

    try:
        leds = ALProxy("ALLeds", robot_ip, robot_port)

        # Test basic LED on/off
        print("1. Basic LED On/Off")
        print("=" * 70 + "\n")

        try:
            print("   Turning on chest LED...")
            leds.on("ChestLeds")
            time.sleep(1)

            print("   Turning off chest LED...")
            leds.off("ChestLeds")
            time.sleep(0.5)

            print("   OK  LED on/off working\n")
            results["Basic LED Control"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Basic LED Control"] = "FAIL"
        total_tests += 1

        # Test LED brightness
        print("=" * 70)
        print("2. LED Brightness Control")
        print("=" * 70 + "\n")

        try:
            print("   Setting chest LED to 25% brightness...")
            leds.setIntensity("ChestLeds", 0.25)
            time.sleep(0.5)

            print("   Setting chest LED to 50% brightness...")
            leds.setIntensity("ChestLeds", 0.5)
            time.sleep(0.5)

            print("   Setting chest LED to 100% brightness...")
            leds.setIntensity("ChestLeds", 1.0)
            time.sleep(0.5)

            print("   Turning off chest LED...")
            leds.off("ChestLeds")
            time.sleep(0.5)

            print("   OK  Brightness control working\n")
            results["Brightness Control"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Brightness Control"] = "WARN"
        total_tests += 1

        # Test RGB color
        print("=" * 70)
        print("3. RGB Color Control")
        print("=" * 70 + "\n")

        try:
            colors = [
                ("Red", 0xFF0000FF, 1),
                ("Green", 0x00FF00FF, 1),
                ("Blue", 0x0000FFFF, 1),
                ("Yellow", 0xFFFF00FF, 1),
                ("Cyan", 0x00FFFFFF, 1),
                ("Magenta", 0xFF00FFFF, 1),
            ]

            for color_name, color_value, duration in colors:
                print("   Setting face LEDs to {0}...".format(color_name))
                leds.fadeRGB("FaceLeds", color_value, duration)
                time.sleep(duration + 0.5)

            # Turn off
            print("   Turning off face LEDs...")
            leds.off("FaceLeds")
            time.sleep(0.5)

            print("   OK  RGB color control working\n")
            results["RGB Color Control"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["RGB Color Control"] = "FAIL"
        total_tests += 1

        # Test different LED groups
        print("=" * 70)
        print("4. LED Groups")
        print("=" * 70 + "\n")

        led_groups = [
            "ChestLeds",
            "FaceLeds",
            "LeftFootLeds",
            "RightFootLeds",
        ]

        for group in led_groups:
            try:
                print("   Testing {0}...".format(group))
                leds.on(group)
                time.sleep(0.5)
                leds.off(group)
                print("      OK\n")
                results["LED Group: {0}".format(group)] = "PASS"
                passed_tests += 1
            except Exception as e:
                print("      WARNING: {0}\n".format(e))
                results["LED Group: {0}".format(group)] = "WARN"
            total_tests += 1

        # Test eye animation
        print("=" * 70)
        print("5. Eye Animation")
        print("=" * 70 + "\n")

        try:
            print("   Running random eye animation...")
            leds.randomEyes()
            time.sleep(3)

            print("   Stopping animation...")
            leds.off("FaceLeds")
            time.sleep(0.5)

            print("   OK  Eye animation working\n")
            results["Eye Animation"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["Eye Animation"] = "WARN"
        total_tests += 1

        # Test synchronized LEDs
        print("=" * 70)
        print("6. Synchronized LED Control")
        print("=" * 70 + "\n")

        try:
            print("   Turning on all LEDs...")
            leds.on("AllLeds")
            time.sleep(1)

            print("   Setting all LEDs to 50% brightness...")
            leds.setIntensity("AllLeds", 0.5)
            time.sleep(1)

            print("   Turning off all LEDs...")
            leds.off("AllLeds")
            time.sleep(0.5)

            print("   OK  All LED control working\n")
            results["All LEDs"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   WARNING: {0}\n".format(e))
            results["All LEDs"] = "WARN"
        total_tests += 1

        # Test fade effect
        print("=" * 70)
        print("7. Fade Effect")
        print("=" * 70 + "\n")

        try:
            print("   Testing fade effect (2 seconds)...")
            leds.fadeRGB("ChestLeds", 0xFF0000FF, 2.0)  # Red fade
            time.sleep(2.5)

            print("   Turning off...")
            leds.off("ChestLeds")
            time.sleep(0.5)

            print("   OK  Fade effect working\n")
            results["Fade Effect"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Fade Effect"] = "FAIL"
        total_tests += 1

        # Final cleanup
        print("=" * 70)
        print("8. Cleanup")
        print("=" * 70 + "\n")

        try:
            print("   Turning off all LEDs...")
            leds.off("AllLeds")
            time.sleep(0.5)
            print("   OK  Cleanup complete\n")
            results["Cleanup"] = "PASS"
            passed_tests += 1
        except Exception as e:
            print("   ERROR: {0}\n".format(e))
            results["Cleanup"] = "FAIL"
        total_tests += 1

    except Exception as e:
        print("\nCRITICAL ERROR: {0}\n".format(e))
        return 1

    # Print summary
    print("=" * 70)
    print("TEST SUMMARY: LED Control")
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
        print("\nOK  LED test PASSED\n")
        return 0
    else:
        print("\nWARNING LED test had issues\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = test_leds()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        sys.exit(1)
