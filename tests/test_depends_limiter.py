from contextlib import asynccontextmanager

import anyio
import sniffio
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing_extensions import Annotated


def get_borrowed_tokens():
    return {lname: lobj.borrowed_tokens for lname, lobj in sorted(limiters.items())}


def limited_dep():
    # run this in the event loop thread:
    tokens = anyio.from_thread.run_sync(get_borrowed_tokens)
    yield tokens


def init_limiters():
    return {
        "default": None,  # should be set in Lifespan handler
        "a": anyio.CapacityLimiter(5),
        "b": anyio.CapacityLimiter(3),
    }


# Note:
# initializing CapacityLimiters at module level before the event loop has started
# needs anyio >= 4.2.0; starlette currently requires anyio >= 3.4.0
# see https://github.com/agronholm/anyio/pull/651

# The following is a temporary workaround for anyio < 4.2.0:
try:
    limiters = init_limiters()
except sniffio.AsyncLibraryNotFoundError:
    # not in an async context yet
    async def _init_limiters():
        return init_limiters()

    limiters = anyio.run(_init_limiters)


@asynccontextmanager
async def lifespan(app: FastAPI):
    limiters["default"] = anyio.to_thread.current_default_thread_limiter()
    yield {
        "limiters": limiters,
    }


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(borrowed_tokens: Annotated[dict, Depends(limited_dep)]):
    return borrowed_tokens


@app.get("/a")
async def a(
    borrowed_tokens: Annotated[dict, Depends(limited_dep, limiter=limiters["a"])],
):
    return borrowed_tokens


@app.get("/b")
async def b(
    borrowed_tokens: Annotated[dict, Depends(limited_dep, limiter=limiters["b"])],
):
    return borrowed_tokens


def test_depends_limiter():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == {"a": 0, "b": 0, "default": 1}

        response = client.get("/a")
        assert response.status_code == 200, response.text
        assert response.json() == {"a": 1, "b": 0, "default": 0}

        response = client.get("/b")
        assert response.status_code == 200, response.text
        assert response.json() == {"a": 0, "b": 1, "default": 0}


def test_openapi_schema():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
        assert response.json()["paths"] == {
            "/": {
                "get": {
                    "summary": "Root",
                    "operationId": "root__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
            "/a": {
                "get": {
                    "summary": "A",
                    "operationId": "a_a_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
            "/b": {
                "get": {
                    "summary": "B",
                    "operationId": "b_b_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
        }
