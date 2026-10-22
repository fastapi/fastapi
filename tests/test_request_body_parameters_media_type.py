from typing import Annotated

import pytest
from fastapi import Body, Depends, FastAPI, File, Form
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel

app = FastAPI()

media_type = "application/vnd.api+json"


# NOTE: These are not valid JSON:API resources
# but they are fine for testing requestBody with custom media_type
class Product(BaseModel):
    name: str
    price: float


class Shop(BaseModel):
    name: str


@app.post("/products")
async def create_product(data: Product = Body(media_type=media_type, embed=True)):
    pass  # pragma: no cover


@app.post("/shops")
async def create_shop(
    data: Shop = Body(media_type=media_type),
    included: list[Product] = Body(default=[], media_type=media_type),
):
    pass  # pragma: no cover


client = TestClient(app)


@pytest.mark.parametrize(
    "first_media_type, second_media_type, expected_media_type",
    [
        (
            "application/x-www-form-urlencoded",
            "application/x-www-form-urlencoded",
            "application/x-www-form-urlencoded",
        ),
        (
            "multipart/form-data",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ),
        (
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "multipart/form-data",
        ),
        ("multipart/form-data", "multipart/form-data", "multipart/form-data"),
        (
            "application/x-www-form-urlencoded; charset=utf-8",
            "application/x-www-form-urlencoded; charset=utf-8",
            "application/x-www-form-urlencoded; charset=utf-8",
        ),
        (
            "application/x-www-form-urlencoded; charset=utf-8",
            "application/x-www-form-urlencoded",
            "application/x-www-form-urlencoded",
        ),
    ],
)
def test_form_parameter_media_types(
    first_media_type, second_media_type, expected_media_type
):
    app = FastAPI()

    @app.post("/")
    def submit(
        name: Annotated[str, Form(media_type=first_media_type)],
        token: Annotated[str, Form(media_type=second_media_type)],
    ):
        return {"name": name, "token": token}

    client = TestClient(app)
    if expected_media_type == "multipart/form-data":
        response = client.post(
            "/", files={"name": (None, "Rick"), "token": (None, "secret")}
        )
    else:
        response = client.post(
            "/",
            content="name=Rick&token=secret",
            headers={"content-type": expected_media_type},
        )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick", "token": "secret"}
    content = app.openapi()["paths"]["/"]["post"]["requestBody"]["content"]
    assert list(content) == [expected_media_type]


@pytest.mark.parametrize("in_dependency", [False, True])
def test_form_model_media_type(in_dependency):
    app = FastAPI()

    class Profile(BaseModel):
        name: str

    class Preferences(BaseModel):
        limit: int

    def preferences_dependency(
        preferences: Annotated[Preferences, Form(media_type="multipart/form-data")],
    ):
        return preferences

    marker = (
        Depends(preferences_dependency)
        if in_dependency
        else Form(media_type="multipart/form-data")
    )

    @app.post("/")
    def submit(
        profile: Annotated[Profile, Form()],
        preferences: Annotated[Preferences, marker],
        token: Annotated[str, Form()],
    ):
        return {"profile": profile, "preferences": preferences, "token": token}

    response = TestClient(app).post(
        "/",
        files={"name": (None, "Rick"), "limit": (None, "2"), "token": (None, "secret")},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "profile": {"name": "Rick"},
        "preferences": {"limit": 2},
        "token": "secret",
    }
    schema = app.openapi()
    content = schema["paths"]["/"]["post"]["requestBody"]["content"]
    assert list(content) == ["multipart/form-data"]
    ref = content["multipart/form-data"]["schema"]["$ref"].rsplit("/", 1)[-1]
    body = schema["components"]["schemas"][ref]
    assert set(body["properties"]) == {"token"}
    assert {item["$ref"] for item in body["allOf"]} == {
        "#/components/schemas/Profile",
        "#/components/schemas/Preferences",
    }
    assert schema["components"]["schemas"]["Profile"]["required"] == ["name"]
    assert schema["components"]["schemas"]["Preferences"]["required"] == ["limit"]


def test_file_media_type_takes_precedence_over_form_media_type():
    app = FastAPI()

    @app.post("/")
    def submit(
        name: Annotated[
            str, Form(media_type="application/x-www-form-urlencoded; charset=utf-8")
        ],
        attachment: Annotated[bytes, File()],
    ):
        return {"name": name, "attachment": attachment}

    response = TestClient(app).post(
        "/", data={"name": "Rick"}, files={"attachment": ("hello.txt", b"hello")}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Rick", "attachment": "hello"}
    content = app.openapi()["paths"]["/"]["post"]["requestBody"]["content"]
    assert list(content) == ["multipart/form-data"]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/products": {
                    "post": {
                        "summary": "Create Product",
                        "operationId": "create_product_products_post",
                        "requestBody": {
                            "content": {
                                "application/vnd.api+json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_create_product_products_post"
                                    }
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
                "/shops": {
                    "post": {
                        "summary": "Create Shop",
                        "operationId": "create_shop_shops_post",
                        "requestBody": {
                            "content": {
                                "application/vnd.api+json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_create_shop_shops_post"
                                    }
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
            },
            "components": {
                "schemas": {
                    "Body_create_product_products_post": {
                        "title": "Body_create_product_products_post",
                        "required": ["data"],
                        "type": "object",
                        "properties": {
                            "data": {"$ref": "#/components/schemas/Product"}
                        },
                    },
                    "Body_create_shop_shops_post": {
                        "title": "Body_create_shop_shops_post",
                        "required": ["data"],
                        "type": "object",
                        "properties": {
                            "data": {"$ref": "#/components/schemas/Shop"},
                            "included": {
                                "title": "Included",
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/Product"},
                                "default": [],
                            },
                        },
                    },
                    "HTTPValidationError": {
                        "title": "HTTPValidationError",
                        "type": "object",
                        "properties": {
                            "detail": {
                                "title": "Detail",
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                    "Product": {
                        "title": "Product",
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"title": "Name", "type": "string"},
                            "price": {"title": "Price", "type": "number"},
                        },
                    },
                    "Shop": {
                        "title": "Shop",
                        "required": ["name"],
                        "type": "object",
                        "properties": {"name": {"title": "Name", "type": "string"}},
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
                            "input": {"title": "Input"},
                            "ctx": {"title": "Context", "type": "object"},
                        },
                    },
                }
            },
        }
    )
