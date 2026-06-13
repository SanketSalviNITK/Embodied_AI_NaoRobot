#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check Available Motion Methods in NAOqi
Lists all available methods for ALMotion service
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def main():
    """List available motion methods"""
    from naoqi import ALProxy

    wifi_ip = '192.168.137.87'

    print("\n" + "=" * 70)
    print("NAOqi ALMotion - Available Methods")
    print("=" * 70)
    print("\nConnecting...")

    try:
        motion = ALProxy('ALMotion', wifi_ip, 9559)
        print("OK  Connected\n")

        # Get all methods
        methods = motion.getMethodList()

        print("Available ALMotion methods ({} total):\n".format(len(methods)))
        print("-" * 70)

        for method in sorted(methods):
            print("  - {}".format(method))

        print("-" * 70)

        # Check for specific methods we need
        print("\nLooking for movement methods:")
        movement_keywords = ['move', 'walk', 'turn', 'step', 'forward', 'backward', 'side']

        found = [m for m in methods if any(k in m.lower() for k in movement_keywords)]

        if found:
            print("Found {} movement-related methods:".format(len(found)))
            for method in sorted(found):
                print("  ✓ {}".format(method))
        else:
            print("No movement-related methods found!")

    except Exception as e:
        print("ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
