import subprocess

from playwright.sync_api import Playwright, sync_playwright


# Run playwright codegen to generate the code below, copy paste the sections in run()
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # Update the viewport manually
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_role("button", name="Item-Input").click()
    page.get_by_role("button", name="Item-Output").click()
    page.set_viewport_size({"width": 960, "height": 820})
    # Manually add the screenshot
    page.screenshot(
        path="docs/en/docs/img/tutorial/separate-openapi-schemas/image04.png"
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
