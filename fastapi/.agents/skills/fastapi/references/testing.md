# Testing

## Use `TestClient`

Use `TestClient` to test *path operations*. Write the tests as regular `def` functions and call the client without `await`, so `pytest` runs them directly.

`TestClient` needs an HTTP client library, included in `fastapi[standard]`.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict:
    return {"item_id": item_id}


client = TestClient(app)


def test_read_item():
    response = client.get("/items/plumbus")
    assert response.status_code == 200
    assert response.json() == {"item_id": "plumbus"}
```

## Create the client in a `with` block to run the `lifespan`

When the app has a `lifespan`, create the `TestClient` in a `with` block, it is what runs the startup and shutdown code.

Skipping it fails silently: the requests still return `200`, but they run against the state the `lifespan` never populated, so the mistake surfaces as a wrong response body instead of an error.

```python
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

catalog: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    catalog["plumbus"] = {"name": "Plumbus"}
    yield
    catalog.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict:
    return catalog[item_id]


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_read_item(client: TestClient):
    response = client.get("/items/plumbus")
    assert response.status_code == 200
    assert response.json() == {"name": "Plumbus"}
```

## Override dependencies instead of patching

Use `app.dependency_overrides` to replace a dependency that would reach an external service, keyed by the original dependency function.

Override the innermost dependency that isolates what should not run. Overriding an outer dependency also discards the parameters it declares, so the validation of those parameters is no longer covered.

Reset the overrides in a fixture. `app.dependency_overrides` is one dict shared by the app, so an entry left behind applies to every later test.

```python
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


class BillingClient:
    def get_username(self, token: str) -> str:
        raise RuntimeError("Real network call")


def get_billing_client() -> BillingClient:
    return BillingClient()


def get_current_username(
    token: str, billing: Annotated[BillingClient, Depends(get_billing_client)]
) -> str:
    return billing.get_username(token)


@app.get("/users/me")
async def read_current_user(
    username: Annotated[str, Depends(get_current_username)],
) -> dict:
    return {"username": username}


class FakeBillingClient:
    def get_username(self, token: str) -> str:
        return "rick"


@pytest.fixture
def client():
    app.dependency_overrides[get_billing_client] = FakeBillingClient
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_read_current_user(client: TestClient):
    response = client.get("/users/me", params={"token": "secret"})
    assert response.status_code == 200
    assert response.json() == {"username": "rick"}


def test_token_is_required(client: TestClient):
    # Still covered because `get_current_username` itself was not overridden.
    response = client.get("/users/me")
    assert response.status_code == 422
```

## Test WebSockets with `TestClient`

Connect with `websocket_connect()` in a `with` block.

```python
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        assert websocket.receive_json() == {"msg": "Hello WebSocket"}
```

## Async tests

Keep using `TestClient` inside `async def` tests. It runs the app in its own event loop on a separate thread, so requests, WebSockets, and the `lifespan` keep working, and the test can `await` its own code.

Declare the `anyio_backend` fixture to pin the backend, otherwise each test runs once per AnyIO backend installed.

```python
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict:
    return {"item_id": item_id}


async def get_stored_item_id() -> str:
    # Stands in for an async database call.
    return "plumbus"


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_read_item():
    with TestClient(app) as client:
        response = client.get("/items/plumbus")
    assert response.status_code == 200
    # Await the rest of the async code as usual.
    assert response.json() == {"item_id": await get_stored_item_id()}
```

Use `httpx.AsyncClient` only when the *path operation* has to run in the same event loop as the test, for example when the test opens an async database transaction that the endpoint must see. Pass the app through `ASGITransport`, the `app` argument was removed in HTTPX v0.28.

`ASGITransport` does not run the `lifespan` and cannot connect to WebSockets. Test those with `TestClient`.

```python
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict:
    return {"item_id": item_id}


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_read_item():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/items/plumbus")
    assert response.status_code == 200
    assert response.json() == {"item_id": "plumbus"}
```
