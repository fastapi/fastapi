from unittest.mock import patch

import pytest
from fastapi import Depends, FastAPI
from fastapi.dependencies.utils import get_dependant
from fastapi.testclient import TestClient


@pytest.mark.parametrize("self_override", [False, True])
def test_unchanged_override_does_not_rebuild_dependant(self_override: bool):
    app = FastAPI()

    async def leaf(q: int):
        return q

    async def dependency(value: int = Depends(leaf)):
        return value

    async def unused():
        return 0

    @app.get("/")
    async def endpoint(value: int = Depends(dependency)):
        return {"value": value}

    if self_override:
        app.dependency_overrides[dependency] = dependency
    else:
        app.dependency_overrides[unused] = leaf

    with TestClient(app) as client:
        with patch(
            "fastapi.dependencies.utils.get_dependant", wraps=get_dependant
        ) as mocked:
            response = client.get("/", params={"q": 42})
            invalid_response = client.get("/", params={"q": "invalid"})

    assert response.status_code == 200
    assert response.json() == {"value": 42}
    assert invalid_response.status_code == 422
    assert invalid_response.json()["detail"][0]["loc"] == ["query", "q"]
    mocked.assert_not_called()


def test_nested_override_under_unchanged_parent():
    app = FastAPI()

    async def leaf():
        return "original"

    async def dependency(value: str = Depends(leaf)):
        return value

    async def replacement(q: int):
        return f"override-{q}"

    @app.get("/")
    async def endpoint(value: str = Depends(dependency)):
        return {"value": value}

    with TestClient(app) as client:
        app.dependency_overrides[leaf] = replacement
        with patch(
            "fastapi.dependencies.utils.get_dependant", wraps=get_dependant
        ) as mocked:
            response = client.get("/", params={"q": 42})

        assert response.status_code == 200
        assert response.json() == {"value": "override-42"}
        assert [call.kwargs["call"] for call in mocked.call_args_list] == [replacement]
        assert client.get("/").status_code == 422

        app.dependency_overrides.clear()
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"value": "original"}
