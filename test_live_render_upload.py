import urllib.request
import json

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

print("==========================================")
print("TESTING LIVE RENDER UPLOAD ENDPOINT...")
print("==========================================")

sample_chat = """[10/01/2026, 10:15:30] Ravi: Hi team, welcome to the live deployment test!
[10/01/2026, 10:16:05] Priya: Awesome! Shared the design wireframes.
[10/01/2026, 10:18:22] Amit: I will complete the server setup by Friday."""

boundary = "----WebKitFormBoundaryRenderTest"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="Live_Render_Upload_Test.txt"\r\n'
    "Content-Type: text/plain\r\n\r\n"
    + sample_chat + "\r\n"
    f"--{boundary}--\r\n"
).encode('utf-8')

req = urllib.request.Request(
    "https://chatlens-backend-csg8.onrender.com/api/upload",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

try:
    res = opener.open(req)
    data = json.loads(res.read().decode('utf-8'))
    print(f"[OK 200] Live Render Upload Success! Response: {data}")
except Exception as e:
    print(f"[FAIL] Live Render Upload Error: {e}")

print("==========================================")
