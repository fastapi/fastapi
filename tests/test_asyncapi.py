from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient


def test_asyncapi_schema():
    """Test AsyncAPI schema endpoint with WebSocket routes."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    @app.websocket("/ws/{item_id}")
    async def websocket_with_param(websocket: WebSocket, item_id: str):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert schema["asyncapi"] == "2.6.0"
    assert schema["info"]["title"] == "Test API"
    assert schema["info"]["version"] == "1.0.0"
    assert "channels" in schema
    assert "/ws" in schema["channels"]
    assert "/ws/{item_id}" in schema["channels"]


def test_asyncapi_no_websockets():
    """Test AsyncAPI schema with no WebSocket routes."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.get("/")
    def read_root():
        return {"message": "Hello World"}

    client = TestClient(app)
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert schema["asyncapi"] == "2.6.0"
    assert schema["info"]["title"] == "Test API"
    assert schema["channels"] == {}


def test_asyncapi_caching():
    """Test that AsyncAPI schema is cached."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    schema1 = app.asyncapi()
    schema2 = app.asyncapi()
    # Should return the same object (identity check)
    assert schema1 is schema2


def test_asyncapi_ui():
    """Test AsyncAPI UI endpoint."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi-docs")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "@asyncapi/react-component" in response.text
    assert "/asyncapi.json" in response.text


def test_asyncapi_ui_navigation():
    """Test navigation links in AsyncAPI UI."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi-docs")
    assert response.status_code == 200, response.text
    # Should contain link to OpenAPI docs
    assert "/docs" in response.text
    assert "OpenAPI Docs" in response.text


def test_swagger_ui_asyncapi_navigation():
    """Test navigation link to AsyncAPI in Swagger UI."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.get("/")
    def read_root():
        return {"message": "Hello World"}

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    # Should contain link to AsyncAPI docs
    assert "/asyncapi-docs" in response.text
    assert "AsyncAPI Docs" in response.text


def test_asyncapi_custom_urls():
    """Test custom AsyncAPI URLs."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        asyncapi_url="/custom/asyncapi.json",
        asyncapi_docs_url="/custom/asyncapi-docs",
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    # Test custom JSON endpoint
    response = client.get("/custom/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert schema["asyncapi"] == "2.6.0"

    # Test custom UI endpoint
    response = client.get("/custom/asyncapi-docs")
    assert response.status_code == 200, response.text
    assert "/custom/asyncapi.json" in response.text

    # Default endpoints should not exist
    response = client.get("/asyncapi.json")
    assert response.status_code == 404
    response = client.get("/asyncapi-docs")
    assert response.status_code == 404


def test_asyncapi_disabled():
    """Test when AsyncAPI is disabled."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        asyncapi_url=None,
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    # Endpoints should return 404
    response = client.get("/asyncapi.json")
    assert response.status_code == 404
    response = client.get("/asyncapi-docs")
    assert response.status_code == 404


def test_asyncapi_channel_structure():
    """Test AsyncAPI channel structure."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    channel = schema["channels"]["/ws"]
    assert "subscribe" in channel
    assert "operationId" in channel["subscribe"]
    assert "message" in channel["subscribe"]


def test_asyncapi_multiple_websockets():
    """Test AsyncAPI with multiple WebSocket routes."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws1")
    async def websocket1(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    @app.websocket("/ws2")
    async def websocket2(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    @app.websocket("/ws3/{param}")
    async def websocket3(websocket: WebSocket, param: str):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert len(schema["channels"]) == 3
    assert "/ws1" in schema["channels"]
    assert "/ws2" in schema["channels"]
    assert "/ws3/{param}" in schema["channels"]


def test_asyncapi_with_metadata():
    """Test AsyncAPI schema includes app metadata."""
    app = FastAPI(
        title="My API",
        version="2.0.0",
        summary="Test summary",
        description="Test description",
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert schema["info"]["title"] == "My API"
    assert schema["info"]["version"] == "2.0.0"
    assert schema["info"]["summary"] == "Test summary"
    assert schema["info"]["description"] == "Test description"


def test_asyncapi_ui_no_docs_url():
    """Test AsyncAPI UI when docs_url is None."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        docs_url=None,
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    response = client.get("/asyncapi-docs")
    assert response.status_code == 200, response.text
    # Should not contain link to /docs if docs_url is None
    # But navigation should still work (just won't show the link)
    assert "/asyncapi.json" in response.text
