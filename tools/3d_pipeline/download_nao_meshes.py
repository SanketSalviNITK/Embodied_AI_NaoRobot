# -*- coding: utf-8 -*-
"""
NAO Robot Meshes Downloader (download_nao_meshes.py)
---------------------------------------------------
This script programmatically downloads the official NAO V40 high-fidelity STL meshes
from the Bullet Physics SDK (bullet3) GitHub repository. It saves them locally so we
can import and rig them inside Blender.

Usage:
  python3 download_nao_meshes.py
"""

import os
import sys
import json

try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request

GITHUB_API_URL = "https://api.github.com/repos/bulletphysics/bullet3/contents/data/humanoid/nao_meshes/meshes/V40"
LOCAL_MESH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nao_meshes")

def download_file(url, local_path):
    """Downloads a single file from url to local_path with progress indication."""
    try:
        req = urllib_request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        response = urllib_request.urlopen(req)
        with open(local_path, 'wb') as f:
            f.write(response.read())
        return True
    except Exception as e:
        print(f"\nFailed to download {url}: {e}")
        return False

def main():
    print("====================================================")
    print("        NAO ROBOT OFFICIAL MESHES DOWNLOADER        ")
    print("====================================================")
    print(f"Target local folder: {LOCAL_MESH_DIR}")
    
    if not os.path.exists(LOCAL_MESH_DIR):
        print("Creating target directory...")
        os.makedirs(LOCAL_MESH_DIR)
        
    print("Connecting to GitHub API to query Bullet Physics nao_meshes manifest...")
    try:
        req = urllib_request.Request(
            GITHUB_API_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        response = urllib_request.urlopen(req)
        items = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"\nERROR: Failed to query GitHub API: {e}")
        print("Please check your internet connection and try again.")
        sys.exit(1)
        
    # Filter for STL files
    stl_items = [item for item in items if item.get('name', '').endswith('.stl')]
    
    if not stl_items:
        print("\nERROR: No STL files found in the repository folder!")
        print("Check if the repository layout changed.")
        sys.exit(1)
        
    total_files = len(stl_items)
    print(f"Detected {total_files} official NAO STL mesh parts ready for download.")
    print("Starting downloads...\n")
    
    success_count = 0
    for idx, item in enumerate(stl_items, 1):
        name = item['name']
        download_url = item['download_url']
        local_path = os.path.join(LOCAL_MESH_DIR, name)
        
        sys.stdout.write(f"[{idx}/{total_files}] Downloading {name:<35}...")
        sys.stdout.flush()
        
        if download_file(download_url, local_path):
            sys.stdout.write(" SUCCESS!\n")
            success_count += 1
        else:
            sys.stdout.write(" FAILED!\n")
            
        sys.stdout.flush()
        
    print("----------------------------------------------------")
    print(f"Download complete! successfully acquired {success_count} / {total_files} meshes.")
    if success_count == total_files:
        print("\n>>> All official NAO meshes downloaded successfully! <<<")
        print("Folder is located at: " + LOCAL_MESH_DIR)
    else:
        print("\nWARNING: Some mesh parts failed to download. Please rerun the script to retry.")

if __name__ == "__main__":
    main()
