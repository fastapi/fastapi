from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, HttpUrl
from starlette.responses import JSONResponse


class CustomModel(BaseModel):
    a: int


app = FastAPI()

callback_router = APIRouter(default_response_class=JSONResponse)


@callback_router.get(
    "{$callback_url}/callback/", responses={400: {"model": CustomModel}}
)
def callback_route():
    pass  # pragma: no cover


@app.post("/", callbacks=callback_router.routes)
def main_route(callback_url: HttpUrl):
    pass  # pragma: no cover


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "post": {
                "summary": "Main Route",
                "operationId": "main_route__post",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Callback Url",
                            "maxLength": 2083,
                            "minLength": 1,
                            "type": "string",
                            "format": "uri",
                        },
                        "name": "callback_url",
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
                "callbacks": {
                    "callback_route": {
                        "{$callback_url}/callback/": {
                            "get": {
                                "summary": "Callback Route",
                                "operationId": "callback_route__callback_url__callback__get",
                                "responses": {
                                    "400": {
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/CustomModel"
                                                }
                                            }
                                        },
                                        "description": "Bad Request",
                                    },
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {"application/json": {"schema": {}}},
                                    },
                                },
                            }
                        }
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "CustomModel": {
                "title": "CustomModel",
                "required": ["a"],
                "type": "object",
                "properties": {"a": {"title": "A", "type": "integer"}},
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
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema
