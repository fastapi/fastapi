# Server-Sent Events (SSE) { #server-sent-events-sse }

You can stream data to the client using **Server-Sent Events** (SSE).

This is similar to [Stream JSON Lines](stream-json-lines.md){.internal-link target=_blank}, but uses the `text/event-stream` format, which is supported natively by browsers with the <a href="https://developer.mozilla.org/en-US/docs/Web/API/EventSource" class="external-link" target="_blank">`EventSource` API</a>.

## What are Server-Sent Events? { #what-are-server-sent-events }

SSE is a standard for streaming data from the server to the client over HTTP.

Each event is a small text block with "fields" like `data`, `event`, `id`, and `retry`, separated by blank lines.

It looks like this:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE is commonly used for AI chat streaming, live notifications, logs and observability, and other cases where the server pushes updates to the client.

/// tip

If you want to stream binary data, for example video or audio, check the advanced guide: [Stream Data](../advanced/stream-data.md){.internal-link target=_blank}.

///

## Stream SSE with FastAPI { #stream-sse-with-fastapi }

To stream SSE with FastAPI, use `yield` in your *path operation function* and set `response_class=EventSourceResponse`.

Import `EventSourceResponse` from `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Each yielded item is encoded as JSON and sent in the `data:` field of an SSE event.

If you declare the return type as `AsyncIterable[Item]`, FastAPI will use it to **validate**, **document**, and **serialize** the data using Pydantic.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip

As Pydantic will serialize it in the **Rust** side, you will get much higher **performance** than if you don't declare a return type.

///

### Non-async *path operation functions* { #non-async-path-operation-functions }

You can also use regular `def` functions (without `async`), and use `yield` the same way.

FastAPI will make sure it's run correctly so that it doesn't block the event loop.

As in this case the function is not async, the right return type would be `Iterable[Item]`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### No Return Type { #no-return-type }

You can also omit the return type. FastAPI will use the [`jsonable_encoder`](./encoder.md){.internal-link target=_blank} to convert the data and send it.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

If you need to set SSE fields like `event`, `id`, `retry`, or `comment`, you can yield `ServerSentEvent` objects instead of plain data.

Import `ServerSentEvent` from `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

The `data` field is always encoded as JSON. You can pass any value that can be serialized as JSON, including Pydantic models.

## Raw Data { #raw-data }

If you need to send data **without** JSON encoding, use `raw_data` instead of `data`.

This is useful for sending pre-formatted text, log lines, or special <dfn title="A value used to indicate a special condition or state">"sentinel"</dfn> values like `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note

`data` and `raw_data` are mutually exclusive. You can only set one of them on each `ServerSentEvent`.

///

## Resuming with `Last-Event-ID` { #resuming-with-last-event-id }

When a browser reconnects after a connection drop, it sends the last received `id` in the `Last-Event-ID` header.

You can read it as a header parameter and use it to resume the stream from where the client left off:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE with POST { #sse-with-post }

SSE works with **any HTTP method**, not just `GET`.

This is useful for protocols like <a href="https://modelcontextprotocol.io" class="external-link" target="_blank">MCP</a> that stream SSE over `POST`:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Technical Details { #technical-details }

FastAPI implements some SSE best practices out of the box.

* Send a **"keep alive" comment** every 15 seconds when there hasn't been any message, to prevent some proxies from closing the connection, as suggested in the <a href="https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes" class="external-link" target="_blank">HTML specification: Server-Sent Events</a>.
* Set the `Cache-Control: no-cache` header to **prevent caching** of the stream.
* Set a special header `X-Accel-Buffering: no` to **prevent buffering** in some proxies like Nginx.

You don't have to do anything about it, it works out of the box. 🤓
