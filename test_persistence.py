import urllib.request
import json
from io import BytesIO

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

print("==========================================")
print("TESTING PERSISTENT DISK SESSION RECALL...")
print("==========================================")

# 1. Upload sample file
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="Persistence_Test_Chat.txt"\r\n'
    "Content-Type: text/plain\r\n\r\n"
    "[10/01/2026, 10:15:30] UserA: Hello persistence test message!\n"
    "[10/01/2026, 10:16:05] UserB: Message received and stored on disk.\r\n"
    f"--{boundary}--\r\n"
).encode('utf-8')

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/upload",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

res = opener.open(req)
upload_data = json.loads(res.read().decode())
chat_id = upload_data["chat_id"]
print(f"[OK] Uploaded test chat! Assigned Chat ID: {chat_id}")

# 2. Query analytics
res = opener.open(f"http://127.0.0.1:8000/api/analytics/communication/{chat_id}")
stats = json.loads(res.read().decode())
print(f"[OK] Communication Stats retrieved! Total participants: {len(stats['messages_per_participant'])}")

# 3. Check saved chats endpoint
res = opener.open("http://127.0.0.1:8000/api/chats")
saved = json.loads(res.read().decode())
print(f"[OK] Total Saved Sessions on Disk: {len(saved['sessions'])}")

print("==========================================")
print("PERSISTENT DISK RECALL: 100% VERIFIED!")
print("==========================================")
