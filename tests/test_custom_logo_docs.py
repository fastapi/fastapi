from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_HTTP_FAVICON_URL = "http://favicon-url.com/favicon.png"
TEST_HTTPS_FAVICON_URL = "http://favicon-url.com/favicon.png"
DEFAULT_FASTAPI_FAVICON = "https://fastapi.tiangolo.com/img/favicon.png"


def get_client_with_custom_docs_logo(favicon_url):
    app = FastAPI(favicon_url=favicon_url)

    @app.get("/items/")
    async def read_items():
        return {"id": "foo"}

    return TestClient(app)


@pytest.mark.parametrize(
    "input_favicon_url,generated_favicon_url",
    [
        [TEST_HTTP_FAVICON_URL, TEST_HTTP_FAVICON_URL],
        [TEST_HTTPS_FAVICON_URL, TEST_HTTPS_FAVICON_URL],
        [None, DEFAULT_FASTAPI_FAVICON],
    ],
)
def test_docs_ui_loads_custom_logo(input_favicon_url, generated_favicon_url):
    client = get_client_with_custom_docs_logo(input_favicon_url)
    response = client.get("/docs")
    redoc_response = client.get("/redoc")

    assert response.status_code == 200, response.text
    assert redoc_response.status_code == 200, redoc_response.text
    assert generated_favicon_url in response.text
    assert generated_favicon_url in redoc_response.text


def test_docs_ui_load_file_as_custom_logo(tmp_path):
    favicon_filename = "custom-favicon.png"
    file_path: Path = tmp_path / favicon_filename
    test_content = b"Fake favicon bytes"
    file_path.write_bytes(test_content)
    client = get_client_with_custom_docs_logo(str(file_path))
    response = client.get("/docs")
    redoc_response = client.get("/redoc")

    assert response.status_code == 200, response.text
    assert redoc_response.status_code == 200, redoc_response.text
    assert favicon_filename in response.text
    assert favicon_filename in redoc_response.text


def test_items_response():
    client = get_client_with_custom_docs_logo(None)
    response = client.get("/items/")
    assert response.json() == {"id": "foo"}
