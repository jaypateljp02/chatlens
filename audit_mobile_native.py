from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # iPhone 12/13 mobile viewport size
    context = browser.new_context(viewport={"width": 390, "height": 844}, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)")
    page = context.new_page()
    
    page.goto("http://localhost:5173/dashboard")
    page.wait_for_timeout(1500)
    page.screenshot(path="d:/whatsapp ai project/Native_Mobile_BottomNav.png")
    print("[OK] Captured Native_Mobile_BottomNav.png")

    # Tap on More sheet button
    page.click(".more-tab")
    page.wait_for_timeout(1000)
    page.screenshot(path="d:/whatsapp ai project/Native_Mobile_MoreSheet.png")
    print("[OK] Captured Native_Mobile_MoreSheet.png")
    
    browser.close()
