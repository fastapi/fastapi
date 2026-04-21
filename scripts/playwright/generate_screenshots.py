"""Generate screenshots for FastAPI documentation.

Usage:
    python generate_screenshots.py                        # Generate all screenshots
    python generate_screenshots.py <name>                 # Generate a specific screenshot
    python generate_screenshots.py --list                 # List available screenshot names
"""

import subprocess
import time

import httpx
from playwright.sync_api import Page, sync_playwright


def wait_for_server(
    url: str = "http://localhost:8000/docs", *, retries: int = 10
) -> None:
    """Wait for the server to be ready by polling the given URL."""
    for _ in range(retries):
        try:
            response = httpx.get(url)
            if response.status_code == 200:
                break
        except httpx.ConnectError:
            time.sleep(1)


# ---- Interaction steps for each screenshot ----


def separate_openapi_schemas_image01(page: Page) -> None:
    page.get_by_text("POST/items/Create Item").click()
    page.get_by_role("tab", name="Schema").first.click()


def separate_openapi_schemas_image02(page: Page) -> None:
    page.get_by_text("GET/items/Read Items").click()
    page.get_by_role("button", name="Try it out").click()
    page.get_by_role("button", name="Execute").click()


def separate_openapi_schemas_image03(page: Page) -> None:
    page.get_by_text("GET/items/Read Items").click()
    page.get_by_role("tab", name="Schema").click()
    page.get_by_label("Schema").get_by_role("button", name="Expand all").click()


def separate_openapi_schemas_image04(page: Page) -> None:
    page.get_by_role("button", name="Item", exact=True).click()
    page.set_viewport_size({"width": 960, "height": 820})


def separate_openapi_schemas_image05(page: Page) -> None:
    page.get_by_role("button", name="Item", exact=True).click()
    page.set_viewport_size({"width": 960, "height": 700})


def request_form_models_image01(page: Page) -> None:
    page.get_by_role("button", name="POST /login/ Login").click()
    page.get_by_role("button", name="Try it out").click()


def header_param_models_image01(page: Page) -> None:
    page.get_by_role("button", name="GET /items/ Read Items").click()
    page.get_by_role("button", name="Try it out").click()


def json_base64_bytes_image01(page: Page) -> None:
    page.get_by_role("button", name="POST /data Post Data").click()


def cookie_param_models_image01(page: Page) -> None:
    page.get_by_role("link", name="/items/").click()


def query_param_models_image01(page: Page) -> None:
    page.get_by_role("button", name="GET /items/ Read Items").click()
    page.get_by_role("button", name="Try it out").click()
    page.get_by_role("heading", name="Servers").click()


def sql_databases_image01(page: Page) -> None:
    page.get_by_label("post /heroes/").click()


def sql_databases_image02(page: Page) -> None:
    page.get_by_label("post /heroes/").click()


# ---- Screenshot configurations ----

SCREENSHOTS: list[dict] = [
    # separate_openapi_schemas
    {
        "name": "separate_openapi_schemas_image01",
        "cmd": ["fastapi", "run", "docs_src/separate_openapi_schemas/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": separate_openapi_schemas_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/separate-openapi-schemas/image01.png",
    },
    {
        "name": "separate_openapi_schemas_image02",
        "cmd": ["fastapi", "run", "docs_src/separate_openapi_schemas/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": separate_openapi_schemas_image02,
        "screenshot_path": "docs/en/docs/img/tutorial/separate-openapi-schemas/image02.png",
    },
    {
        "name": "separate_openapi_schemas_image03",
        "cmd": ["fastapi", "run", "docs_src/separate_openapi_schemas/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": separate_openapi_schemas_image03,
        "screenshot_path": "docs/en/docs/img/tutorial/separate-openapi-schemas/image03.png",
    },
    {
        "name": "separate_openapi_schemas_image04",
        "cmd": ["fastapi", "run", "docs_src/separate_openapi_schemas/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": separate_openapi_schemas_image04,
        "screenshot_path": "docs/en/docs/img/tutorial/separate-openapi-schemas/image04.png",
    },
    {
        "name": "separate_openapi_schemas_image05",
        "cmd": ["fastapi", "run", "docs_src/separate_openapi_schemas/tutorial002_py310.py"],
        "wait_for_server": True,
        "interact": separate_openapi_schemas_image05,
        "screenshot_path": "docs/en/docs/img/tutorial/separate-openapi-schemas/image05.png",
    },
    # request_form_models
    {
        "name": "request_form_models_image01",
        "cmd": ["fastapi", "run", "docs_src/request_form_models/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": request_form_models_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/request-form-models/image01.png",
    },
    # header_param_models
    {
        "name": "header_param_models_image01",
        "cmd": ["fastapi", "run", "docs_src/header_param_models/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": header_param_models_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/header-param-models/image01.png",
    },
    # json_base64_bytes
    {
        "name": "json_base64_bytes_image01",
        "cmd": ["fastapi", "run", "docs_src/json_base64_bytes/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": json_base64_bytes_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/json-base64-bytes/image01.png",
    },
    # cookie_param_models
    {
        "name": "cookie_param_models_image01",
        "cmd": ["fastapi", "run", "docs_src/cookie_param_models/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": cookie_param_models_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/cookie-param-models/image01.png",
    },
    # query_param_models
    {
        "name": "query_param_models_image01",
        "cmd": ["fastapi", "run", "docs_src/query_param_models/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": query_param_models_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/query-param-models/image01.png",
    },
    # sql_databases
    {
        "name": "sql_databases_image01",
        "cmd": ["fastapi", "run", "docs_src/sql_databases/tutorial001_py310.py"],
        "wait_for_server": True,
        "interact": sql_databases_image01,
        "screenshot_path": "docs/en/docs/img/tutorial/sql-databases/image01.png",
    },
    {
        "name": "sql_databases_image02",
        "cmd": ["fastapi", "run", "docs_src/sql_databases/tutorial002_py310.py"],
        "wait_for_server": True,
        "interact": sql_databases_image02,
        "screenshot_path": "docs/en/docs/img/tutorial/sql-databases/image02.png",
    },
]


def generate_screenshot(config: dict) -> None:
    """Generate a single screenshot based on the given configuration."""
    process = subprocess.Popen(config["cmd"])
    try:
        if config.get("wait_for_server"):
            wait_for_server()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            # Update the viewport manually
            context = browser.new_context(viewport={"width": 960, "height": 1080})
            page = context.new_page()
            page.goto("http://localhost:8000/docs")

            # Run custom interaction steps
            config["interact"](page)

            # Manually add the screenshot
            page.screenshot(path=config["screenshot_path"])

            # ---------------------
            context.close()
            browser.close()
    finally:
        process.terminate()


if __name__ == "__main__":
    import sys

    if "--list" in sys.argv:
        for config in SCREENSHOTS:
            print(config["name"])
        sys.exit(0)

    name = sys.argv[1] if len(sys.argv) > 1 else None
    failed: list[str] = []
    for config in SCREENSHOTS:
        if name is None or config["name"] == name:
            try:
                generate_screenshot(config)
            except Exception as e:
                print(f"ERROR: Failed to generate '{config['name']}': {e}")
                failed.append(config["name"])
    if failed:
        print(f"\nFailed screenshots: {', '.join(failed)}")
        sys.exit(1)
