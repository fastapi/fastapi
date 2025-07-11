from pathlib import Path
from typing import Optional

from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

router = APIRouter()


class ContentSizeLimitMiddleware:
    """Content size limiting middleware for ASGI applications
    Args:
      app (ASGI application): ASGI application
      max_content_size (optional): the maximum content size allowed in bytes, None for no limit
    """

    def __init__(self, app: APIRouter, max_content_size: Optional[int] = None):
        self.app = app
        self.max_content_size = max_content_size

    def receive_wrapper(self, receive):
        received = 0

        async def inner():
            nonlocal received
            message = await receive()
            if message["type"] != "http.request":
                return message  # pragma: no cover

            body_len = len(message.get("body", b""))
            received += body_len
            if received > self.max_content_size:
                raise HTTPException(
                    422,
                    detail={
                        "name": "ContentSizeLimitExceeded",
                        "code": 999,
                        "message": "File limit exceeded",
                    },
                )
            return message

        return inner

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or self.max_content_size is None:
            await self.app(scope, receive, send)
            return

        wrapper = self.receive_wrapper(receive)
        await self.app(scope, wrapper, send)


@router.post("/middleware")
def run_middleware(file: UploadFile = File(..., description="Big File")):
    return {"message": "OK"}


app.include_router(router)
app.add_middleware(ContentSizeLimitMiddleware, max_content_size=2**8)


client = TestClient(app)


def test_custom_middleware_exception(tmp_path: Path):
    default_pydantic_max_size = 2**16
    path = tmp_path / "test.txt"
    path.write_bytes(b"x" * (default_pydantic_max_size + 1))

    with client:
        with open(path, "rb") as file:
            response = client.post("/middleware", files={"file": file})
        assert response.status_code == 422, response.text
        assert response.json() == {
            "detail": {
                "name": "ContentSizeLimitExceeded",
                "code": 999,
                "message": "File limit exceeded",
            }
        }


def test_custom_middleware_exception_not_raised(tmp_path: Path):
    path = tmp_path / "test.txt"
    path.write_bytes(b"<file content>")

    with client:
        with open(path, "rb") as file:
            response = client.post("/middleware", files={"file": file})
        assert response.status_code == 200, response.text
        assert response.json() == {"message": "OK"}
