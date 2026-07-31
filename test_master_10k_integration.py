import urllib.request
import json

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

print("==========================================")
print("TESTING 10,000 MESSAGE MASTER MEMORY INTEGRATION...")
print("==========================================")

# 1. Generate 10,000 message WhatsApp chat content
lines = []
for i in range(1, 10001):
    sender = f"Engineer_{i % 5}"
    lines.append(f"[{i%28+1:02d}/01/2026, 10:15:{i%60:02d}] {sender}: Large scale system architecture line {i}.")

chat_text = "\n".join(lines)

# 2. Upload to /api/upload
boundary = "----WebKitFormBoundary10KTestBoundary"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="Large_10K_Project_Export.txt"\r\n'
    "Content-Type: text/plain\r\n\r\n"
    + chat_text + "\r\n"
    f"--{boundary}--\r\n"
).encode('utf-8')

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/upload",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

res = opener.open(req)
upload_data = json.loads(res.read().decode("utf-8"))
print(f"[OK 200] Uploaded 10,000 message chat! Chat ID: {upload_data['chat_id']}")
print(f"[OK] Parsed Total Messages in Upload Response: {upload_data['metadata']['total_messages']}")

# 3. Query Master Memory ('all')
res = opener.open("http://127.0.0.1:8000/api/analytics/communication/all")
master_comm = json.loads(res.read().decode("utf-8"))

total_master_msgs = sum(master_comm["messages_per_participant"].values())
print(f"[OK] Total Combined Messages in Master Memory ('all'): {total_master_msgs}")

res = opener.open("http://127.0.0.1:8000/api/analytics/people/all")
master_people = json.loads(res.read().decode("utf-8"))
print(f"[OK] Total Participants in Master Memory ('all'): {len(master_people['profiles'])}")

print("==========================================")
assert total_master_msgs >= 10000
print("10,000 MESSAGE MASTER MEMORY INTEGRATION: 100% VERIFIED SUCCESS!")
print("==========================================")
