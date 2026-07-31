import asyncio
from playwright.async_api import async_playwright

async def run_audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        
        print("1. Navigating to http://localhost:5173/...")
        await page.goto("http://localhost:5173/")
        await page.wait_for_timeout(3000)
        
        title = await page.title()
        content = await page.content()
        print(f"Page Title: {title}")
        print("Console logs captured:", len(console_logs))
        for log in console_logs:
            print("  ", log)
            
        header_text = await page.inner_text("#main-header") if await page.query_selector("#main-header") else "No header"
        print("Header Text:", header_text.replace("\n", " | "))
        
        # Check Dashboard content
        body_text = await page.inner_text(".content-wrapper") if await page.query_selector(".content-wrapper") else "No content wrapper"
        print("Dashboard Body Preview:", body_text[:300].replace("\n", " | "))
        
        await page.screenshot(path="d:/whatsapp ai project/live_audit_dashboard.png")
        print("Screenshot saved to live_audit_dashboard.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_audit())
