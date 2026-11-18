from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()

captured: dict[str, Any] = {}


async def handler() -> int:
    return "not an int"  # type: ignore[return-value]  # ty: ignore[invalid-return-type]


app.add_api_route("/a", handler)
app.add_api_route("/b", handler)


@app.exception_handler(ResponseValidationError)
async def capture_handler(request: Request, exc: ResponseValidationError):
    assert exc.endpoint_ctx is not None
    captured[request.url.path] = exc.endpoint_ctx
    return JSONResponse({"path": exc.endpoint_ctx.get("path")}, status_code=500)


client = TestClient(app)


def test_endpoint_context_is_not_shared_between_routes():
    captured.clear()
    response_a = client.get("/a")
    assert response_a.json() == {"path": "GET /a"}
    response_b = client.get("/b")
    assert response_b.json() == {"path": "GET /b"}
    # The context of the error raised for /a must not be modified by the later
    # request to /b, even though both routes use the same endpoint function
    assert captured["/a"]["path"] == "GET /a"
    assert captured["/b"]["path"] == "GET /b"
    assert captured["/a"] is not captured["/b"]
