# WebSockets

You can use <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> with **FastAPI**.

## WebSockets client

### In production

In your production system, you probably have a frontend created with a modern framework like React, Vue.js or Angular.

And to communicate using WebSockets with your backend you would probably use your frontend's utilities.

Or you might have a native mobile application that communicates with your WebSocket backend directly, in native code.

Or you might have any other way to communicate with the WebSocket endpoint.

---

But for this example, we'll use a very simple HTML document with some JavaScript, all inside a long string.

This, of course, is not optimal and you wouldn't use it for production.

In production you would have one of the options above.

But it's the simplest way to focus on the server-side of WebSockets and have a working example:

```Python hl_lines="2  6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38  41 42 43"
{!../../../docs_src/websockets/tutorial001.py!}
```

## Create a `websocket`

In your **FastAPI** application, create a `websocket`:

```Python hl_lines="1 46 47"
{!../../../docs_src/websockets/tutorial001.py!}
```

!!! note "Technical Details"
    You could also use `from starlette.websockets import WebSocket`.

    **FastAPI** provides the same `WebSocket` directly just as a convenience for you, the developer. But it comes directly from Starlette.

## Await for messages and send messages

In your WebSocket route you can `await` for messages and send messages.

```Python hl_lines="48 49 50 51 52"
{!../../../docs_src/websockets/tutorial001.py!}
```

You can receive and send binary, text, and JSON data.

## Try it

If your file is named `main.py`, run your application with:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Open your browser at <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

You will see a simple page like:

<img src="/img/tutorial/websockets/image01.png">

You can type messages in the input box, and send them:

<img src="/img/tutorial/websockets/image02.png">

And your **FastAPI** application with WebSockets will respond back:

<img src="/img/tutorial/websockets/image03.png">

You can send (and receive) many messages:

<img src="/img/tutorial/websockets/image04.png">

And all of them will use the same WebSocket connection.

## Using `Depends` and others

In WebSocket endpoints you can import from `fastapi` and use:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

They work the same way as for other FastAPI endpoints/*path operations*:

```Python hl_lines="58 59 60 61 62 63 64 65  68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83"
{!../../../docs_src/websockets/tutorial002.py!}
```

!!! info
    In a WebSocket it doesn't really make sense to raise an `HTTPException`. So it's better to close the WebSocket connection directly.

    You can use a closing code from the <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">valid codes defined in the specification</a>.

    In the future, there will be a `WebSocketException` that you will be able to `raise` from anywhere, and add exception handlers for it. It depends on the <a href="https://github.com/encode/starlette/pull/527" class="external-link" target="_blank">PR #527</a> in Starlette.

### Try the WebSockets with dependencies

If your file is named `main.py`, run your application with:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Open your browser at <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

There you can set:

* The "Item ID", used in the path.
* The "Token" used as a query parameter.

!!! tip
    Notice that the query `token` will be handled by a dependency.

With that you can connect the WebSocket and then send and receive messages:

<img src="/img/tutorial/websockets/image05.png">

## More info

To learn more about the options, check Starlette's documentation for:

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank">The `WebSocket` class</a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">Class-based WebSocket handling</a>.
