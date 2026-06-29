from fastapi import FastAPI
from fastapi.middleware.security_headers import SecurityHeadersMiddleware
from fastapi.testclient import TestClient

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


client = TestClient(app)


def test_default_security_headers():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert response.headers["cross-origin-opener-policy"] == "same-origin"
    assert response.headers["strict-transport-security"] == (
        "max-age=31536000; includeSubDomains"
    )


def test_no_extra_headers():
    response = client.get("/")
    assert "content-security-policy" not in response.headers
    assert "permissions-policy" not in response.headers
    assert "cross-origin-embedder-policy" not in response.headers
    assert "cross-origin-resource-policy" not in response.headers
    assert "cache-control" not in response.headers


def test_does_not_overwrite_existing_headers():
    app2 = FastAPI()
    app2.add_middleware(SecurityHeadersMiddleware)

    @app2.get("/")
    def read_root():
        from starlette.responses import PlainTextResponse

        return PlainTextResponse(
            "ok",
            headers={
                "x-frame-options": "SAMEORIGIN",
                "x-content-type-options": "nosniff",
            },
        )

    client2 = TestClient(app2)
    response = client2.get("/")
    assert response.headers["x-frame-options"] == "SAMEORIGIN"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"


def test_custom_hsts_value():
    app2 = FastAPI()
    app2.add_middleware(SecurityHeadersMiddleware, hsts="max-age=63072000")
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["strict-transport-security"] == "max-age=63072000"


def test_disable_hsts():
    app2 = FastAPI()
    app2.add_middleware(SecurityHeadersMiddleware, hsts=False)
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert "strict-transport-security" not in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"


def test_disable_all_headers():
    app2 = FastAPI()
    app2.add_middleware(
        SecurityHeadersMiddleware,
        hsts=False,
        x_content_type_options=None,
        x_frame_options=None,
        referrer_policy=None,
        cross_origin_opener_policy=None,
        content_security_policy=None,
        permissions_policy=None,
        cross_origin_embedder_policy=None,
        cross_origin_resource_policy=None,
        cache_control=None,
    )
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    for header in [
        "strict-transport-security",
        "x-content-type-options",
        "x-frame-options",
        "referrer-policy",
        "cross-origin-opener-policy",
        "content-security-policy",
        "permissions-policy",
        "cross-origin-embedder-policy",
        "cross-origin-resource-policy",
    ]:
        assert header not in response.headers


def test_content_security_policy():
    app2 = FastAPI()
    csp = "default-src 'self'; script-src 'self'"
    app2.add_middleware(SecurityHeadersMiddleware, content_security_policy=csp)
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["content-security-policy"] == csp


def test_permissions_policy():
    app2 = FastAPI()
    perms = "geolocation=(), microphone=()"
    app2.add_middleware(SecurityHeadersMiddleware, permissions_policy=perms)
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["permissions-policy"] == perms


def test_cross_origin_embedder_policy():
    app2 = FastAPI()
    app2.add_middleware(
        SecurityHeadersMiddleware, cross_origin_embedder_policy="credentialless"
    )
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["cross-origin-embedder-policy"] == "credentialless"


def test_cross_origin_resource_policy():
    app2 = FastAPI()
    app2.add_middleware(
        SecurityHeadersMiddleware, cross_origin_resource_policy="same-origin"
    )
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["cross-origin-resource-policy"] == "same-origin"


def test_cache_control():
    app2 = FastAPI()
    app2.add_middleware(
        SecurityHeadersMiddleware, cache_control="no-store, no-cache, must-revalidate"
    )
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["cache-control"] == "no-store, no-cache, must-revalidate"


def test_custom_x_frame_options():
    app2 = FastAPI()
    app2.add_middleware(SecurityHeadersMiddleware, x_frame_options="SAMEORIGIN")
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["x-frame-options"] == "SAMEORIGIN"


def test_custom_referrer_policy():
    app2 = FastAPI()
    app2.add_middleware(SecurityHeadersMiddleware, referrer_policy="no-referrer")
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["referrer-policy"] == "no-referrer"


def test_custom_cross_origin_opener_policy():
    app2 = FastAPI()
    app2.add_middleware(
        SecurityHeadersMiddleware,
        cross_origin_opener_policy="same-origin-allow-popups",
    )
    client2 = TestClient(app2)

    @app2.get("/")
    def read_root():
        return {"message": "hi"}

    response = client2.get("/")
    assert response.headers["cross-origin-opener-policy"] == "same-origin-allow-popups"


def test_websocket_not_affected():
    app2 = FastAPI()
    app2.add_middleware(SecurityHeadersMiddleware)
    client2 = TestClient(app2)

    from starlette.websockets import WebSocket

    @app2.websocket("/ws")
    async def ws_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text("hello")

    with client2.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "hello"
