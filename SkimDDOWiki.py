from playwright.sync_api import sync_playwright

# URL to get the website, the level will be set later
level = 0
websiteURL = f"https://ddowiki.com/page/Level_{level}_quests"

for i in range(36, 37):
    level = i   # for the website URL, changes the level
    websiteURL = f"https://ddowiki.com/page/Level_{level}_quests"

    with sync_playwright() as p:
        # Launch Chromium in headful mode (headless=False) initially to watch the challenge solve.
        # Set headless=True once confirmed working.
        browser = p.chromium.launch(headless=False)
        
        # Create a context with realistic desktop screen dimensions
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        print("Navigating to page...")
        # 'commit' waits until the initial network response is received
        page.goto(websiteURL, wait_until="commit")

        # Wait for a known element that only appears AFTER the challenge succeeds
        # Replace '#target-content' with an actual selector from your target page
        try:
            # Give Cloudflare or the JS challenge 15 seconds to solve and redirect
            page.wait_for_selector(".quote, #content, main", timeout=15000)
        except Exception:
            # Fallback: give extra time if waiting for a specific selector timed out
            page.wait_for_load_state("networkidle", timeout=10000)

        # Extract the fully rendered DOM HTML
        html_content = page.content()
        browser.close()

    # Make a file with the contents
    with open(f".\\LvLFiles\\level_{level}.html", "w", encoding='utf-8') as f:
        f.write(html_content)