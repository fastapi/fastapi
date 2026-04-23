# SSE Streaming Response - Specification

## Overview

Server-Sent Events (SSE) streaming response support for FastAPI, providing a `StreamingResponse` subclass with automatic event formatting, retry configuration, and client disconnect handling.

## Features

### 1. EventSourceResponse Class

A `StreamingResponse` subclass for SSE with `text/event-stream` media type.

```python
from fastapi.sse import EventSourceResponse

@app.get("/stream", response_class=EventSourceResponse)
async def stream():
    yield {"message": "hello"}
```

### 2. Automatic Event Formatting

- Plain objects, dicts, and Pydantic models are automatically JSON-serialized as `data:` fields
- `ServerSentEvent` class for full control over SSE fields

```python
from fastapi.sse import ServerSentEvent

yield ServerSentEvent(data={"status": "ok"}, event="status", id="1", retry=3000)
yield ServerSentEvent(raw_data="plain text", event="log")  # No JSON encoding
```

### 3. Retry Configuration

Set a default reconnection time for all events:

```python
@app.get("/stream", response_class=EventSourceResponse(default_retry=5000))
async def stream():
    yield {"msg": "hello"}  # Includes retry: 5000
```

Event-level retry overrides the default.

### 4. Client Disconnect Handling

Callback invoked when client disconnects or stream ends:

```python
async def cleanup():
    # Clean up resources
    pass

@app.get("/stream", response_class=EventSourceResponse(on_disconnect=cleanup))
async def stream():
    yield {"msg": "hello"}
```

### 5. Helper Utilities

#### sse_event() Function

```python
from fastapi.sse import sse_event

yield sse_event(data={"status": "ok"}, event="status", id="1")
yield sse_event(raw_data="[DONE]", event="end")
```

#### SSEStream Class

```python
from fastapi.sse import SSEStream

async with SSEStream() as sse:
    for i in range(100):
        if sse.disconnected:
            break
        yield {"count": i}
```

#### create_sse_stream() Factory

```python
from fastapi.sse import create_sse_stream

@app.get("/stream")
async def stream():
    sse, response = create_sse_stream(on_disconnect=cleanup)
```

## API Reference

### EventSourceResponse

```python
class EventSourceResponse(StreamingResponse):
    media_type = "text/event-stream"
    
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        stream_key: str | None = None,
        default_retry: int | None = None,
        on_disconnect: Callable[[], Awaitable[None] | None] | None = None,
    ) -> None
```

**Parameters:**
- `default_retry` - Default reconnection time in milliseconds
- `on_disconnect` - Async callback called on disconnect/stream end

### ServerSentEvent

```python
class ServerSentEvent(BaseModel):
    data: Any = None           # JSON-serialized payload
    raw_data: str | None = None  # Pre-formatted string
    event: str | None = None     # Event type name
    id: str | None = None        # Event ID (no null chars)
    retry: int | None = None     # Reconnection time (ms)
    comment: str | None = None   # Comment lines
```

### format_sse_event()

```python
def format_sse_event(
    *,
    data_str: str | None = None,
    event: str | None = None,
    id: str | None = None,
    retry: int | None = None,
    comment: str | None = None,
) -> bytes
```

### Helper Functions

```python
def sse_event(
    data: Any = None,
    *,
    event: str | None = None,
    id: str | None = None,
    retry: int | None = None,
    comment: str | None = None,
    raw_data: str | None = None,
) -> ServerSentEvent

def create_sse_stream(
    on_disconnect: Callable[[], Awaitable[None] | None] | None = None,
) -> tuple[SSEStream, EventSourceResponse]
```

### SSEStream Class

```python
class SSEStream:
    @property
    def disconnected(self) -> bool: ...
    def mark_disconnected(self) -> None: ...
    async def __aenter__(self) -> "SSEStream": ...
    async def __aexit__(self, ...) -> None: ...
```

## SSE Wire Format

```
event: <event-name>
data: <json-encoded-data>
id: <event-id>
retry: <milliseconds>
: <comment>

```

Each event terminated by blank line (`\n\n`).

## Technical Details

- Keep-alive `: ping` comments sent every 15 seconds when idle
- `Cache-Control: no-cache` header set automatically
- `X-Accel-Buffering: no` header for Nginx compatibility
- Works with any HTTP method (GET, POST, etc.)
- Compatible with MCP protocol (SSE over POST)

## Files

- `fastapi/sse.py` - Core implementation
- `fastapi/routing.py` - Routing layer integration
- `tests/test_sse.py` - Test coverage (28 tests)

## Testing

All 28 tests pass:
- Basic SSE streaming with models, dicts, and no annotations
- SSE events with all fields
- Raw data without JSON encoding
- Default retry configuration
- Event-level retry override
- Disconnect callback invocation
- Helper utilities (sse_event, SSEStream, create_sse_stream)
