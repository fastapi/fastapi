from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/items/")
async def create_item(data: dict):
    return data


client = TestClient(app)


def test_json_content_type_with_charset_utf8():
    """Content-Type: application/json; charset=utf-8 should be accepted."""
    response = client.post(
        "/items/",
        content='{"key": "value"}',
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


def test_vendor_json_content_type_with_charset_utf8():
    """Content-Type: application/vnd.api+json; charset=utf-8 should be accepted."""
    response = client.post(
        "/items/",
        content='{"key": "value"}',
        headers={"Content-Type": "application/vnd.api+json; charset=utf-8"},
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


def test_json_content_type_with_charset_iso_8859_1():
    """Content-Type: application/json; charset=iso-8859-1 should be accepted."""
    response = client.post(
        "/items/",
        content='{"key": "value"}',
        headers={"Content-Type": "application/json; charset=iso-8859-1"},
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}


def test_text_plain_content_type_is_rejected():
    """Content-Type: text/plain should be rejected with 422."""
    response = client.post(
        "/items/",
        content='{"key": "value"}',
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 422
