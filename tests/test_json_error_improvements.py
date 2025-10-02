from dirty_equals import IsDict
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    description: str = None


@app.post("/items/")
async def create_item(item: Item):
    return item


client = TestClient(app)


def test_json_decode_error_single_line():
    response = client.post(
        "/items/",
        content='{"name": "Test", "price": None}',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert error["loc"] == ["body", 26]
    assert error["msg"] == "JSON decode error"
    assert error["input"] == {}
    assert error["ctx"]["error"] == "Expecting value"
    assert error["ctx"]["position"] == 26
    assert error["ctx"]["line"] == 0
    assert error["ctx"]["column"] == 26
    assert "None" in error["ctx"]["snippet"]


def test_json_decode_error_multiline():
    invalid_json = """
{
  "name": "Test",
  "price": 'invalid'
}"""

    response = client.post(
        "/items/", content=invalid_json, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert error["loc"][0] == "body"
    assert isinstance(error["loc"][1], int)
    assert error["msg"] == "JSON decode error"
    assert error["input"] == {}
    assert error["ctx"]["line"] == 3
    assert error["ctx"]["column"] == 11
    assert "invalid" in error["ctx"]["snippet"]


def test_json_decode_error_shows_snippet():
    long_json = '{"very_long_field_name_here": "some value", "another_field": invalid}'

    response = client.post(
        "/items/", content=long_json, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert error["msg"] == "JSON decode error"
    assert error["input"] == {}
    assert "invalid" in error["ctx"]["snippet"]
    assert len(error["ctx"]["snippet"]) <= 83


def test_json_decode_error_empty_body():
    response = client.post(
        "/items/", content="", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    # Handle both Pydantic v1 and v2 - empty body is handled differently
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "Field required",
                    "type": "missing",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_json_decode_error_unclosed_brace():
    response = client.post(
        "/items/",
        content='{"name": "Test"',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert error["msg"] == "JSON decode error"
    assert error["type"] == "json_invalid"
    assert error["input"] == {}
    assert "position" in error["ctx"]
    assert "line" in error["ctx"]
    assert "column" in error["ctx"]
    assert "snippet" in error["ctx"]


def test_json_decode_error_in_middle_of_long_document():
    # Create a JSON with error early in a long document (need >40 chars after error)
    # The error is at position for "invalid" which needs at least 41 chars after it
    long_json = '{"field": invalid, "padding_field": "this needs to be long enough that we have more than forty characters after the error position"}'

    response = client.post(
        "/items/", content=long_json, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert error["msg"] == "JSON decode error"
    assert error["input"] == {}
    assert error["ctx"]["snippet"].endswith("...")
    assert "invalid" in error["ctx"]["snippet"]
    assert error["type"] == "json_invalid"


def test_successful_item_creation():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 19.99, "description": "A test item"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 19.99
    assert data["description"] == "A test item"
