# -*- coding: utf-8 -*-
"""
NAO Digital Twin Bridge (nao_twin_bridge.py)
--------------------------------------------
This service runs a continuous loop (10Hz) to synchronize the physical NAO robot
with the 3D Blender model. If the physical robot is offline, it automatically runs in
Mock Demonstration Mode, sending smooth, lifelike sinusoidal movements (breathing, scanning, waving).
"""

import time
import socket
import json
import math
import sys

# Try importing urllib2 (Python 2) or urllib.request (Python 3) for polling the bridge
try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request

BLENDER_HOST = '127.0.0.1'
BLENDER_PORT = 9876
BRIDGE_URL = 'http://127.0.0.1:5001/joints'

# Active Joint Axis Mapping matching build_nao_model.py
JOINT_AXIS_MAP = {
    "HeadYaw": "Z",
    "HeadPitch": "Y",
    
    # Left Arm
    "LShoulderPitch": "Y",
    "LShoulderRoll": "X",
    "LElbowYaw": "Z",
    "LElbowRoll": "X",
    "LWristYaw": "Z",
    "LHand": "X",
    
    # Right Arm
    "RShoulderPitch": "Y",
    "RShoulderRoll": "X",
    "RElbowYaw": "Z",
    "RElbowRoll": "X",
    "RWristYaw": "Z",
    "RHand": "X",
    
    # Left Leg
    "LHipYawPitch": "Z",
    "LHipRoll": "X",
    "LHipPitch": "Y",
    "LKneePitch": "Y",
    "LAnklePitch": "Y",
    "LAnkleRoll": "X",
    
    # Right Leg
    "RHipYawPitch": "Z",
    "RHipRoll": "X",
    "RHipPitch": "Y",
    "RKneePitch": "Y",
    "RAnklePitch": "Y",
    "RAnkleRoll": "X",
}

def send_to_blender(code_str):
    """Sends the python command block to the Blender Add-on server."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((BLENDER_HOST, BLENDER_PORT))
        s.sendall(code_str.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        # We don't necessarily need to read the full output in the fast loop to minimize latency
        s.close()
        return True
    except Exception as e:
        return False

def generate_blender_rotation_code(joint_angles):
    """Generates the bpy Python script to rotate the active bones inside Blender."""
    code_lines = [
        "import bpy",
        "arm = bpy.data.objects.get('NAO_Armature')",
        "if arm:"
    ]
    
    for name, angle in joint_angles.items():
        axis = JOINT_AXIS_MAP.get(name)
        if not axis:
            continue
        code_lines.extend([
            "    bone = arm.pose.bones.get('{}')".format(name),
            "    if bone:",
            "        bone.rotation_mode = 'XYZ'",
            "        euler = list(bone.rotation_euler)",
            "        euler[{}] = {}".format('XYZ'.index(axis), angle),
            "        bone.rotation_euler = euler"
        ])
    code_lines.append("    bpy.context.view_layer.update()")
    return "\n".join(code_lines)

def poll_bridge_joints():
    """Queries the running Python 2.7 bridge for real-time joints."""
    try:
        response = urllib_request.urlopen(BRIDGE_URL, timeout=0.5)
        data = json.loads(response.read().decode('utf-8'))
        if "status" in data and data["status"] == "error":
            return None
        return data
    except Exception:
        return None

def generate_mock_telemetry(t):
    """Generates smooth, organic sine-wave joint values to simulate a live robot."""
    joints = {}
    
    # 1. Breathing motion (subtle shoulder pitch & roll shifts)
    breathing = math.sin(t * 2.0) * 0.03
    joints["LShoulderPitch"] = 1.4 + breathing
    joints["RShoulderPitch"] = 1.4 + breathing
    joints["LShoulderRoll"] = 0.1 + math.cos(t * 2.0) * 0.01
    joints["RShoulderRoll"] = -0.1 - math.cos(t * 2.0) * 0.01
    
    # 2. Scanning head motion (looking around slowly)
    joints["HeadYaw"] = math.sin(t * 0.5) * 0.4
    joints["HeadPitch"] = math.cos(t * 1.0) * 0.08
    
    # 3. Wave hand animation (L hand waving back and forth every few seconds)
    cycle = (t % 8.0)
    if cycle < 4.0:
        # High wave pose
        joints["LShoulderPitch"] = -0.8
        joints["LShoulderRoll"] = 0.4
        joints["LElbowYaw"] = -1.2
        # Wave bend
        joints["LElbowRoll"] = 0.6 + math.sin(t * 6.0) * 0.4
    else:
        # Normal standing arm pose
        joints["LShoulderPitch"] = 1.4
        joints["LShoulderRoll"] = 0.1
        joints["LElbowYaw"] = -0.8
        joints["LElbowRoll"] = -0.4
        
    # Symmetrical stand-by pose for limbs
    joints["RElbowYaw"] = 0.8
    joints["RElbowRoll"] = 0.4
    
    # Legs (slight standing flexion)
    joints["LHipPitch"] = -0.2
    joints["LKneePitch"] = 0.4
    joints["LAnklePitch"] = -0.2
    
    joints["RHipPitch"] = -0.2
    joints["RKneePitch"] = 0.4
    joints["RAnklePitch"] = -0.2
    
    return joints

def run_bridge():
    print("====================================================")
    print("        NAO ROBOT DIGITAL TWIN SYNC BRIDGE          ")
    print("====================================================")
    print("Connecting to Blender Server: {}:{}".format(BLENDER_HOST, BLENDER_PORT))
    print("Polling NAOqi Bridge API: {}".format(BRIDGE_URL))
    print("----------------------------------------------------")
    
    # Check if Blender server is online before beginning
    print("Checking Blender connection...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((BLENDER_HOST, BLENDER_PORT))
        print("Blender connection established successfully!")
        s.close()
    except Exception:
        print("WARNING: Cannot connect to Blender Server on port 9876.")
        print("Please start Blender and run 'blender_addon_server.py' first!")
        print("----------------------------------------------------")
        
    t_start = time.time()
    mode = "checking"
    
    try:
        while True:
            t = time.time() - t_start
            
            # 1. Attempt to get joints from the real bridge
            joints = poll_bridge_joints()
            
            if joints:
                if mode != "LIVE":
                    print("\n>>> NAOqi Telemetry detected! Running in LIVE SYNC MODE <<<")
                    mode = "LIVE"
                sys.stdout.write("\r[LIVE] Mirroring {} joints to Blender... (Elapsed: {}s)".format(len(joints), int(t)))
                sys.stdout.flush()
            else:
                if mode != "MOCK":
                    print("\n>>> NAOqi Bridge offline or resting. Running in MOCK DEMONSTRATION MODE <<<")
                    mode = "MOCK"
                joints = generate_mock_telemetry(t)
                sys.stdout.write("\r[MOCK] Dispatching sinusoidal path coordinates to Blender... (Elapsed: {}s)".format(int(t)))
                sys.stdout.flush()
                
            # 2. Build code block and send to Blender
            blender_code = generate_blender_rotation_code(joints)
            success = send_to_blender(blender_code)
            
            if not success and t % 5 < 0.1:
                # Print connection warning occasionally
                sys.stdout.write("\n[Warning] Failed to push data. Is 'blender_addon_server.py' running in Blender?\n")
                sys.stdout.flush()
                
            # 10Hz loop rate for fluid, real-time animation
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nDigital Twin Bridge terminated by user.")

if __name__ == "__main__":
    run_bridge()
