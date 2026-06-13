# -*- coding: utf-8 -*-
import sys
import os
import time
import logging
import base64
import json
from flask import Flask, request, jsonify
from nao_motions import parse_and_execute_mood

# Setup NAOqi SDK path
SDK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649", "lib")
if SDK_PATH not in sys.path:
    sys.path.append(SDK_PATH)
if SDK_PATH not in os.environ['PATH']:
    os.environ['PATH'] = SDK_PATH + os.pathsep + os.environ['PATH']

try:
    from naoqi import ALProxy
except ImportError:
    print("Warning: naoqi not found, running in mock mode for hardware")
    ALProxy = None

ROBOT_IP = "169.254.116.8"
PORT = 9559

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

video_proxy = None
face_proxy = None
memory_proxy = None
animation_proxy = None
leds_proxy = None
subscriber_id = None

def init_proxies():
    global video_proxy, face_proxy, memory_proxy, animation_proxy, leds_proxy, subscriber_id
    if ALProxy is None: return
    try:
        print("[Bridge] Connecting to Proxies...")
        video_proxy = ALProxy("ALVideoDevice", ROBOT_IP, PORT)
        face_proxy = ALProxy("ALFaceDetection", ROBOT_IP, PORT)
        memory_proxy = ALProxy("ALMemory", ROBOT_IP, PORT)
        animation_proxy = ALProxy("ALAnimationPlayer", ROBOT_IP, PORT)
        leds_proxy = ALProxy("ALLeds", ROBOT_IP, PORT)
        
        # Subscribe to camera (Name, CameraIndex=0, Resolution=2 (VGA), ColorSpace=11 (RGB), FPS=5)
        subscriber_id = video_proxy.subscribeCamera("vision_bridge", 0, 2, 11, 5)
        print("[Bridge] ALVideoDevice connected. Subscriber ID:", subscriber_id)
        
        # Ensure Face Detection is active
        face_proxy.subscribe("bridge_face_detect")
        print("[Bridge] ALFaceDetection active.")
        print("✅ NAO Hardware Proxies Initialized (Vision, Face, Memory, Animation, LEDs)")
        
    except Exception as e:
        print("[Bridge] Error initializing proxies:", e)

@app.route('/capture', methods=['GET'])
def capture_image():
    if not video_proxy or not subscriber_id:
        return jsonify({"status": "error", "reason": "Camera not initialized"})
    try:
        image_data = video_proxy.getImageRemote(subscriber_id)
        if not image_data:
            return jsonify({"status": "error", "reason": "No image data received from camera"})
        width = image_data[0]
        height = image_data[1]
        raw_rgb = image_data[6]
        raw_rgb_b64 = base64.b64encode(raw_rgb)
        
        return jsonify({
            "status": "ok",
            "width": width,
            "height": height,
            "data": raw_rgb_b64
        })
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)})

@app.route('/face/register', methods=['POST'])
def register_face():
    data = request.json
    name = data.get("name", "")
    if not name or not face_proxy:
        return jsonify({"status": "error", "reason": "Invalid name or proxy offline"})
    try:
        success = face_proxy.learnFace(name)
        if success:
            return jsonify({"status": "ok", "message": "Face registered as " + name})
        else:
            return jsonify({"status": "error", "reason": "Failed to learn face. Please look at the camera."})
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)})

@app.route('/face/detect', methods=['GET'])
def detect_face():
    if not memory_proxy:
        return jsonify({"status": "error", "reason": "Memory proxy offline"})
    try:
        faces = memory_proxy.getData("FaceDetected")
        if faces and len(faces) > 1 and faces[1]:
            face_info = faces[1][0]
            # Extra info contains face ID/name if recognized
            extra_info = face_info[1]
            face_name = extra_info[2] if len(extra_info) > 2 else "Unknown"
            
            return jsonify({
                "status": "ok",
                "face_detected": True,
                "name": face_name
            })
        return jsonify({"status": "ok", "face_detected": False})
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)})

@app.route('/joints', methods=['GET'])
def get_joints():
    # Placeholder for joint telemetry for Blender if needed
    return jsonify({"status": "ok", "joints": {}})

@app.route('/gesture', methods=['POST'])
def trigger_gesture():
    data = request.json
    mood = data.get("mood", "NEUTRAL")
    
    if animation_proxy and leds_proxy:
        parse_and_execute_mood(mood, animation_proxy, leds_proxy)
        return jsonify({"status": "success", "mood": mood})
    else:
        return jsonify({"status": "mock", "mood": mood})

if __name__ == "__main__":
    print("="*50)
    print("🤖 NAO Hardware Bridge (Python 2.7)")
    print("="*50)
    init_proxies()
    # Run Flask on port 5001
    app.run(host='0.0.0.0', port=5001, threaded=True)
