"""
Robot Bridge - Clean interface to NAOqi robot functionality
Supports both LAN and WiFi connections
"""

from .motion_bridge import MotionBridge

__version__ = "1.0.0"
__all__ = ["MotionBridge"]

# Main entry point
RobotBridge = MotionBridge
