import subprocess
import time

import httpx
from playwright.sync_api import Playwright, sync_playwright


# Run playwright codegen to generate the code below, copy paste the sections in run()
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # Update the viewport manually
    page = browser.new_context(viewport={"width": 960, "height": 1080}).new_page()
    # page created from context; use page.context to close it
    page.goto("http://localhost:8000/docs")
    page.get_by_role("button", name="GET /items/ Read Items").click()
    page.get_by_role("button", name="Try it out").click()
    page.get_by_role("heading", name="Servers").click()
    # Manually add the screenshot
    page.screenshot(path="docs/en/docs/img/tutorial/query-param-models/image01.png")

    # ---------------------
    page.context.close()
    browser.close()


_fastapi_cmd = __import__("shutil").which("fastapi")
if not _fastapi_cmd or not __import__("os").path.isabs(_fastapi_cmd) or not __import__("os").access(
    _fastapi_cmd, __import__("os").X_OK
):
    raise RuntimeError("fastapi executable not found or not executable")
process = subprocess.Popen(
    [_fastapi_cmd, "run", "docs_src/query_param_models/tutorial001.py"],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    close_fds=True,
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
