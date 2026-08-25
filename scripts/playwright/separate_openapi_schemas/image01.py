import subprocess

from playwright.sync_api import Playwright, sync_playwright


# Run playwright codegen to generate the code below, copy paste the sections in run()
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # Update the viewport manually
    context = browser.new_context(viewport={"width": 960, "height": 1080})
    page = context.new_page()
    page.goto("http://localhost:8000/docs")
    page.get_by_text("POST/items/Create Item").click()
    page.get_by_role("tab", name="Schema").first.click()
    # Manually add the screenshot
    page.screenshot(
        path="docs/en/docs/img/tutorial/separate-openapi-schemas/image01.png"
    )

    # ---------------------
    context.close()
    browser.close()


process = subprocess.Popen([(lambda p: p if p is not None else (_ for _ in ()).throw(FileNotFoundError("uvicorn not found")))(__import__('shutil').which('uvicorn')), "docs_src.separate_openapi_schemas.tutorial001:app"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
try:
    with sync_playwright() as playwright:
        run(playwright)
finally:
    process.terminate()
