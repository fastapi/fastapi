import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_HTTP_FAVICON_URL = "http://favicon-url.com/favicon.png"
TEST_HTTPS_FAVICON_URL = "http://favicon-url.com/favicon.png"
LOCAL_FILE_FAVICON_URL = "/static/favicon.ico"
DEFAULT_FASTAPI_FAVICON = "https://fastapi.tiangolo.com/img/favicon.png"


@pytest.fixture
def app_with_custom_docs_logo():
    def app_wrapper(favicon_url=None, skip_favicon=False):
        if skip_favicon:
            app = FastAPI()
        else:
            app = FastAPI(favicon_url=favicon_url)

        @app.get("/items/")
        async def read_items():
            return {"id": "foo"}

        return app

    return app_wrapper


@pytest.mark.parametrize(
    "input_favicon_url,generated_favicon_url",
    [
        [TEST_HTTP_FAVICON_URL, TEST_HTTP_FAVICON_URL],
        [TEST_HTTPS_FAVICON_URL, TEST_HTTPS_FAVICON_URL],
        [LOCAL_FILE_FAVICON_URL, LOCAL_FILE_FAVICON_URL],
        [None, DEFAULT_FASTAPI_FAVICON],
    ],
)
def test_docs_ui_loads_custom_logo(
    input_favicon_url, generated_favicon_url, app_with_custom_docs_logo
):
    client = TestClient(app_with_custom_docs_logo(input_favicon_url))
    response = client.get("/docs")
    redoc_response = client.get("/redoc")

    assert response.status_code == 200, response.text
    assert redoc_response.status_code == 200, redoc_response.text
    assert generated_favicon_url in response.text
    assert generated_favicon_url in redoc_response.text


def test_docs_ui_loads_default_logo_when_no_logo_set(app_with_custom_docs_logo):
    client = TestClient(app_with_custom_docs_logo(skip_favicon=True))
    response = client.get("/docs")
    redoc_response = client.get("/redoc")
    items_response = client.get("/items/")

    assert items_response.json() == {"id": "foo"}
    assert response.status_code == 200, response.text
    assert redoc_response.status_code == 200, redoc_response.text
    assert DEFAULT_FASTAPI_FAVICON in response.text
    assert DEFAULT_FASTAPI_FAVICON in redoc_response.text
