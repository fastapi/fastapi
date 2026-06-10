from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from starlette.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
)

app = FastAPI()


class Item(BaseModel):
    name: str


class User(BaseModel):
    username: str
    age: int


@app.get("/none")
def none() -> None:
    return None


@app.get("/response")
def response() -> Response:
    return Response(content="ok")


@app.get("/response-or-none")
def response_or_none() -> Response | None:
    return Response(content="ok")


@app.get("/plaintext-response")
def plaintext_response() -> PlainTextResponse:
    return PlainTextResponse("ok")


@app.get("/html-response")
def html_response() -> HTMLResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get("/none-or-html-response")
def none_or_html_response() -> None | HTMLResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get("/json-response")
def json_response() -> JSONResponse:
    return JSONResponse({"x": 1})


@app.get("/json-response-or-none")
def json_response_or_none() -> JSONResponse | None:
    return JSONResponse({"x": 1})


@app.get("/streaming-response")
def streaming_response() -> StreamingResponse:
    return StreamingResponse(iter((b"x",)))


@app.get("/file-response")
def file_response() -> FileResponse:
    return FileResponse(__file__)


@app.get("/redirect-response")
def redirect_response() -> RedirectResponse:
    return RedirectResponse("https://example.com")


@app.get("/response-or-item-response")
def response_or_item_response() -> Response | Item:
    return JSONResponse({"name": "foo"})


@app.get("/response-or-item-dict")
def response_or_item_dict() -> Response | Item:
    return {"name": "foo"}


@app.get("/response-or-item-model")
def response_or_item_model() -> Response | Item:
    return Item(name="foo")


@app.get("/item-or-html-response")
def item_or_html_response() -> Item | HTMLResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get("/item-or-html-response-or-none")
def item_or_html_response_or_none() -> Item | HTMLResponse | None:
    return HTMLResponse("<h1>ok</h1>")


@app.get("/plaintext-response-or-html-response")
def plaintext_response_or_html_response() -> PlainTextResponse | HTMLResponse:
    return PlainTextResponse("ok")


@app.get("/html-response-or-plaintext-response")
def html_response_or_plaintext_response() -> HTMLResponse | PlainTextResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get("/html-response-or-plaintext-response-or-none")
def html_response_or_plaintext_response_or_none() -> (
    HTMLResponse | PlainTextResponse | None
):
    return HTMLResponse("<h1>ok</h1>")


@app.get("/three-responses")
def three_responses() -> PlainTextResponse | HTMLResponse | JSONResponse:
    return JSONResponse({"x": 1})


@app.get("/three-responses-or-none")
def three_responses_or_none() -> JSONResponse | None | HTMLResponse | PlainTextResponse:
    return JSONResponse({"x": 1})


@app.get("/two-models-or-response")
def two_models_or_response() -> Item | Response | User:
    return JSONResponse({"name": "foo"})


@app.get("/two-models-or-html-response")
def two_models_or_html_response() -> User | Item | HTMLResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get("/two-models-or-two-responses")
def two_models_or_two_responses() -> Item | PlainTextResponse | User | RedirectResponse:
    return User(username="foo", age=42)


@app.get("/two-models-or-two-responses-or-none")
def two_models_or_two_responses_or_none() -> (
    User | RedirectResponse | None | Item | PlainTextResponse
):
    return User(username="foo", age=42)


@app.get(
    "/decorator-response-matches-return-response",
    response_class=HTMLResponse,
)
def decorator_response_matches_return_response() -> HTMLResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get(
    "/decorator-response-differs-from-return-response",
    response_class=PlainTextResponse,
)
def decorator_response_differs_from_return_response() -> HTMLResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get(
    "/decorator-response-in-return-response-union",
    response_class=HTMLResponse,
)
def decorator_response_in_return_response_union() -> HTMLResponse | PlainTextResponse:
    return HTMLResponse("<h1>ok</h1>")


@app.get(
    "/decorator-response-not-in-return-response-union",
    response_class=RedirectResponse,
)
def decorator_response_not_in_return_response_union() -> (
    PlainTextResponse | JSONResponse
):
    return JSONResponse({"x": 1})


@app.get(
    "/decorator-response-with-str-in-return-union-response",
    response_class=PlainTextResponse,
)
def decorator_response_with_str_in_return_union_response() -> HTMLResponse | str:
    return HTMLResponse("<h1>ok</h1>")


@app.get(
    "/decorator-response-with-str-in-return-union-str",
    response_class=PlainTextResponse,
)
def decorator_response_with_str_in_return_union_str() -> HTMLResponse | str:
    return "ok"


@app.get(
    "/decorator-response-with-dict-in-return-union",
    response_class=JSONResponse,
)
def decorator_response_with_dict_in_return_union() -> RedirectResponse | dict[str, str]:
    return {"name": "foo"}


@app.get(
    "/decorator-response-with-model-in-return-union",
    response_class=JSONResponse,
)
def decorator_response_with_model_in_return_union() -> RedirectResponse | User:
    return User(username="foo", age=42)


@app.get(
    "/decorator-response-with-model-and-int-in-return-union",
    response_class=JSONResponse,
)
def decorator_response_with_multiple_non_response_in_return_union() -> (
    User | int | PlainTextResponse
):
    return 1


@app.get(
    "/decorator-response-with-model-and-str-in-return-union",
    response_class=JSONResponse,
)
def decorator_response_with_model_and_str_in_return_union() -> (
    User | PlainTextResponse | str
):
    return "ok"


client = TestClient(app)


def test_none():
    response = client.get("/none")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() is None


def test_response():
    response = client.get("/response")
    assert response.status_code == 200
    assert "content-type" not in response.headers
    assert response.text == "ok"


def test_response_or_none():
    response = client.get("/response-or-none")
    assert response.status_code == 200
    assert "content-type" not in response.headers
    assert response.text == "ok"


def test_plaintext_response():
    response = client.get("/plaintext-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "ok"


def test_html_response():
    response = client.get("/html-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_none_or_html_response():
    response = client.get("/none-or-html-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_json_response():
    response = client.get("/json-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"x": 1}


def test_json_response_or_none():
    response = client.get("/json-response-or-none")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"x": 1}


def test_streaming_response():
    response = client.get("/streaming-response")
    assert response.status_code == 200
    assert "content-type" not in response.headers


def test_file_response():
    response = client.get("/file-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/x-python")


def test_redirect_response():
    response = client.get("/redirect-response", follow_redirects=False)
    assert response.status_code == 307
    assert "content-type" not in response.headers


def test_response_or_item_response():
    response = client.get("/response-or-item-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"name": "foo"}


def test_response_or_item_dict():
    response = client.get("/response-or-item-dict")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"name": "foo"}


def test_response_or_item_model():
    response = client.get("/response-or-item-model")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"name": "foo"}


def test_item_or_html_response():
    response = client.get("/item-or-html-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_item_or_html_response_or_none():
    response = client.get("/item-or-html-response-or-none")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_plaintext_response_or_html_response():
    response = client.get("/plaintext-response-or-html-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "ok"


def test_html_response_or_plaintext_response():
    response = client.get("/html-response-or-plaintext-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_html_response_or_plaintext_response_or_none():
    response = client.get("/html-response-or-plaintext-response-or-none")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_three_responses():
    response = client.get("/three-responses")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"x": 1}


def test_three_responses_or_none():
    response = client.get("/three-responses-or-none")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"x": 1}


def test_two_models_or_response():
    response = client.get("/two-models-or-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"name": "foo"}


def test_two_models_or_html_response():
    response = client.get("/two-models-or-html-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_two_models_or_two_responses():
    response = client.get("/two-models-or-two-responses")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"username": "foo", "age": 42}


def test_two_models_or_two_responses_or_none():
    response = client.get("/two-models-or-two-responses-or-none")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"username": "foo", "age": 42}


def test_decorator_response_matches_return_response():
    response = client.get("/decorator-response-matches-return-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_decorator_response_differs_from_return_response():
    response = client.get("/decorator-response-differs-from-return-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_decorator_response_in_return_response_union():
    response = client.get("/decorator-response-in-return-response-union")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_decorator_response_not_in_return_response_union():
    response = client.get("/decorator-response-not-in-return-response-union")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"x": 1}


def test_decorator_response_with_str_in_return_union_response():
    response = client.get("/decorator-response-with-str-in-return-union-response")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == "<h1>ok</h1>"


def test_decorator_response_with_str_in_return_union_str():
    response = client.get("/decorator-response-with-str-in-return-union-str")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "ok"


def test_decorator_response_with_dict_in_return_union():
    response = client.get("/decorator-response-with-dict-in-return-union")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"name": "foo"}


def test_decorator_response_with_model_in_return_union():
    response = client.get("/decorator-response-with-model-in-return-union")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"username": "foo", "age": 42}


def test_decorator_response_with_model_and_int_in_return_union():
    response = client.get("/decorator-response-with-model-and-int-in-return-union")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == 1


def test_decorator_response_with_model_and_str_in_return_union():
    response = client.get("/decorator-response-with-model-and-str-in-return-union")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.text == '"ok"'


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/none": {
                    "get": {
                        "summary": "None",
                        "operationId": "none_none_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                },
                "/response": {
                    "get": {
                        "summary": "Response",
                        "operationId": "response_response_get",
                        "responses": {"200": {"description": "Successful Response"}},
                    }
                },
                "/response-or-none": {
                    "get": {
                        "summary": "Response Or None",
                        "operationId": "response_or_none_response_or_none_get",
                        "responses": {"200": {"description": "Successful Response"}},
                    }
                },
                "/plaintext-response": {
                    "get": {
                        "summary": "Plaintext Response",
                        "operationId": "plaintext_response_plaintext_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/html-response": {
                    "get": {
                        "summary": "Html Response",
                        "operationId": "html_response_html_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/none-or-html-response": {
                    "get": {
                        "summary": "None Or Html Response",
                        "operationId": "none_or_html_response_none_or_html_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/json-response": {
                    "get": {
                        "summary": "Json Response",
                        "operationId": "json_response_json_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                },
                "/json-response-or-none": {
                    "get": {
                        "summary": "Json Response Or None",
                        "operationId": "json_response_or_none_json_response_or_none_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                },
                "/streaming-response": {
                    "get": {
                        "summary": "Streaming Response",
                        "operationId": "streaming_response_streaming_response_get",
                        "responses": {"200": {"description": "Successful Response"}},
                    }
                },
                "/file-response": {
                    "get": {
                        "summary": "File Response",
                        "operationId": "file_response_file_response_get",
                        "responses": {"200": {"description": "Successful Response"}},
                    }
                },
                "/redirect-response": {
                    "get": {
                        "summary": "Redirect Response",
                        "operationId": "redirect_response_redirect_response_get",
                        "responses": {"307": {"description": "Successful Response"}},
                    }
                },
                "/response-or-item-response": {
                    "get": {
                        "summary": "Response Or Item Response",
                        "operationId": "response_or_item_response_response_or_item_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            }
                        },
                    }
                },
                "/response-or-item-dict": {
                    "get": {
                        "summary": "Response Or Item Dict",
                        "operationId": "response_or_item_dict_response_or_item_dict_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            }
                        },
                    }
                },
                "/response-or-item-model": {
                    "get": {
                        "summary": "Response Or Item Model",
                        "operationId": "response_or_item_model_response_or_item_model_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            }
                        },
                    }
                },
                "/item-or-html-response": {
                    "get": {
                        "summary": "Item Or Html Response",
                        "operationId": "item_or_html_response_item_or_html_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    },
                                    "text/html": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/item-or-html-response-or-none": {
                    "get": {
                        "summary": "Item Or Html Response Or None",
                        "operationId": "item_or_html_response_or_none_item_or_html_response_or_none_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    },
                                    "text/html": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/plaintext-response-or-html-response": {
                    "get": {
                        "summary": "Plaintext Response Or Html Response",
                        "operationId": "plaintext_response_or_html_response_plaintext_response_or_html_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}},
                                    "text/html": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/html-response-or-plaintext-response": {
                    "get": {
                        "summary": "Html Response Or Plaintext Response",
                        "operationId": "html_response_or_plaintext_response_html_response_or_plaintext_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}},
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/html-response-or-plaintext-response-or-none": {
                    "get": {
                        "summary": "Html Response Or Plaintext Response Or None",
                        "operationId": "html_response_or_plaintext_response_or_none_html_response_or_plaintext_response_or_none_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}},
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/three-responses": {
                    "get": {
                        "summary": "Three Responses",
                        "operationId": "three_responses_three_responses_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}},
                                    "text/html": {"schema": {"type": "string"}},
                                    "application/json": {"schema": {}},
                                },
                            }
                        },
                    }
                },
                "/three-responses-or-none": {
                    "get": {
                        "summary": "Three Responses Or None",
                        "operationId": "three_responses_or_none_three_responses_or_none_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {"schema": {}},
                                    "text/html": {"schema": {"type": "string"}},
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/two-models-or-response": {
                    "get": {
                        "summary": "Two Models Or Response",
                        "operationId": "two_models_or_response_two_models_or_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/Item"},
                                                {"$ref": "#/components/schemas/User"},
                                            ],
                                            "title": "Response Two Models Or Response Two Models Or Response Get",
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/two-models-or-html-response": {
                    "get": {
                        "summary": "Two Models Or Html Response",
                        "operationId": "two_models_or_html_response_two_models_or_html_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/User"},
                                                {"$ref": "#/components/schemas/Item"},
                                            ],
                                            "title": "Response Two Models Or Html Response Two Models Or Html Response Get",
                                        }
                                    },
                                    "text/html": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/two-models-or-two-responses": {
                    "get": {
                        "summary": "Two Models Or Two Responses",
                        "operationId": "two_models_or_two_responses_two_models_or_two_responses_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/Item"},
                                                {"$ref": "#/components/schemas/User"},
                                            ],
                                            "title": "Response Two Models Or Two Responses Two Models Or Two Responses Get",
                                        }
                                    },
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            },
                            "307": {"description": "Successful Response"},
                        },
                    }
                },
                "/two-models-or-two-responses-or-none": {
                    "get": {
                        "summary": "Two Models Or Two Responses Or None",
                        "operationId": "two_models_or_two_responses_or_none_two_models_or_two_responses_or_none_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/User"},
                                                {"$ref": "#/components/schemas/Item"},
                                            ],
                                            "title": "Response Two Models Or Two Responses Or None Two Models Or Two Responses Or None Get",
                                        }
                                    },
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            },
                            "307": {"description": "Successful Response"},
                        },
                    }
                },
                "/decorator-response-matches-return-response": {
                    "get": {
                        "summary": "Decorator Response Matches Return Response",
                        "operationId": "decorator_response_matches_return_response_decorator_response_matches_return_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/decorator-response-differs-from-return-response": {
                    "get": {
                        "summary": "Decorator Response Differs From Return Response",
                        "operationId": "decorator_response_differs_from_return_response_decorator_response_differs_from_return_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}}
                                },
                            }
                        },
                    }
                },
                "/decorator-response-in-return-response-union": {
                    "get": {
                        "summary": "Decorator Response In Return Response Union",
                        "operationId": "decorator_response_in_return_response_union_decorator_response_in_return_response_union_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/html": {"schema": {"type": "string"}},
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/decorator-response-not-in-return-response-union": {
                    "get": {
                        "summary": "Decorator Response Not In Return Response Union",
                        "operationId": "decorator_response_not_in_return_response_union_decorator_response_not_in_return_response_union_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}},
                                    "application/json": {"schema": {}},
                                },
                            }
                        },
                    }
                },
                "/decorator-response-with-str-in-return-union-response": {
                    "get": {
                        "summary": "Decorator Response With Str In Return Union Response",
                        "operationId": "decorator_response_with_str_in_return_union_response_decorator_response_with_str_in_return_union_response_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}},
                                    "text/html": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/decorator-response-with-str-in-return-union-str": {
                    "get": {
                        "summary": "Decorator Response With Str In Return Union Str",
                        "operationId": "decorator_response_with_str_in_return_union_str_decorator_response_with_str_in_return_union_str_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/plain": {"schema": {"type": "string"}},
                                    "text/html": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/decorator-response-with-dict-in-return-union": {
                    "get": {
                        "summary": "Decorator Response With Dict In Return Union",
                        "operationId": "decorator_response_with_dict_in_return_union_decorator_response_with_dict_in_return_union_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "additionalProperties": {"type": "string"},
                                            "type": "object",
                                            "title": "Response Decorator Response With Dict In Return Union Decorator Response With Dict In Return Union Get",
                                        }
                                    }
                                },
                            },
                            "307": {"description": "Successful Response"},
                        },
                    }
                },
                "/decorator-response-with-model-in-return-union": {
                    "get": {
                        "summary": "Decorator Response With Model In Return Union",
                        "operationId": "decorator_response_with_model_in_return_union_decorator_response_with_model_in_return_union_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/User"}
                                    }
                                },
                            },
                            "307": {"description": "Successful Response"},
                        },
                    }
                },
                "/decorator-response-with-model-and-int-in-return-union": {
                    "get": {
                        "summary": "Decorator Response With Multiple Non Response In Return Union",
                        "operationId": "decorator_response_with_multiple_non_response_in_return_union_decorator_response_with_model_and_int_in_return_union_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/User"},
                                                {"type": "integer"},
                                            ],
                                            "title": "Response Decorator Response With Multiple Non Response In Return Union Decorator Response With Model And Int In Return Union Get",
                                        }
                                    },
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
                "/decorator-response-with-model-and-str-in-return-union": {
                    "get": {
                        "summary": "Decorator Response With Model And Str In Return Union",
                        "operationId": "decorator_response_with_model_and_str_in_return_union_decorator_response_with_model_and_str_in_return_union_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/User"},
                                                {"type": "string"},
                                            ],
                                            "title": "Response Decorator Response With Model And Str In Return Union Decorator Response With Model And Str In Return Union Get",
                                        }
                                    },
                                    "text/plain": {"schema": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "Item": {
                        "properties": {"name": {"type": "string", "title": "Name"}},
                        "type": "object",
                        "required": ["name"],
                        "title": "Item",
                    },
                    "User": {
                        "properties": {
                            "username": {"type": "string", "title": "Username"},
                            "age": {"type": "integer", "title": "Age"},
                        },
                        "type": "object",
                        "required": ["username", "age"],
                        "title": "User",
                    },
                }
            },
        }
    )
