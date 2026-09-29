import asyncio
from contextlib import asynccontextmanager

import anyio
import pytest
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse
from fastapi.testclient import TestClient
from opentelemetry import baggage, propagate, trace
from opentelemetry.propagators import textmap
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF
from opentelemetry.trace import SpanKind, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from starlette.middleware import Middleware
from starlette.types import Scope

from ._subprocess import run_in_subprocess
from .conftest import metric_points, server_spans


def test_request_context_and_span_attributes(telemetry):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)
    seen = []

    @app.get("/items/{item_id}")
    async def endpoint(item_id: int):
        seen.append(trace.get_current_span().get_span_context())
        return item_id

    client = TestClient(app)
    parent_trace = "0123456789abcdef0123456789abcdef"
    parent_span = "0123456789abcdef"
    response = client.get(
        "/items/123?page=2&sig=signature-secret",
        headers={
            "traceparent": f"00-{parent_trace}-{parent_span}-01",
            "authorization": "Bearer authorization-secret",
        },
    )
    assert response.json() == 123
    (span,) = server_spans(exporter)
    assert span.kind == SpanKind.SERVER
    assert span.name == "GET /items/{item_id}"
    endpoint_span = next(
        s for s in exporter.get_finished_spans() if s.name == "fastapi.endpoint"
    )
    assert endpoint_span.context == seen[0]
    assert endpoint_span.parent.span_id == span.context.span_id
    assert span.context.trace_id == int(parent_trace, 16)
    assert span.parent.span_id == int(parent_span, 16)
    assert span.status.status_code == StatusCode.UNSET
    assert span.attributes["http.route"] == "/items/{item_id}"
    assert span.attributes["http.response.status_code"] == 200
    assert "signature-secret" not in repr(span.attributes)
    assert "authorization-secret" not in repr(span.attributes)
    assert span.attributes["url.path"] == "/items/123"
    assert span.attributes["url.query"] == "page=2&sig=REDACTED"
    points = metric_points(reader=reader)
    assert len(points) == 1
    assert points[0].count == 1
    assert points[0].sum > 0
    assert points[0].attributes["http.route"] == "/items/{item_id}"
    assert points[0].explicit_bounds == (
        0.005,
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1,
        2.5,
        5,
        7.5,
        10,
    )
    assert (
        metric_points(reader=reader, name="http.server.active_requests")[0].value == 0
    )
    assert not trace.get_current_span().get_span_context().is_valid


@pytest.mark.parametrize("split_headers", [False, True])
def test_propagation_headers(telemetry, split_headers):
    config, exporter, _ = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/")
    async def endpoint():
        return dict(baggage.get_all())

    trace_id = "0123456789abcdef0123456789abcdef"
    parent_id = "0123456789abcdef"
    headers = [("traceparent", f"00-{trace_id}-{parent_id}-01")]
    for name, values in [
        ("tracestate", ["vendora=one", "vendorb=two"]),
        ("baggage", ["first=one", "second=two"]),
    ]:
        headers.extend(
            (name, value) for value in (values if split_headers else [",".join(values)])
        )
    response = TestClient(app).get("/", headers=headers)
    assert response.json() == {"first": "one", "second": "two"}
    (span,) = server_spans(exporter)
    assert span.context.trace_id == int(trace_id, 16)
    assert span.parent.span_id == int(parent_id, 16)
    assert list(span.context.trace_state.items()) == [
        ("vendora", "one"),
        ("vendorb", "two"),
    ]
    assert not baggage.get_all()


def test_custom_propagator_can_read_repeated_headers(telemetry, monkeypatch):
    class HeaderPropagator(TraceContextTextMapPropagator):
        def extract(self, carrier, context=None, getter=textmap.default_getter):
            assert "x-custom-context" in getter.keys(carrier)
            values = getter.get(carrier, "X-Custom-Context")
            assert values is not None
            assert values == ["one, two", "three"]
            assert getter.get(carrier, "missing-header") is None
            context = super().extract(carrier, context=context, getter=getter)
            return baggage.set_baggage("custom", "|".join(values), context=context)

    monkeypatch.setattr(propagate, "get_global_textmap", lambda: HeaderPropagator())
    config, _, _ = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/")
    async def endpoint():
        return baggage.get_baggage("custom")

    response = TestClient(app).get(
        "/", headers=[("x-custom-context", "one, two"), ("x-custom-context", "three")]
    )
    assert response.json() == "one, two|three"
    assert not baggage.get_all()


@pytest.mark.parametrize(
    "path,status,route,error",
    [
        ("/ok", 200, "/ok", False),
        ("/missing", 404, None, False),
        ("/validation/no", 422, "/validation/{value}", False),
        ("/validation/1", 200, "/validation/{value}", False),
        ("/fail", 500, "/fail", True),
        ("/handled", 503, "/handled", True),
        ("/ok/", 307, "/ok", False),
    ],
)
def test_http_statuses(telemetry, path, status, route, error):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/ok")
    def ok():
        return "ok"

    @app.get("/validation/{value}")
    def validation(value: int):
        return value

    @app.get("/fail")
    def fail():
        raise ValueError("endpoint failed")

    @app.get("/handled")
    async def handled():
        raise HTTPException(503, "Unavailable")

    assert (
        TestClient(app, raise_server_exceptions=False)
        .get(path, follow_redirects=False)
        .status_code
        == status
    )
    (span,) = server_spans(exporter)
    assert span.attributes["http.response.status_code"] == status
    assert span.attributes.get("http.route") == route
    assert (span.status.status_code == StatusCode.ERROR) == error
    assert "endpoint failed" not in repr(span.attributes)
    assert span.events == ()
    assert sum(p.count for p in metric_points(reader=reader)) == 1


def test_custom_error_handler_sees_span(telemetry):
    config, exporter, reader = telemetry
    seen = []

    async def error_handler(request, exc):
        span = trace.get_current_span()
        seen.append(span.is_recording())
        span.set_attribute("handled", True)
        return JSONResponse({"error": "handled"}, status_code=500)

    app = FastAPI(telemetry=config, exception_handlers={500: error_handler})

    @app.get("/")
    def endpoint():
        raise ValueError("endpoint failed")

    assert TestClient(app, raise_server_exceptions=False).get("/").json() == {
        "error": "handled"
    }
    (span,) = server_spans(exporter)
    assert seen == [True]
    assert span.attributes["handled"] is True
    assert span.attributes["error.type"] == "ValueError"


def test_route_prefix_and_dynamic_mount(telemetry):
    config, exporter, reader = telemetry
    parent = FastAPI(telemetry=config, root_path="/proxy")
    child = FastAPI()
    router = APIRouter(prefix="/v1")

    @router.get("/items/{item_id}")
    def endpoint(item_id: int):
        return item_id

    child.include_router(router, prefix="/api")
    parent.mount("/tenants/{tenant}", child)
    response = TestClient(parent).get("/proxy/tenants/acme/api/v1/items/4")
    assert response.json() == 4
    (span,) = server_spans(exporter)
    assert (
        span.attributes["http.route"]
        == "/proxy/tenants/{tenant}/api/v1/items/{item_id}"
    )
    assert span.name == "GET /proxy/tenants/{tenant}/api/v1/items/{item_id}"
    assert span.attributes["url.path"] == "/proxy/tenants/acme/api/v1/items/4"
    assert "acme" not in repr(metric_points(reader=reader)[0].attributes)
    assert sum(p.count for p in metric_points(reader=reader)) == 1


@pytest.mark.parametrize("nested", [False, True])
@pytest.mark.parametrize("route_type", ["fastapi", "starlette"])
def test_included_router_redirect_template(telemetry, nested, route_type):
    config, exporter, reader = telemetry
    router = APIRouter()

    def endpoint(request: Request):
        return PlainTextResponse("ok")

    if route_type == "fastapi":
        router.add_api_route("/items/{item_id}/", endpoint)
    else:
        router.add_route("/items/{item_id}/", endpoint)
    if nested:
        outer = APIRouter()
        outer.include_router(router, prefix="/v1")
        router = outer
    child = FastAPI()
    child.include_router(router, prefix="/api")
    app = FastAPI(telemetry=config)
    app.mount("/tenants/{tenant}", child)
    prefix = "/api" + ("/v1" if nested else "")
    path = "/tenants/acme" + prefix + "/items/1"
    template = "/tenants/{tenant}" + prefix + "/items/{item_id}/"
    client = TestClient(app)
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "http://testserver" + path + "/"
    (span,) = server_spans(exporter)
    assert span.name == "GET " + template
    assert span.attributes["http.route"] == template
    (point,) = metric_points(reader=reader)
    assert point.count == 1
    assert point.attributes["http.route"] == template
    assert client.get(path + "/").text == "ok"


def test_method_not_allowed_and_docs(telemetry):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/items/{value}")
    def endpoint(value: str):
        return value

    client = TestClient(app)
    assert client.post("/items/x").status_code == 405
    assert client.get("/docs").status_code == 200
    assert [s.attributes["http.route"] for s in exporter.get_finished_spans()] == [
        "/items/{value}",
        "/docs",
    ]
    assert client.get("/items/x").json() == "x"


def test_stream_completes_before_background_and_cleanup(telemetry):
    config, exporter, reader = telemetry
    seen = []
    app = FastAPI(telemetry=config)

    async def dependency():
        yield
        seen.append(("cleanup", len(server_spans(exporter))))

    async def background():
        seen.append(("background", len(server_spans(exporter))))

    @app.get("/", dependencies=[Depends(dependency)])
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(background)

        async def stream():
            yield "one"
            assert not server_spans(exporter)
            await anyio.sleep(0)
            yield "two"

        return StreamingResponse(stream())

    assert TestClient(app).get("/").text == "onetwo"
    assert seen == [("background", 1), ("cleanup", 1)]
    assert sum(p.count for p in metric_points(reader=reader)) == 1


@pytest.mark.parametrize(
    "tracing,metering", [(True, False), (False, True), (False, False)]
)
def test_independent_signals(telemetry, tracing, metering):
    config, exporter, reader = telemetry
    config["tracing"], config["metrics"] = tracing, metering
    app = FastAPI(telemetry=config)
    TestClient(app).get("/missing")
    assert len(exporter.get_finished_spans()) == int(tracing)
    assert sum(p.count for p in metric_points(reader=reader)) == int(metering)


def test_configuration_is_copied_for_each_app(telemetry):
    config, exporter, reader = telemetry
    original = config.copy()
    enabled = FastAPI(telemetry=config)
    assert config == original

    config["tracing"] = False
    disabled = FastAPI(telemetry=config)
    config["tracing"] = True

    assert TestClient(enabled).get("/").status_code == 404
    assert TestClient(disabled).get("/").status_code == 404
    assert len(server_spans(exporter)) == 1
    assert sum(point.count for point in metric_points(reader=reader)) == 2


def test_unsampled_requests_still_record_metrics(telemetry):
    config, exporter, reader = telemetry
    config["tracer_provider"].sampler = ALWAYS_OFF
    TestClient(FastAPI(telemetry=config)).get("/missing")
    assert not exporter.get_finished_spans()
    assert metric_points(reader=reader)[0].count == 1


def test_exclusion(telemetry):
    config, exporter, reader = telemetry
    config["exclude"] = lambda scope: scope["path"] == "/health"
    client = TestClient(FastAPI(telemetry=config))
    client.get("/health")
    assert not exporter.get_finished_spans()
    assert not metric_points(reader=reader)
    client.get("/other")
    assert len(exporter.get_finished_spans()) == 1


@pytest.mark.parametrize("raises", [False, True])
def test_middleware_response_or_error(telemetry, raises):
    config, exporter, reader = telemetry

    class CustomMiddleware:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            if raises:
                raise RuntimeError("middleware failed")
            await PlainTextResponse("middleware")(scope, receive, send)

    app = FastAPI(telemetry=config, middleware=[Middleware(CustomMiddleware)])
    response = TestClient(app, raise_server_exceptions=False).get("/")
    assert response.status_code == (500 if raises else 200)
    (span,) = server_spans(exporter)
    assert "http.route" not in span.attributes
    if raises:
        assert span.attributes["error.type"] == "RuntimeError"


@pytest.mark.parametrize(
    "kind", ["trailers", "disconnect", "cancel", "pathsend", "incomplete", "send_error"]
)
def test_asgi_lifecycle(telemetry, kind):
    from fastapi.telemetry._asgi import NativeTelemetry

    config, exporter, reader = telemetry
    sent = []
    scope: Scope = {
        "type": "http",
        "method": "GET",
        "scheme": "http",
        "path": "/",
        "headers": [],
    }

    async def receive():
        return {"type": "http.disconnect"}

    async def send(message):
        if kind == "send_error":
            raise OSError("closed")
        sent.append(message)

    async def app(scope, receive, send):
        if kind == "disconnect":
            await receive()
            return
        if kind == "cancel":
            raise asyncio.CancelledError()
        if kind == "incomplete":
            return
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "trailers": kind == "trailers",
            }
        )
        if kind == "pathsend":
            await send({"type": "http.response.pathsend", "path": "/tmp/example"})
        else:
            await send({"type": "http.response.body", "body": b"ok"})
        if kind == "trailers":
            assert not exporter.get_finished_spans()
            await send(
                {"type": "http.response.trailers", "headers": [], "more_trailers": True}
            )
            assert not exporter.get_finished_spans()
            await send({"type": "http.response.trailers", "headers": []})

    async def run():
        await NativeTelemetry(FastAPI(telemetry=config)._telemetry)(
            app=app, scope=scope, receive=receive, send=send
        )

    if kind == "cancel":
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(run())
    elif kind == "send_error":
        with pytest.raises(OSError):
            asyncio.run(run())
    else:
        asyncio.run(run())
    (span,) = server_spans(exporter)
    assert (span.status.status_code == StatusCode.ERROR) == (
        kind in {"cancel", "disconnect", "incomplete", "send_error"}
    )
    assert metric_points(reader=reader)[0].count == 1
    assert (
        metric_points(reader=reader, name="http.server.active_requests")[0].value == 0
    )
    assert "fastapi.telemetry" not in scope


def test_multiple_lifespans_borrowed_providers(telemetry):
    config, exporter, reader = telemetry
    lifecycle = []

    @asynccontextmanager
    async def lifespan(app):
        lifecycle.append("start")
        yield {"state": True}
        lifecycle.append("stop")

    first = FastAPI(telemetry=config, lifespan=lifespan)
    second = FastAPI(telemetry=config)
    for app in [first, second, first]:
        with TestClient(app) as client:
            assert client.get("/").status_code == 404
    assert lifecycle == ["start", "stop", "start", "stop"]
    assert len(exporter.get_finished_spans()) == 3
    assert sum(p.count for p in metric_points(reader=reader)) == 3


@pytest.mark.parametrize(
    "method",
    [
        "CONNECT",
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
        "QUERY",
        "TRACE",
    ],
)
def test_known_http_methods(telemetry, method):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.api_route("/items/{value}", methods=[method])
    def endpoint(value: str):
        return value

    assert TestClient(app).request(method, "/items/1").status_code == 200
    (span,) = server_spans(exporter)
    assert span.name == f"{method} /items/{{value}}"
    assert span.attributes["http.request.method"] == method
    assert "http.request.method_original" not in span.attributes
    assert metric_points(reader=reader)[0].attributes["http.request.method"] == method
    assert (
        metric_points(reader=reader, name="http.server.active_requests")[0].attributes[
            "http.request.method"
        ]
        == method
    )


@pytest.mark.parametrize(
    "path,status,span_name",
    [("/items/1", 405, "HTTP /items/{value}"), ("/missing", 404, "HTTP")],
)
def test_unknown_method_has_bounded_span_name(telemetry, path, status, span_name):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/items/{value}")
    def endpoint(value: str):
        return value

    assert TestClient(app).request("PRIVATE_METHOD", path).status_code == status
    (span,) = server_spans(exporter)
    assert span.name == span_name
    assert span.attributes["http.request.method"] == "_OTHER"
    assert span.attributes["http.request.method_original"] == "PRIVATE_METHOD"
    for name in ("http.server.request.duration", "http.server.active_requests"):
        attributes = metric_points(reader=reader, name=name)[0].attributes
        assert attributes["http.request.method"] == "_OTHER"
        assert "http.request.method_original" not in attributes
    assert TestClient(app).get("/items/1").json() == "1"


@pytest.mark.parametrize("matched", [True, False])
@pytest.mark.parametrize(
    "known_methods,method,expected",
    [
        (" QUERY , PROPFIND , ", "QUERY", "QUERY"),
        (" QUERY , PROPFIND , ", "PROPFIND", "PROPFIND"),
        ("QUERY,PROPFIND", "GET", "_OTHER"),
        ("query", "QUERY", "_OTHER"),
        ("CUSTOM", "CUSTOM", "CUSTOM"),
        ("", "QUERY", "QUERY"),
        ("  ", "QUERY", "QUERY"),
    ],
)
def test_known_http_methods_override(
    telemetry, monkeypatch, known_methods, method, expected, matched
):
    monkeypatch.setenv("OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS", known_methods)
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.api_route("/items/{value}", methods=[method])
    def endpoint(value: str):
        return value

    path = "/items/1" if matched else "/missing"
    assert TestClient(app).request(method, path).status_code == (
        200 if matched else 404
    )
    (span,) = server_spans(exporter)
    span_method = "HTTP" if expected == "_OTHER" else method
    assert span.name == span_method + (" /items/{value}" if matched else "")
    assert span.attributes["http.request.method"] == expected
    if expected == "_OTHER":
        assert span.attributes["http.request.method_original"] == method
    else:
        assert "http.request.method_original" not in span.attributes
    for name in ("http.server.request.duration", "http.server.active_requests"):
        attributes = metric_points(reader=reader, name=name)[0].attributes
        assert attributes["http.request.method"] == expected
        assert "http.request.method_original" not in attributes


def test_frontend_and_static_templates(telemetry, tmp_path):
    from fastapi.staticfiles import StaticFiles

    config, exporter, reader = telemetry
    (tmp_path / "index.html").write_text("index")
    (tmp_path / "script.js").write_text("script")
    app = FastAPI(telemetry=config)
    app.mount("/static", StaticFiles(directory=tmp_path))
    router = APIRouter()
    router.frontend("/ui", directory=tmp_path, fallback="index.html")
    app.include_router(router, prefix="/app")
    client = TestClient(app)
    assert client.get("/static/script.js").text == "script"
    assert (
        client.get("/app/ui/arbitrary/path", headers={"accept": "text/html"}).text
        == "index"
    )
    assert [s.attributes["http.route"] for s in exporter.get_finished_spans()] == [
        "/static/{path}",
        "/app/ui/{path}",
    ]


def test_included_mount_template(telemetry):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)
    child = FastAPI()

    @child.get("/items/{value}")
    def endpoint(value: str):
        return value

    router = APIRouter()
    router.mount("/tenants/{tenant}", child)
    app.include_router(router, prefix="/api")
    assert TestClient(app).get("/api/tenants/acme/items/1").json() == "1"
    (span,) = server_spans(exporter)
    assert span.attributes["http.route"] == "/api/tenants/{tenant}/items/{value}"


@pytest.mark.parametrize("explicit_proxy", [False, True])
@run_in_subprocess
def test_late_global_providers_enable_existing_app(explicit_proxy):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from opentelemetry import metrics, trace
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    app = FastAPI(
        telemetry={
            "tracer_provider": trace.get_tracer_provider(),
            "meter_provider": metrics.get_meter_provider(),
        }
        if explicit_proxy
        else None
    )
    client = TestClient(app)
    assert client.get("/").status_code == 404
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    reader = InMemoryMetricReader()
    trace.set_tracer_provider(provider)
    metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
    assert client.get("/").status_code == 404
    assert len(exporter.get_finished_spans()) == 1
    assert reader.get_metrics_data() is not None


def test_base_http_middleware_preserves_context_and_route(telemetry):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)
    seen = []

    @app.middleware("http")
    async def middleware(request, call_next):
        seen.append(trace.get_current_span().get_span_context().span_id)
        return await call_next(request)

    @app.get("/items/{item_id}")
    async def endpoint(item_id: int):
        seen.append(trace.get_current_span().get_span_context().span_id)
        return item_id

    assert TestClient(app).get("/items/1").json() == 1
    (span,) = server_spans(exporter)
    endpoint_span = next(
        s for s in exporter.get_finished_spans() if s.name == "fastapi.endpoint"
    )
    assert seen == [span.context.span_id, endpoint_span.context.span_id]
    assert endpoint_span.parent.span_id == span.context.span_id
    assert span.attributes["http.route"] == "/items/{item_id}"
