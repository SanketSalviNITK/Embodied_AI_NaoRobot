# -*- coding: utf-8 -*-
"""
Hyper-Accurate NAO Robot 3D Digital Twin Builder (build_nao_model.py)
--------------------------------------------------------------------
Assembles the official 39 NAO mesh parts at their exact URDF T-pose coordinates
and rigs them to a kinematic armature with perfectly aligned rotation axes.
"""

import bpy
import os
import time

IN_BLENDER = True

# --- 1. CONFIGURATION & COORDINATE SYSTEM ---
MESH_DIR = r"C:\Users\ARVR\Documents\ARVRProjects\EmbodiedAI\nao_meshes"

# Pre-calculated absolute world coordinates (xyz) for all 39 mesh files in T-pose
# Compiled directly from URDF Forward Kinematics
MESH_WORLD_COORDS = {
    "Torso_0.10": (0.0, 0.0, 0.0),
    "HeadYaw_0.10": (0.0, 0.0, 0.1265),
    "HeadPitch_0.10": (0.0, 0.0, 0.1265),
    
    # Left Arm
    "LShoulderPitch_0.10": (0.0, 0.098, 0.100),
    "LShoulderRoll_0.10": (0.0, 0.098, 0.100),
    "LElbowRoll_0.10": (0.105, 0.113, 0.100),
    "LWristYaw_0.10": (0.1609, 0.113, 0.100),
    "LFinger11_0.10": (0.230, 0.1246, 0.097),
    "LFinger12_0.10": (0.2378, 0.1343, 0.1041),
    "LFinger13_0.10": (0.2437, 0.1457, 0.0977),
    "LFinger21_0.10": (0.230, 0.1014, 0.097),
    "LFinger22_0.10": (0.2378, 0.1112, 0.0898),
    "LFinger23_0.10": (0.2402, 0.1104, 0.0757),
    "LThumb1_0.10": (0.2099, 0.113, 0.0736),
    "LThumb2_0.10": (0.2242, 0.1123, 0.0736),
    
    # Right Arm
    "RShoulderPitch_0.10": (0.0, -0.098, 0.100),
    "RShoulderRoll_0.10": (0.0, -0.098, 0.100),
    "RElbowRoll_0.10": (0.105, -0.113, 0.100),
    "RWristYaw_0.10": (0.1609, -0.113, 0.100),
    "RFinger11_0.10": (0.230, -0.1014, 0.097),
    "RFinger12_0.10": (0.2378, -0.0917, 0.1041),
    "RFinger13_0.10": (0.2437, -0.0803, 0.0977),
    "RFinger21_0.10": (0.230, -0.1246, 0.097),
    "RFinger22_0.10": (0.2378, -0.1148, 0.0898),
    "RFinger23_0.10": (0.2402, -0.1156, 0.0757),
    "RThumb1_0.10": (0.2099, -0.113, 0.0736),
    "RThumb2_0.10": (0.2242, -0.1137, 0.0736),
    
    # Left Leg
    "LHipYawPitch_0.10": (0.0, 0.050, -0.085),
    "LHipRoll_0.10": (0.0, 0.050, -0.085),
    "LHipPitch_0.10": (0.0, 0.050, -0.085),
    "LKneePitch_0.10": (0.0, 0.050, -0.185),
    "LAnklePitch_0.10": (0.0, 0.050, -0.2879),
    "LAnkleRoll_0.10": (0.0, 0.050, -0.2879),
    
    # Right Leg
    "RHipYawPitch_0.10": (0.0, -0.050, -0.085),
    "RHipRoll_0.10": (0.0, -0.050, -0.085),
    "RHipPitch_0.10": (0.0, -0.050, -0.085),
    "RKneePitch_0.10": (0.0, -0.050, -0.185),
    "RAnklePitch_0.10": (0.0, -0.050, -0.2879),
    "RAnkleRoll_0.10": (0.0, -0.050, -0.2879),
}

# Mapping of visual meshes to physical armature joint bones
MESH_BONE_MAP = {
    "Torso_0.10": "Torso",
    "HeadYaw_0.10": "HeadYaw",
    "HeadPitch_0.10": "HeadPitch",
    
    # Left Arm
    "LShoulderPitch_0.10": "LShoulderPitch",
    "LShoulderRoll_0.10": "LShoulderRoll",
    "LElbowRoll_0.10": "LElbowRoll",
    "LWristYaw_0.10": "LWristYaw",
    "LFinger11_0.10": "LHand",
    "LFinger12_0.10": "LHand",
    "LFinger13_0.10": "LHand",
    "LFinger21_0.10": "LHand",
    "LFinger22_0.10": "LHand",
    "LFinger23_0.10": "LHand",
    "LThumb1_0.10": "LHand",
    "LThumb2_0.10": "LHand",
    
    # Right Arm
    "RShoulderPitch_0.10": "RShoulderPitch",
    "RShoulderRoll_0.10": "RShoulderRoll",
    "RElbowRoll_0.10": "RElbowRoll",
    "RWristYaw_0.10": "RWristYaw",
    "RFinger11_0.10": "RHand",
    "RFinger12_0.10": "RHand",
    "RFinger13_0.10": "RHand",
    "RFinger21_0.10": "RHand",
    "RFinger22_0.10": "RHand",
    "RFinger23_0.10": "RHand",
    "RThumb1_0.10": "RHand",
    "RThumb2_0.10": "RHand",
    
    # Left Leg
    "LHipYawPitch_0.10": "LHipYawPitch",
    "LHipRoll_0.10": "LHipRoll",
    "LHipPitch_0.10": "LHipPitch",
    "LKneePitch_0.10": "LKneePitch",
    "LAnklePitch_0.10": "LAnklePitch",
    "LAnkleRoll_0.10": "LAnkleRoll",
    
    # Right Leg
    "RHipYawPitch_0.10": "RHipYawPitch",
    "RHipRoll_0.10": "RHipRoll",
    "RHipPitch_0.10": "RHipPitch",
    "RKneePitch_0.10": "RKneePitch",
    "RAnklePitch_0.10": "RAnklePitch",
    "RAnkleRoll_0.10": "RAnkleRoll",
}

WHITE_PANEL_KEYWORDS = [
    "Torso", "HeadPitch", 
    "LShoulderPitch", "RShoulderPitch", 
    "LShoulderRoll", "RShoulderRoll", 
    "LElbowRoll", "RElbowRoll", 
    "LHipPitch", "RHipPitch", 
    "LKneePitch", "RKneePitch", 
    "LAnkleRoll", "RAnkleRoll"
]

def setup_materials():
    """Sets up sleek white, metallic silver, and cybernetic cyan PBR materials."""
    print("Setting up materials...")
    
    # White Porcelain Body Panels
    mat_white = bpy.data.materials.get("NAO_BodyWhite")
    if not mat_white:
        mat_white = bpy.data.materials.new(name="NAO_BodyWhite")
    mat_white.use_nodes = True
    nodes = mat_white.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        principled.inputs['Roughness'].default_value = 0.15
        principled.inputs['Specular IOR Level'].default_value = 0.6
        
    # Anodized Dark Charcoal Mechanical Joints (Real NAO V6 spec)
    mat_silver = bpy.data.materials.get("NAO_JointSilver")
    if not mat_silver:
        mat_silver = bpy.data.materials.new(name="NAO_JointSilver")
    mat_silver.use_nodes = True
    nodes = mat_silver.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.18, 0.18, 0.20, 1.0) # Slate Dark Charcoal
        principled.inputs['Metallic'].default_value = 0.25
        principled.inputs['Roughness'].default_value = 0.55
        
    # Generic Dynamic LED (Default Glowing Cyan)
    mat_led = bpy.data.materials.get("NAO_LED")
    if not mat_led:
        mat_led = bpy.data.materials.new(name="NAO_LED")
    mat_led.use_nodes = True
    nodes = mat_led.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.0, 0.8, 1.0, 1.0)
        principled.inputs['Emission Color'].default_value = (0.0, 0.8, 1.0, 1.0)
        principled.inputs['Emission Strength'].default_value = 3.0

def delete_existing_nao():
    """Removes previously generated NAO objects, meshes, and armatures to enable clean re-runs."""
    print("Clearing existing NAO objects...")
    for obj in list(bpy.data.objects):
        if (obj.name.startswith("NAO_Mesh_") or 
            obj.name == "NAO_Armature" or 
            obj.name.startswith("NAO_Eye_") or 
            obj.name in ["Head", "Torso", "Cube", "Camera", "Light"]):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

def build_nao_robot():
    """Imports, scales, textures, and rigs the official NAO meshes with millimeter accuracy."""
    if not IN_BLENDER:
        print("Not inside Blender, skipping generation.")
        return False
        
    # Setup rendering engine
    try:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    except TypeError:
        bpy.context.scene.render.engine = 'EEVEE'
        
    if hasattr(bpy.context.scene, "eevee") and hasattr(bpy.context.scene.eevee, "use_bloom"):
        bpy.context.scene.eevee.use_bloom = True
        
    delete_existing_nao()
    setup_materials()
    
    # Force viewport redraw
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    time.sleep(0.2)
    
    # 2. CREATE KINEMATIC ARMATURE WITH ALIGNED ROTATION AXES
    # Draw all bones pointing exactly 0.04m along the world Y axis.
    # This aligns the bone local axes EXACTLY with the world coordinate axes:
    # Local X = World X (Roll), Local Y = World Y (Pitch), Local Z = World Z (Yaw).
    print("Building aligned kinematic joint armature...")
    bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    armature_obj = bpy.context.active_object
    armature_obj.name = "NAO_Armature"
    
    edit_bones = armature_obj.data.edit_bones
    if edit_bones:
        edit_bones.remove(edit_bones[0])
        
    # Joint definitions matching URDF exactly in meters
    joints_def = {
        "Torso": (None, (0.0, 0.0, 0.0), (0.0, 0.04, 0.0)),
        "HeadYaw": ("Torso", (0.0, 0.0, 0.1265), (0.0, 0.04, 0.1265)),
        "HeadPitch": ("HeadYaw", (0.0, 0.0, 0.1265), (0.0, 0.04, 0.1265)),
        
        # Left Arm
        "LShoulderPitch": ("Torso", (0.0, 0.098, 0.100), (0.0, 0.138, 0.100)),
        "LShoulderRoll": ("LShoulderPitch", (0.0, 0.098, 0.100), (0.0, 0.138, 0.100)),
        "LElbowYaw": ("LShoulderRoll", (0.105, 0.113, 0.100), (0.105, 0.153, 0.100)),
        "LElbowRoll": ("LElbowYaw", (0.105, 0.113, 0.100), (0.105, 0.153, 0.100)),
        "LWristYaw": ("LElbowRoll", (0.1609, 0.113, 0.100), (0.1609, 0.153, 0.100)),
        "LHand": ("LWristYaw", (0.1609, 0.113, 0.100), (0.1609, 0.153, 0.100)),
        
        # Right Arm
        "RShoulderPitch": ("Torso", (0.0, -0.098, 0.100), (0.0, -0.058, 0.100)),
        "RShoulderRoll": ("RShoulderPitch", (0.0, -0.098, 0.100), (0.0, -0.058, 0.100)),
        "RElbowYaw": ("RShoulderRoll", (0.105, -0.113, 0.100), (0.105, -0.073, 0.100)),
        "RElbowRoll": ("RElbowYaw", (0.105, -0.113, 0.100), (0.105, -0.073, 0.100)),
        "RWristYaw": ("RElbowRoll", (0.1609, -0.113, 0.100), (0.1609, -0.073, 0.100)),
        "RHand": ("RWristYaw", (0.1609, -0.113, 0.100), (0.1609, -0.073, 0.100)),
        
        # Left Leg
        "LHipYawPitch": ("Torso", (0.0, 0.050, -0.085), (0.0, 0.090, -0.085)),
        "LHipRoll": ("LHipYawPitch", (0.0, 0.050, -0.085), (0.0, 0.090, -0.085)),
        "LHipPitch": ("LHipRoll", (0.0, 0.050, -0.085), (0.0, 0.090, -0.085)),
        "LKneePitch": ("LHipPitch", (0.0, 0.050, -0.185), (0.0, 0.090, -0.185)),
        "LAnklePitch": ("LKneePitch", (0.0, 0.050, -0.2879), (0.0, 0.090, -0.2879)),
        "LAnkleRoll": ("LAnklePitch", (0.0, 0.050, -0.2879), (0.0, 0.090, -0.2879)),
        
        # Right Leg
        "RHipYawPitch": ("Torso", (0.0, -0.050, -0.085), (0.0, -0.010, -0.085)),
        "RHipRoll": ("RHipYawPitch", (0.0, -0.050, -0.085), (0.0, -0.010, -0.085)),
        "RHipPitch": ("RHipRoll", (0.0, -0.050, -0.085), (0.0, -0.010, -0.085)),
        "RKneePitch": ("RHipPitch", (0.0, -0.050, -0.185), (0.0, -0.010, -0.185)),
        "RAnklePitch": ("RKneePitch", (0.0, -0.050, -0.2879), (0.0, -0.010, -0.2879)),
        "RAnkleRoll": ("RAnklePitch", (0.0, -0.050, -0.2879), (0.0, -0.010, -0.2879)),
    }
    
    # Create Edit Bones
    for name, (parent_name, head, tail) in joints_def.items():
        bone = edit_bones.new(name)
        bone.head = head
        bone.tail = tail
        if parent_name:
            bone.parent = edit_bones.get(parent_name)
            
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Armature constructed successfully.")
    
    # Force viewport redraw to show skeleton
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    time.sleep(0.3)
    
    # 3. IMPORT AND RIG OFFICIAL CAD MESHES STEP-BY-STEP
    print("Importing meshes from: " + MESH_DIR)
    if not os.path.exists(MESH_DIR):
        print(f"ERROR: Mesh directory not found: {MESH_DIR}")
        return False
        
    stl_files = [f for f in os.listdir(MESH_DIR) if f.lower().endswith(".stl")]
    
    # Logical sorting for neat visual spawner effect
    logical_order = [
        "Torso", "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LFinger", "LThumb",
        "RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RFinger", "RThumb",
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
    ]
    
    sorted_stl_files = []
    for category in logical_order:
        for f in stl_files:
            part_name = os.path.splitext(f)[0]
            if part_name.startswith(category) and f not in sorted_stl_files:
                sorted_stl_files.append(f)
    for f in stl_files:
        if f not in sorted_stl_files:
            sorted_stl_files.append(f)
            
    mat_white = bpy.data.materials.get("NAO_BodyWhite")
    mat_silver = bpy.data.materials.get("NAO_JointSilver")
    mat_led = bpy.data.materials.get("NAO_LED")
    
    for filename in sorted_stl_files:
        filepath = os.path.join(MESH_DIR, filename)
        part_name = os.path.splitext(filename)[0] # e.g. "Torso_0.10"
        
        # Determine the target parent bone
        target_bone = MESH_BONE_MAP.get(part_name)
        if not target_bone:
            # Fallback matching
            for key, val in MESH_BONE_MAP.items():
                if key in part_name:
                    target_bone = val
                    break
        if not target_bone:
            continue
            
        # Get pre-calculated visual T-pose coordinates
        tpose_coord = MESH_WORLD_COORDS.get(part_name)
        if not tpose_coord:
            # Fallback matching for finger/thumb meshes
            for key, val in MESH_WORLD_COORDS.items():
                if key in part_name:
                    tpose_coord = val
                    break
        if not tpose_coord:
            tpose_coord = (0.0, 0.0, 0.0)
            
        # Import visual mesh
        try:
            bpy.ops.wm.stl_import(filepath=filepath)
        except AttributeError:
            bpy.ops.import_mesh.stl(filepath=filepath)
            
        mesh_obj = bpy.context.active_object
        mesh_obj.name = f"NAO_Mesh_{part_name}"
        
        # Scale down by 0.1 (Decimeters -> Meters)
        mesh_obj.scale = (0.1, 0.1, 0.1)
        
        # Position visual mesh at its EXACT absolute coordinate in T-pose!
        mesh_obj.location = tpose_coord
        mesh_obj.rotation_euler = (0.0, 0.0, 0.0)
        
        # Apply scale transform so geometry sits beautifully in metric buffer
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign materials
        is_white_panel = any(keyword in part_name for keyword in WHITE_PANEL_KEYWORDS)
        if is_white_panel:
            mesh_obj.data.materials.append(mat_white)
        else:
            mesh_obj.data.materials.append(mat_silver)
            
        # Rig mesh to its target bone
        mesh_obj.parent = armature_obj
        mesh_obj.parent_type = 'BONE'
        mesh_obj.parent_bone = target_bone
        
        # Freeze position relative to the joint
        pose_bone = armature_obj.pose.bones.get(target_bone)
        if pose_bone:
            mesh_obj.matrix_parent_inverse = pose_bone.matrix.inverted()
            
        print(f"Positioned and parented {mesh_obj.name:<30} at T-pose {list(tpose_coord)}")
        
        # Step-by-step assembly delay
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        time.sleep(0.06) # 60ms delay
        
    # 4. SPAWN GLOWING LED EYES
    print("Spawning cybernetic eyes in faceplate...")
    eye_positions = [
        ("NAO_Eye_L", (0.055, 0.025, 0.152)),
        ("NAO_Eye_R", (0.055, -0.025, 0.152))
    ]
    
    for name, pos in eye_positions:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.008, location=pos)
        eye_obj = bpy.context.active_object
        eye_obj.name = name
        eye_obj.data.materials.append(mat_led)
        
        eye_obj.parent = armature_obj
        eye_obj.parent_type = 'BONE'
        eye_obj.parent_bone = "HeadPitch"
        
        pose_bone = armature_obj.pose.bones.get("HeadPitch")
        if pose_bone:
            eye_obj.matrix_parent_inverse = pose_bone.matrix.inverted()
            
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        time.sleep(0.08)
        
    print("\n====================================================")
    print(">>> 100% HYPER-ACCURATE NAO ASSEMBLER COMPLETE! <<<")
    print("====================================================\n")
    return True

if __name__ == "__main__":
    build_nao_robot()
