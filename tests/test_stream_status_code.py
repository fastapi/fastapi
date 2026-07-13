from collections.abc import AsyncIterable

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.responses import EventSourceResponse, StreamingResponse
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

SSE_RESPONSE = {
    "description": "Successful Response",
    "content": {
        "text/event-stream": {
            "itemSchema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "contentMediaType": "application/json",
                        "contentSchema": {
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                            "title": "SSE stream item",
                        },
                    },
                    "event": {"type": "string"},
                    "id": {"type": "string"},
                    "retry": {"type": "integer", "minimum": 0},
                },
                "required": ["data"],
            }
        }
    },
}

JSONL_RESPONSE = {
    "description": "Successful Response",
    "content": {
        "application/jsonl": {
            "itemSchema": {
                "type": "object",
                "additionalProperties": {"type": "string"},
                "title": "JSONL stream item",
            }
        }
    },
}


app = FastAPI()


def set_accepted(response: Response) -> None:
    response.status_code = 202


@app.post("/sse", response_class=EventSourceResponse, status_code=201)
async def sse() -> AsyncIterable[dict[str, str]]:
    yield {"message": "created"}


@app.post("/jsonl", status_code=201)
async def jsonl() -> AsyncIterable[dict[str, str]]:
    yield {"message": "created"}


@app.post("/raw", response_class=StreamingResponse, status_code=201)
async def raw() -> AsyncIterable[str]:
    yield "accepted"


@app.post(
    "/sse-dependency",
    response_class=EventSourceResponse,
    responses={202: SSE_RESPONSE},
)
async def sse_dependency(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "accepted"}


@app.post("/jsonl-dependency", responses={202: JSONL_RESPONSE})
async def jsonl_dependency(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "accepted"}


@app.post(
    "/raw-dependency",
    response_class=StreamingResponse,
    responses={202: {"description": "Accepted"}},
)
async def raw_dependency(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[str]:
    yield "accepted"


@app.post(
    "/sse-dependency-override",
    response_class=EventSourceResponse,
    status_code=201,
    responses={202: SSE_RESPONSE},
)
async def sse_dependency_override(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "overridden"}


@app.post(
    "/jsonl-dependency-override",
    status_code=201,
    responses={202: JSONL_RESPONSE},
)
async def jsonl_dependency_override(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "overridden"}


@app.post(
    "/raw-dependency-override",
    response_class=StreamingResponse,
    status_code=201,
    responses={202: {"description": "Accepted"}},
)
async def raw_dependency_override(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[str]:
    yield "overridden"


client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status_code",
    [
        ("/sse", 201),
        ("/jsonl", 201),
        ("/raw", 201),
        ("/sse-dependency", 202),
        ("/jsonl-dependency", 202),
        ("/raw-dependency", 202),
        ("/sse-dependency-override", 202),
        ("/jsonl-dependency-override", 202),
        ("/raw-dependency-override", 202),
    ],
)
def test_status_code(path: str, expected_status_code: int) -> None:
    response = client.post(path)
    assert response.status_code == expected_status_code


def test_openapi() -> None:
    openapi = app.openapi()

    assert openapi == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/sse": {
                    "post": {
                        "summary": "Sse",
                        "operationId": "sse_sse_post",
                        "responses": {
                            "201": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "type": "object",
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "title": "Streamitem Sse Sse Post",
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/jsonl": {
                    "post": {
                        "summary": "Jsonl",
                        "operationId": "jsonl_jsonl_post",
                        "responses": {
                            "201": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {
                                            "type": "object",
                                            "additionalProperties": {"type": "string"},
                                            "title": "Streamitem Jsonl Jsonl Post",
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/raw": {
                    "post": {
                        "summary": "Raw",
                        "operationId": "raw_raw_post",
                        "responses": {"201": {"description": "Successful Response"}},
                    }
                },
                "/sse-dependency": {
                    "post": {
                        "summary": "Sse Dependency",
                        "operationId": "sse_dependency_sse_dependency_post",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "type": "object",
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "title": "Streamitem Sse Dependency Sse Dependency Post",
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            },
                            "202": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "type": "object",
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "title": "SSE stream item",
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/jsonl-dependency": {
                    "post": {
                        "summary": "Jsonl Dependency",
                        "operationId": "jsonl_dependency_jsonl_dependency_post",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {
                                            "type": "object",
                                            "additionalProperties": {"type": "string"},
                                            "title": "Streamitem Jsonl Dependency Jsonl Dependency Post",
                                        }
                                    }
                                },
                            },
                            "202": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {
                                            "type": "object",
                                            "additionalProperties": {"type": "string"},
                                            "title": "JSONL stream item",
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/raw-dependency": {
                    "post": {
                        "summary": "Raw Dependency",
                        "operationId": "raw_dependency_raw_dependency_post",
                        "responses": {
                            "200": {"description": "Successful Response"},
                            "202": {"description": "Accepted"},
                        },
                    }
                },
                "/sse-dependency-override": {
                    "post": {
                        "summary": "Sse Dependency Override",
                        "operationId": "sse_dependency_override_sse_dependency_override_post",
                        "responses": {
                            "201": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "type": "object",
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "title": "Streamitem Sse Dependency Override Sse Dependency Override Post",
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            },
                            "202": {
                                "description": "Successful Response",
                                "content": {
                                    "text/event-stream": {
                                        "itemSchema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "string",
                                                    "contentMediaType": "application/json",
                                                    "contentSchema": {
                                                        "type": "object",
                                                        "additionalProperties": {
                                                            "type": "string"
                                                        },
                                                        "title": "SSE stream item",
                                                    },
                                                },
                                                "event": {"type": "string"},
                                                "id": {"type": "string"},
                                                "retry": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                },
                                            },
                                            "required": ["data"],
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/jsonl-dependency-override": {
                    "post": {
                        "summary": "Jsonl Dependency Override",
                        "operationId": "jsonl_dependency_override_jsonl_dependency_override_post",
                        "responses": {
                            "201": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {
                                            "type": "object",
                                            "additionalProperties": {"type": "string"},
                                            "title": "Streamitem Jsonl Dependency Override Jsonl Dependency Override Post",
                                        }
                                    }
                                },
                            },
                            "202": {
                                "description": "Successful Response",
                                "content": {
                                    "application/jsonl": {
                                        "itemSchema": {
                                            "type": "object",
                                            "additionalProperties": {"type": "string"},
                                            "title": "JSONL stream item",
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/raw-dependency-override": {
                    "post": {
                        "summary": "Raw Dependency Override",
                        "operationId": "raw_dependency_override_raw_dependency_override_post",
                        "responses": {
                            "201": {"description": "Successful Response"},
                            "202": {"description": "Accepted"},
                        },
                    }
                },
            },
        }
    )
