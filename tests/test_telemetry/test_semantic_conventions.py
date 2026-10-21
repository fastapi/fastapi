import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .conftest import metric_points, server_spans


@pytest.mark.parametrize(
    "scheme,host,expected",
    [
        (
            "http",
            "public.example",
            {"server.address": "public.example", "server.port": 80},
        ),
        (
            "https",
            "public.example",
            {"server.address": "public.example", "server.port": 443},
        ),
        (
            "http",
            "public.example:8443",
            {"server.address": "public.example", "server.port": 8443},
        ),
        (
            "http",
            "[2001:db8::1]:8443",
            {"server.address": "2001:db8::1", "server.port": 8443},
        ),
        ("http", "[2001:db8::1]", {"server.address": "2001:db8::1", "server.port": 80}),
        ("http", "public.example:invalid", {}),
        ("http", "[invalid", {}),
        ("http", "public.example:99999", {}),
        ("http", "user:password@public.example", {}),
        ("http", "public.example/path", {}),
        ("http", "", {}),
        ("custom", "public.example", {"server.address": "public.example"}),
    ],
)
def test_request_authority_is_only_on_spans(telemetry, scheme, host, expected):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/")
    async def endpoint():
        return "ok"

    async def asgi(scope, receive, send):
        scope["scheme"] = scheme
        await app(scope, receive, send)

    client = TestClient(asgi, base_url="http://listener:8000")
    assert client.get("/", headers={"host": host}).json() == "ok"
    (span,) = server_spans(exporter)
    assert {
        key: value
        for key, value in span.attributes.items()
        if key.startswith("server.")
    } == expected
    for name in ("http.server.request.duration", "http.server.active_requests"):
        (point,) = metric_points(reader=reader, name=name)
        assert not any(key.startswith("server.") for key in point.attributes)


def test_server_fallback_without_host_header(telemetry):
    config, exporter, _ = telemetry
    app = FastAPI(telemetry=config)

    async def asgi(scope, receive, send):
        scope["headers"] = [
            (name, value) for name, value in scope["headers"] if name != b"host"
        ]
        await app(scope, receive, send)

    assert TestClient(asgi, base_url="http://listener:8000").get("/").status_code == 404
    (span,) = server_spans(exporter)
    assert span.attributes["server.address"] == "listener"
    assert span.attributes["server.port"] == 8000


@pytest.mark.parametrize(
    "query,expected",
    [
        ("", None),
        (
            "?tag=one&tag=two&empty=&flag",
            "tag=one&tag=two&empty=&flag=",
        ),
        (
            "?X-Amz-Signature=secret&X-Amz-Credential=secret&X-Amz-Security-Token=secret&sig=secret&X-Goog-Signature=secret",
            "X-Amz-Signature=REDACTED&X-Amz-Credential=REDACTED&X-Amz-Security-Token=REDACTED&sig=REDACTED&X-Goog-Signature=REDACTED",
        ),
        (
            "?%70age=2&q=fastapi%20tutorial&sort%20by=name",
            "page=2&q=fastapi+tutorial&sort+by=name",
        ),
        (
            "?%73ig=secret&q=hello%26world",
            "sig=REDACTED&q=hello%26world",
        ),
        (
            "?x-amz-signature=keep&x-amz-credential=keep&x-amz-security-token=keep&SIG=keep&x-goog-signature=keep",
            "x-amz-signature=keep&x-amz-credential=keep&x-amz-security-token=keep&SIG=keep&x-goog-signature=keep",
        ),
        (
            "?sig=one&sig=two&sig=&q=hello+world",
            "sig=REDACTED&sig=REDACTED&sig=REDACTED&q=hello+world",
        ),
    ],
)
def test_url_attributes_do_not_split_metrics(telemetry, query, expected):
    config, exporter, reader = telemetry
    app = FastAPI(telemetry=config)

    @app.get("/items/{item_id}")
    async def endpoint(item_id: int):
        return item_id

    client = TestClient(app)
    for item_id in (1, 2):
        assert (
            client.get(
                f"/items/{item_id}{query}", headers={"host": f"host-{item_id}.example"}
            ).json()
            == item_id
        )
    first, second = server_spans(exporter)
    assert first.attributes["url.path"] == "/items/1"
    assert second.attributes["url.path"] == "/items/2"
    assert first.attributes.get("url.query") == expected
    assert second.attributes.get("url.query") == expected
    (point,) = metric_points(reader=reader)
    assert point.count == 2
    assert "url.path" not in point.attributes
    assert "url.query" not in point.attributes
    assert point.attributes["http.route"] == "/items/{item_id}"


@pytest.mark.parametrize("metrics", [None, False, True])
def test_active_requests_follow_metrics_setting(telemetry, metrics):
    config, _, reader = telemetry
    if metrics is not None:
        config["metrics"] = metrics
    app = FastAPI(telemetry=config)
    seen = []

    @app.get("/")
    async def endpoint():
        seen.extend(
            point.value
            for point in metric_points(
                reader=reader, name="http.server.active_requests"
            )
        )
        return "ok"

    assert TestClient(app).get("/").json() == "ok"
    active = metrics is not False
    assert seen == ([1] if active else [])
    points = metric_points(reader=reader, name="http.server.active_requests")
    assert [point.value for point in points] == ([0] if active else [])
    assert bool(metric_points(reader=reader)) == active
