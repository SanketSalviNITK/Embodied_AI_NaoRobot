#!/usr/bin/env python3
"""
Test 2: Network Stability
Tests ping latency, consistency, and network quality
"""

import subprocess
import time
import statistics
import sys

def test_ping_stability(ip_address="169.254.80.144", count=15):
    """Test ping latency and stability"""

    print("=" * 60)
    print("TEST 2: Network Stability")
    print("=" * 60)
    print(f"\nTesting network latency to {ip_address}")
    print(f"Sending {count} ping packets...\n")

    latencies = []
    lost = 0
    timeout_count = 0

    for i in range(count):
        try:
            # Windows ping command (1 packet)
            result = subprocess.run(
                ["ping", "-n", "1", "-w", "2000", ip_address],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Parse latency from output
            if "time=" in result.stdout:
                # Extract time value
                parts = result.stdout.split("time=")
                if len(parts) > 1:
                    time_str = parts[1].split("ms")[0]
                    latency = float(time_str)
                    latencies.append(latency)
                    status = "✅"
                    if latency > 50:
                        status = "⚠️"
                    print(f"   Ping {i+1:2d}/{count}: {latency:6.2f}ms {status}")
                else:
                    print(f"   Ping {i+1:2d}/{count}: No time data ❌")
                    lost += 1
            else:
                print(f"   Ping {i+1:2d}/{count}: Lost (no response) ❌")
                lost += 1

        except subprocess.TimeoutExpired:
            print(f"   Ping {i+1:2d}/{count}: Timeout ❌")
            timeout_count += 1
            lost += 1
        except Exception as e:
            print(f"   Ping {i+1:2d}/{count}: Error - {e}")
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
        avg_lat = statistics.mean(latencies)
        median_lat = statistics.median(latencies)
        stddev_lat = statistics.stdev(latencies) if len(latencies) > 1 else 0

        print(f"\nLatency (milliseconds):")
        print(f"  Minimum:  {min_lat:6.2f}ms")
        print(f"  Maximum:  {max_lat:6.2f}ms")
        print(f"  Average:  {avg_lat:6.2f}ms")
        print(f"  Median:   {median_lat:6.2f}ms")
        print(f"  Std Dev:  {stddev_lat:6.2f}ms")

        print(f"\nPacket Statistics:")
        print(f"  Packets sent:     {count}")
        print(f"  Packets received: {len(latencies)}")
        print(f"  Packets lost:     {lost}")
        print(f"  Loss rate:        {(lost/count)*100:.1f}%")

        # Quality assessment
        print(f"\nNetwork Quality Assessment:")

        quality_score = 0

        # Latency check
        if max_lat < 30:
            print(f"  ✅ Latency: Excellent (max {max_lat:.0f}ms < 30ms)")
            quality_score += 2
        elif max_lat < 50:
            print(f"  ✅ Latency: Very Good (max {max_lat:.0f}ms < 50ms)")
            quality_score += 2
        elif max_lat < 100:
            print(f"  ⚠️  Latency: Good (max {max_lat:.0f}ms < 100ms)")
            quality_score += 1
        else:
            print(f"  ❌ Latency: Poor (max {max_lat:.0f}ms > 100ms)")

        # Consistency check
        if stddev_lat < 5:
            print(f"  ✅ Stability: Excellent (std dev {stddev_lat:.2f}ms)")
            quality_score += 2
        elif stddev_lat < 10:
            print(f"  ✅ Stability: Good (std dev {stddev_lat:.2f}ms)")
            quality_score += 1
        else:
            print(f"  ⚠️  Stability: Variable (std dev {stddev_lat:.2f}ms)")

        # Packet loss check
        if lost == 0:
            print(f"  ✅ Packet loss: None (0%)")
            quality_score += 2
        elif lost < 2:
            print(f"  ✅ Packet loss: Minimal ({lost}/{count})")
            quality_score += 1
        else:
            print(f"  ❌ Packet loss: High ({lost}/{count})")

        # Overall assessment
        print(f"\n📊 Overall Quality Score: {quality_score}/6")

        if quality_score >= 5:
            print("✅ Network quality is EXCELLENT for real-time robotics!")
            result = True
        elif quality_score >= 3:
            print("⚠️  Network quality is ACCEPTABLE but monitor for issues")
            result = True
        else:
            print("❌ Network quality is POOR - may cause issues")
            result = False

    else:
        print("\n❌ All ping packets lost! Network is not responding.")
        print(f"   Timeouts: {timeout_count}")
        print(f"   Lost: {lost}")
        result = False

    print("\n" + "=" * 60)
    if result:
        print("✅ NETWORK TEST PASSED!")
        print("\nNext test: Run test_3_joint_movement.py")
    else:
        print("❌ NETWORK TEST FAILED!")
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
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
