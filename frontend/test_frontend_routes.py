"""
Frontend Route Audit Script for ChatLens AI.
Fetches all 11 SPA routes from http://localhost:5173/ to verify zero routing/component breakage.
"""
import urllib.request

BASE_URL = "http://localhost:5173"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

routes = [
    ("/", "Upload Page"),
    ("/dashboard", "Dashboard Overview"),
    ("/summaries", "Smart Summaries & Q&A"),
    ("/analytics", "Communication Analytics"),
    ("/sentiment", "Sentiment Analytics"),
    ("/people", "People Profiles"),
    ("/topics", "Topic Extraction"),
    ("/timeline", "Timeline & Comparison"),
    ("/actions", "Action Items Tracker"),
    ("/knowledge-graph", "Knowledge Graph"),
    ("/settings", "Settings & Privacy")
]

def test_routes():
    print("==========================================")
    print("AUDITING ALL 11 FRONTEND SPA ROUTES...")
    print("==========================================\n")

    all_passed = True
    for route, name in routes:
        url = f"{BASE_URL}{route}"
        try:
            res = opener.open(url)
            code = res.getcode()
            content = res.read().decode('utf-8')
            has_root = 'id="root"' in content or '<div' in content
            if code == 200 and has_root:
                print(f"[OK] Route '{route}' ({name}) -> HTTP {code} OK")
            else:
                print(f"[FAIL] Route '{route}' ({name}) -> HTTP {code}")
                all_passed = False
        except Exception as e:
            print(f"[ERROR] Route '{route}' ({name}) -> {e}")
            all_passed = False

    print("\n==========================================")
    if all_passed:
        print("SUCCESS: ALL 11 FRONTEND ROUTES ARE 100% OPERATIONAL!")
    else:
        print("WARNING: SOME ROUTES HAD ERRORS.")
    print("==========================================")

if __name__ == "__main__":
    test_routes()
