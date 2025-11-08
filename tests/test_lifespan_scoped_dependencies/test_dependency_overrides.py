from typing import Any, AsyncGenerator, List, Tuple

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
    Request,
    WebSocket,
)
from fastapi.exceptions import DependencyScopeError
from fastapi.params import Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient
from typing_extensions import Annotated, Literal

from tests.test_lifespan_scoped_dependencies.testing_utilities import (
    DependencyFactory,
    DependencyStyle,
    IntentionallyBadDependency,
    create_endpoint_0_annotations,
    create_endpoint_1_annotation,
    create_endpoint_3_annotations,
    use_endpoint,
    use_websocket,
)


def expect_correct_amount_of_dependency_activations(
    *,
    app: FastAPI,
    dependency_factory: DependencyFactory,
    override_dependency_factory: DependencyFactory,
    urls_and_responses: List[Tuple[str, Any]],
    expected_activation_times: int,
    is_websocket: bool,
) -> None:
    assert dependency_factory.activation_times == 0
    assert dependency_factory.deactivation_times == 0
    assert override_dependency_factory.activation_times == 0
    assert override_dependency_factory.deactivation_times == 0

    with TestClient(app) as client:
        assert dependency_factory.activation_times == 0
        assert dependency_factory.deactivation_times == 0
        assert override_dependency_factory.activation_times == expected_activation_times
        assert override_dependency_factory.deactivation_times == 0

        for url, expected_response in urls_and_responses:
            if is_websocket:
                response = use_websocket(client, url)
            else:
                response = use_endpoint(client, url)

            assert response == expected_response

            assert dependency_factory.activation_times == 0
            assert dependency_factory.deactivation_times == 0
            assert (
                override_dependency_factory.activation_times
                == expected_activation_times
            )
            assert override_dependency_factory.deactivation_times == 0

    assert dependency_factory.activation_times == 0
    assert override_dependency_factory.activation_times == expected_activation_times
    if dependency_factory.dependency_style not in (
        DependencyStyle.SYNC_FUNCTION,
        DependencyStyle.ASYNC_FUNCTION,
    ):
        assert dependency_factory.deactivation_times == 0
        assert (
            override_dependency_factory.deactivation_times == expected_activation_times
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoint_dependencies(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    create_endpoint_1_annotation(
        router=router,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[
            None,
            Depends(
                dependency_factory.get_dependency(),
                scope="lifespan",
                use_cache=use_cache,
            ),
        ],
        expected_value=11,
    )
    if routing_style == "router_endpoint":
        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        override_dependency_factory=override_dependency_factory,
        urls_and_responses=[("/test", 11)] * 2,
        expected_activation_times=1,
        is_websocket=is_websocket,
    )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("dependency_duplication", [1, 2])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_router_dependencies(
    dependency_style: DependencyStyle,
    routing_style,
    use_cache,
    dependency_duplication,
    is_websocket,
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )

    if routing_style == "app":
        app = FastAPI(dependencies=[depends] * dependency_duplication)

        create_endpoint_0_annotations(
            router=app, path="/test", is_websocket=is_websocket
        )
    else:
        app = FastAPI()
        router = APIRouter(dependencies=[depends] * dependency_duplication)

        create_endpoint_0_annotations(
            router=router, path="/test", is_websocket=is_websocket
        )

        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        override_dependency_factory=override_dependency_factory,
        urls_and_responses=[("/test", None)] * 2,
        expected_activation_times=1 if use_cache else dependency_duplication,
        is_websocket=is_websocket,
    )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
@pytest.mark.parametrize("main_dependency_scope", ["function", "request", "lifespan"])
def test_dependency_cache_in_same_dependency(
    dependency_style: DependencyStyle,
    routing_style,
    use_cache,
    main_dependency_scope: Literal["function", "request", "lifespan"],
    is_websocket,
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
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

    create_endpoint_1_annotation(
        router=router,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[
            List[int],
            Depends(
                dependency,
                use_cache=use_cache,
                scope=main_dependency_scope,
            ),
        ],
    )

    if routing_style == "router":
        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    if use_cache:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [11, 11]),
                ("/test", [11, 11]),
            ],
            dependency_factory=dependency_factory,
            override_dependency_factory=override_dependency_factory,
            expected_activation_times=1,
            is_websocket=is_websocket,
        )
    else:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [11, 12]),
                ("/test", [11, 12]),
            ],
            dependency_factory=dependency_factory,
            override_dependency_factory=override_dependency_factory,
            expected_activation_times=2,
            is_websocket=is_websocket,
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_dependency_cache_in_same_endpoint(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    async def endpoint_dependency(dependency3: Annotated[int, depends]) -> int:
        return dependency3

    create_endpoint_3_annotations(
        router=router,
        path="/test1",
        is_websocket=is_websocket,
        annotation1=Annotated[int, depends],
        annotation2=Annotated[int, depends],
        annotation3=Annotated[int, Depends(endpoint_dependency)],
    )

    if routing_style == "router":
        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    if use_cache:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [11, 11, 11]),
                ("/test1", [11, 11, 11]),
            ],
            dependency_factory=dependency_factory,
            override_dependency_factory=override_dependency_factory,
            expected_activation_times=1,
            is_websocket=is_websocket,
        )
    else:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [11, 12, 13]),
                ("/test1", [11, 12, 13]),
            ],
            dependency_factory=dependency_factory,
            override_dependency_factory=override_dependency_factory,
            expected_activation_times=3,
            is_websocket=is_websocket,
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_dependency_cache_in_different_endpoints(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    async def endpoint_dependency(dependency3: Annotated[int, depends]) -> int:
        return dependency3

    create_endpoint_3_annotations(
        router=router,
        path="/test1",
        is_websocket=is_websocket,
        annotation1=Annotated[int, depends],
        annotation2=Annotated[int, depends],
        annotation3=Annotated[int, Depends(endpoint_dependency)],
    )

    create_endpoint_3_annotations(
        router=router,
        path="/test2",
        is_websocket=is_websocket,
        annotation1=Annotated[int, depends],
        annotation2=Annotated[int, depends],
        annotation3=Annotated[int, Depends(endpoint_dependency)],
    )

    if routing_style == "router":
        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    if use_cache:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [11, 11, 11]),
                ("/test2", [11, 11, 11]),
                ("/test1", [11, 11, 11]),
                ("/test2", [11, 11, 11]),
            ],
            dependency_factory=dependency_factory,
            override_dependency_factory=override_dependency_factory,
            expected_activation_times=1,
            is_websocket=is_websocket,
        )
    else:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [11, 12, 13]),
                ("/test2", [14, 15, 13]),
                ("/test1", [11, 12, 13]),
                ("/test2", [14, 15, 13]),
            ],
            dependency_factory=dependency_factory,
            override_dependency_factory=override_dependency_factory,
            expected_activation_times=5,
            is_websocket=is_websocket,
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_no_cached_dependency(
    dependency_style: DependencyStyle, routing_style, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=False,
    )

    app = FastAPI()

    if routing_style == "app":
        router = app

    else:
        router = APIRouter()

    create_endpoint_1_annotation(
        router=router,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[int, depends],
    )

    if routing_style == "router":
        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        override_dependency_factory=override_dependency_factory,
        urls_and_responses=[("/test", 11)] * 2,
        expected_activation_times=1,
        is_websocket=is_websocket,
    )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
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
        Request,
        WebSocket,
    ],
)
def test_override_lifespan_scoped_dependency_cannot_use_endpoint_scoped_parameters(
    annotation, is_websocket
):
    async def dependency_func() -> None:
        yield  # pragma: nocover

    async def override_dependency_func(param: annotation) -> None:
        yield  # pragma: nocover

    app = FastAPI()
    app.dependency_overrides[dependency_func] = override_dependency_func

    create_endpoint_1_annotation(
        router=app,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[
            None, Depends(dependency_func, scope="lifespan")
        ],
    )

    with pytest.raises(DependencyScopeError):
        with TestClient(app):
            pass


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
def test_non_override_lifespan_scoped_dependency_can_use_overridden_lifespan_scoped_dependencies(
    dependency_style: DependencyStyle, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, value_offset=10)

    async def lifespan_scoped_dependency(
        param: Annotated[
            int,
            Depends(dependency_factory.get_dependency(), scope="lifespan"),
        ],
    ) -> AsyncGenerator[int, None]:
        yield param

    app = FastAPI()

    create_endpoint_1_annotation(
        router=app,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[
            int, Depends(lifespan_scoped_dependency, scope="lifespan")
        ],
    )

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        override_dependency_factory=override_dependency_factory,
        expected_activation_times=1,
        urls_and_responses=[("/test", 11)] * 2,
        is_websocket=is_websocket,
    )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("depends_class", [Depends, Security])
def test_override_lifespan_scoped_dependency_cannot_use_endpoint_scoped_dependencies(
    depends_class, is_websocket
):
    async def sub_dependency() -> None:
        pass  # pragma: nocover

    async def dependency_func() -> None:
        yield  # pragma: nocover

    async def override_dependency_func(
        param: Annotated[None, depends_class(sub_dependency)],
    ) -> None:
        yield  # pragma: nocover

    app = FastAPI()

    create_endpoint_1_annotation(
        router=app,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[
            None, Depends(dependency_func, scope="lifespan")
        ],
    )

    app.dependency_overrides[dependency_func] = override_dependency_func

    with pytest.raises(DependencyScopeError):
        with TestClient(app):
            pass


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_bad_override_lifespan_scoped_dependencies(
    use_cache, dependency_style: DependencyStyle, routing_style, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)
    override_dependency_factory = DependencyFactory(dependency_style, should_error=True)

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app

    else:
        router = APIRouter()

    create_endpoint_1_annotation(
        router=router,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[int, depends],
    )

    if routing_style == "router_endpoint":
        app.include_router(router)

    app.dependency_overrides[dependency_factory.get_dependency()] = (
        override_dependency_factory.get_dependency()
    )

    with pytest.raises(IntentionallyBadDependency) as exception_info:
        with TestClient(app):
            pass

    assert exception_info.value.args == (1,)
