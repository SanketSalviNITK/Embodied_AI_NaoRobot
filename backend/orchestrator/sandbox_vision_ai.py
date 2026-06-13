import requests
import base64
import json
from PIL import Image
from io import BytesIO

import subprocess
import time

# Configuration
VISION_BRIDGE_URL = "http://localhost:5003/capture"
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def init_lm_studio():
    """Automates starting the LM Studio server and loading the model."""
    try:
        print("[Vision AI] Automating LM Studio startup...")
        subprocess.Popen("lms server start --bind 0.0.0.0", shell=True)
        time.sleep(4)
        print("[Vision AI] Loading model google/gemma-4-e4b...")
        subprocess.call("lms load google/gemma-4-e4b", shell=True)
        print("[Vision AI] LM Studio ready.")
    except Exception as e:
        print(f"[Vision AI] Warning: Failed to automate LM Studio startup: {e}")

def get_nao_image_as_jpeg_base64():
    """Fetches raw RGB frame from Vision Bridge, converts to JPEG, returns base64."""
    print("[Vision AI] Fetching image from NAO...")
    try:
        response = requests.get(VISION_BRIDGE_URL)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            print(f"[Error] Bridge returned: {data.get('reason')}")
            return None
            
        width = data["width"]
        height = data["height"]
        raw_rgb_b64 = data["data"]
        
        # Decode base64 to raw bytes
        raw_rgb = base64.b64decode(raw_rgb_b64)
        
        # Create a PIL Image from raw RGB bytes
        img = Image.frombytes("RGB", (width, height), raw_rgb)
        
        # Save to memory buffer as JPEG
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        
        # Get base64 string of the JPEG
        jpeg_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # (Optional) Save locally to verify what the robot sees
        img.save("sandbox_latest_vision.jpg")
        
        return jpeg_b64

    except Exception as e:
        print(f"[Vision AI] Failed to fetch/convert image from robot: {e}")
        print("[Vision AI] Generating a test image since robot is offline...")
        # Create a 320x240 red image to test the VLM
        test_img = Image.new('RGB', (320, 240), color = 'red')
        buffered = BytesIO()
        test_img.save(buffered, format="JPEG")
        test_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return test_b64

def ask_vlm(jpeg_b64, question):
    """Sends the image and question to the local Vision Language Model in LM Studio."""
    print("[Vision AI] Thinking...")
    
    # OpenAI Vision API format
    payload = {
        "model": "local-model", # LM Studio usually ignores this and uses the loaded model
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{jpeg_b64}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 512,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        answer = result["choices"][0]["message"]["content"]
        return answer
    except Exception as e:
        print(f"[Vision AI] Failed to communicate with VLM: {e}")
        return None

import sys

def main():
    print("="*50)
    print("🤖 NAO VQA Sandbox (Local VLM)")
    print("="*50)
    print("Ensure sandbox_vision_bridge.py is running on port 5003.")
    print("Type 'exit' to quit.\n")
    
    init_lm_studio()
    
    # If a question is passed via command line, run it once and exit
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"[You]: {question}")
        jpeg_b64 = get_nao_image_as_jpeg_base64()
        if jpeg_b64:
            answer = ask_vlm(jpeg_b64, question)
            print(f"\n[NAO Vision]: {answer}\n")
        return
        
    while True:
        question = input("\n[You]: ")
        if question.lower().strip() in ['exit', 'quit']:
            break
            
        if not question.strip():
            continue
            
        jpeg_b64 = get_nao_image_as_jpeg_base64()
        if not jpeg_b64:
            print("[System] Could not retrieve image. Retrying loop...")
            continue
            
        answer = ask_vlm(jpeg_b64, question)
        if answer:
            print(f"\n[NAO Vision]: {answer}\n")
            
if __name__ == "__main__":
    main()
