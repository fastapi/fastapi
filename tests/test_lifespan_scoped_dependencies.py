from enum import StrEnum, auto
from typing import Any, AsyncGenerator, List, Tuple, TypeVar

import pytest
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Cookie,
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    Path,
    Query,
)
from fastapi.exceptions import FastAPIError
from fastapi.params import Security
from fastapi.security import SecurityScopes
from starlette.testclient import TestClient
from typing_extensions import Annotated, Generator, Literal, assert_never

T = TypeVar("T")


class DependencyStyle(StrEnum):
    SYNC_FUNCTION = auto()
    ASYNC_FUNCTION = auto()
    SYNC_GENERATOR = auto()
    ASYNC_GENERATOR = auto()


class DependencyFactory:
    def __init__(
        self, dependency_style: DependencyStyle, *, should_error: bool = False
    ):
        self.activation_times = 0
        self.deactivation_times = 0
        self.dependency_style = dependency_style
        self._should_error = should_error

    def get_dependency(self):
        if self.dependency_style == DependencyStyle.SYNC_FUNCTION:
            return self._synchronous_function_dependency

        if self.dependency_style == DependencyStyle.SYNC_GENERATOR:
            return self._synchronous_generator_dependency

        if self.dependency_style == DependencyStyle.ASYNC_FUNCTION:
            return self._asynchronous_function_dependency

        if self.dependency_style == DependencyStyle.ASYNC_GENERATOR:
            return self._asynchronous_generator_dependency

        assert_never(self.dependency_style)

    async def _asynchronous_generator_dependency(self) -> AsyncGenerator[T, None]:
        self.activation_times += 1
        if self._should_error:
            raise ValueError(self.activation_times)

        yield self.activation_times
        self.deactivation_times += 1

    def _synchronous_generator_dependency(self) -> Generator[T, None, None]:
        self.activation_times += 1
        if self._should_error:
            raise ValueError(self.activation_times)

        yield self.activation_times
        self.deactivation_times += 1

    async def _asynchronous_function_dependency(self) -> T:
        self.activation_times += 1
        if self._should_error:
            raise ValueError(self.activation_times)

        return self.activation_times

    def _synchronous_function_dependency(self) -> T:
        self.activation_times += 1
        if self._should_error:
            raise ValueError(self.activation_times)

        return self.activation_times


def _expect_correct_amount_of_dependency_activations(
    *,
    app: FastAPI,
    dependency_factory: DependencyFactory,
    urls_and_responses: List[Tuple[str, Any]],
    expected_activation_times: int,
) -> None:
    assert dependency_factory.activation_times == 0
    assert dependency_factory.deactivation_times == 0
    with TestClient(app) as client:
        assert dependency_factory.activation_times == expected_activation_times
        assert dependency_factory.deactivation_times == 0

        for url, expected_response in urls_and_responses:
            response = client.post(url)
            response.raise_for_status()
            assert response.json() == expected_response

            assert dependency_factory.activation_times == expected_activation_times
            assert dependency_factory.deactivation_times == 0

    assert dependency_factory.activation_times == expected_activation_times
    if dependency_factory.dependency_style not in (
        DependencyStyle.SYNC_FUNCTION,
        DependencyStyle.ASYNC_FUNCTION,
    ):
        assert dependency_factory.deactivation_times == expected_activation_times


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoint_dependencies(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    @router.post("/test")
    async def endpoint(
        dependency: Annotated[
            None,
            Depends(
                dependency_factory.get_dependency(),
                dependency_scope="lifespan",
                use_cache=use_cache,
            ),
        ],
    ) -> None:
        assert dependency == 1
        return dependency

    if routing_style == "router_endpoint":
        app.include_router(router)

    _expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        urls_and_responses=[("/test", 1)] * 2,
        expected_activation_times=1,
    )


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_router_dependencies(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    if routing_style == "app":
        app = FastAPI(dependencies=[depends])

        @app.post("/test")
        async def endpoint() -> None:
            return None
    else:
        app = FastAPI()
        router = APIRouter(dependencies=[depends])

        @router.post("/test")
        async def endpoint() -> None:
            return None

        app.include_router(router)

    _expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        urls_and_responses=[("/test", None)] * 2,
        expected_activation_times=1,
    )


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
@pytest.mark.parametrize("main_dependency_scope", ["endpoint", "lifespan"])
def test_dependency_cache_in_same_dependency(
    dependency_style: DependencyStyle,
    routing_style,
    use_cache,
    main_dependency_scope: Literal["endpoint", "lifespan"],
):
    dependency_factory = DependencyFactory(dependency_style)

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    async def dependency(
        sub_dependency1: Annotated[int, depends],
        sub_dependency2: Annotated[int, depends],
    ) -> List[int]:
        return [sub_dependency1, sub_dependency2]

    @router.post("/test")
    async def endpoint(
        dependency: Annotated[
            List[int],
            Depends(
                dependency,
                use_cache=use_cache,
                dependency_scope=main_dependency_scope,
            ),
        ],
    ) -> List[int]:
        return dependency

    if routing_style == "router":
        app.include_router(router)

    if use_cache:
        _expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [1, 1]),
                ("/test", [1, 1]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=1,
        )
    else:
        _expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [1, 2]),
                ("/test", [1, 2]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=2,
        )


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_dependency_cache_in_same_endpoint(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    async def endpoint_dependency(dependency3: Annotated[int, depends]) -> int:
        return dependency3

    @router.post("/test1")
    async def endpoint(
        dependency1: Annotated[int, depends],
        dependency2: Annotated[int, depends],
        dependency3: Annotated[int, Depends(endpoint_dependency)],
    ) -> List[int]:
        return [dependency1, dependency2, dependency3]

    if routing_style == "router":
        app.include_router(router)

    if use_cache:
        _expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [1, 1, 1]),
                ("/test1", [1, 1, 1]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=1,
        )
    else:
        _expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [1, 2, 3]),
                ("/test1", [1, 2, 3]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=3,
        )


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_dependency_cache_in_different_endpoints(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    async def endpoint_dependency(dependency3: Annotated[int, depends]) -> int:
        return dependency3

    @router.post("/test1")
    async def endpoint(
        dependency1: Annotated[int, depends],
        dependency2: Annotated[int, depends],
        dependency3: Annotated[int, Depends(endpoint_dependency)],
    ) -> List[int]:
        return [dependency1, dependency2, dependency3]

    @router.post("/test2")
    async def endpoint2(
        dependency1: Annotated[int, depends],
        dependency2: Annotated[int, depends],
        dependency3: Annotated[int, Depends(endpoint_dependency)],
    ) -> List[int]:
        return [dependency1, dependency2, dependency3]

    if routing_style == "router":
        app.include_router(router)

    if use_cache:
        _expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [1, 1, 1]),
                ("/test2", [1, 1, 1]),
                ("/test1", [1, 1, 1]),
                ("/test2", [1, 1, 1]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=1,
        )
    else:
        _expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [1, 2, 3]),
                ("/test2", [4, 5, 3]),
                ("/test1", [1, 2, 3]),
                ("/test2", [4, 5, 3]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=5,
        )


@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_no_cached_dependency(
    dependency_style: DependencyStyle,
    routing_style,
):
    dependency_factory = DependencyFactory(dependency_style)

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=False,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    @router.post("/test")
    async def endpoint(
        dependency: Annotated[int, depends],
    ) -> int:
        return dependency

    if routing_style == "router":
        app.include_router(router)

    _expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        urls_and_responses=[("/test", 1)] * 2,
        expected_activation_times=1,
    )


@pytest.mark.parametrize(
    "annotation",
    [
        Annotated[str, Path()],
        Annotated[str, Body()],
        Annotated[str, Query()],
        Annotated[str, Header()],
        SecurityScopes,
        Annotated[str, Cookie()],
        Annotated[str, Form()],
        Annotated[str, File()],
        BackgroundTasks,
    ],
)
def test_lifespan_scoped_dependency_cannot_use_endpoint_scoped_parameters(annotation):
    async def dependency_func(param: annotation) -> None:
        yield

    app = FastAPI()

    with pytest.raises(FastAPIError):

        @app.post("/test")
        async def endpoint(
            dependency: Annotated[
                None, Depends(dependency_func, dependency_scope="lifespan")
            ],
        ) -> None:
            return


@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
def test_lifespan_scoped_dependency_can_use_other_lifespan_scoped_dependencies(
    dependency_style: DependencyStyle,
):
    dependency_factory = DependencyFactory(dependency_style)

    async def lifespan_scoped_dependency(
        param: Annotated[
            int,
            Depends(dependency_factory.get_dependency(), dependency_scope="lifespan"),
        ],
    ) -> AsyncGenerator[int, None]:
        yield param

    app = FastAPI()

    @app.post("/test")
    async def endpoint(
        dependency: Annotated[
            int, Depends(lifespan_scoped_dependency, dependency_scope="lifespan")
        ],
    ) -> int:
        return dependency

    _expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        expected_activation_times=1,
        urls_and_responses=[("/test", 1)] * 2,
    )


@pytest.mark.parametrize("depends_class", [Depends, Security])
@pytest.mark.parametrize(
    "route_type", [FastAPI.post, FastAPI.websocket], ids=["websocket", "endpoint"]
)
def test_lifespan_scoped_dependency_cannot_use_endpoint_scoped_dependencies(
    depends_class, route_type
):
    async def sub_dependency() -> None:
        pass

    async def dependency_func(
        param: Annotated[None, depends_class(sub_dependency)],
    ) -> None:
        yield

    app = FastAPI()
    route_decorator = route_type(app, "/test")

    with pytest.raises(FastAPIError):

        @route_decorator
        async def endpoint(
            x: Annotated[None, Depends(dependency_func, dependency_scope="lifespan")],
        ) -> None:
            return


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_dependencies_must_provide_correct_dependency_scope(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    with pytest.raises(FastAPIError):

        @router.post("/test")
        async def endpoint(
            dependency: Annotated[
                None,
                Depends(
                    dependency_factory.get_dependency(),
                    dependency_scope="incorrect",
                    use_cache=use_cache,
                ),
            ],
        ) -> None:
            assert dependency == 1
            return dependency


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoints_report_incorrect_dependency_scope(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )
    # We intentionally change the dependency scope here to bypass the
    # validation at the function level.
    depends.dependency_scope = "asdad"

    with pytest.raises(FastAPIError):

        @router.post("/test")
        async def endpoint(dependency: Annotated[int, depends]) -> int:
            assert dependency == 1
            return dependency


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoints_report_uninitialized_dependency(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    @router.post("/test")
    async def endpoint(dependency: Annotated[int, depends]) -> int:
        assert dependency == 1
        return dependency

    if routing_style == "router_endpoint":
        app.include_router(router)

    with TestClient(app) as client:
        dependencies = client.app_state["__fastapi__"]["lifespan_scoped_dependencies"]
        client.app_state["__fastapi__"]["lifespan_scoped_dependencies"] = {}

        try:
            with pytest.raises(FastAPIError):
                client.post("/test")
        finally:
            client.app_state["__fastapi__"]["lifespan_scoped_dependencies"] = (
                dependencies
            )


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoints_report_uninitialized_internal_lifespan(
    dependency_style: DependencyStyle, routing_style, use_cache
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    @router.post("/test")
    async def endpoint(dependency: Annotated[int, depends]) -> int:
        assert dependency == 1
        return dependency

    if routing_style == "router_endpoint":
        app.include_router(router)

    with TestClient(app) as client:
        internal_state = client.app_state["__fastapi__"]
        del client.app_state["__fastapi__"]

        try:
            with pytest.raises(FastAPIError):
                client.post("/test")
        finally:
            client.app_state["__fastapi__"] = internal_state


@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_bad_lifespan_scoped_dependencies(
    use_cache, dependency_style: DependencyStyle, routing_style
):
    dependency_factory = DependencyFactory(dependency_style, should_error=True)
    depends = Depends(
        dependency_factory.get_dependency(),
        dependency_scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app

    else:
        router = APIRouter()

    @router.post("/test")
    async def endpoint(dependency: Annotated[int, depends]) -> int:
        assert dependency == 1
        return dependency

    if routing_style == "router_endpoint":
        app.include_router(router)

    with pytest.raises(ValueError) as exception_info:
        with TestClient(app):
            pass

    assert exception_info.value.args == (1,)


# TODO: Add tests for dependency_overrides
# TODO: Add a websocket equivalent to all tests
