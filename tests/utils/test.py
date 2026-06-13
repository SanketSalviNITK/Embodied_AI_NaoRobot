import urllib.request
import urllib.error

try:
    req = urllib.request.Request(
        'http://localhost:5002/vqa_chat', 
        data=b'{"text": "hello"}', 
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req)
    print("SUCCESS:")
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print(e.read().decode())
except Exception as e:
    print("ERROR:", e)
