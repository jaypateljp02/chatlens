from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    pages_to_test = [
        ("Dashboard", "http://localhost:5173/dashboard"),
        ("Summaries", "http://localhost:5173/summaries"),
        ("Analytics", "http://localhost:5173/analytics"),
        ("Sentiment", "http://localhost:5173/sentiment"),
        ("People", "http://localhost:5173/people"),
        ("Topics", "http://localhost:5173/topics"),
        ("Timeline", "http://localhost:5173/timeline"),
        ("Actions", "http://localhost:5173/actions"),
        ("KnowledgeGraph", "http://localhost:5173/knowledge-graph")
    ]
    
    for name, url in pages_to_test:
        page.goto(url)
        page.wait_for_timeout(1500)
        page.screenshot(path=f"d:/whatsapp ai project/page_{name}.png")
        print(f"[OK] Captured screenshot for {name} ({url})")
        
    browser.close()
