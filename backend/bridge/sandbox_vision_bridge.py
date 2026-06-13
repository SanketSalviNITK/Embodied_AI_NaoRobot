# -*- coding: utf-8 -*-
import sys
import os
import time
import logging
import base64
import json
from flask import Flask, request, jsonify

# Setup NAOqi SDK path
SDK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649", "lib")
if SDK_PATH not in sys.path:
    sys.path.append(SDK_PATH)
if SDK_PATH not in os.environ['PATH']:
    os.environ['PATH'] = SDK_PATH + os.pathsep + os.environ['PATH']

from naoqi import ALProxy

ROBOT_IP = "169.254.80.144" # Same as bridge_nao.py
PORT = 9559

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

video_proxy = None
subscriber_id = None

def init_vision():
    global video_proxy, subscriber_id
    try:
        print("[Vision Sandbox] Connecting to ALVideoDevice...")
        video_proxy = ALProxy("ALVideoDevice", ROBOT_IP, PORT)
        
        # Parameters: Name, Camera Index (0=Top), Resolution (2=VGA 640x480, 1=QVGA 320x240), Color Space (11=RGB), FPS
        # We use QVGA (320x240) to keep base64 payload small, or VGA for better VQA. Let's use VGA.
        subscriber_name = "vqa_sandbox_" + str(int(time.time()))
        subscriber_id = video_proxy.subscribeCamera(subscriber_name, 0, 2, 11, 5)
        print("[Vision Sandbox] Subscribed to Top Camera. ID: " + str(subscriber_id))
    except Exception as e:
        print("[Vision Sandbox] ERROR connecting to ALVideoDevice: " + str(e))

@app.route('/capture', methods=['GET'])
def capture_frame():
    global video_proxy, subscriber_id
    if not video_proxy or not subscriber_id:
        return jsonify({"status": "error", "reason": "Video device not initialized"}), 500

    try:
        # Get image from NAO
        nao_image = video_proxy.getImageRemote(subscriber_id)
        if not nao_image:
            return jsonify({"status": "error", "reason": "Failed to capture image"}), 500

        width = nao_image[0]
        height = nao_image[1]
        raw_rgb = nao_image[6]

        # The image is raw RGB bytes. To avoid needing PIL or cv2 in Python 2.7,
        # we'll just base64 encode the raw RGB array and let the Python 3 client format it into an image.
        b64_img = base64.b64encode(raw_rgb)
        
        # Release the image buffer
        video_proxy.releaseImage(subscriber_id)

        return jsonify({
            "status": "ok",
            "width": width,
            "height": height,
            "format": "RGB",
            "data": b64_img
        })
    except Exception as e:
        print("[Vision Sandbox] Capture Error: " + str(e))
        return jsonify({"status": "error", "reason": str(e)}), 500

if __name__ == "__main__":
    init_vision()
    print("[Vision Sandbox] Server running on port 5003")
    try:
        app.run(host="0.0.0.0", port=5003)
    finally:
        # Cleanup
        if video_proxy and subscriber_id:
            print("[Vision Sandbox] Unsubscribing camera...")
            video_proxy.unsubscribe(subscriber_id)
