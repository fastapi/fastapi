import json

import pytest
from fastapi import APIRouter, FastAPI
from pydantic import UUID4, BaseModel, UrlStr
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

app = FastAPI()

# Model definitions
class HealthResponse(BaseModel):
    status: str


class HealthRequest(BaseModel):
    endpoint_name: str


class ClientInfo(BaseModel):
    name: str
    health: UrlStr = None


class ClientAddedResponse(BaseModel):
    id: UUID4


callback_router = APIRouter()


@callback_router.get(
    "{$request.body.health}",
    name="health",
    response_model=HealthResponse,
    response_class=JSONResponse,
)
async def health(endpoint: str):
    return {"status": f"{endpoint} ok"}


@app.post(
    "/clients/", response_model=ClientAddedResponse, callbacks=callback_router.routes
)
async def register_client(client_info: ClientInfo):
    pass


client = TestClient(app)

expected_schema = """
{
  "openapi": "3.0.2",
  "info": {
    "title": "Fast API",
    "version": "0.1.0"
  },
  "paths": {
    "/clients/": {
      "post": {
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ClientAddedResponse"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "summary": "Register Client",
        "operationId": "register_client_clients__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ClientInfo"
              }
            }
          },
          "required": true
        },
        "callbacks": {
          "health": {
            "{$request.body.health}": {
              "get": {
                "summary": "Health",
                "operationId": "health_$request.body.health__get",
                "parameters": [
                  {
                    "name": "endpoint",
                    "in": "query",
                    "required": true,
                    "schema": {
                      "title": "Endpoint",
                      "type": "string"
                    }
                  }
                ],
                "responses": {
                  "200": {
                    "description": "Successful Response",
                    "content": {
                      "application/json": {
                        "schema": {
                          "$ref": "#/components/schemas/HealthResponse"
                        }
                      }
                    }
                  },
                  "422": {
                    "description": "Validation Error",
                    "content": {
                      "application/json": {
                        "schema": {
                          "$ref": "#/components/schemas/HTTPValidationError"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "ClientAddedResponse": {
        "title": "ClientAddedResponse",
        "required": [
          "id"
        ],
        "type": "object",
        "properties": {
          "id": {
            "title": "Id",
            "type": "string",
            "format": "uuid4"
          }
        }
      },
      "ClientInfo": {
        "title": "ClientInfo",
        "required": [
          "name"
        ],
        "type": "object",
        "properties": {
          "name": {
            "title": "Name",
            "type": "string"
          },
          "health": {
            "title": "Health",
            "maxLength": 65536,
            "minLength": 1,
            "type": "string",
            "format": "uri"
          }
        }
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
            }
          }
        }
      },
      "HealthResponse": {
        "title": "HealthResponse",
        "required": [
          "status"
        ],
        "type": "object",
        "properties": {
          "status": {
            "title": "Status",
            "type": "string"
          }
        }
      },
      "ValidationError": {
        "title": "ValidationError",
        "required": [
          "loc",
          "msg",
          "type"
        ],
        "type": "object",
        "properties": {
          "loc": {
            "title": "Location",
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "msg": {
            "title": "Message",
            "type": "string"
          },
          "type": {
            "title": "Error Type",
            "type": "string"
          }
        }
      }
    }
  }
}
"""

schema_as_dict = json.loads(expected_schema)


def test_openapi_callback():
    with client:
        response = client.get("/openapi.json")

        assert response.json() == schema_as_dict
