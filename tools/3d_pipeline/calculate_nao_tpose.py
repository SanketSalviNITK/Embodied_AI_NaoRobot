# -*- coding: utf-8 -*-
"""
NAO Kinematic T-Pose Coordinate Calculator (calculate_nao_tpose.py)
-------------------------------------------------------------------
Downloads the official PyBullet nao.urdf, builds the kinematic tree,
and computes the exact absolute world coordinates (xyz) and orientations
for all 39 mesh parts in their T-pose configuration.
"""

import urllib.request as urllib_request
import xml.etree.ElementTree as ET
import numpy as np
import os

URDF_URL = "https://raw.githubusercontent.com/bulletphysics/bullet3/master/data/humanoid/nao.urdf"
LOCAL_URDF = "nao.urdf"

# Simple 4x4 matrix math utilities for coordinate transformation
def translation_matrix(v):
    M = np.identity(4)
    M[:3, 3] = v
    return M

def euler_matrix(ai, aj, ak):
    """Returns 4x4 rotation matrix from euler angles (roll, pitch, yaw)."""
    s_i, c_i = np.sin(ai), np.cos(ai)
    s_j, c_j = np.sin(aj), np.cos(aj)
    s_k, c_k = np.sin(ak), np.cos(ak)
    
    R = np.identity(4)
    R[0, 0] = c_j * c_k
    R[0, 1] = -c_j * s_k
    R[0, 2] = s_j
    
    R[1, 0] = c_i * s_k + s_i * s_j * c_k
    R[1, 1] = c_i * c_k - s_i * s_j * s_k
    R[1, 2] = -s_i * c_j
    
    R[2, 0] = s_i * s_k - c_i * s_j * c_k
    R[2, 1] = s_i * c_k + c_i * s_j * s_k
    R[2, 2] = c_i * c_j
    return R

def main():
    print("Downloading nao.urdf for kinematic compilation...")
    try:
        req = urllib_request.Request(URDF_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib_request.urlopen(req)
        with open(LOCAL_URDF, 'wb') as f:
            f.write(response.read())
    except Exception as e:
        print(f"Failed to download URDF: {e}")
        return

    # Parse XML URDF
    tree = ET.parse(LOCAL_URDF)
    root = tree.getroot()

    # Build standard structures
    links = {}
    for link in root.findall('link'):
        name = link.get('name')
        visual = link.find('visual')
        mesh_file = "none"
        v_xyz = np.zeros(3)
        v_rpy = np.zeros(3)
        
        if visual is not None:
            origin = visual.find('origin')
            if origin is not None:
                if origin.get('xyz'):
                    v_xyz = np.array([float(x) for x in origin.get('xyz').split()])
                if origin.get('rpy'):
                    v_rpy = np.array([float(r) for r in origin.get('rpy').split()])
            
            geometry = visual.find('geometry')
            if geometry is not None:
                mesh = geometry.find('mesh')
                if mesh is not None:
                    mesh_file = os.path.basename(mesh.get('filename'))
                    
        links[name] = {
            "mesh": mesh_file,
            "v_xyz": v_xyz,
            "v_rpy": v_rpy,
            "child_joints": []
        }

    # Parse joints to establish parent-child relationships
    joints = {}
    for joint in root.findall('joint'):
        name = joint.get('name')
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')
        
        origin = joint.find('origin')
        xyz = np.array([float(x) for x in origin.get('xyz').split()]) if origin is not None and origin.get('xyz') else np.zeros(3)
        rpy = np.array([float(r) for r in origin.get('rpy').split()]) if origin is not None and origin.get('rpy') else np.zeros(3)
        
        joints[child] = {
            "name": name,
            "parent": parent,
            "xyz": xyz,
            "rpy": rpy
        }
        
        if parent in links:
            links[parent]["child_joints"].append(child)

    # Compute absolute world transforms via recursive depth-first traversal
    world_transforms = {}
    
    def traverse(link_name, parent_transform):
        # 1. Calculate joint transform
        joint_transform = parent_transform
        if link_name in joints:
            j = joints[link_name]
            T_joint = translation_matrix(j["xyz"])
            R_joint = euler_matrix(j["rpy"][0], j["rpy"][1], j["rpy"][2])
            joint_transform = parent_transform @ T_joint @ R_joint
            
        # 2. Calculate visual mesh transform
        v_xyz = links[link_name]["v_xyz"]
        v_rpy = links[link_name]["v_rpy"]
        T_visual = translation_matrix(v_xyz)
        R_visual = euler_matrix(v_rpy[0], v_rpy[1], v_rpy[2])
        mesh_transform = joint_transform @ T_visual @ R_visual
        
        world_transforms[link_name] = mesh_transform
        
        # 3. Recurse to children
        for child_link in links[link_name]["child_joints"]:
            traverse(child_link, joint_transform)

    # Begin traversal from base_link root
    traverse("base_link", np.identity(4))

    print("\n" + "="*70)
    print(f"{'Link Name':<20} | {'Associated Mesh File':<25} | {'World XYZ Coordinates':<22}")
    print("="*70)
    
    # Filter and display coordinate mapping for active meshes
    coordinate_mapping = {}
    for link_name, transform in sorted(world_transforms.items()):
        mesh_file = links[link_name]["mesh"]
        if mesh_file != "none" and mesh_file.endswith(".stl"):
            # Extract world translation xyz
            world_xyz = transform[:3, 3]
            coordinate_mapping[mesh_file] = world_xyz
            print(f"{link_name:<20} | {mesh_file:<25} | {list(np.round(world_xyz, 4))}")
            
    print("="*70 + "\n")
    
    # Clean up local URDF
    try:
        os.remove(LOCAL_URDF)
    except:
        pass

if __name__ == "__main__":
    main()
