import subprocess

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_role("button", name="Item", exact=True).click()
    page.set_viewport_size({"width": 960, "height": 700})
    page.screenshot(
        path="docs/en/docs/img/tutorial/separate-openapi-schemas/image05.png"
    )

    # ---------------------
    context.close()
    browser.close()


process = subprocess.Popen(
    ["uvicorn", "docs_src.separate_openapi_schemas.tutorial002:app"]
)
try:
    with sync_playwright() as playwright:
        run(playwright)
finally:
    process.terminate()
