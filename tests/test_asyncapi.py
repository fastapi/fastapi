from fastapi import APIRouter, Body, Depends, FastAPI, WebSocket
from fastapi.asyncapi.utils import get_asyncapi, get_asyncapi_channel
from fastapi.testclient import TestClient
from pydantic import BaseModel


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
    with client.websocket_connect("/ws"):
        pass
    with client.websocket_connect("/ws/foo"):
        pass
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
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
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

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
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
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws1"):
        pass
    with client.websocket_connect("/ws2"):
        pass
    with client.websocket_connect("/ws3/bar"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
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
    with client.websocket_connect("/ws"):
        pass
    response = client.get("/asyncapi-docs")
    assert response.status_code == 200, response.text
    # Should not contain link to /docs if docs_url is None
    # But navigation should still work (just won't show the link)
    assert "/asyncapi.json" in response.text


def test_asyncapi_with_servers():
    """Test AsyncAPI schema with custom servers."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        servers=[{"url": "wss://example.com", "protocol": "wss"}],
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert "servers" in schema
    assert schema["servers"] == [{"url": "wss://example.com", "protocol": "wss"}]


def test_asyncapi_with_all_metadata():
    """Test AsyncAPI schema with all optional metadata fields."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        summary="Test summary",
        description="Test description",
        terms_of_service="https://example.com/terms",
        contact={"name": "API Support", "email": "support@example.com"},
        license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert schema["info"]["summary"] == "Test summary"
    assert schema["info"]["description"] == "Test description"
    assert schema["info"]["termsOfService"] == "https://example.com/terms"
    assert schema["info"]["contact"] == {
        "name": "API Support",
        "email": "support@example.com",
    }
    assert schema["info"]["license"] == {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }


def test_asyncapi_with_external_docs():
    """Test AsyncAPI schema with external documentation."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    # Set external_docs after app creation
    app.openapi_external_docs = {
        "description": "External API documentation",
        "url": "https://docs.example.com",
    }

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert "externalDocs" in schema
    assert schema["externalDocs"] == {
        "description": "External API documentation",
        "url": "https://docs.example.com",
    }


def test_asyncapi_channel_with_route_name():
    """Test AsyncAPI channel with named route."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws", name="my_websocket")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    channel = schema["channels"]["/ws"]
    assert channel["subscribe"]["operationId"] == "my_websocket"
    assert channel["publish"]["operationId"] == "my_websocket_publish"


def test_get_asyncapi_channel_direct():
    """Test get_asyncapi_channel function directly."""
    from fastapi import routing

    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws", name="test_ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    # Get the route from the app
    route = next(r for r in app.routes if isinstance(r, routing.APIWebSocketRoute))
    channel = get_asyncapi_channel(route=route)
    assert "subscribe" in channel
    assert "publish" in channel
    assert channel["subscribe"]["operationId"] == "test_ws"
    assert channel["publish"]["operationId"] == "test_ws_publish"


def test_get_asyncapi_direct():
    """Test get_asyncapi function directly."""
    app = FastAPI(title="Test API", version="1.0.0")

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    schema = get_asyncapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    assert schema["asyncapi"] == "2.6.0"
    assert schema["info"]["title"] == "Test API"
    assert "/ws" in schema["channels"]


def test_asyncapi_url_none_no_link_in_swagger():
    """Test that Swagger UI doesn't show AsyncAPI link when asyncapi_url is None."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        asyncapi_url=None,  # Explicitly disabled
        # asyncapi_docs_url defaults to "/asyncapi-docs"
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    client = TestClient(app)
    with client.websocket_connect("/ws"):
        pass
    # Swagger UI should not show AsyncAPI link when asyncapi_url is None
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert "/asyncapi-docs" not in response.text

    # AsyncAPI endpoint should not exist
    response = client.get("/asyncapi-docs")
    assert response.status_code == 404


def test_asyncapi_components_and_message_payload():
    """Test AsyncAPI schema includes components/schemas and message payload when models are used."""
    app = FastAPI(title="Test API", version="1.0.0")

    class QueryMessage(BaseModel):
        """Message sent on /query channel."""

        text: str
        limit: int = 10

    def get_query_message(
        msg: QueryMessage = Body(default=QueryMessage(text="", limit=10)),
    ) -> QueryMessage:
        return msg

    @app.websocket("/query")
    async def query_ws(
        websocket: WebSocket, msg: QueryMessage = Depends(get_query_message)
    ):
        await websocket.accept()
        await websocket.close()

    # Connect to websocket so handler and dependency are covered (body default used)
    client = TestClient(app)
    with client.websocket_connect("/query"):
        pass

    # Generate schema and assert components
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()

    # Should have components with schemas (reusable model definitions)
    assert "components" in schema
    assert "schemas" in schema["components"]
    assert "QueryMessage" in schema["components"]["schemas"]
    query_schema = schema["components"]["schemas"]["QueryMessage"]
    assert query_schema.get("title") == "QueryMessage"
    assert "text" in query_schema.get("properties", {})
    assert "limit" in query_schema.get("properties", {})

    # Channel messages should reference the payload schema
    channel = schema["channels"]["/query"]
    for operation_key in ("subscribe", "publish"):
        msg_spec = channel[operation_key]["message"]
        assert msg_spec["contentType"] == "application/json"
        assert "payload" in msg_spec
        assert msg_spec["payload"] == {"$ref": "#/components/schemas/QueryMessage"}


def test_asyncapi_explicit_subscribe_publish_schema():
    """Test AsyncAPI schema when websocket uses subscribe_schema and publish_schema (no Body in deps).

    Covers: components/schemas built from explicit subscribe_schema/publish_schema ModelFields,
    and channel message payloads set from explicit subscribe_model/publish_model $refs.
    """
    app = FastAPI(title="Test API", version="1.0.0")
    router = APIRouter()

    class ClientMessage(BaseModel):
        """Message the client sends."""

        action: str
        payload: str = ""

    class ServerMessage(BaseModel):
        """Message the server sends."""

        event: str
        data: dict = {}

    @router.websocket(
        "/chat",
        subscribe_schema=ClientMessage,
        publish_schema=ServerMessage,
    )
    async def chat_ws(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    app.include_router(router)
    client = TestClient(app)
    with client.websocket_connect("/chat"):
        pass

    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()

    # Components should include both models (from explicit subscribe_schema/publish_schema ModelFields)
    assert "components" in schema
    assert "schemas" in schema["components"]
    assert "ClientMessage" in schema["components"]["schemas"]
    assert "ServerMessage" in schema["components"]["schemas"]
    client_schema = schema["components"]["schemas"]["ClientMessage"]
    server_schema = schema["components"]["schemas"]["ServerMessage"]
    assert client_schema.get("title") == "ClientMessage"
    assert "action" in client_schema.get("properties", {})
    assert server_schema.get("title") == "ServerMessage"
    assert "event" in server_schema.get("properties", {})

    # Channel subscribe/publish should use explicit $refs (subscribe_model / publish_model path)
    channel = schema["channels"]["/chat"]
    sub_msg = channel["subscribe"]["message"]
    pub_msg = channel["publish"]["message"]
    assert sub_msg["contentType"] == "application/json"
    assert sub_msg["payload"] == {"$ref": "#/components/schemas/ClientMessage"}
    assert pub_msg["contentType"] == "application/json"
    assert pub_msg["payload"] == {"$ref": "#/components/schemas/ServerMessage"}


def test_asyncapi_with_root_path_in_servers():
    """Test AsyncAPI schema includes root_path in servers when root_path_in_servers is True."""
    app = FastAPI(
        title="Test API",
        version="1.0.0",
        root_path_in_servers=True,
    )

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    # Use TestClient with root_path to trigger the root_path logic
    client = TestClient(app, root_path="/api/v1")
    with client.websocket_connect("/ws"):
        pass
    response = client.get("/asyncapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert "servers" in schema
    # Root path should be added to servers
    server_urls = [s["url"] for s in schema["servers"]]
    assert "/api/v1" in server_urls
