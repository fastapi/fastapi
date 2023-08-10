import pydantic
from fastapi import (
    Cookie,
    CookieEx,
    FastAPI,
    Form,
    FormEx,
    Header,
    HeaderEx,
    Path,
    PathEx,
    Query,
    QueryEx,
)
from fastapi.testclient import TestClient
from typing_extensions import TypedDict

app = FastAPI()


@app.post("/some/{p}")
def with_shortcuts(
    c: Cookie[int],
    f: Form[int],
    h: Header[int],
    p: Path[int],
    q: Query[int],
):
    return {
        "q": q,
        "c": c,
        "f": f,
        "h": h,
        "p": p,
    }


class P(TypedDict):
    ge: int
    # le ... etc


@app.post("/some-ex/{p}")
def with_shortcuts_ex(
    c: CookieEx[int, P(ge=1)],
    f: FormEx[int, P(ge=1)],
    h: HeaderEx[int, P(ge=1)],
    p: PathEx[int, P(ge=1)],
    q: QueryEx[int, P(ge=1)],
):
    return {
        "q": q,
        "c": c,
        "f": f,
        "h": h,
        "p": p,
    }


def test_shortcuts():
    client = TestClient(app, cookies={"c": "2"})
    response = client.post("/some/5?q=1", headers={"H": "4"}, data={"f": 3})
    assert response.status_code == 200, response.json()
    assert response.json() == {
        "q": 1,
        "c": 2,
        "f": 3,
        "h": 4,
        "p": 5,
    }


def test_shortcuts_not_valid():
    client = TestClient(app, cookies={"c": "0"})
    response = client.post("/some-ex/0?q=0", headers={"H": "0"}, data={"f": 0})
    assert response.status_code == 422, response.json()
    print(response.json())
    if pydantic.__version__.split(".")[0] == "1":
        assert response.json()["detail"] == [
            {
                "loc": ["path", "p"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["query", "q"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["header", "h"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["cookie", "c"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
                "ctx": {"limit_value": 1},
            },
            {
                "loc": ["body", "f"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
                "ctx": {"limit_value": 1},
            },
        ]
    else:
        assert response.json()["detail"] == [
            {
                "type": "greater_than_equal",
                "loc": ["path", "p"],
                "msg": "Input should be greater than or equal to 1",
                "input": "0",
                "ctx": {"ge": 1},
                "url": "https://errors.pydantic.dev/2.1/v/greater_than_equal",
            },
            {
                "type": "greater_than_equal",
                "loc": ["query", "q"],
                "msg": "Input should be greater than or equal to 1",
                "input": "0",
                "ctx": {"ge": 1},
                "url": "https://errors.pydantic.dev/2.1/v/greater_than_equal",
            },
            {
                "type": "greater_than_equal",
                "loc": ["header", "h"],
                "msg": "Input should be greater than or equal to 1",
                "input": "0",
                "ctx": {"ge": 1},
                "url": "https://errors.pydantic.dev/2.1/v/greater_than_equal",
            },
            {
                "type": "greater_than_equal",
                "loc": ["cookie", "c"],
                "msg": "Input should be greater than or equal to 1",
                "input": "0",
                "ctx": {"ge": 1},
                "url": "https://errors.pydantic.dev/2.1/v/greater_than_equal",
            },
            {
                "type": "greater_than_equal",
                "loc": ["body", "f"],
                "msg": "Input should be greater than or equal to 1",
                "input": "0",
                "ctx": {"ge": 1},
                "url": "https://errors.pydantic.dev/2.1/v/greater_than_equal",
            },
        ]


def test_shortcuts_ex():
    client = TestClient(app, cookies={"c": "2"})
    response = client.post("/some-ex/5?q=1", headers={"H": "4"}, data={"f": 3})
    assert response.status_code == 200, response.json()
    assert response.json() == {
        "q": 1,
        "c": 2,
        "f": 3,
        "h": 4,
        "p": 5,
    }


def test_shortcuts_ex_schema():
    schema = app.openapi()
    print(schema)
    assert schema["paths"] == {
        "/some/{p}": {
            "post": {
                "summary": "With Shortcuts",
                "operationId": "with_shortcuts_some__p__post",
                "parameters": [
                    {
                        "name": "p",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer", "title": "P"},
                    },
                    {
                        "name": "q",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "integer", "title": "Q"},
                    },
                    {
                        "name": "h",
                        "in": "header",
                        "required": True,
                        "schema": {"type": "integer", "title": "H"},
                    },
                    {
                        "name": "c",
                        "in": "cookie",
                        "required": True,
                        "schema": {"type": "integer", "title": "C"},
                    },
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_with_shortcuts_some__p__post"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
        "/some-ex/{p}": {
            "post": {
                "summary": "With Shortcuts Ex",
                "operationId": "with_shortcuts_ex_some_ex__p__post",
                "parameters": [
                    {
                        "name": "p",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer", "minimum": 1, "title": "P"},
                    },
                    {
                        "name": "q",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "integer", "minimum": 1, "title": "Q"},
                    },
                    {
                        "name": "h",
                        "in": "header",
                        "required": True,
                        "schema": {"type": "integer", "minimum": 1, "title": "H"},
                    },
                    {
                        "name": "c",
                        "in": "cookie",
                        "required": True,
                        "schema": {"type": "integer", "minimum": 1, "title": "C"},
                    },
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_with_shortcuts_ex_some_ex__p__post"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        },
    }
