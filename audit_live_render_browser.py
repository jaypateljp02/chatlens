from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Navigating to https://chatlens-frontend.onrender.com/dashboard...")
    page.goto("https://chatlens-frontend.onrender.com/dashboard")
    page.wait_for_timeout(3000)
    
    page.screenshot(path="d:/whatsapp ai project/Live_Render_Dashboard.png")
    print("[OK] Captured Live_Render_Dashboard.png")
    
    page.goto("https://chatlens-frontend.onrender.com/summaries")
    page.wait_for_timeout(3000)
    
    page.screenshot(path="d:/whatsapp ai project/Live_Render_Summaries.png")
    print("[OK] Captured Live_Render_Summaries.png")
    
    browser.close()
