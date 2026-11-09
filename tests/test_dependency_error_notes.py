import inspect
import sys
import traceback
from typing import Annotated, Any

import pytest
from fastapi import APIRouter, Depends, FastAPI, Path
from fastapi.exceptions import FastAPIError

needs_notes = pytest.mark.skipif(
    sys.version_info < (3, 11), reason="exception notes require Python 3.11+"
)


def located(func: Any) -> str:
    _, line = inspect.getsourcelines(func)
    return f"{func.__qualname__} ({inspect.getfile(func)}, line {line})"


def notes(error: BaseException) -> list[str]:
    # Read with getattr, `__notes__` only exists in Python 3.11+.
    return getattr(error, "__notes__", [])


def get_tenant(tenant_id: dict = Path()):  # invalid type for a path parameter
    return tenant_id  # pragma: no cover


def get_user(tenant=Depends(get_tenant)):
    return tenant  # pragma: no cover


def get_db():
    return "db"  # pragma: no cover


def get_repository(
    db: Annotated[str, Depends(get_db)] = Depends(get_db),
):  # invalid: Depends in Annotated and as default value
    return db  # pragma: no cover


@needs_notes
def test_nested_dependency_error_notes_show_the_chain() -> None:
    app = FastAPI()

    def read_me(user=Depends(get_user)):
        return user  # pragma: no cover

    with pytest.raises(AssertionError) as exc_info:
        app.get("/tenants/{tenant_id}/me")(read_me)

    # The original exception and message are unchanged.
    assert str(exc_info.value) == "Path params must be of one of the supported types"
    assert notes(exc_info.value) == [
        f"While analyzing {located(get_tenant)}, "
        "the dependency for the parameter 'tenant'",
        f"While analyzing {located(get_user)}, the dependency for the parameter 'user'",
        f"While analyzing {located(read_me)}",
        "While creating the path operation GET /tenants/{tenant_id}/me",
    ]


@needs_notes
def test_error_notes_are_visible_in_the_traceback() -> None:
    app = FastAPI()

    def read_me(user=Depends(get_user)):
        return user  # pragma: no cover

    with pytest.raises(AssertionError) as exc_info:
        app.get("/tenants/{tenant_id}/me")(read_me)

    # What a developer sees at the end of the traceback when the app starts.
    output = "".join(traceback.format_exception(exc_info.value))
    assert output.endswith(
        "AssertionError: Path params must be of one of the supported types\n"
        f"While analyzing {located(get_tenant)}, "
        "the dependency for the parameter 'tenant'\n"
        f"While analyzing {located(get_user)}, "
        "the dependency for the parameter 'user'\n"
        f"While analyzing {located(read_me)}\n"
        "While creating the path operation GET /tenants/{tenant_id}/me\n"
    )


@needs_notes
def test_error_notes_with_router_and_multiple_methods() -> None:
    router = APIRouter()

    def write_items(repository=Depends(get_repository)):
        return repository  # pragma: no cover

    with pytest.raises(AssertionError, match="Cannot specify `Depends`") as exc_info:
        router.api_route("/items", methods=["post", "PUT"])(write_items)

    assert notes(exc_info.value) == [
        f"While analyzing {located(get_repository)}, "
        "the dependency for the parameter 'repository'",
        f"While analyzing {located(write_items)}",
        "While creating the path operation POST, PUT /items",
    ]


@needs_notes
def test_error_notes_for_parameterless_dependency() -> None:
    app = FastAPI()

    def read_items():
        return []  # pragma: no cover

    with pytest.raises(AssertionError) as exc_info:
        app.get("/tenants/{tenant_id}/items", dependencies=[Depends(get_user)])(
            read_items
        )

    assert notes(exc_info.value) == [
        f"While analyzing {located(get_tenant)}, "
        "the dependency for the parameter 'tenant'",
        f"While analyzing {located(get_user)}",
        "While creating the path operation GET /tenants/{tenant_id}/items",
    ]


@needs_notes
def test_error_notes_for_websocket_route() -> None:
    app = FastAPI()

    async def websocket_endpoint(user=Depends(get_user)):
        pass  # pragma: no cover

    with pytest.raises(AssertionError) as exc_info:
        app.websocket("/tenants/{tenant_id}/ws")(websocket_endpoint)

    assert notes(exc_info.value)[-2:] == [
        f"While analyzing {located(websocket_endpoint)}",
        "While creating the WebSocket route /tenants/{tenant_id}/ws",
    ]


class InvalidChecker:
    def __call__(self, value: Annotated[int, Depends(get_db)] = Depends(get_db)):
        return value  # pragma: no cover


@needs_notes
def test_error_notes_for_callable_instance_without_source() -> None:
    app = FastAPI()

    def read_items(checked=Depends(InvalidChecker())):
        return checked  # pragma: no cover

    with pytest.raises(AssertionError) as exc_info:
        app.get("/items")(read_items)

    # An instance has no source location of its own, only its type name is shown.
    assert notes(exc_info.value)[0] == (
        "While analyzing InvalidChecker instance, "
        "the dependency for the parameter 'checked'"
    )


@needs_notes
def test_error_notes_keep_the_original_exception_type() -> None:
    app = FastAPI()

    class NotAModel:
        pass

    def read_items(item: NotAModel):
        return item  # pragma: no cover

    with pytest.raises(FastAPIError, match="request parameter 'item'") as e:
        app.post("/items")(read_items)

    assert notes(e.value) == [
        f"While analyzing {located(read_items)}",
        "While creating the path operation POST /items",
    ]


@needs_notes
def test_no_notes_when_there_is_no_error() -> None:
    app = FastAPI()

    def read_items(db=Depends(get_db)):
        return db  # pragma: no cover

    app.get("/items")(read_items)
    assert len(app.routes) == 5  # openapi, docs, oauth2-redirect, redoc, items


@pytest.mark.skipif(
    sys.version_info >= (3, 11), reason="Python 3.10 has no exception notes"
)
def test_python_310_errors_are_unchanged() -> None:
    app = FastAPI()

    def read_me(user=Depends(get_user)):
        return user  # pragma: no cover

    with pytest.raises(AssertionError) as exc_info:
        app.get("/tenants/{tenant_id}/me")(read_me)

    assert str(exc_info.value) == "Path params must be of one of the supported types"
    assert not hasattr(exc_info.value, "__notes__")
