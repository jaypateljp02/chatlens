import urllib.request
import json

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

endpoints = [
    ("GET", "/api/analytics/communication/all", None),
    ("GET", "/api/analytics/sentiment/all", None),
    ("GET", "/api/analytics/people/all", None),
    ("GET", "/api/analytics/actions/all", None),
    ("GET", "/api/analytics/timeline/all", None),
    ("GET", "/api/topics/all", None),
    ("POST", "/api/summarize/all", {"mode": "bullet"}),
    ("POST", "/api/ask/all", {"question": "What tasks are pending?"}),
    ("GET", "/api/graph/all", None)
]

print("==========================================")
print("TESTING ALL MASTER MEMORY ENDPOINTS ('all')")
print("==========================================")

for method, path, body in endpoints:
    url = f"http://127.0.0.1:8000{path}"
    try:
        if method == "POST":
            data = json.dumps(body).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        else:
            req = urllib.request.Request(url)
            
        res = opener.open(req)
        raw = res.read().decode("utf-8")
        parsed = json.loads(raw)
        print(f"[OK 200] {path} -> Success!")
    except Exception as e:
        print(f"[ERROR] {path} -> Failed: {e}")

print("==========================================")
