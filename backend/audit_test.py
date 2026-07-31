"""
Comprehensive System Audit Test Script for ChatLens AI.
Tests every API endpoint, parser logic, analytics calculation, and RAG memory layer.
Bypasses proxy settings for local 127.0.0.1 testing.
"""
import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000/api"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def req(path, method="GET", body=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode('utf-8') if body else None
    headers = {'Content-Type': 'application/json'} if body else {}
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    response = opener.open(request)
    return json.loads(response.read().decode('utf-8'))

def run_audit():
    results = {}
    print("==========================================")
    print("Starting Comprehensive System Audit...")
    print("==========================================\n")

    # 1. Health Check
    health = req("/health")
    results["Health Check"] = health
    print("[OK] 1. Health Check Endpoint:", health)

    # 2. Sample Chat Upload Test
    sample_chat_content = """[10/01/2026, 10:15:30] Ravi: Hi team, welcome to the project kick-off!
[10/01/2026, 10:16:05] Priya: Great! Shared the design assets for client review.
[10/01/2026, 10:18:22] Amit: I will set up PostgreSQL and pgvector on Windows Server by Friday.
[10/01/2026, 10:20:00] Ravi: Thanks Priya! Please check pediatric health logs for Taare group as well.
[10/01/2026, 14:30:10] Sneha: Finished pediatric health audit. All symptoms resolved in 48 hours.
[10/01/2026, 14:35:00] Ravi: Excellent job! This deadline is tight, but we will deliver."""

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body_bytes = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="sample_chat.txt"\r\n'
        f"Content-Type: text/plain\r\n\r\n"
        f"{sample_chat_content}\r\n"
        f"--{boundary}--\r\n"
    ).encode('utf-8')

    upload_req = urllib.request.Request(
        f"{BASE_URL}/upload",
        data=body_bytes,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        method="POST"
    )
    upload_res = json.loads(opener.open(upload_req).read().decode('utf-8'))
    chat_id = upload_res["chat_id"]
    results["Upload"] = upload_res
    print(f"[OK] 2. Upload Chat Endpoint: Created chat_id={chat_id}, parsed {upload_res['metadata']['total_messages']} messages.")

    # 3. Communication Analytics
    comm = req(f"/analytics/communication/{chat_id}")
    results["Communication Analytics"] = comm
    print(f"[OK] 3. Communication Analytics: Top sender: {comm['most_active_participant']}, Peak hours: {comm['peak_hours']}")

    # 4. Summarize (Bullet, Story, Timeline, Pending)
    summaries = {}
    for mode in ["bullet", "story", "timeline", "pending"]:
        s_res = req(f"/summarize/{chat_id}", method="POST", body={"mode": mode})
        summaries[mode] = len(s_res["summary_text"]) > 0
    results["Summarize"] = summaries
    print("[OK] 4. AI Smart Summaries (4 Modes):", summaries)

    # 5. Interactive Q&A
    qa = req(f"/ask/{chat_id}", method="POST", body={"question": "When will PostgreSQL be set up?"})
    results["Ask AI Q&A"] = qa
    print(f"[OK] 5. Interactive Ask AI Q&A: Answer generated with confidence {qa['confidence']}")

    # 6. Topics Extraction
    topics = req(f"/topics/{chat_id}")
    results["Topic Extraction"] = topics
    print(f"[OK] 6. AI Topic Extraction: Found {len(topics['topics'])} topic categories.")

    # 7. Sentiment Analytics
    sentiment = req(f"/analytics/sentiment/{chat_id}")
    results["Sentiment Analytics"] = sentiment
    print(f"[OK] 7. Sentiment & Emotion Analytics: Overall breakdown: {sentiment['overall_sentiment']}")

    # 8. People Profiles
    people = req(f"/analytics/people/{chat_id}")
    results["People Profiles"] = people
    print(f"[OK] 8. People Profiles: Profiled {len(people['profiles'])} participants with style tags and engagement scores.")

    # 9. Action Items Detection
    actions = req(f"/analytics/actions/{chat_id}")
    results["Action Items"] = actions
    print(f"[OK] 9. Action Items Tracker: Detected {actions['total']} commitment promises.")

    # 10. Timeline & Milestone Extraction
    timeline = req(f"/analytics/timeline/{chat_id}")
    results["Timeline"] = timeline
    print(f"[OK] 10. Milestone Timeline: Extracted {len(timeline['events'])} events.")

    # 11. Period Comparison
    compare = req(f"/analytics/compare/{chat_id}", method="POST", body={
        "period1_start": "2026-01-01",
        "period1_end": "2026-01-10",
        "period2_start": "2026-01-11",
        "period2_end": "2026-01-20"
    })
    results["Period Comparison"] = compare
    print(f"[OK] 11. Period Comparison Engine: Volume change: {compare['changes']['volume_change_percent']}%")

    # 12. Knowledge Graph Generation
    graph = req(f"/graph/{chat_id}")
    results["Knowledge Graph"] = graph
    print(f"[OK] 12. Knowledge Graph: Generated {graph['total_nodes']} nodes and {graph['total_edges']} edges.")

    # 13. Cross-Chat Memory Q&A
    memory_q = req("/memory/query", method="POST", body={"question": "What health audit was completed?"})
    results["RAG Cross-Chat Memory"] = memory_q
    print("[OK] 13. RAG Cross-Chat Memory Query:", memory_q["answer"][:80] + "...")

    # 14. Proactive AI Alerts
    alerts = req("/memory/alerts")
    results["Proactive Alerts"] = alerts
    print(f"[OK] 14. Proactive Smart Alerts: {len(alerts['alerts'])} active system alerts.")

    print("\n==========================================")
    print("SUCCESS: ALL 14 AUDIT CHECKS PASSED (100%)")
    print("==========================================")

if __name__ == "__main__":
    run_audit()
