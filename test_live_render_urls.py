import urllib.request
import json

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

print("==========================================")
print("TESTING LIVE RENDER PRODUCTION DEPLOYMENT URLS...")
print("==========================================")

# 1. Test Backend Health
try:
    res = opener.open("https://chatlens-backend-csg8.onrender.com/api/health")
    data = json.loads(res.read().decode('utf-8'))
    print(f"[OK 200] Live Backend Health API: {data}")
except Exception as e:
    print(f"[FAIL] Backend Health Error: {e}")

# 2. Test Backend Master Communication Analytics
try:
    res = opener.open("https://chatlens-backend-csg8.onrender.com/api/analytics/communication/all")
    data = json.loads(res.read().decode('utf-8'))
    print(f"[OK 200] Live Master Analytics API: Total msgs per participant -> {list(data.get('messages_per_participant', {}).items())[:3]}")
except Exception as e:
    print(f"[FAIL] Master Analytics Error: {e}")

# 3. Test Frontend Live Site
try:
    res = opener.open("https://chatlens-frontend.onrender.com/")
    html = res.read().decode('utf-8')
    print(f"[OK 200] Live Frontend Web App HTML Length: {len(html)} bytes")
except Exception as e:
    print(f"[FAIL] Frontend Web App Error: {e}")

print("==========================================")
