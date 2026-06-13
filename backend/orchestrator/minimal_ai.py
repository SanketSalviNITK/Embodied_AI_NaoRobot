import requests
import base64
import json
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BRIDGE_URL = "http://localhost:5001"
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def get_nao_image_as_jpeg_base64():
    """Fetches raw RGB frame from Vision Bridge, converts to JPEG, returns base64."""
    try:
        response = requests.get(f"{BRIDGE_URL}/capture", timeout=5)
        if response.status_code != 200:
            return None
            
        data = response.json()
        if data.get("status") != "ok":
            return None
            
        width = data["width"]
        height = data["height"]
        raw_rgb = base64.b64decode(data["data"])
        img = Image.frombytes("RGB", (width, height), raw_rgb)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"[minimal_ai] Vision fetch error: {e}")
        return None

def check_face_detected():
    """Checks if NAO currently sees a face."""
    try:
        response = requests.get(f"{BRIDGE_URL}/face/detect", timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {"status": "ok", "face_detected": False}

@app.route('/vqa_chat', methods=['POST'])
def vqa_chat_endpoint():
    try:
        data = request.json
        question = data.get("message", "").strip()
        
        if not question:
            return jsonify({"status": "error", "message": "Empty message"})
            
        # 1. Check for Face Registration command
        if question.lower().startswith("register my face as") or question.lower().startswith("register face"):
            words = question.split()
            name = words[-1] # Simplistic extraction
            
            # Send command to bridge
            resp = requests.post(f"{BRIDGE_URL}/face/register", json={"name": name})
            if resp.status_code == 200:
                bridge_data = resp.json()
                if bridge_data.get("status") == "ok":
                    return jsonify({"status": "success", "reply": f"Got it. I have registered your face as {name}."})
                else:
                    return jsonify({"status": "error", "reply": f"Failed to register face: {bridge_data.get('reason')}"})
                    
        # 2. Normal VQA Flow
        jpeg_b64 = get_nao_image_as_jpeg_base64()
        if not jpeg_b64:
            return jsonify({"status": "error", "reply": "I cannot see anything right now. Camera is offline."})
            
        # Optional: Inject face detection info into prompt
        face_info = check_face_detected()
        system_prompt = (
            "You are NAO, an advanced humanoid robot assistant. "
            "Your personality is helpful, slightly technical, but friendly. "
            "Keep responses concise (1-3 sentences) as they will be spoken aloud. "
            "Answer the user based on what you see in the image. "
            "CRITICAL: You MUST begin your response with a mood tag indicating your expression. "
            "Valid tags are: [MOOD: HAPPY], [MOOD: SAD], [MOOD: SURPRISED], [MOOD: CURIOUS], [MOOD: NEUTRAL]."
        )
        if face_info.get("face_detected"):
            face_name = face_info.get("name", "Unknown")
            if face_name != "Unknown":
                system_prompt += f" You currently see {face_name} looking at you."
            else:
                system_prompt += " You currently see an unknown person looking at you."
                
        payload = {
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{jpeg_b64}"}}
                    ]
                }
            ],
            "temperature": 0.7,
            "max_tokens": 512,
            "stream": False
        }
        
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        # Trigger physical gesture based on mood tag in response
        try:
            requests.post(f"{BRIDGE_URL}/gesture", json={"mood": answer}, timeout=1)
        except requests.exceptions.RequestException as e:
            print(f"[minimal_ai] Failed to send gesture to bridge: {e}")
            
        return jsonify({"status": "success", "reply": answer})
        
    except Exception as e:
        print(f"[minimal_ai] /vqa_chat error: {e}")
        return jsonify({"status": "error", "reply": f"Internal Brain Error: {str(e)}"})

@app.route('/stream_frame', methods=['GET'])
def stream_frame():
    """Returns the latest image for the dashboard."""
    jpeg_b64 = get_nao_image_as_jpeg_base64()
    if jpeg_b64:
        return jsonify({"status": "ok", "image": jpeg_b64})
    return jsonify({"status": "error"})

if __name__ == '__main__':
    print("="*50)
    print("🧠 Minimal AI Orchestrator (Python 3)")
    print("="*50)
    app.run(host='0.0.0.0', port=5002, threaded=True)
