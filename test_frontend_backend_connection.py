import urllib.request
import json

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

print("==========================================")
print("TESTING FRONTEND-BACKEND API ENDPOINTS...")
print("==========================================")

endpoints = [
    ("/api/health", "GET"),
    ("/api/chats", "GET"),
    ("/api/analytics/communication/all", "GET"),
    ("/api/analytics/sentiment/all", "GET"),
    ("/api/analytics/people/all", "GET"),
    ("/api/analytics/actions/all", "GET"),
    ("/api/analytics/timeline/all", "GET"),
    ("/api/topics/all", "GET"),
    ("/api/graph/all", "GET"),
    ("/api/memory/alerts", "GET")
]

success = 0
for ep, method in endpoints:
    url = f"http://127.0.0.1:8000{ep}"
    try:
        req = urllib.request.Request(url, method=method)
        res = opener.open(req)
        data = json.loads(res.read().decode('utf-8'))
        print(f"[OK 200] {method} {ep} -> Success")
        success += 1
    except Exception as e:
        print(f"[FAIL] {method} {ep} -> Error: {e}")

print("==========================================")
print(f"VERIFIED {success}/{len(endpoints)} API ENDPOINTS OPERATIONAL!")
print("==========================================")
