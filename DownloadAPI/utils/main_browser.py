from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def block(route):
    if route.request.resource_type not in ["document", "xhr", "fetch", "script"]:
        await route.abort()
    else:
        await route.continue_()

engine = None
browser = None
context_browser = None

async def start():
    global browser, context_browser, engine
    engine = await Stealth().use_async(async_playwright()).start()
    browser = await engine.chromium.launch(
        headless=True,
    )
    context_browser = await browser.new_context(
        viewport={"width": 50, "height": 50}
    )

async def get_page():
    page = await context_browser.new_page()
    await page.route("**/*", block)
    return page

