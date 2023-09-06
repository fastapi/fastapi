from typing import Union

import pytest
from dirty_equals import IsDict
from fastapi import Body, Cookie, FastAPI, Header, Path, Query
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict


def create_app():
    app = FastAPI()

    class Item(BaseModel):
        data: str

        if PYDANTIC_V2:
            model_config = ConfigDict(
                json_schema_extra={"example": {"data": "Data in schema_extra"}}
            )
        else:

            class Config:
                schema_extra = {"example": {"data": "Data in schema_extra"}}

    @app.post("/schema_extra/")
    def schema_extra(item: Item):
        return item

    with pytest.warns(DeprecationWarning):

        @app.post("/example/")
        def example(item: Item = Body(example={"data": "Data in Body example"})):
            return item

    @app.post("/examples/")
    def examples(
        item: Item = Body(
            examples=[
                {"data": "Data in Body examples, example1"},
                {"data": "Data in Body examples, example2"},
            ],
        )
    ):
        return item

    with pytest.warns(DeprecationWarning):

        @app.post("/example_examples/")
        def example_examples(
            item: Item = Body(
                example={"data": "Overridden example"},
                examples=[
                    {"data": "examples example_examples 1"},
                    {"data": "examples example_examples 2"},
                ],
            )
        ):
            return item

    # TODO: enable these tests once/if Form(embed=False) is supported
    # TODO: In that case, define if File() should support example/examples too
    # @app.post("/form_example")
    # def form_example(firstname: str = Form(example="John")):
    #     return firstname

    # @app.post("/form_examples")
    # def form_examples(
    #     lastname: str = Form(
    #         ...,
    #         examples={
    #             "example1": {"summary": "last name summary", "value": "Doe"},
    #             "example2": {"value": "Doesn't"},
    #         },
    #     ),
    # ):
    #     return lastname

    # @app.post("/form_example_examples")
    # def form_example_examples(
    #     lastname: str = Form(
    #         ...,
    #         example="Doe overridden",
    #         examples={
    #             "example1": {"summary": "last name summary", "value": "Doe"},
    #             "example2": {"value": "Doesn't"},
    #         },
    #     ),
    # ):
    #     return lastname

    with pytest.warns(DeprecationWarning):

        @app.get("/path_example/{item_id}")
        def path_example(
            item_id: str = Path(
                example="item_1",
            ),
        ):
            return item_id

    @app.get("/path_examples/{item_id}")
    def path_examples(
        item_id: str = Path(
            examples=["item_1", "item_2"],
        ),
    ):
        return item_id

    with pytest.warns(DeprecationWarning):

        @app.get("/path_example_examples/{item_id}")
        def path_example_examples(
            item_id: str = Path(
                example="item_overridden",
                examples=["item_1", "item_2"],
            ),
        ):
            return item_id

    with pytest.warns(DeprecationWarning):

        @app.get("/query_example/")
        def query_example(
            data: Union[str, None] = Query(
                default=None,
                example="query1",
            ),
        ):
            return data

    @app.get("/query_examples/")
    def query_examples(
        data: Union[str, None] = Query(
            default=None,
            examples=["query1", "query2"],
        ),
    ):
        return data

    with pytest.warns(DeprecationWarning):

        @app.get("/query_example_examples/")
        def query_example_examples(
            data: Union[str, None] = Query(
                default=None,
                example="query_overridden",
                examples=["query1", "query2"],
            ),
        ):
            return data

    with pytest.warns(DeprecationWarning):

        @app.get("/header_example/")
        def header_example(
            data: Union[str, None] = Header(
                default=None,
                example="header1",
            ),
        ):
            return data

    @app.get("/header_examples/")
    def header_examples(
        data: Union[str, None] = Header(
            default=None,
            examples=[
                "header1",
                "header2",
            ],
        ),
    ):
        return data

    with pytest.warns(DeprecationWarning):

        @app.get("/header_example_examples/")
        def header_example_examples(
            data: Union[str, None] = Header(
                default=None,
                example="header_overridden",
                examples=["header1", "header2"],
            ),
        ):
            return data

    with pytest.warns(DeprecationWarning):

        @app.get("/cookie_example/")
        def cookie_example(
            data: Union[str, None] = Cookie(
                default=None,
                example="cookie1",
            ),
        ):
            return data

    @app.get("/cookie_examples/")
    def cookie_examples(
        data: Union[str, None] = Cookie(
            default=None,
            examples=["cookie1", "cookie2"],
        ),
    ):
        return data

    with pytest.warns(DeprecationWarning):

        @app.get("/cookie_example_examples/")
        def cookie_example_examples(
            data: Union[str, None] = Cookie(
                default=None,
                example="cookie_overridden",
                examples=["cookie1", "cookie2"],
            ),
        ):
            return data

    return app


def test_call_api():
    app = create_app()
    client = TestClient(app)
    response = client.post("/schema_extra/", json={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.post("/example/", json={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.post("/examples/", json={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.post("/example_examples/", json={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.get("/path_example/foo")
    assert response.status_code == 200, response.text
    response = client.get("/path_examples/foo")
    assert response.status_code == 200, response.text
    response = client.get("/path_example_examples/foo")
    assert response.status_code == 200, response.text
    response = client.get("/query_example/")
    assert response.status_code == 200, response.text
    response = client.get("/query_examples/")
    assert response.status_code == 200, response.text
    response = client.get("/query_example_examples/")
    assert response.status_code == 200, response.text
    response = client.get("/header_example/")
    assert response.status_code == 200, response.text
    response = client.get("/header_examples/")
    assert response.status_code == 200, response.text
    response = client.get("/header_example_examples/")
    assert response.status_code == 200, response.text
    response = client.get("/cookie_example/")
    assert response.status_code == 200, response.text
    response = client.get("/cookie_examples/")
    assert response.status_code == 200, response.text
    response = client.get("/cookie_example_examples/")
    assert response.status_code == 200, response.text


def test_openapi_schema():
    """
    Test that example overrides work:

    * pydantic model schema_extra is included
    * Body(example={}) overrides schema_extra in pydantic model
    * Body(examples{}) overrides Body(example={}) and schema_extra in pydantic model
    """
    app = create_app()
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/schema_extra/": {
                "post": {
                    "summary": "Schema Extra",
                    "operationId": "schema_extra_schema_extra__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                        "required": True,
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
            "/example/": {
                "post": {
                    "summary": "Example",
                    "operationId": "example_example__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"},
                                "example": {"data": "Data in Body example"},
                            }
                        },
                        "required": True,
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
            "/examples/": {
                "post": {
                    "summary": "Examples",
                    "operationId": "examples_examples__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": IsDict(
                                    {
                                        "$ref": "#/components/schemas/Item",
                                        "examples": [
                                            {"data": "Data in Body examples, example1"},
                                            {"data": "Data in Body examples, example2"},
                                        ],
                                    }
                                )
                                | IsDict(
                                    # TODO: remove this when deprecating Pydantic v1
                                    {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Item",
                                        "examples": [
                                            {"data": "Data in Body examples, example1"},
                                            {"data": "Data in Body examples, example2"},
                                        ],
                                    }
                                )
                            }
                        },
                        "required": True,
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
            "/example_examples/": {
                "post": {
                    "summary": "Example Examples",
                    "operationId": "example_examples_example_examples__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": IsDict(
                                    {
                                        "$ref": "#/components/schemas/Item",
                                        "examples": [
                                            {"data": "examples example_examples 1"},
                                            {"data": "examples example_examples 2"},
                                        ],
                                    }
                                )
                                | IsDict(
                                    # TODO: remove this when deprecating Pydantic v1
                                    {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Item",
                                        "examples": [
                                            {"data": "examples example_examples 1"},
                                            {"data": "examples example_examples 2"},
                                        ],
                                    },
                                ),
                                "example": {"data": "Overridden example"},
                            }
                        },
                        "required": True,
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
            "/path_example/{item_id}": {
                "get": {
                    "summary": "Path Example",
                    "operationId": "path_example_path_example__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "string"},
                            "example": "item_1",
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
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
            "/path_examples/{item_id}": {
                "get": {
                    "summary": "Path Examples",
                    "operationId": "path_examples_path_examples__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "string",
                                "examples": ["item_1", "item_2"],
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
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
            "/path_example_examples/{item_id}": {
                "get": {
                    "summary": "Path Example Examples",
                    "operationId": "path_example_examples_path_example_examples__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "string",
                                "examples": ["item_1", "item_2"],
                            },
                            "example": "item_overridden",
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
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
            "/query_example/": {
                "get": {
                    "summary": "Query Example",
                    "operationId": "query_example_query_example__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {"title": "Data", "type": "string"}
                            ),
                            "example": "query1",
                            "name": "data",
                            "in": "query",
                        }
                    ],
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
            "/query_examples/": {
                "get": {
                    "summary": "Query Examples",
                    "operationId": "query_examples_query_examples__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                    "examples": ["query1", "query2"],
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {
                                    "type": "string",
                                    "title": "Data",
                                    "examples": ["query1", "query2"],
                                }
                            ),
                            "name": "data",
                            "in": "query",
                        }
                    ],
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
            "/query_example_examples/": {
                "get": {
                    "summary": "Query Example Examples",
                    "operationId": "query_example_examples_query_example_examples__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                    "examples": ["query1", "query2"],
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {
                                    "type": "string",
                                    "title": "Data",
                                    "examples": ["query1", "query2"],
                                }
                            ),
                            "example": "query_overridden",
                            "name": "data",
                            "in": "query",
                        }
                    ],
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
            "/header_example/": {
                "get": {
                    "summary": "Header Example",
                    "operationId": "header_example_header_example__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {"title": "Data", "type": "string"}
                            ),
                            "example": "header1",
                            "name": "data",
                            "in": "header",
                        }
                    ],
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
            "/header_examples/": {
                "get": {
                    "summary": "Header Examples",
                    "operationId": "header_examples_header_examples__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                    "examples": ["header1", "header2"],
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {
                                    "type": "string",
                                    "title": "Data",
                                    "examples": ["header1", "header2"],
                                }
                            ),
                            "name": "data",
                            "in": "header",
                        }
                    ],
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
            "/header_example_examples/": {
                "get": {
                    "summary": "Header Example Examples",
                    "operationId": "header_example_examples_header_example_examples__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                    "examples": ["header1", "header2"],
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {
                                    "title": "Data",
                                    "type": "string",
                                    "examples": ["header1", "header2"],
                                }
                            ),
                            "example": "header_overridden",
                            "name": "data",
                            "in": "header",
                        }
                    ],
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
            "/cookie_example/": {
                "get": {
                    "summary": "Cookie Example",
                    "operationId": "cookie_example_cookie_example__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {"title": "Data", "type": "string"}
                            ),
                            "example": "cookie1",
                            "name": "data",
                            "in": "cookie",
                        }
                    ],
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
            "/cookie_examples/": {
                "get": {
                    "summary": "Cookie Examples",
                    "operationId": "cookie_examples_cookie_examples__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                    "examples": ["cookie1", "cookie2"],
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {
                                    "title": "Data",
                                    "type": "string",
                                    "examples": ["cookie1", "cookie2"],
                                }
                            ),
                            "name": "data",
                            "in": "cookie",
                        }
                    ],
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
            "/cookie_example_examples/": {
                "get": {
                    "summary": "Cookie Example Examples",
                    "operationId": "cookie_example_examples_cookie_example_examples__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Data",
                                    "examples": ["cookie1", "cookie2"],
                                }
                            )
                            | IsDict(
                                # TODO: Remove this when deprecating Pydantic v1
                                {
                                    "title": "Data",
                                    "type": "string",
                                    "examples": ["cookie1", "cookie2"],
                                }
                            ),
                            "example": "cookie_overridden",
                            "name": "data",
                            "in": "cookie",
                        }
                    ],
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
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
                "Item": {
                    "title": "Item",
                    "required": ["data"],
                    "type": "object",
                    "properties": {"data": {"title": "Data", "type": "string"}},
                    "example": {"data": "Data in schema_extra"},
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
            }
        },
    }
