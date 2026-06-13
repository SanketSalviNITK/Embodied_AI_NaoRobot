# -*- coding: utf-8 -*-
"""
NAO URDF Link & Visual Parser (parse_nao_urdf.py)
-----------------------------------------------
Downloads and parses the official PyBullet nao.urdf to extract the exact
visual origins (xyz, rpy) and joint definitions to build a 100% physically
accurate 3D model.

Usage:
  python3 parse_nao_urdf.py
"""

import urllib.request as urllib_request
import xml.etree.ElementTree as ET
import os

URDF_URL = "https://raw.githubusercontent.com/bulletphysics/bullet3/master/data/humanoid/nao.urdf"
LOCAL_URDF = "nao.urdf"

def main():
    print("====================================================")
    print("           NAO URDF GEOMETRY OFFSET PARSER          ")
    print("====================================================")
    print("Downloading nao.urdf from Bullet Physics...")
    
    try:
        req = urllib_request.Request(
            URDF_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response = urllib_request.urlopen(req)
        with open(LOCAL_URDF, 'wb') as f:
            f.write(response.read())
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download URDF: {e}")
        return

    # Parse URDF
    tree = ET.parse(LOCAL_URDF)
    root = tree.getroot()
    
    print("\n--- Visual Mesh Offsets in URDF ---")
    
    # Store joint information
    joints = {}
    for joint in root.findall('joint'):
        name = joint.get('name')
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')
        origin = joint.find('origin')
        xyz = [float(x) for x in origin.get('xyz').split()] if origin is not None and origin.get('xyz') else [0.0, 0.0, 0.0]
        rpy = [float(r) for r in origin.get('rpy').split()] if origin is not None and origin.get('rpy') else [0.0, 0.0, 0.0]
        joints[child] = {
            "name": name,
            "parent": parent,
            "xyz": xyz,
            "rpy": rpy
        }

    # Parse visual link offsets
    for link in root.findall('link'):
        link_name = link.get('name')
        visual = link.find('visual')
        if visual is not None:
            origin = visual.find('origin')
            xyz = origin.get('xyz') if origin is not None else "0 0 0"
            rpy = origin.get('rpy') if origin is not None else "0 0 0"
            
            geometry = visual.find('geometry')
            mesh = geometry.find('mesh')
            mesh_file = os.path.basename(mesh.get('filename')) if mesh is not None else "none"
            
            print(f"Link: {link_name:<20}")
            print(f"  Mesh:   {mesh_file:<35}")
            print(f"  Origin: xyz='{xyz}' rpy='{rpy}'")
            
            # Show parent joint offset if exists
            if link_name in joints:
                j = joints[link_name]
                print(f"  Joint:  {j['name']:<20} xyz='{j['xyz']}' rpy='{j['rpy']}'")
            print()
            
    # Clean up local URDF file
    try:
        os.remove(LOCAL_URDF)
    except:
        pass

if __name__ == "__main__":
    main()
