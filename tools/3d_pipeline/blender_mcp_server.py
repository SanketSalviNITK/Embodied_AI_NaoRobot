# -*- coding: utf-8 -*-
"""
Blender MCP Server (blender_mcp_server.py)
-----------------------------------------
Host-side Model Context Protocol (MCP) server built with FastMCP.
Exposes tools to interact with Blender on port 9876, allowing direct scene control,
spawning the rigged NAO Robot, and real-time joint rotations for digital twin behavior.
"""

import socket
import json
import os
import sys
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Blender Control Server")

BLENDER_HOST = "127.0.0.1"
BLENDER_PORT = 9876

# Joint Axis Mapping for NAO Robot
# Maps NAO joint names to their active rotation axis in Blender
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
    "LFoot": "Y",
    
    # Right Leg
    "RHipYawPitch": "Z",
    "RHipRoll": "X",
    "RHipPitch": "Y",
    "RKneePitch": "Y",
    "RAnklePitch": "Y",
    "RAnkleRoll": "X",
    "RFoot": "Y",
}

def send_code_to_blender(code_str: str) -> dict:
    """Connects to Blender on port 9876, sends python code, and returns the response dict."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((BLENDER_HOST, BLENDER_PORT))
        s.sendall(code_str.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        
        # Read response
        response_chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_chunks.append(chunk.decode('utf-8'))
            
        s.close()
        
        response_str = "".join(response_chunks)
        if not response_str.strip():
            return {"success": False, "stdout": "", "stderr": "No response received from Blender addon server."}
            
        return json.loads(response_str)
    except ConnectionRefusedError:
        return {
            "success": False, 
            "stdout": "", 
            "stderr": "CRITICAL: Connection refused! Is the Blender Add-on Server running on port 9876 inside Blender?"
        }
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": f"Error communicating with Blender: {str(e)}"}

@mcp.tool()
def execute_blender_script(code: str) -> str:
    """
    Executes raw Python code in the running Blender session.
    Has full access to the Blender python API ('bpy').
    
    Args:
        code: A string of Python code to execute.
    """
    res = send_code_to_blender(code)
    if res["success"]:
        return f"SUCCESS:\nStdout:\n{res['stdout']}\nStderr:\n{res['stderr']}"
    else:
        return f"FAILED:\nStdout:\n{res['stdout']}\nStderr:\n{res['stderr']}"

@mcp.tool()
def build_nao_robot() -> str:
    """
    Programmatically builds and rigs the 3D NAO Robot model inside Blender.
    Clears any existing NAO models first to enable clean re-runs.
    """
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_nao_model.py")
    if not os.path.exists(script_path):
        return f"Error: Cannot find build_nao_model.py at {script_path}."
        
    try:
        with open(script_path, 'r') as f:
            builder_code = f.read()
            
        # Append active call
        builder_code += "\n\nbuild_nao_robot()\n"
        
        res = send_code_to_blender(builder_code)
        if res["success"]:
            return "SUCCESS: Rigged NAO Robot model created in active Blender scene!"
        else:
            return f"FAILED: Error creating model.\nStdout: {res['stdout']}\nStderr: {res['stderr']}"
    except Exception as e:
        return f"Error reading builder script: {str(e)}"

@mcp.tool()
def update_joint_angles(joints: str) -> str:
    """
    Updates the joint rotation angles (in radians) of the rigged NAO model in Blender.
    
    Args:
        joints: A JSON-formatted string mapping joint names to target angles.
                Example: '{"HeadYaw": 0.5, "LShoulderRoll": -0.2}'
    """
    try:
        joint_data = json.loads(joints)
    except Exception as e:
        return f"Error: Invalid JSON format for joints: {str(e)}"
        
    # Build python code block to rotate bones in Blender
    code_lines = [
        "import bpy",
        "import math",
        "arm = bpy.data.objects.get('NAO_Armature')",
        "if arm:",
        "    bpy.context.view_layer.objects.active = arm"
    ]
    
    for joint_name, angle in joint_data.items():
        axis = JOINT_AXIS_MAP.get(joint_name)
        if not axis:
            continue
            
        # Normalize angle float
        try:
            angle_val = float(angle)
        except:
            continue
            
        # Create rotation script for this bone
        code_lines.extend([
            f"    bone = arm.pose.bones.get('{joint_name}')",
            "    if bone:",
            "        bone.rotation_mode = 'XYZ'",
            "        euler = list(bone.rotation_euler)",
            f"        euler[{'XYZ'.index(axis)}] = {angle_val}",
            "        bone.rotation_euler = euler"
        ])
        
    code_lines.append("    bpy.context.view_layer.update()")
    code_lines.append("    print('[MCP Server] Successfully updated joint rotations.')")
    
    full_code = "\n".join(code_lines)
    res = send_code_to_blender(full_code)
    
    if res["success"]:
        return f"SUCCESS: Rotated {len(joint_data)} joints in Blender."
    else:
        return f"FAILED:\n{res['stderr']}"

@mcp.tool()
def get_scene_status() -> str:
    """
    Queries Blender for the status of the scene, object count, and NAO Armature state.
    """
    query_code = """
import bpy
print("=== Blender Scene Status ===")
print("File name:", bpy.data.filepath or "Untitled")
print("Total objects in scene:", len(bpy.data.objects))
print("Objects list:", [obj.name for obj in bpy.data.objects])
arm = bpy.data.objects.get("NAO_Armature")
if arm:
    print("NAO_Armature Detected: YES")
    print("Total bones:", len(arm.pose.bones))
    print("Active Pose Angles:")
    for bone in arm.pose.bones:
        if bone.rotation_euler.length > 0.001:
            print(f"  {bone.name}: rx={bone.rotation_euler.x:.3f}, ry={bone.rotation_euler.y:.3f}, rz={bone.rotation_euler.z:.3f}")
else:
    print("NAO_Armature Detected: NO")
"""
    res = send_code_to_blender(query_code)
    if res["success"]:
        return res["stdout"]
    else:
        return f"FAILED to query scene: {res['stderr']}"

if __name__ == "__main__":
    # Start FastMCP server
    print("Starting Blender MCP Server via stdio...")
    mcp.run()
