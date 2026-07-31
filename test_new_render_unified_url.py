import urllib.request
import json

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

print("==========================================")
print("TESTING NEW UNIFIED RENDER DEPLOYMENT URL...")
print("==========================================")

# 1. Test Root URL
try:
    res = opener.open("https://chatlens-olmp.onrender.com/")
    html = res.read().decode('utf-8')
    print(f"[OK 200] Live Unified App Web Page: Received {len(html)} bytes")
except Exception as e:
    print(f"[FAIL] Root Web Page Error: {e}")

# 2. Test API Health
try:
    res = opener.open("https://chatlens-olmp.onrender.com/api/health")
    data = json.loads(res.read().decode('utf-8'))
    print(f"[OK 200] Live API Health: {data}")
except Exception as e:
    print(f"[FAIL] API Health Error: {e}")

# 3. Test Master Analytics
try:
    res = opener.open("https://chatlens-olmp.onrender.com/api/analytics/communication/all")
    data = json.loads(res.read().decode('utf-8'))
    print(f"[OK 200] Live Master Analytics: {list(data.get('messages_per_participant', {}).items())[:3]}")
except Exception as e:
    print(f"[FAIL] Master Analytics Error: {e}")

# 4. Test Live Upload
sample_chat = """[10/01/2026, 10:15:30] Ravi: Live unified Render deployment test!
[10/01/2026, 10:16:05] Priya: Tested and verified 100% operational."""

boundary = "----WebKitFormBoundaryUnifiedTest"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="Unified_Render_Test.txt"\r\n'
    "Content-Type: text/plain\r\n\r\n"
    + sample_chat + "\r\n"
    f"--{boundary}--\r\n"
).encode('utf-8')

req = urllib.request.Request(
    "https://chatlens-olmp.onrender.com/api/upload",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

try:
    res = opener.open(req)
    data = json.loads(res.read().decode('utf-8'))
    print(f"[OK 200] Live Upload Success! Chat ID: {data.get('chat_id')}")
except Exception as e:
    print(f"[FAIL] Live Upload Error: {e}")

print("==========================================")
