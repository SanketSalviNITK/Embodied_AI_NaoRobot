# -*- coding: utf-8 -*-
"""
Spawns the 3D Rigged NAO Robot in Blender (spawn_nao.py)
--------------------------------------------------------
Run this script from your terminal to instantly build, paint, and rig the NAO robot
inside your active Blender GUI session!

Usage:
  python3 spawn_nao.py
"""

import socket
import json
import os
import sys

BLENDER_HOST = '127.0.0.1'
BLENDER_PORT = 9876

def main():
    print("====================================================")
    print("            NAO ROBOT 3D MODEL SPAWNER              ")
    print("====================================================")
    print(f"Connecting to Blender Server: {BLENDER_HOST}:{BLENDER_PORT}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_script = os.path.join(script_dir, "build_nao_model.py")
    
    if not os.path.exists(model_script):
        print(f"ERROR: Cannot find model script: {model_script}")
        sys.exit(1)
        
    print("Reading 3D model geometry definitions...")
    with open(model_script, 'r') as f:
        code = f.read()
        
    # Append the active trigger command
    code += "\n\nbuild_nao_robot()\n"
    
    print("Sending build instructions to Blender...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect((BLENDER_HOST, BLENDER_PORT))
        s.sendall(code.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        
        # Read build response
        response_data = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_data.append(chunk.decode('utf-8'))
        s.close()
        
        result_str = "".join(response_data)
        if not result_str.strip():
            print("WARNING: Empty response from Blender.")
            return
            
        result = json.loads(result_str)
        if result.get("success"):
            print("\n>>> SUCCESS: Fully rigged 3D NAO robot spawned in Blender! <<<")
            print("Check your Blender viewport - you will see the white, silver, and cyan robot.")
        else:
            print("\nERROR: Blender failed to execute model builder:")
            print(result.get("stderr"))
            
    except ConnectionRefusedError:
        print("\nERROR: Connection refused!")
        print("Is Blender open? Did you paste and run 'blender_addon_server.py' in Blender?")
    except Exception as e:
        print(f"\nERROR: Unexpected connection issue: {str(e)}")

if __name__ == "__main__":
    main()
