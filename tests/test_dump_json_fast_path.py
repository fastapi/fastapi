from unittest.mock import patch

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get("/default")
def get_default() -> Item:
    return Item(name="widget", price=9.99)


@app.get("/explicit", response_class=JSONResponse)
def get_explicit() -> Item:
    return Item(name="widget", price=9.99)


client = TestClient(app)


def test_default_response_class_skips_json_dumps():
    """When no response_class is set, the fast path serializes directly to
    JSON bytes via Pydantic's dump_json and never calls json.dumps."""
    with patch(
        "starlette.responses.json.dumps", wraps=__import__("json").dumps
    ) as mock_dumps:
        response = client.get("/default")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}
    mock_dumps.assert_not_called()


def test_explicit_response_class_uses_json_dumps():
    """When response_class is explicitly set to JSONResponse, the normal path
    is used and json.dumps is called via JSONResponse.render()."""
    with patch(
        "starlette.responses.json.dumps", wraps=__import__("json").dumps
    ) as mock_dumps:
        response = client.get("/explicit")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}
    mock_dumps.assert_called_once()


class CustomJSONResponse(JSONResponse):
    media_type = "application/vnd.custom+json"


app_custom_default = FastAPI(default_response_class=CustomJSONResponse)


@app_custom_default.get("/default")
def get_default_custom() -> Item:
    return Item(name="widget", price=9.99)


client_custom_default = TestClient(app_custom_default)


def test_app_level_default_response_class_skips_fast_path():
    """When a custom default_response_class is set at the app level (not
    per-route), the fast path must NOT be used, so the custom response
    class's own rendering (and media_type) is respected instead of being
    bypassed by the generic dump_json Response."""
    with patch(
        "starlette.responses.json.dumps", wraps=__import__("json").dumps
    ) as mock_dumps:
        response = client_custom_default.get("/default")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "price": 9.99}
    assert response.headers["content-type"] == "application/vnd.custom+json"
    mock_dumps.assert_called_once()
