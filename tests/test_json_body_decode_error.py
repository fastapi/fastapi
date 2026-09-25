import pytest
from dirty_equals import IsDict
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


INVALID_JSON = """
{
  "name": "Test",
  "price": 'invalid'
}"""


class Item(BaseModel):
    name: str
    price: float
    description: str = None


@app.post("/items/")
async def create_item(item: Item):
    return item  # pragma: no cover


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
    response = client.post(
        "/items/", content=INVALID_JSON, headers={"Content-Type": "application/json"}
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


@pytest.mark.parametrize(
    "json_content,expected_starts_with_ellipsis,expected_ends_with_ellipsis",
    [
        (
            '{"field": invalid, "padding_field": "this needs to be long enough that we have more than forty characters after the error position"}',
            False,
            True,
        ),
        (
            '{"very_long_field_name_here": "some value that is long enough to push us past the forty character mark", "another_field": invalid}',
            True,
            False,
        ),
        (
            '{"very_long_field_name_here": "some value", "field": invalid, "padding_field": "this needs to be long enough that we have more than forty characters after the error position"}',
            True,
            True,
        ),
        ('{"field": invalid}', False, False),
    ],
)
def test_json_decode_error_snippet_ellipsis(
    json_content, expected_starts_with_ellipsis, expected_ends_with_ellipsis
):
    response = client.post(
        "/items/", content=json_content, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
    error = response.json()["detail"][0]

    assert error["msg"] == "JSON decode error"
    assert error["input"] == {}
    assert "invalid" in error["ctx"]["snippet"]
    assert error["type"] == "json_invalid"

    snippet = error["ctx"]["snippet"]
    assert snippet.startswith("...") == expected_starts_with_ellipsis
    assert snippet.endswith("...") == expected_ends_with_ellipsis
