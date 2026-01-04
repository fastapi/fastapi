# Test with parts from, and to verify the report in:
# https://github.com/fastapi/fastapi/discussions/14177
# Made an issue in:
# https://github.com/fastapi/fastapi/issues/14247
from enum import Enum

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field


class MessageEventType(str, Enum):
    alpha = "alpha"
    beta = "beta"


class MessageEvent(BaseModel):
    event_type: MessageEventType = Field(default=MessageEventType.alpha)
    output: str


class MessageOutput(BaseModel):
    body: str = ""
    events: list[MessageEvent] = []


class Message(BaseModel):
    input: str
    output: MessageOutput


app = FastAPI(title="Minimal FastAPI App", version="1.0.0")


@app.post("/messages", response_model=Message)
async def create_message(input_message: str) -> Message:
    return Message(
        input=input_message,
        output=MessageOutput(body=f"Processed: {input_message}"),
    )


client = TestClient(app)


def test_create_message():
    response = client.post("/messages", params={"input_message": "Hello"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "input": "Hello",
        "output": {"body": "Processed: Hello", "events": []},
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "Minimal FastAPI App", "version": "1.0.0"},
            "paths": {
                "/messages": {
                    "post": {
                        "summary": "Create Message",
                        "operationId": "create_message_messages_post",
                        "parameters": [
                            {
                                "name": "input_message",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "string", "title": "Input Message"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Message"
                                        }
                                    }
                                },
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
                }
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "Message": {
                        "properties": {
                            "input": {"type": "string", "title": "Input"},
                            "output": {"$ref": "#/components/schemas/MessageOutput"},
                        },
                        "type": "object",
                        "required": ["input", "output"],
                        "title": "Message",
                    },
                    "MessageEvent": {
                        "properties": {
                            "event_type": {
                                "$ref": "#/components/schemas/MessageEventType",
                                "default": "alpha",
                            },
                            "output": {"type": "string", "title": "Output"},
                        },
                        "type": "object",
                        "required": ["output"],
                        "title": "MessageEvent",
                    },
                    "MessageEventType": {
                        "type": "string",
                        "enum": ["alpha", "beta"],
                        "title": "MessageEventType",
                    },
                    "MessageOutput": {
                        "properties": {
                            "body": {"type": "string", "title": "Body", "default": ""},
                            "events": {
                                "items": {"$ref": "#/components/schemas/MessageEvent"},
                                "type": "array",
                                "title": "Events",
                                "default": [],
                            },
                        },
                        "type": "object",
                        "title": "MessageOutput",
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
                }
            },
        }
    )
