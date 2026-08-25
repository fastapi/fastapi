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
    page.get_by_role("button", name="Try it out").click()
    page.get_by_role("button", name="Execute").click()
    # Manually add the screenshot
    page.screenshot(
        path="docs/en/docs/img/tutorial/separate-openapi-schemas/image02.png"
    )

    # ---------------------
    context.close()
    browser.close()


uvicorn_path = __import__("shutil").which("uvicorn")
if not uvicorn_path:
    raise RuntimeError("uvicorn not found")
process = subprocess.Popen([uvicorn_path, "docs_src.separate_openapi_schemas.tutorial001:app"], shell=False, close_fds=True)
try:
    with sync_playwright() as playwright:
        run(playwright)
finally:
    process.terminate()
