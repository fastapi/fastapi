from collections.abc import AsyncIterator
from typing import Annotated

import anyio
import httpx
import pytest
from fastapi import APIRouter, Body, FastAPI, File, Request, UploadFile, WebSocket
from fastapi._form_limits import _FormLimits
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp

pytestmark = pytest.mark.anyio


async def echo(request: Request):
    return PlainTextResponse(await request.body())


async def parse_body(
    data: Annotated[bytes, Body(media_type="application/octet-stream")],
):
    return PlainTextResponse(data)


class BodyStream(httpx.AsyncByteStream):
    def __init__(self, chunks: list[bytes]):
        self.chunks = iter(chunks)
        self.consumed: list[bytes] = []

    def __aiter__(self) -> AsyncIterator[bytes]:
        return self

    async def __anext__(self) -> bytes:
        try:
            chunk = next(self.chunks)
        except StopIteration:
            raise StopAsyncIteration from None
        self.consumed.append(chunk)
        return chunk


async def request(
    app: ASGIApp,
    chunks: list[bytes] | BodyStream,
    *,
    path: str = "/",
    method: str = "POST",
    content_length: str | None = None,
    content_type: str = "application/octet-stream",
) -> httpx.Response:
    headers = {"content-type": content_type}
    if content_length is not None:
        headers["content-length"] = content_length
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        with anyio.fail_after(5):
            return await client.send(
                httpx.Request(
                    method,
                    "http://test" + path,
                    stream=chunks
                    if isinstance(chunks, BodyStream)
                    else BodyStream(chunks),
                    headers=headers,
                )
            )


@pytest.mark.parametrize("content_length", [None, "2", "5", "6", "invalid"])
async def test_body_limit_counts_actual_bytes(content_length):
    app = FastAPI(max_body_size=5)
    app.post("/")(parse_body)
    response = await request(app, [b"123", b"456"], content_length=content_length)
    assert response.status_code == 413


async def test_direct_api_route():
    app = FastAPI()
    app.router.routes.append(
        APIRoute("/", parse_body, methods=["POST"], max_body_size=5)
    )
    assert (await request(app, [b"12345"])).status_code == 200
    assert (await request(app, [b"123456"])).status_code == 413


@pytest.mark.parametrize(
    "limit,size,expected",
    [(None, 6, 200), (0, 0, 200), (0, 1, 413), (5, 4, 200), (5, 5, 200), (5, 6, 413)],
)
async def test_boundary_sizes(limit, size, expected):
    app = FastAPI(max_body_size=limit)
    app.post("/")(echo)
    response = await request(app, [b"x" * size])
    assert response.status_code == expected
    if expected == 200:
        assert response.content == b"x" * size


@pytest.mark.parametrize("owner", ["app", "router"])
@pytest.mark.parametrize(
    "method",
    [
        "get",
        "put",
        "post",
        "delete",
        "options",
        "head",
        "patch",
        "trace",
        "api_route",
        "add_api_route",
    ],
)
async def test_operation_methods_forward_limits(owner, method):
    app = FastAPI(max_body_size=1)
    router = APIRouter()
    target = app if owner == "app" else router
    limits: _FormLimits = {"max_fields": 1}
    if method == "add_api_route":
        target.add_api_route(
            "/", echo, methods=["POST"], max_body_size=5, form_limits=limits
        )
    elif method == "api_route":
        target.api_route("/", methods=["POST"], max_body_size=5, form_limits=limits)(
            echo
        )
    else:
        getattr(target, method)("/", max_body_size=5, form_limits=limits)(echo)
    route = target.routes[-1]
    assert isinstance(route, APIRoute)
    assert route.form_limits == limits
    if owner == "router":
        app.include_router(router)
    http_method = "POST" if method in {"api_route", "add_api_route"} else method.upper()
    assert (await request(app, [b"12345"], method=http_method)).status_code == 200
    assert (await request(app, [b"123456"], method=http_method)).status_code == 413


@pytest.mark.parametrize(
    "app_limit,parent_limit,include_limit,child_limit,route_limit,expected",
    [
        (None, None, None, None, None, 200),
        (5, None, None, None, None, 413),
        (5, 10, None, None, None, 200),
        (10, 5, None, None, None, 413),
        (5, 5, 10, None, None, 200),
        (10, 10, 5, None, None, 413),
        (5, 5, 5, 10, None, 200),
        (10, 10, 10, 5, None, 413),
        (5, 5, 5, 5, 10, 200),
        (10, 10, 10, 10, 5, 413),
        (10, 10, 10, 10, 0, 413),
        (None, None, 0, None, None, 413),
    ],
)
async def test_nested_limit_precedence(
    app_limit, parent_limit, include_limit, child_limit, route_limit, expected
):
    child = APIRouter(max_body_size=child_limit)
    child.post("/", max_body_size=route_limit)(echo)
    parent = APIRouter(max_body_size=parent_limit)
    parent.include_router(child, prefix="/child", max_body_size=include_limit)
    app = FastAPI(max_body_size=app_limit)
    app.include_router(parent, prefix="/parent")
    response = await request(app, [b"123456"], path="/parent/child/")
    assert response.status_code == expected


async def test_shared_router_has_independent_inclusion_defaults():
    router = APIRouter()
    router.post("/")(echo)
    small = FastAPI(max_body_size=5)
    large = FastAPI(max_body_size=10)
    small.include_router(router)
    large.include_router(router)
    large.include_router(router, prefix="/small", max_body_size=5)
    assert (await request(small, [b"123456"])).status_code == 413
    assert (await request(large, [b"123456"])).status_code == 200
    assert (await request(large, [b"123456"], path="/small/")).status_code == 413
    assert (await request(large, [b"123456"])).status_code == 200
    assert router.max_body_size is None
    assert isinstance(router.routes[0], APIRoute)
    assert router.routes[0].max_body_size is None


@pytest.mark.parametrize(
    "parent_limit,child_limit,expected", [(5, None, 413), (5, 10, 200), (10, 5, 413)]
)
@pytest.mark.parametrize("mounted_router", [False, True])
async def test_mounts_inherit_and_override(
    parent_limit, child_limit, expected, mounted_router
):
    child = (
        APIRouter(max_body_size=child_limit)
        if mounted_router
        else FastAPI(max_body_size=child_limit)
    )
    child.post("/")(echo)
    app = FastAPI(max_body_size=parent_limit)
    app.mount("/child", child)
    assert (await request(app, [b"123456"], path="/child/")).status_code == expected


async def test_shared_frontend_uses_each_inclusions_body_limit(tmp_path):
    (tmp_path / "index.html").write_text("hello")
    router = APIRouter()
    router.frontend("/", directory=tmp_path)
    app = FastAPI()
    app.include_router(router, prefix="/empty", max_body_size=0)
    app.include_router(router, prefix="/small", max_body_size=10)

    for path, expected in [("/empty/index.html", 413), ("/small/index.html", 200)]:
        response = await request(
            app, [b"x"], path=path, method="GET", content_length="1"
        )
        assert response.status_code == expected


async def test_mount_in_an_included_router_inherits_its_limit():
    mounted = FastAPI()
    mounted.post("/")(echo)
    router = APIRouter()
    router.mount("/mounted", mounted)
    app = FastAPI()
    app.include_router(router, prefix="/nested", max_body_size=5)
    path = "/nested/mounted/"
    assert (await request(app, [b"12345"], path=path)).status_code == 200
    assert (await request(app, [b"123456"], path=path)).status_code == 413


# Starlette BaseHTTPMiddleware abandons its Request.stream generator after each
# chunk, including when no body limit is configured. Keep other warnings as errors.
@pytest.mark.parametrize("limit", [None, 5])
@pytest.mark.parametrize("body_field", [False, True])
@pytest.mark.parametrize("content_length", [None, "6"])
@pytest.mark.filterwarnings(
    "ignore:Async generator .starlette.requests.Request.stream. was garbage collected:ResourceWarning"
)
async def test_base_http_middleware_preserves_413(limit, body_field, content_length):
    app = FastAPI(max_body_size=limit)
    app.post("/")(parse_body if body_field else echo)

    @app.middleware("http")
    async def pass_through(request, call_next):
        return await call_next(request)

    response = await request(app, [b"123", b"456"], content_length=content_length)
    assert response.status_code == (413 if limit is not None else 200)
    assert (await request(app, [b"12345"])).status_code == 200


@pytest.mark.filterwarnings(
    "ignore:Async generator .starlette.requests.Request.stream. was garbage collected:ResourceWarning"
)
@pytest.mark.parametrize(
    "app_limit,router_limit,route_limit,expected",
    [
        (5, None, 10, 413),  # The middleware reads under the app limit.
        (10, None, 5, 413),  # The route can still reject a cached body.
        (10, 5, 10, 200),  # The selected route overrides the router default.
        (10, 5, None, 413),  # A route without an override inherits that default.
    ],
)
async def test_limits_when_middleware_reads_the_body(
    app_limit, router_limit, route_limit, expected
):
    app = FastAPI(max_body_size=app_limit)
    router = APIRouter(max_body_size=router_limit)
    router.post("/", max_body_size=route_limit)(echo)
    app.include_router(router)

    @app.middleware("http")
    async def read_body(request, call_next):
        await request.body()
        return await call_next(request)

    response = await request(app, [b"123", b"456"])
    assert response.status_code == expected
    if expected == 200:
        assert response.content == b"123456"
    assert (await request(app, [b"12345"])).status_code == 200


@pytest.mark.filterwarnings(
    "ignore:Async generator .starlette.requests.Request.stream. was garbage collected:ResourceWarning"
)
@pytest.mark.parametrize("read_in_parent", [True, False])
@pytest.mark.parametrize("content_length", [None, "6"])
async def test_mounted_app_returns_413_when_middleware_reads_body(
    read_in_parent, content_length
):
    parent = FastAPI(max_body_size=10 if read_in_parent else 5)
    child = FastAPI(max_body_size=5 if read_in_parent else None)
    child.post("/")(echo)
    parent.mount("/child", child)

    reader = parent if read_in_parent else child

    @reader.middleware("http")
    async def read_body(request, call_next):
        await request.body()
        return await call_next(request)

    path = "/child/"
    response = await request(
        parent, [b"123", b"456"], path=path, content_length=content_length
    )
    assert response.status_code == 413
    assert (await request(parent, [b"12345"], path=path)).status_code == 200


async def test_limit_stops_consumption_before_endpoint():
    app = FastAPI(max_body_size=5)
    calls = []

    @app.post("/")
    async def endpoint(data: Annotated[bytes, Body()]):
        calls.append(data)
        return data

    stream = BodyStream([b"123", b"456", b"unread"])
    response = await request(app, stream)
    assert response.status_code == 413
    assert calls == []
    assert stream.consumed == [b"123", b"456"]
    accepted = await request(app, [b"ok"])
    assert accepted.status_code == 200
    assert accepted.json() == "ok"
    assert calls == [b"ok"]


@pytest.mark.parametrize("limit", [0, 5])
async def test_query_and_headers_do_not_count_as_body(limit):
    app = FastAPI(max_body_size=limit)
    app.post("/")(echo)
    response = await request(app, [b""], path="/?q=" + "x" * 100)
    assert response.status_code == 200


@pytest.mark.parametrize("value", [-1, True, False, 1.5, "5"])
def test_invalid_application_limit(value):
    with pytest.raises(ValueError, match="non-negative integer"):
        FastAPI(max_body_size=value)


@pytest.mark.parametrize(
    "configure",
    [
        lambda: APIRouter(max_body_size=-1),
        lambda: FastAPI().post("/", max_body_size=-1)(echo),
        lambda: FastAPI().include_router(APIRouter(), max_body_size=-1),
        lambda: APIRoute("/", echo, max_body_size=-1),
    ],
    ids=["router", "operation", "include", "direct"],
)
def test_invalid_limit_fails_at_registration(configure):
    with pytest.raises(ValueError, match="non-negative integer"):
        configure()


def test_lifespan_and_websockets_are_unaffected():
    events = []

    async def lifespan(app):
        events.append("startup")
        yield
        events.append("shutdown")

    app = FastAPI(max_body_size=0, lifespan=lifespan)

    @app.websocket("/ws")
    async def websocket(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text(await websocket.receive_text())

    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket_client:
            websocket_client.send_text("larger than the HTTP limit")
            assert websocket_client.receive_text() == "larger than the HTTP limit"
    assert events == ["startup", "shutdown"]


async def test_multipart_rejection_closes_temporary_files(monkeypatch):
    from starlette import formparsers

    created = []
    original = formparsers.SpooledTemporaryFile

    def track_file(*args, **kwargs):
        file = original(*args, **kwargs)
        created.append(file)
        return file

    monkeypatch.setattr(formparsers, "SpooledTemporaryFile", track_file)
    prefix = (
        b"--boundary\r\n"
        b'Content-Disposition: form-data; name="file"; filename="example.txt"\r\n'
        b"Content-Type: text/plain\r\n\r\n"
        b"hello"
    )
    suffix = b"more data\r\n--boundary--\r\n"
    app = FastAPI(max_body_size=len(prefix))

    @app.post("/")
    async def endpoint(file: Annotated[UploadFile, File()]):
        return {"name": file.filename}

    response = await request(
        app, [prefix, suffix], content_type="multipart/form-data; boundary=boundary"
    )
    assert response.status_code == 413
    assert created
    assert all(file.closed for file in created)

    # A complete accepted upload still reaches the endpoint and is closed.
    accepted = prefix + b"\r\n--boundary--\r\n"
    larger = FastAPI(max_body_size=len(accepted))
    larger.post("/")(endpoint)
    response = await request(
        larger, [accepted], content_type="multipart/form-data; boundary=boundary"
    )
    assert response.status_code == 200
    assert response.json() == {"name": "example.txt"}
    assert all(file.closed for file in created)


async def test_body_parsing_without_limit_preserves_existing_error_response(
    monkeypatch,
):
    async def failed_read(self):
        raise ExceptionGroup("read failed", [HTTPException(413)])

    monkeypatch.setattr(Request, "body", failed_read)
    app = FastAPI()
    app.post("/")(parse_body)
    response = await request(app, [b"hello"])
    assert response.status_code == 400
    assert response.json() == {"detail": "There was an error parsing the body"}


async def test_group_with_a_limit_error_preserves_other_errors():
    app = FastAPI(max_body_size=0)
    cleanup_error = RuntimeError("cleanup failed")

    @app.post("/")
    async def endpoint(request: Request):
        try:
            await request.body()
        except HTTPException as exc:
            raise ExceptionGroup("read and cleanup", [exc, cleanup_error]) from exc

    with pytest.raises(ExceptionGroup) as caught:
        await request(app, [b"x"])
    assert len(caught.value.exceptions) == 2
    assert isinstance(caught.value.exceptions[0], HTTPException)
    assert caught.value.exceptions[0].status_code == 413
    assert caught.value.exceptions[1] is cleanup_error


@pytest.mark.parametrize(
    "error",
    [
        ExceptionGroup("other", [RuntimeError("other error")]),
        ExceptionGroup("application error", [HTTPException(413)]),
        ExceptionGroup("mixed", [HTTPException(413), ValueError("unrelated")]),
    ],
)
@pytest.mark.parametrize("mounted", [False, True])
async def test_body_limit_does_not_hide_unrelated_exception_groups(error, mounted):
    app = FastAPI(max_body_size=5)

    @app.post("/")
    async def endpoint():
        raise error

    parent = FastAPI(max_body_size=10)
    parent.mount("/child", app)
    with pytest.raises(ExceptionGroup) as caught:
        if mounted:
            await request(parent, [b""], path="/child/")
        else:
            await request(app, [b""])
    assert caught.value is error
