import subprocess

from playwright.sync_api import Playwright, sync_playwright


# Run playwright codegen to generate the code below, copy paste the sections in run()
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # Update the viewport manually
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_text("GET/items/Read Items").click()
    page.get_by_role("tab", name="Schema").click()
    page.get_by_label("Schema").get_by_role("button", name="Expand all").click()
    # Manually add the screenshot
    page.screenshot(
        path="docs/en/docs/img/tutorial/separate-openapi-schemas/image03.png"
    )

    # ---------------------
    context.close()
    browser.close()


import os

os.environ["PATH"] = "/usr/bin:/bin:/usr/local/bin"
process = subprocess.Popen(
    ["uvicorn", "docs_src.separate_openapi_schemas.tutorial001:app"],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    close_fds=True,
    start_new_session=True,
)
try:
    with sync_playwright() as playwright:
        run(playwright)
finally:
    process.terminate()
