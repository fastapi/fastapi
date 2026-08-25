import subprocess
import time

import httpx
from playwright.sync_api import Playwright, sync_playwright


# Run playwright codegen to generate the code below, copy paste the sections in run()
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # Update the viewport manually
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_role("link", name="/items/").click()
    # Manually add the screenshot
    page.screenshot(path="docs/en/docs/img/tutorial/cookie-param-models/image01.png")

    # ---------------------
    context.close()
    browser.close()


import shutil
import os

fastapi_exec = shutil.which("fastapi")
if fastapi_exec is None:
    raise RuntimeError("fastapi executable not found in PATH")
script_path = os.path.abspath("docs_src/cookie_param_models/tutorial001.py")
process = subprocess.Popen(
    [fastapi_exec, "run", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True, start_new_session=True
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
