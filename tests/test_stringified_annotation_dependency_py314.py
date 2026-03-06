from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from .utils import needs_py314

if TYPE_CHECKING:  # pragma: no cover

    class DummyUser: ...


@needs_py314
def test_stringified_annotation():
    # python3.14: Use forward reference without "from __future__ import annotations"
    async def get_current_user() -> DummyUser | None:
        return None

    app = FastAPI()

    client = TestClient(app)

    @app.get("/")
    async def get(
        current_user: Annotated[DummyUser | None, Depends(get_current_user)],
    ) -> str:
        return "hello world"

    response = client.get("/")
    assert response.status_code == 200
