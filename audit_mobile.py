from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # iPhone 12/13 mobile viewport size
    context = browser.new_context(viewport={"width": 390, "height": 844}, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)")
    page = context.new_page()
    
    pages = [
        ("Mobile_Dashboard", "http://localhost:5173/dashboard"),
        ("Mobile_Summaries", "http://localhost:5173/summaries"),
        ("Mobile_People", "http://localhost:5173/people"),
        ("Mobile_Actions", "http://localhost:5173/actions")
    ]
    
    for name, url in pages:
        page.goto(url)
        page.wait_for_timeout(1500)
        page.screenshot(path=f"d:/whatsapp ai project/{name}.png")
        print(f"[OK] Mobile screenshot captured for {name}")
        
    browser.close()
