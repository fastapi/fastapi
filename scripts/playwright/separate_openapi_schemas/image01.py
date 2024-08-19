import subprocess

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_text("POST/items/Create Item").click()
    page.get_by_role("tab", name="Schema").first.click()
    page.screenshot(
        path="docs/en/docs/img/tutorial/separate-openapi-schemas/image01.png"
    )

    # ---------------------
    context.close()
    browser.close()


process = subprocess.Popen(
    ["uvicorn", "docs_src.separate_openapi_schemas.tutorial001:app"]
)
try:
    with sync_playwright() as playwright:
        run(playwright)
finally:
    process.terminate()
