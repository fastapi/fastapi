import warnings
from contextlib import asynccontextmanager
from time import sleep
from typing import Any, AsyncGenerator, Dict, List, Tuple

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
from fastapi.dependencies.utils import get_endpoint_dependant
from fastapi.exceptions import (
    DependencyScopeError,
    InvalidDependencyScope,
    UninitializedLifespanDependency,
)
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
    create_endpoint_2_annotations,
    create_endpoint_3_annotations,
    use_endpoint,
    use_websocket,
)


def expect_correct_amount_of_dependency_activations(
    *,
    app: FastAPI,
    dependency_factory: DependencyFactory,
    urls_and_responses: List[Tuple[str, Any]],
    expected_activation_times: int,
    is_websocket: bool,
) -> None:
    assert dependency_factory.activation_times == 0
    assert dependency_factory.deactivation_times == 0
    with TestClient(app) as client:
        assert dependency_factory.activation_times == expected_activation_times
        assert dependency_factory.deactivation_times == 0

        for url, expected_response in urls_and_responses:
            if is_websocket:
                assert use_websocket(client, url) == expected_response
            else:
                assert use_endpoint(client, url) == expected_response

            assert dependency_factory.activation_times == expected_activation_times
            assert dependency_factory.deactivation_times == 0

    assert dependency_factory.activation_times == expected_activation_times
    if dependency_factory.dependency_style not in (
        DependencyStyle.SYNC_FUNCTION,
        DependencyStyle.ASYNC_FUNCTION,
    ):
        assert dependency_factory.deactivation_times == expected_activation_times


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize(
    "use_cache", [True, False], ids=["With Cache", "Without Cache"]
)
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoint_dependencies(
    dependency_style: DependencyStyle,
    routing_style,
    use_cache,
    is_websocket: bool,
):
    dependency_factory = DependencyFactory(dependency_style)

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
        expected_value=1,
    )

    if routing_style == "router_endpoint":
        app.include_router(router)

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        urls_and_responses=[("/test", 1)] * 2,
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
    is_websocket: bool,
):
    dependency_factory = DependencyFactory(dependency_style)

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

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        urls_and_responses=[("/test", None)] * 2,
        expected_activation_times=1 if use_cache else dependency_duplication,
        is_websocket=is_websocket,
    )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
@pytest.mark.parametrize("main_dependency_scope", ["request", "function", "lifespan"])
def test_dependency_cache_in_same_dependency(
    dependency_style: DependencyStyle,
    routing_style,
    use_cache,
    main_dependency_scope: Literal["request", "function", "lifespan"],
    is_websocket: bool,
):
    dependency_factory = DependencyFactory(dependency_style)

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

    if use_cache:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [1, 1]),
                ("/test", [1, 1]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=1,
            is_websocket=is_websocket,
        )
    else:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [1, 2]),
                ("/test", [1, 2]),
            ],
            dependency_factory=dependency_factory,
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
        path="/test",
        is_websocket=is_websocket,
        annotation1=Annotated[int, depends],
        annotation2=Annotated[int, depends],
        annotation3=Annotated[int, Depends(endpoint_dependency)],
    )

    if routing_style == "router":
        app.include_router(router)

    if use_cache:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [1, 1, 1]),
                ("/test", [1, 1, 1]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=1,
            is_websocket=is_websocket,
        )
    else:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test", [1, 2, 3]),
                ("/test", [1, 2, 3]),
            ],
            dependency_factory=dependency_factory,
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

    if use_cache:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [1, 1, 1]),
                ("/test2", [1, 1, 1]),
                ("/test1", [1, 1, 1]),
                ("/test2", [1, 1, 1]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=1,
            is_websocket=is_websocket,
        )
    else:
        expect_correct_amount_of_dependency_activations(
            app=app,
            urls_and_responses=[
                ("/test1", [1, 2, 3]),
                ("/test2", [4, 5, 3]),
                ("/test1", [1, 2, 3]),
                ("/test2", [4, 5, 3]),
            ],
            dependency_factory=dependency_factory,
            expected_activation_times=5,
            is_websocket=is_websocket,
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_no_cached_dependency(
    dependency_style: DependencyStyle,
    routing_style,
    is_websocket,
):
    dependency_factory = DependencyFactory(dependency_style)

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
        expected_value=1,
    )

    if routing_style == "router":
        app.include_router(router)

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        urls_and_responses=[("/test", 1)] * 2,
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
def test_lifespan_scoped_dependency_cannot_use_endpoint_scoped_parameters(
    annotation, is_websocket
):
    async def dependency_func(param: annotation) -> None:
        yield  # pragma: nocover

    app = FastAPI()

    with pytest.raises(DependencyScopeError):
        create_endpoint_1_annotation(
            router=app,
            path="/test",
            is_websocket=is_websocket,
            annotation=Annotated[None, Depends(dependency_func, scope="lifespan")],
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
def test_lifespan_scoped_dependency_can_use_other_lifespan_scoped_dependencies(
    dependency_style: DependencyStyle, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)

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
        annotation=Annotated[int, Depends(lifespan_scoped_dependency)],
        expected_value=1,
    )

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        expected_activation_times=1,
        urls_and_responses=[("/test", 1)] * 2,
        is_websocket=is_websocket,
    )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize(
    ["dependency_style", "supports_teardown"],
    [
        (DependencyStyle.SYNC_FUNCTION, False),
        (DependencyStyle.ASYNC_FUNCTION, False),
        (DependencyStyle.SYNC_GENERATOR, True),
        (DependencyStyle.ASYNC_GENERATOR, True),
    ],
)
@pytest.mark.parametrize("endpoint_dependency_scope", ["request", "function"])
def test_the_same_dependency_can_work_in_different_scopes(
    dependency_style: DependencyStyle,
    supports_teardown,
    is_websocket,
    endpoint_dependency_scope: Literal["request", "function"],
):
    dependency_factory = DependencyFactory(dependency_style)
    app = FastAPI()

    create_endpoint_2_annotations(
        router=app,
        path="/test",
        is_websocket=is_websocket,
        annotation1=Annotated[
            int,
            Depends(
                dependency_factory.get_dependency(), scope=endpoint_dependency_scope
            ),
        ],
        annotation2=Annotated[
            int,
            Depends(dependency_factory.get_dependency(), scope="lifespan"),
        ],
    )
    if is_websocket:
        get_response = use_websocket
    else:
        get_response = use_endpoint

    assert dependency_factory.activation_times == 0
    assert dependency_factory.deactivation_times == 0
    with TestClient(app) as client:
        assert dependency_factory.activation_times == 1
        assert dependency_factory.deactivation_times == 0

        assert get_response(client, "/test") == [2, 1]
        assert dependency_factory.activation_times == 2
        if supports_teardown:
            if is_websocket:
                # Websockets teardown might take some time after the test client
                # has disconnected
                sleep(0.1)
            assert dependency_factory.deactivation_times == 1
        else:
            assert dependency_factory.deactivation_times == 0

        assert get_response(client, "/test") == [3, 1]
        assert dependency_factory.activation_times == 3
        if supports_teardown:
            if is_websocket:
                # Websockets teardown might take some time after the test client
                # has disconnected
                sleep(0.1)
            assert dependency_factory.deactivation_times == 2
        else:
            assert dependency_factory.deactivation_times == 0

    assert dependency_factory.activation_times == 3
    if supports_teardown:
        assert dependency_factory.deactivation_times == 3
    else:
        assert dependency_factory.deactivation_times == 0


@pytest.mark.parametrize(
    "lifespan_style", ["lifespan_generator", "events_decorator", "events_constructor"]
)
@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
def test_lifespan_scoped_dependency_can_be_used_alongside_custom_lifespans(
    dependency_style: DependencyStyle,
    is_websocket,
    lifespan_style: Literal["lifespan_function", "lifespan_events"],
):
    lifespan_started = False
    lifespan_ended = False
    if lifespan_style == "lifespan_generator":

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[Dict[str, int], None]:
            nonlocal lifespan_started
            nonlocal lifespan_ended
            lifespan_started = True
            yield
            lifespan_ended = True

        app = FastAPI(lifespan=lifespan)
    elif lifespan_style == "events_decorator":
        app = FastAPI()
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            @app.on_event("startup")
            async def startup() -> None:
                nonlocal lifespan_started
                lifespan_started = True

            @app.on_event("shutdown")
            async def shutdown() -> None:
                nonlocal lifespan_ended
                lifespan_ended = True
    else:
        assert lifespan_style == "events_constructor"

        async def startup() -> None:
            nonlocal lifespan_started
            lifespan_started = True

        async def shutdown() -> None:
            nonlocal lifespan_ended
            lifespan_ended = True

        app = FastAPI(on_startup=[startup], on_shutdown=[shutdown])

    dependency_factory = DependencyFactory(dependency_style)

    create_endpoint_1_annotation(
        router=app,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[
            int,
            Depends(dependency_factory.get_dependency(), scope="lifespan"),
        ],
        expected_value=1,
    )

    expect_correct_amount_of_dependency_activations(
        app=app,
        dependency_factory=dependency_factory,
        expected_activation_times=1,
        urls_and_responses=[("/test", 1)] * 2,
        is_websocket=is_websocket,
    )
    assert lifespan_started and lifespan_ended


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("depends_class", [Depends, Security])
def test_lifespan_scoped_dependency_cannot_use_endpoint_scoped_dependencies(
    depends_class, is_websocket
):
    async def sub_dependency() -> None:
        pass  # pragma: nocover

    async def dependency_func(
        param: Annotated[None, depends_class(sub_dependency)],
    ) -> None:
        pass  # pragma: nocover

    app = FastAPI()

    with pytest.raises(DependencyScopeError):
        create_endpoint_1_annotation(
            router=app,
            path="/test",
            is_websocket=is_websocket,
            annotation=Annotated[None, Depends(dependency_func, scope="lifespan")],
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_dependencies_must_provide_correct_dependency_scope(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    with pytest.raises(
        InvalidDependencyScope,
        match=r'Dependency received an invalid scope: "incorrect"',
    ):
        create_endpoint_1_annotation(
            router=router,
            path="/test",
            is_websocket=is_websocket,
            annotation=Annotated[
                None,
                Depends(
                    dependency_factory.get_dependency(),
                    scope="incorrect",
                    use_cache=use_cache,
                ),
            ],
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoints_report_incorrect_dependency_scope(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )
    # We intentionally change the dependency scope here to bypass the
    # validation at the function level.
    depends.scope = "asdad"

    with pytest.raises(InvalidDependencyScope):
        create_endpoint_1_annotation(
            router=router,
            path="/test",
            is_websocket=is_websocket,
            annotation=Annotated[int, depends],
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app", "router"])
def test_endpoints_report_incorrect_dependency_scope_at_router_scope(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(DependencyStyle.ASYNC_GENERATOR)

    depends = Depends(dependency_factory.get_dependency(), scope="lifespan")

    # We intentionally change the dependency scope here to bypass the
    # validation at the function level.
    depends.scope = "asdad"

    if routing_style == "app":
        app = FastAPI(dependencies=[depends])
        router = app
    else:
        router = APIRouter(dependencies=[depends])

    with pytest.raises(InvalidDependencyScope):
        create_endpoint_0_annotations(
            router=router,
            path="/test",
            is_websocket=is_websocket,
        )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoints_report_uninitialized_dependency(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )

    create_endpoint_1_annotation(
        router=router,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[int, depends],
        expected_value=1,
    )

    if routing_style == "router_endpoint":
        app.include_router(router)

    with TestClient(app) as client:
        dependencies = client.app_state["__fastapi__"]["lifespan_scoped_dependencies"]
        client.app_state["__fastapi__"]["lifespan_scoped_dependencies"] = {}

        try:
            with pytest.raises(UninitializedLifespanDependency):
                if is_websocket:
                    with client.websocket_connect("/test"):
                        pass  # pragma: nocover
                else:
                    client.post("/test")
        finally:
            client.app_state["__fastapi__"]["lifespan_scoped_dependencies"] = (
                dependencies
            )


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_endpoints_report_uninitialized_internal_lifespan(
    dependency_style: DependencyStyle, routing_style, use_cache, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style)

    app = FastAPI()

    if routing_style == "app_endpoint":
        router = app
    else:
        router = APIRouter()

    depends = Depends(
        dependency_factory.get_dependency(),
        scope="lifespan",
        use_cache=use_cache,
    )

    create_endpoint_1_annotation(
        router=router,
        path="/test",
        is_websocket=is_websocket,
        annotation=Annotated[int, depends],
        expected_value=1,
    )

    if routing_style == "router_endpoint":
        app.include_router(router)

    with TestClient(app) as client:
        internal_state = client.app_state["__fastapi__"]
        del client.app_state["__fastapi__"]

        try:
            with pytest.raises(UninitializedLifespanDependency):
                if is_websocket:
                    with client.websocket_connect("/test"):
                        pass  # pragma: nocover
                else:
                    client.post("/test")
        finally:
            client.app_state["__fastapi__"] = internal_state


@pytest.mark.parametrize("is_websocket", [True, False], ids=["Websocket", "Endpoint"])
@pytest.mark.parametrize("use_cache", [True, False])
@pytest.mark.parametrize("dependency_style", list(DependencyStyle))
@pytest.mark.parametrize("routing_style", ["app_endpoint", "router_endpoint"])
def test_bad_lifespan_scoped_dependencies(
    use_cache, dependency_style: DependencyStyle, routing_style, is_websocket
):
    dependency_factory = DependencyFactory(dependency_style, should_error=True)
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
        expected_value=1,
    )

    if routing_style == "router_endpoint":
        app.include_router(router)

    with pytest.raises(IntentionallyBadDependency) as exception_info:
        with TestClient(app):
            pass

    assert exception_info.value.args == (1,)


def test_endpoint_dependant_backwards_compatibility():
    dependency_factory = DependencyFactory(DependencyStyle.ASYNC_GENERATOR)

    def endpoint(
        dependency1: Annotated[int, Depends(dependency_factory.get_dependency())],
        dependency2: Annotated[
            int,
            Depends(dependency_factory.get_dependency(), scope="lifespan"),
        ],
    ):
        pass  # pragma: nocover

    dependant = get_endpoint_dependant(
        path="/test",
        call=endpoint,
        name="endpoint",
    )

    assert dependant.dependencies == tuple(
        dependant.lifespan_dependencies + dependant.endpoint_dependencies
    )
