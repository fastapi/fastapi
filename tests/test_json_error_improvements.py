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

    assert error["loc"] == ["body", 1, 27]
    assert "line 1" in error["msg"]
    assert "column 27" in error["msg"]
    assert error["ctx"]["line"] == 1
    assert error["ctx"]["column"] == 27
    assert "None" in error["input"]


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

    assert error["loc"] == ["body", 4, 12]
    assert "line 4" in error["msg"]
    assert "column 12" in error["msg"]
    assert error["ctx"]["line"] == 4
    assert error["ctx"]["column"] == 12
    assert "invalid" in error["input"]


def test_json_decode_error_shows_snippet():
    long_json = '{"very_long_field_name_here": "some value", "another_field": invalid}'

    response = client.post(
        "/items/", content=long_json, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert "..." in error["input"]
    assert "invalid" in error["input"]
    assert len(error["input"]) <= 83


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

    assert "line" in error["msg"].lower()
    assert "column" in error["msg"].lower()
    assert error["type"] == "json_invalid"
    assert "position" in error["ctx"]
