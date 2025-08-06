from dataclasses import dataclass
from typing import AsyncGenerator, Generator
from unittest.mock import call, patch

from fastapi import Depends, FastAPI
from fastapi.dependencies.utils import inspect_callable
from fastapi.testclient import TestClient


def direct_dependency() -> str:
    return "direct dependency"


async def async_dependency() -> str:
    return "async dependency"


def sync_dependency() -> str:
    return "sync dependency"


async def async_generator() -> AsyncGenerator[str, None]:
    yield "async generator"


def sync_generator() -> Generator[str, None, None]:
    yield "generator"


@dataclass
class class_dependency:
    pass


# Nested dependency
async def async_nested_dependency(
    via_sync_dependency: dict = Depends(sync_dependency),
    via_async_dependency: str = Depends(async_dependency),
    via_async_generator: str = Depends(async_generator),
    via_sync_generator: str = Depends(sync_generator),
    via_class_dependency: class_dependency = Depends(),
) -> dict:
    return {
        "via_sync_dependency": via_sync_dependency,
        "via_async_dependency": via_async_dependency,
        "via_async_generator": via_async_generator,
        "via_sync_generator": via_sync_generator,
        "via_class_dependency": via_class_dependency,
    }


def test_get_callable_info():
    async_dependency_info = inspect_callable(async_dependency)
    assert not async_dependency_info.is_gen_callable
    assert not async_dependency_info.is_async_gen_callable
    assert async_dependency_info.is_coroutine_callable

    sync_dependency_info = inspect_callable(sync_dependency)
    assert not sync_dependency_info.is_gen_callable
    assert not sync_dependency_info.is_async_gen_callable
    assert not sync_dependency_info.is_coroutine_callable

    async_generator_info = inspect_callable(async_generator)
    assert not async_generator_info.is_gen_callable
    assert async_generator_info.is_async_gen_callable
    assert not async_generator_info.is_coroutine_callable

    sync_generator_info = inspect_callable(sync_generator)
    assert sync_generator_info.is_gen_callable
    assert not sync_generator_info.is_async_gen_callable
    assert not sync_generator_info.is_coroutine_callable

    class_dependency_info = inspect_callable(class_dependency)
    assert not class_dependency_info.is_gen_callable
    assert not class_dependency_info.is_async_gen_callable
    assert not class_dependency_info.is_coroutine_callable


def test_callable_info_is_cached():
    with patch(
        "fastapi.dependencies.utils.inspect_callable",
        side_effect=inspect_callable,
    ) as inspect_callable_mock:
        app = FastAPI()
        inspect_callable_mock.assert_not_called()

        @app.get("/items/{item_id}", dependencies=[Depends(direct_dependency)])
        async def endpoint(
            item_id: str,
            context: dict = Depends(async_nested_dependency),
        ) -> dict:
            return {"item_id": item_id, "context": context}

        # endpoint and direct dependency info is cached immediately.
        # nested dependencies require additional resolution
        inspect_callable_mock.assert_has_calls(
            [
                call(endpoint),
                call(async_nested_dependency),
                call(sync_dependency),
                call(async_dependency),
                call(async_generator),
                call(sync_generator),
                call(class_dependency),
                call(direct_dependency),
            ],
        )

        # first call of endpoint
        inspect_callable_mock.reset_mock()
        client = TestClient(app)
        response = client.get("/items/via-query")
        assert response.status_code == 200, response.text
        assert response.json() == {
            "item_id": "via-query",
            "context": {
                "via_sync_dependency": "sync dependency",
                "via_async_dependency": "async dependency",
                "via_async_generator": "async generator",
                "via_sync_generator": "generator",
                "via_class_dependency": {},
            },
        }

        # inspection is performed only once
        inspect_callable_mock.assert_not_called()
