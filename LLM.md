# FastAPI Library API Documentation

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Installation
```bash
pip install fastapi
pip install "uvicorn[standard]"  # ASGI server
```

## Core Application

### FastAPI Class
```python
from fastapi import FastAPI

class FastAPI(Starlette):
    """FastAPI app class, the main entrypoint to use FastAPI."""
```

### Constructor Parameters
```python
app = FastAPI(
    debug: bool = False,
    routes: Optional[List[BaseRoute]] = None,
    title: str = "FastAPI",
    summary: Optional[str] = None,
    description: str = "",
    version: str = "0.1.0",
    openapi_url: Optional[str] = "/openapi.json",
    openapi_tags: Optional[List[Dict[str, Any]]] = None,
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
    dependencies: Optional[Sequence[Depends]] = None,
    default_response_class: Type[Response] = JSONResponse,
    redirect_slashes: bool = True,
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
    swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
    swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
    middleware: Optional[Sequence[Middleware]] = None,
    exception_handlers: Optional[Dict[Union[int, Type[Exception]], Callable]] = None,
    on_startup: Optional[Sequence[Callable]] = None,
    on_shutdown: Optional[Sequence[Callable]] = None,
    lifespan: Optional[Lifespan] = None,
    terms_of_service: Optional[str] = None,
    contact: Optional[Dict[str, Union[str, Any]]] = None,
    license_info: Optional[Dict[str, Union[str, Any]]] = None,
    openapi_prefix: str = "",
    root_path: str = "",
    root_path_in_servers: bool = True,
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    webhooks: Optional[APIRouter] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    swagger_ui_parameters: Optional[Dict[str, Any]] = None,
    generate_unique_id_function: Callable[[APIRoute], str] = generate_unique_id,
    separate_input_output_schemas: bool = True,
)
```

### HTTP Method Decorators
```python
@app.get(path: str, **kwargs)
@app.post(path: str, **kwargs)
@app.put(path: str, **kwargs)
@app.delete(path: str, **kwargs)
@app.patch(path: str, **kwargs)
@app.options(path: str, **kwargs)
@app.head(path: str, **kwargs)
@app.trace(path: str, **kwargs)
```

### Core Methods
```python
app.api_route(path: str, methods: List[str], **kwargs)
app.add_api_route(path: str, endpoint: Callable, **kwargs)
app.websocket(path: str, **kwargs)
app.include_router(router: APIRouter, prefix: str = "", **kwargs)
app.openapi() -> Dict[str, Any]
```


## Routing and Path Operations

### APIRouter
```python
from fastapi import APIRouter

router = APIRouter(
    prefix: str = "",
    tags: Optional[List[Union[str, Enum]]] = None,
    dependencies: Optional[Sequence[Depends]] = None,
    default_response_class: Type[Response] = JSONResponse,
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    routes: Optional[List[routing.BaseRoute]] = None,
    redirect_slashes: bool = True,
    default: Optional[ASGIApp] = None,
    dependency_overrides_provider: Optional[Any] = None,
    route_class: Type[APIRoute] = APIRoute,
    on_startup: Optional[Sequence[Callable[[], Any]]] = None,
    on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
    lifespan: Optional[Lifespan[Any]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    generate_unique_id_function: Callable[[APIRoute], str] = generate_unique_id,
)
```

### Router Methods
```python
# HTTP method decorators (same as FastAPI app)
@router.get(path: str, **kwargs)
@router.post(path: str, **kwargs)
@router.put(path: str, **kwargs)
@router.delete(path: str, **kwargs)
@router.patch(path: str, **kwargs)
@router.options(path: str, **kwargs)
@router.head(path: str, **kwargs)
@router.trace(path: str, **kwargs)

# Core methods
router.api_route(path: str, methods: List[str], **kwargs)
router.add_api_route(path: str, endpoint: Callable, **kwargs)
router.websocket(path: str, **kwargs)
router.include_router(router: APIRouter, **kwargs)
```

## Parameter Functions

### Path Parameters
```python
from fastapi import Path

def Path(
    default: Any = ...,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    **extra: Any,
) -> Any
```

### Query Parameters
```python
from fastapi import Query

def Query(
    default: Any = Undefined,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    **extra: Any,
) -> Any
```

### Request Body
```python
from fastapi import Body

def Body(
    default: Any = Undefined,
    *,
    embed: bool = False,
    media_type: str = "application/json",
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    **extra: Any,
) -> Any
```

### Headers and Cookies
```python
from fastapi import Header, Cookie

def Header(
    default: Any = Undefined,
    *,
    alias: Optional[str] = None,
    convert_underscores: bool = True,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    **extra: Any,
) -> Any

def Cookie(
    default: Any = Undefined,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    **extra: Any,
) -> Any
```

### Form Data and File Uploads
```python
from fastapi import Form, File, UploadFile

def Form(
    default: Any = Undefined,
    *,
    media_type: str = "application/x-www-form-urlencoded",
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    **extra: Any,
) -> Any

def File(
    default: Any = Undefined,
    *,
    media_type: str = "multipart/form-data",
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    example: Any = Undefined,
    examples: Optional[Dict[str, Any]] = None,
    **extra: Any,
) -> Any
```


## Dependency Injection

### Depends Function
```python
from fastapi import Depends

def Depends(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    use_cache: bool = True,
) -> Any
```

### Security Function
```python
from fastapi import Security

def Security(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    scopes: Optional[Sequence[str]] = None,
    use_cache: bool = True,
) -> Any
```

## Security and Authentication

### API Key Authentication
```python
from fastapi.security import APIKeyQuery, APIKeyHeader, APIKeyCookie

# API key in query parameters
api_key_query = APIKeyQuery(name="api_key", auto_error=True)

# API key in headers
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# API key in cookies
api_key_cookie = APIKeyCookie(name="api_key", auto_error=True)
```

### HTTP Authentication
```python
from fastapi.security import HTTPBasic, HTTPBearer, HTTPDigest
from fastapi.security.http import HTTPBasicCredentials, HTTPAuthorizationCredentials

# HTTP Basic authentication
basic_auth = HTTPBasic(auto_error=True)

# HTTP Bearer token
bearer_auth = HTTPBearer(auto_error=True)

# HTTP Digest authentication
digest_auth = HTTPDigest(auto_error=True)
```

### OAuth2 Authentication
```python
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, SecurityScopes

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"read": "Read access", "write": "Write access"},
    auto_error=True
)

# OAuth2 authorization code
oauth2_code = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://example.com/auth",
    tokenUrl="https://example.com/token",
    auto_error=True
)
```

### OpenID Connect
```python
from fastapi.security.open_id_connect_url import OpenIdConnect

openid_connect = OpenIdConnect(
    openIdConnectUrl="https://example.com/.well-known/openid_configuration",
    auto_error=True
)
```

## Response Types

### Standard Responses
```python
from fastapi.responses import (
    Response, JSONResponse, HTMLResponse, PlainTextResponse,
    RedirectResponse, StreamingResponse, FileResponse
)

# JSON response (default)
return JSONResponse(content={"message": "Hello World"})

# HTML response
return HTMLResponse(content="<html><body><h1>Hello World</h1></body></html>")

# Plain text response
return PlainTextResponse(content="Hello World")

# Redirect response
return RedirectResponse(url="https://example.com")

# File response
return FileResponse(path="/path/to/file.pdf", filename="download.pdf")

# Streaming response
def generate():
    for i in range(1000):
        yield f"data chunk {i}\n"

return StreamingResponse(generate(), media_type="text/plain")
```

### High-Performance JSON Responses
```python
from fastapi.responses import UJSONResponse, ORJSONResponse

# Ultra-fast JSON with ujson
return UJSONResponse(content={"message": "Fast JSON"})

# Ultra-fast JSON with orjson
return ORJSONResponse(content={"message": "Faster JSON"})
```

## Exception Handling

### HTTP Exceptions
```python
from fastapi import HTTPException
from fastapi.exceptions import (
    RequestValidationError, WebSocketRequestValidationError,
    ResponseValidationError, FastAPIError
)

# Raise HTTP exception
raise HTTPException(
    status_code=404,
    detail="Item not found",
    headers={"X-Error": "There goes my error"}
)

# Custom exception handler
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    validation_exception_handler
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)
```

### WebSocket Exceptions
```python
from fastapi import WebSocketException

# Raise WebSocket exception
raise WebSocketException(code=1008, reason="Invalid data")
```


## WebSocket Support

### WebSocket Endpoint
```python
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### WebSocket Methods
```python
# Connection management
await websocket.accept(subprotocol=None)
await websocket.close(code=1000)

# Receiving data
data = await websocket.receive()  # Any message
text = await websocket.receive_text()  # Text message
bytes_data = await websocket.receive_bytes()  # Binary message
json_data = await websocket.receive_json()  # JSON message

# Sending data
await websocket.send(message)
await websocket.send_text(data)
await websocket.send_bytes(data)
await websocket.send_json(data)

# Iterating over messages
async for message in websocket.iter_text():
    print(message)

async for message in websocket.iter_bytes():
    print(message)

async for message in websocket.iter_json():
    print(message)
```

### WebSocket States
```python
from fastapi.websockets import WebSocketState

# WebSocketState.CONNECTING
# WebSocketState.CONNECTED
# WebSocketState.DISCONNECTED

if websocket.client_state == WebSocketState.CONNECTED:
    await websocket.send_text("Hello")
```

## Background Tasks

### Background Task Execution
```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent in the background"}
```

## Testing

### TestClient
```python
from fastapi.testclient import TestClient

client = TestClient(app)

# HTTP requests
response = client.get("/")
response = client.post("/items/", json={"name": "Foo"})
response = client.put("/items/1", json={"name": "Bar"})
response = client.delete("/items/1")

# WebSocket testing
with client.websocket_connect("/ws") as websocket:
    websocket.send_text("Hello")
    data = websocket.receive_text()
    assert data == "Message: Hello"

# File uploads
with open("test.txt", "rb") as f:
    response = client.post("/upload/", files={"file": f})

# Form data
response = client.post("/form/", data={"username": "testuser"})
```

## Middleware

### CORS Middleware
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Other Middleware
```python
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# HTTPS redirect
app.add_middleware(HTTPSRedirectMiddleware)

# Trusted host validation
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

## Utilities

### JSON Encoder
```python
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    timestamp: datetime

item = Item(name="Foo", timestamp=datetime.now())
json_data = jsonable_encoder(item)
```

### Static Files
```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Status Codes

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item():
    return {"message": "Item created"}

# Common status codes
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_204_NO_CONTENT
status.HTTP_400_BAD_REQUEST
status.HTTP_401_UNAUTHORIZED
status.HTTP_403_FORBIDDEN
status.HTTP_404_NOT_FOUND
status.HTTP_422_UNPROCESSABLE_ENTITY
status.HTTP_500_INTERNAL_SERVER_ERROR
```


## Complete Usage Examples

### Basic FastAPI Application
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My API", version="1.0.0")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

items_db = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "q": q, "item": items_db[item_id]}

@app.post("/items/")
def create_item(item: Item):
    items_db.append(item)
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db.pop(item_id)
```

### Advanced Application with Authentication
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user (simplified)
    if form_data.username == "testuser" and form_data.password == "testpass":
        access_token_expires = timedelta(minutes=30)
        access_token = jwt.encode(
            {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires},
            "secret",
            algorithm="HS256"
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: str = Depends(verify_token)):
    return User(username=current_user, email="test@example.com")

@app.get("/protected")
async def protected_route(current_user: str = Depends(verify_token)):
    return {"message": f"Hello {current_user}, this is a protected route"}
```

### File Upload Example
```python
from fastapi import FastAPI, File, UploadFile, Form
from typing import List
import shutil

app = FastAPI()

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "content_type": file.content_type}

@app.post("/upload-files/")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        with open(f"uploads/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        filenames.append(file.filename)
    return {"filenames": filenames}

@app.post("/upload-with-form/")
async def upload_with_form(
    file: UploadFile = File(...),
    description: str = Form(...)
):
    return {
        "filename": file.filename,
        "description": description,
        "content_type": file.content_type
    }
```

### WebSocket Chat Example
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
```

## Running the Application

### Development Server
```bash
# Install uvicorn
pip install "uvicorn[standard]"

# Run the application
uvicorn main:app --reload

# Run with custom host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Deployment
```bash
# With Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# With Docker
# Dockerfile
FROM python:3.9
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

## Key Import Statements Summary

```python
# Core FastAPI
from fastapi import (
    FastAPI, APIRouter, Request, Response,
    HTTPException, WebSocketException,
    Depends, Security, BackgroundTasks,
    status
)

# Parameter functions
from fastapi import (
    Path, Query, Body, Header, Cookie,
    Form, File, UploadFile
)

# WebSocket support
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

# Security
from fastapi.security import (
    HTTPBasic, HTTPBearer, HTTPDigest,
    OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer,
    OAuth2PasswordRequestForm, SecurityScopes,
    APIKeyQuery, APIKeyHeader, APIKeyCookie
)

# Responses
from fastapi.responses import (
    JSONResponse, HTMLResponse, PlainTextResponse,
    RedirectResponse, StreamingResponse, FileResponse,
    UJSONResponse, ORJSONResponse
)

# Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Testing
from fastapi.testclient import TestClient

# Utilities
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
```

This documentation covers the complete FastAPI API for building modern, fast web APIs with Python. FastAPI provides automatic API documentation, request/response validation, dependency injection, security, and high performance through async support.
