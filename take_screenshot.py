import asyncio
import os
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\ccccd3a4-4030-4a99-a9f1-7f4ec15cda51"

async def capture_screenshots():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        # Step 1: Open Home Upload page and click "Try Sample Chat Demo"
        print("Opening Home page...")
        await page.goto("http://localhost:5173/", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "upload_page.png"))

        # Click Try Sample Chat Demo button
        print("Clicking Sample Demo button...")
        try:
            btn = page.get_by_text("Try Sample Chat Demo")
            await btn.click()
            await page.wait_for_timeout(2000)
        except Exception as e:
            print("Could not click sample button:", e)

        # Step 2: Capture all feature screens
        pages = [
            ("http://localhost:5173/dashboard", "dashboard_overview.png"),
            ("http://localhost:5173/analytics", "communication_analytics.png"),
            ("http://localhost:5173/summaries", "smart_summaries.png"),
            ("http://localhost:5173/sentiment", "sentiment_analytics.png"),
            ("http://localhost:5173/people", "people_profiles.png"),
            ("http://localhost:5173/topics", "topic_extraction.png"),
            ("http://localhost:5173/timeline", "timeline_milestones.png"),
            ("http://localhost:5173/actions", "action_tracker.png"),
            ("http://localhost:5173/knowledge-graph", "knowledge_graph.png"),
            ("http://localhost:5173/settings", "settings_page.png")
        ]

        for url, fname in pages:
            try:
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(1000)
                out_path = os.path.join(ARTIFACT_DIR, fname)
                await page.screenshot(path=out_path)
                print(f"Captured: {fname} -> {out_path}")
            except Exception as e:
                print(f"Error capturing {url}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_screenshots())
