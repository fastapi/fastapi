from datetime import datetime

from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()

bearer_scheme = HTTPBearer()


class Subscription(BaseModel):
    username: str
    montly_fee: float
    start_date: datetime


@app.webhooks.post("new-subscription")
def new_subscription(
    body: Subscription, token: Annotated[str, Security(bearer_scheme)]
):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """


client = TestClient(app)


def test_dummy_webhook():
    # Just for coverage
    new_subscription(body={}, token="Bearer 123")


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    # insert_assert(response.json())
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {},
        "webhooks": {
            "new-subscription": {
                "post": {
                    "summary": "New Subscription",
                    "description": "When a new user subscribes to your service we'll send you a POST request with this\ndata to the URL that you register for the event `new-subscription` in the dashboard.",
                    "operationId": "new_subscriptionnew_subscription_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Subscription"}
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
                    "security": [{"HTTPBearer": []}],
                }
            }
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "Subscription": {
                    "properties": {
                        "username": {"type": "string", "title": "Username"},
                        "montly_fee": {"type": "number", "title": "Montly Fee"},
                        "start_date": {
                            "type": "string",
                            "format": "date-time",
                            "title": "Start Date",
                        },
                    },
                    "type": "object",
                    "required": ["username", "montly_fee", "start_date"],
                    "title": "Subscription",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            },
            "securitySchemes": {"HTTPBearer": {"type": "http", "scheme": "bearer"}},
        },
    }
