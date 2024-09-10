import subprocess
import time

import httpx
from playwright.sync_api import Playwright, sync_playwright


# Run playwright codegen to generate the code below, copy paste the sections in run()
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_role("button", name="POST /login/ Login").click()
    page.get_by_role("button", name="Try it out").click()
    page.screenshot(path="docs/en/docs/img/tutorial/request-form-models/image01.png")

    # ---------------------
    context.close()
    browser.close()


process = subprocess.Popen(
    ["fastapi", "run", "docs_src/request_form_models/tutorial001.py"]
)
try:
    for _ in range(3):
        try:
            response = httpx.get("http://localhost:8000/docs")
        except httpx.ConnectError:
            time.sleep(1)
            break
    with sync_playwright() as playwright:
        run(playwright)
finally:
    process.terminate()
