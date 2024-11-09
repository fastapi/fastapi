from enum import Enum
from typing import Any, AsyncGenerator, Generator, List, TypeVar, Union

from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.testclient import TestClient
from typing_extensions import assert_never

T = TypeVar("T")


class DependencyStyle(str, Enum):
    SYNC_FUNCTION = "sync_function"
    ASYNC_FUNCTION = "async_function"
    SYNC_GENERATOR = "sync_generator"
    ASYNC_GENERATOR = "async_generator"


class IntentionallyBadDependency(Exception):
    pass


class DependencyFactory:
    def __init__(
        self,
        dependency_style: DependencyStyle,
        *,
        should_error: bool = False,
        value_offset: int = 0,
    ):
        self.activation_times = 0
        self.deactivation_times = 0
        self.dependency_style = dependency_style
        self._should_error = should_error
        self._value_offset = value_offset

    def get_dependency(self):
        if self.dependency_style == DependencyStyle.SYNC_FUNCTION:
            return self._synchronous_function_dependency

        if self.dependency_style == DependencyStyle.SYNC_GENERATOR:
            return self._synchronous_generator_dependency

        if self.dependency_style == DependencyStyle.ASYNC_FUNCTION:
            return self._asynchronous_function_dependency

        if self.dependency_style == DependencyStyle.ASYNC_GENERATOR:
            return self._asynchronous_generator_dependency

        assert_never(self.dependency_style)  # pragma: nocover

    async def _asynchronous_generator_dependency(self) -> AsyncGenerator[T, None]:
        self.activation_times += 1
        if self._should_error:
            raise IntentionallyBadDependency(self.activation_times)

        yield self.activation_times + self._value_offset
        self.deactivation_times += 1

    def _synchronous_generator_dependency(self) -> Generator[T, None, None]:
        self.activation_times += 1
        if self._should_error:
            raise IntentionallyBadDependency(self.activation_times)

        yield self.activation_times + self._value_offset
        self.deactivation_times += 1

    async def _asynchronous_function_dependency(self) -> T:
        self.activation_times += 1
        if self._should_error:
            raise IntentionallyBadDependency(self.activation_times)

        return self.activation_times + self._value_offset

    def _synchronous_function_dependency(self) -> T:
        self.activation_times += 1
        if self._should_error:
            raise IntentionallyBadDependency(self.activation_times)

        return self.activation_times + self._value_offset


def use_endpoint(client: TestClient, url: str) -> Any:
    response = client.post(url)
    response.raise_for_status()
    return response.json()


def use_websocket(client: TestClient, url: str) -> Any:
    with client.websocket_connect(url) as connection:
        return connection.receive_json()


def create_endpoint_0_annotations(
    *,
    router: Union[APIRouter, FastAPI],
    path: str,
    is_websocket: bool,
) -> None:
    if is_websocket:

        @router.websocket(path)
        async def endpoint(websocket: WebSocket) -> None:
            await websocket.accept()
            await websocket.send_json(None)
    else:

        @router.post(path)
        async def endpoint() -> None:
            return None


def create_endpoint_1_annotation(
    *,
    router: Union[APIRouter, FastAPI],
    path: str,
    is_websocket: bool,
    annotation: Any,
    expected_value: Any = None,
) -> None:
    if is_websocket:

        @router.websocket(path)
        async def endpoint(websocket: WebSocket, value: annotation) -> None:
            if expected_value is not None:
                assert value == expected_value

            await websocket.accept()
            await websocket.send_json(value)
    else:

        @router.post(path)
        async def endpoint(value: annotation) -> Any:
            if expected_value is not None:
                assert value == expected_value

            return value


def create_endpoint_2_annotations(
    *,
    router: Union[APIRouter, FastAPI],
    path: str,
    is_websocket: bool,
    annotation1: Any,
    annotation2: Any,
) -> None:
    if is_websocket:

        @router.websocket(path)
        async def endpoint(
            websocket: WebSocket,
            value1: annotation1,
            value2: annotation2,
        ) -> None:
            await websocket.accept()
            await websocket.send_json([value1, value2])
    else:

        @router.post(path)
        async def endpoint(
            value1: annotation1,
            value2: annotation2,
        ) -> List[Any]:
            return [value1, value2]


def create_endpoint_3_annotations(
    *,
    router: Union[APIRouter, FastAPI],
    path: str,
    is_websocket: bool,
    annotation1: Any,
    annotation2: Any,
    annotation3: Any,
) -> None:
    if is_websocket:

        @router.websocket(path)
        async def endpoint(
            websocket: WebSocket,
            value1: annotation1,
            value2: annotation2,
            value3: annotation3,
        ) -> None:
            await websocket.accept()
            await websocket.send_json([value1, value2, value3])
    else:

        @router.post(path)
        async def endpoint(
            value1: annotation1, value2: annotation2, value3: annotation3
        ) -> List[Any]:
            return [value1, value2, value3]
