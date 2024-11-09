import typing

from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
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
    included: typing.List[Product] = Body(default=[], media_type=media_type),
):
    pass  # pragma: no cover


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
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
                    "properties": {"data": {"$ref": "#/components/schemas/Product"}},
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
                            "items": {"$ref": "#/components/schemas/ValidationError"},
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
                    },
                },
            }
        },
    }
