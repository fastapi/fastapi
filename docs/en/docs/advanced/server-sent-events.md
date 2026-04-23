# Server-Sent Events (SSE) { #server-sent-events-sse }

**Added in FastAPI 0.134.0**

FastAPI has built-in support for **Server-Sent Events (SSE)**, a simple yet powerful protocol for streaming updates from the server to clients over HTTP.

## What are Server-Sent Events? { #what-are-server-sent-events }

Server-Sent Events (SSE) is a lightweight protocol for one-way communication from server to client. The client establishes a persistent HTTP connection, and the server can push events to the client as they occur.

SSE is perfect for:
- **Live notifications** and updates
- **Real-time dashboards** and monitoring
- **AI/LLM token streaming** (chat responses)
- **Log streaming** and debugging interfaces
- **Stock prices**, sports scores, and other live data

/// info

Unlike WebSockets, SSE is **unidirectional** (server → client only) and uses standard HTTP, making it simpler to implement and often more compatible with proxies and load balancers.

///

## Basic Usage { #basic-usage }

To use SSE in FastAPI:

1. Import `EventSourceResponse` and optionally `ServerSentEvent` from `fastapi.sse`
2. Use `response_class=EventSourceResponse` on your *path operation*
3. `yield` events from your endpoint function

{* ../../docs_src/server_sent_events/tutorial001_py310.py hl[4,22,23,24,25] *}

## SSE Event Structure { #sse-event-structure }

Each SSE event can contain several fields:

- **`data`**: The event payload (any JSON-serializable value)
- **`event`**: Event type name (for `addEventListener` in JavaScript)
- **`id`**: Event ID (sent back as `Last-Event-ID` header on reconnection)
- **`retry`**: Reconnection time in milliseconds
- **`comment`**: Comment/keepalive line (ignored by clients)

### Using ServerSentEvent { #using-serversentevent }

For full control over the SSE format, yield `ServerSentEvent` objects:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,23,24,25,26] *}

### Automatic Formatting { #automatic-formatting }

You can also yield plain objects (dicts, Pydantic models) - they are automatically JSON-encoded and wrapped in SSE format:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[22:25] hl[23,24,25] *}

This produces SSE events like:
```
data: {"name":"Plumbus","description":"A multi-purpose household device."}

```

### Raw Data { #raw-data }

To send pre-formatted text (not JSON), use `raw_data`:

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[10,17] *}

This produces plain SSE events:
```
data: 2025-01-01 INFO  Application started

```

## Default Retry Configuration { #default-retry-configuration }

You can set a default reconnection time for all events by creating a custom `EventSourceResponse` subclass:

{* ../../docs_src/server_sent_events/tutorial006_py310.py ln[19:22] hl[20,21,22] *}

Then use it in your *path operation*:

{* ../../docs_src/server_sent_events/tutorial006_py310.py ln[30:32] hl[30] *}

Individual events can override the default:

{* ../../docs_src/server_sent_events/tutorial006_py310.py ln[39:42] hl[42] *}

## Client Disconnect Handling { #client-disconnect-handling }

FastAPI supports an optional `on_disconnect` callback that is invoked when a client disconnects. This is useful for cleanup tasks like:
- Closing database connections
- Stopping background tasks
- Logging disconnections
- Releasing resources

To use it, create a custom `EventSourceResponse` subclass with an `on_disconnect` callback:

{* ../../docs_src/server_sent_events/tutorial007_py310.py ln[10:12] hl[10,11,12] *}

{* ../../docs_src/server_sent_events/tutorial007_py310.py ln[15:18] hl[15,16,17,18] *}

Then use it in your *path operation*:

{* ../../docs_src/server_sent_events/tutorial007_py310.py ln[34:36] hl[34] *}

The callback will be invoked after the response completes or when the client disconnects.

## Keepalive Support { #keepalive-support }

FastAPI automatically sends keepalive comments (`: ping`) every 15 seconds to prevent proxy/load-balancer timeouts. This ensures that idle connections remain open even when no events are being sent.

You can also send manual keepalive pings by yielding `ServerSentEvent(comment="ping")`.

## Resuming from Last Event { #resuming-from-last-event }

SSE clients automatically send a `Last-Event-ID` header when reconnecting. You can use this to resume streaming from where the client left off:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[24,25,26,27,28,29,30,31] *}

## Streaming AI/LLM Responses { #streaming-ai-llm-responses }

SSE is ideal for streaming AI/LLM responses token-by-token:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14,15,16,17,18,19] *}

## Technical Details { #technical-details }

### Cancellation Support { #cancellation-support }

FastAPI's SSE implementation properly handles client disconnects and cancels the streaming generator to prevent resource leaks.

### Thread-Safe { #thread-safe }

SSE streaming works with both `async def` and regular `def` endpoint functions. For synchronous generators, FastAPI runs them in a thread pool to avoid blocking the event loop.

### OpenAPI Documentation { #openapi-documentation }

When using `EventSourceResponse`, FastAPI automatically documents the endpoint in OpenAPI with the correct `text/event-stream` media type and SSE event schema.

## See Also { #see-also }

- [Stream Data](stream-data.md) - General streaming for binary data
- [Stream JSON Lines](../tutorial/stream-json-lines.md) - Streaming JSON Lines responses
- [Custom Response](custom-response.md) - Other custom response types
