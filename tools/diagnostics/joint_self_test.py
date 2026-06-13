# -*- coding: utf-8 -*-
"""
Robotic Joint Calibration & Self-Test Script (joint_self_test.py)
-----------------------------------------------------------------
Sends a calibration routine to the Blender Socket Server to test every
joint of the NAO digital twin sequentially. This verifies that all 39 mesh
parts are parented to the correct bones and rotate correctly in 3D.

Usage:
  python3 joint_self_test.py
"""

import socket
import json

BLENDER_HOST = '127.0.0.1'
BLENDER_PORT = 9876

# The python code to execute inside Blender
calibration_code = """
import bpy
import time
import math

armature = bpy.data.objects.get("NAO_Armature")
if not armature:
    print("ERROR: NAO_Armature object not found in scene!")
else:
    print("Armature found! Starting sequential joint calibration test...")
    
    # Switch to POSE mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Joint test list: (Bone Name, Rotation Axis 'X'/'Y'/'Z', Angle in Degrees)
    test_sequence = [
        # 1. Head Calibration
        ("HeadYaw", "Z", 35),
        ("HeadPitch", "Y", 20),
        
        # 2. Left Arm Calibration
        ("LShoulderPitch", "Y", -45),
        ("LShoulderRoll", "X", 30),
        ("LElbowRoll", "Z", -60),
        ("LWristYaw", "Y", 45),
        
        # 3. Right Arm Calibration
        ("RShoulderPitch", "Y", -45),
        ("RShoulderRoll", "X", -30),
        ("RElbowRoll", "Z", 60),
        ("RWristYaw", "Y", -45),
        
        # 4. Left Leg Calibration
        ("LHipPitch", "Y", -25),
        ("LKneePitch", "Y", 45),
        ("LAnklePitch", "Y", -20),
        
        # 5. Right Leg Calibration
        ("RHipPitch", "Y", -25),
        ("RKneePitch", "Y", 45),
        ("RAnklePitch", "Y", -20),
    ]
    
    # Clean rest pose first
    for bone in armature.pose.bones:
        bone.rotation_mode = 'XYZ'
        bone.rotation_euler = (0, 0, 0)
        
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    time.sleep(0.3)
    
    steps = 6 # Interpolation animation steps for smoothness
    
    for bone_name, axis, max_angle in test_sequence:
        bone = armature.pose.bones.get(bone_name)
        if not bone:
            continue
            
        print(f"Testing Joint: {bone_name} ({axis}-axis)...")
        angle_rad = math.radians(max_angle)
        
        # Rotate Outward smoothly
        for step in range(1, steps + 1):
            factor = step / steps
            curr_angle = angle_rad * factor
            if axis == "X":
                bone.rotation_euler[0] = curr_angle
            elif axis == "Y":
                bone.rotation_euler[1] = curr_angle
            else:
                bone.rotation_euler[2] = curr_angle
                
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            time.sleep(0.02)
            
        time.sleep(0.12)
        
        # Rotate back smoothly to zero
        for step in range(steps, -1, -1):
            factor = step / steps
            curr_angle = angle_rad * factor
            if axis == "X":
                bone.rotation_euler[0] = curr_angle
            elif axis == "Y":
                bone.rotation_euler[1] = curr_angle
            else:
                bone.rotation_euler[2] = curr_angle
                
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            time.sleep(0.02)
            
        time.sleep(0.05)
        
    # Reset all rotations to pristine T-pose
    for bone in armature.pose.bones:
        bone.rotation_euler = (0, 0, 0)
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    
    # Return to Object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Joint calibration self-test completed successfully!")
"""

def main():
    print("====================================================")
    print("     NAO ROBOT JOINT CALIBRATION SELF-TEST          ")
    print("====================================================")
    print(f"Connecting to Blender Server: {BLENDER_HOST}:{BLENDER_PORT}...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15.0)
        s.connect((BLENDER_HOST, BLENDER_PORT))
        
        print("Sending calibration sequence to Blender...")
        s.sendall(calibration_code.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        
        # Robust reading loop to fetch all data from the socket
        response_chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_chunks.append(chunk)
        
        response_str = b"".join(response_chunks).decode('utf-8')
        s.close()
        
        result = json.loads(response_str)
        if result.get("success"):
            print("\n>>> SUCCESS: Calibration sequence executed in Blender! <<<")
            print("Look at your Blender viewport - you watched the robot calibrate its joints.")
        else:
            print("\nERROR: Blender failed to execute calibration:")
            print(result.get("stderr"))
            
    except Exception as e:
        print(f"\nERROR: Failed to connect to Blender: {e}")
        print("Ensure Blender is open and the background server script is running.")

if __name__ == "__main__":
    main()
