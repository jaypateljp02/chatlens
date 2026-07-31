from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Navigating to https://chatlens-olmp.onrender.com/...")
    page.goto("https://chatlens-olmp.onrender.com/")
    page.wait_for_timeout(3000)
    page.screenshot(path="d:/whatsapp ai project/Unified_Render_Home.png")
    print("[OK] Captured Unified_Render_Home.png")

    page.goto("https://chatlens-olmp.onrender.com/dashboard")
    page.wait_for_timeout(3000)
    page.screenshot(path="d:/whatsapp ai project/Unified_Render_Dashboard.png")
    print("[OK] Captured Unified_Render_Dashboard.png")

    page.goto("https://chatlens-olmp.onrender.com/sentiment")
    page.wait_for_timeout(3000)
    page.screenshot(path="d:/whatsapp ai project/Unified_Render_Sentiment.png")
    print("[OK] Captured Unified_Render_Sentiment.png")
    
    browser.close()
