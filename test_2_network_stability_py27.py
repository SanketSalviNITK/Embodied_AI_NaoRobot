#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test 2: Network Stability (Python 2.7 Compatible)
Tests ping latency, consistency, and network quality
Compatible with NAOqi 2.8.6.23
"""

import subprocess
import time
import statistics
import sys
import platform

def test_ping_stability(ip_address="169.254.80.144", count=15):
    """Test ping latency and stability"""

    print("=" * 60)
    print("TEST 2: Network Stability (Python 2.7)")
    print("=" * 60)
    print("\nTesting network latency to {0}".format(ip_address))
    print("Sending {0} ping packets...\n".format(count))

    latencies = []
    lost = 0
    timeout_count = 0

    # Determine ping command based on OS
    if platform.system() == "Windows":
        ping_cmd = ["ping", "-n", "1", "-w", "2000", ip_address]
    else:
        ping_cmd = ["ping", "-c", "1", "-W", "2000", ip_address]

    for i in range(count):
        try:
            # Run ping command
            result = subprocess.Popen(
                ping_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = result.communicate()

            # Parse latency from output
            if "time=" in stdout:
                # Extract time value
                parts = stdout.split("time=")
                if len(parts) > 1:
                    time_str = parts[1].split("ms")[0]
                    latency = float(time_str)
                    latencies.append(latency)
                    status = "OK"
                    if latency > 50:
                        status = "WARNING"
                    print("   Ping {0:2d}/{1}: {2:6.2f}ms {3}".format(i+1, count, latency, status))
                else:
                    print("   Ping {0:2d}/{1}: No time data (LOST)".format(i+1, count))
                    lost += 1
            else:
                print("   Ping {0:2d}/{1}: Lost (no response)".format(i+1, count))
                lost += 1

        except subprocess.CalledProcessError:
            print("   Ping {0:2d}/{1}: Timeout".format(i+1, count))
            timeout_count += 1
            lost += 1
        except Exception as e:
            print("   Ping {0:2d}/{1}: Error - {2}".format(i+1, count, str(e)))
            lost += 1

        # Small delay between pings
        if i < count - 1:
            time.sleep(0.5)

    # Calculate statistics
    print("\n" + "=" * 60)
    print("NETWORK STATISTICS:")
    print("=" * 60)

    if latencies:
        min_lat = min(latencies)
        max_lat = max(latencies)
        avg_lat = sum(latencies) / float(len(latencies))

        # Calculate median
        sorted_lat = sorted(latencies)
        if len(sorted_lat) % 2 == 0:
            median_lat = (sorted_lat[len(sorted_lat)/2-1] + sorted_lat[len(sorted_lat)/2]) / 2.0
        else:
            median_lat = sorted_lat[len(sorted_lat)/2]

        # Calculate standard deviation
        if len(latencies) > 1:
            variance = sum((x - avg_lat) ** 2 for x in latencies) / float(len(latencies) - 1)
            stddev_lat = variance ** 0.5
        else:
            stddev_lat = 0

        print("\nLatency (milliseconds):")
        print("  Minimum:  {0:6.2f}ms".format(min_lat))
        print("  Maximum:  {0:6.2f}ms".format(max_lat))
        print("  Average:  {0:6.2f}ms".format(avg_lat))
        print("  Median:   {0:6.2f}ms".format(median_lat))
        print("  Std Dev:  {0:6.2f}ms".format(stddev_lat))

        print("\nPacket Statistics:")
        print("  Packets sent:     {0}".format(count))
        print("  Packets received: {0}".format(len(latencies)))
        print("  Packets lost:     {0}".format(lost))
        print("  Loss rate:        {0:.1f}%".format((lost/float(count))*100))

        # Quality assessment
        print("\nNetwork Quality Assessment:")

        quality_score = 0

        # Latency check
        if max_lat < 30:
            print("  OK  Latency: Excellent (max {0:.0f}ms < 30ms)".format(max_lat))
            quality_score += 2
        elif max_lat < 50:
            print("  OK  Latency: Very Good (max {0:.0f}ms < 50ms)".format(max_lat))
            quality_score += 2
        elif max_lat < 100:
            print("  WARNING Latency: Good (max {0:.0f}ms < 100ms)".format(max_lat))
            quality_score += 1
        else:
            print("  ERROR Latency: Poor (max {0:.0f}ms > 100ms)".format(max_lat))

        # Consistency check
        if stddev_lat < 5:
            print("  OK  Stability: Excellent (std dev {0:.2f}ms)".format(stddev_lat))
            quality_score += 2
        elif stddev_lat < 10:
            print("  OK  Stability: Good (std dev {0:.2f}ms)".format(stddev_lat))
            quality_score += 1
        else:
            print("  WARNING Stability: Variable (std dev {0:.2f}ms)".format(stddev_lat))

        # Packet loss check
        if lost == 0:
            print("  OK  Packet loss: None (0%)")
            quality_score += 2
        elif lost < 2:
            print("  OK  Packet loss: Minimal ({0}/{1})".format(lost, count))
            quality_score += 1
        else:
            print("  ERROR Packet loss: High ({0}/{1})".format(lost, count))

        # Overall assessment
        print("\nOverall Quality Score: {0}/6".format(quality_score))

        if quality_score >= 5:
            print("OK  Network quality is EXCELLENT for real-time robotics!")
            result = True
        elif quality_score >= 3:
            print("WARNING Network quality is ACCEPTABLE but monitor for issues")
            result = True
        else:
            print("ERROR Network quality is POOR - may cause issues")
            result = False

    else:
        print("\nERROR: All ping packets lost! Network is not responding.")
        print("   Timeouts: {0}".format(timeout_count))
        print("   Lost: {0}".format(lost))
        result = False

    print("\n" + "=" * 60)
    if result:
        print("OK  NETWORK TEST PASSED!")
        print("\nNext test: Run test_3_robot_sensors_py27.py")
    else:
        print("ERROR: NETWORK TEST FAILED!")
        print("\nTroubleshooting:")
        print("  - Check network cable connection")
        print("  - Verify robot IP: 169.254.80.144")
        print("  - Check for network congestion")
        print("  - Ensure no firewall blocking ICMP")
    print("=" * 60)

    return result

if __name__ == "__main__":
    try:
        success = test_ping_stability()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nWARNING: Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\nERROR: Unexpected error: {0}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)
