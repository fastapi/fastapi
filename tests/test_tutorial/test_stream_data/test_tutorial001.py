import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.stream_data.{request.param}")

    client = TestClient(mod.app)
    return client


expected_text = (
    ""
    "Rick: (stumbles in drunkenly, and turns on the lights)"
    " Morty! You gotta come on. You got--... you gotta come with me."
    "Morty: (rubs his eyes) What, Rick? What's going on?"
    "Rick: I got a surprise for you, Morty."
    "Morty: It's the middle of the night. What are you talking about?"
    "Rick: (spills alcohol on Morty's bed) Come on, I got a surprise for you."
    " (drags Morty by the ankle) Come on, hurry up."
    " (pulls Morty out of his bed and into the hall)"
    "Morty: Ow! Ow! You're tugging me too hard!"
    "Rick: We gotta go, gotta get outta here, come on."
    " Got a surprise for you Morty."
)


@pytest.mark.parametrize(
    "path",
    [
        "/story/stream",
        "/story/stream-no-async",
        "/story/stream-no-annotation",
        "/story/stream-no-async-no-annotation",
        "/story/stream-bytes",
        "/story/stream-no-async-bytes",
        "/story/stream-no-annotation-bytes",
        "/story/stream-no-async-no-annotation-bytes",
    ],
)
def test_stream_story(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.text == expected_text


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/story/stream": {
                    "get": {
                        "summary": "Stream Story",
                        "operationId": "stream_story_story_stream_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-no-async": {
                    "get": {
                        "summary": "Stream Story No Async",
                        "operationId": "stream_story_no_async_story_stream_no_async_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-no-annotation": {
                    "get": {
                        "summary": "Stream Story No Annotation",
                        "operationId": "stream_story_no_annotation_story_stream_no_annotation_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-no-async-no-annotation": {
                    "get": {
                        "summary": "Stream Story No Async No Annotation",
                        "operationId": "stream_story_no_async_no_annotation_story_stream_no_async_no_annotation_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-bytes": {
                    "get": {
                        "summary": "Stream Story Bytes",
                        "operationId": "stream_story_bytes_story_stream_bytes_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-no-async-bytes": {
                    "get": {
                        "summary": "Stream Story No Async Bytes",
                        "operationId": "stream_story_no_async_bytes_story_stream_no_async_bytes_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-no-annotation-bytes": {
                    "get": {
                        "summary": "Stream Story No Annotation Bytes",
                        "operationId": "stream_story_no_annotation_bytes_story_stream_no_annotation_bytes_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
                "/story/stream-no-async-no-annotation-bytes": {
                    "get": {
                        "summary": "Stream Story No Async No Annotation Bytes",
                        "operationId": "stream_story_no_async_no_annotation_bytes_story_stream_no_async_no_annotation_bytes_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                            }
                        },
                    }
                },
            },
        }
    )
