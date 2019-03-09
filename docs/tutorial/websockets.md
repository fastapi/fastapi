
You can use <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" target="_blank">WebSockets</a> with **FastAPI**.

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

```Python hl_lines="2 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 42 43 44"
{!./src/websockets/tutorial001.py!}
```

## Create a `websocket_route`

In your **FastAPI** application, create a `websocket_route`:

```Python hl_lines="3 47 48"
{!./src/websockets/tutorial001.py!}
```

!!! tip
    In this example we are importing `WebSocket` from `starlette.websockets` to use it in the type declaration in the WebSocket route function.

    That is not required, but it's recommended as it will provide you completion and checks inside the function.


!!! info
    This `websocket_route` we are using comes directly from <a href="https://www.starlette.io/applications/" target="_blank">Starlette</a>. 
    
    That's why the naming convention is not the same as with other API path operations (`get`, `post`, etc).


## Await for messages and send messages

In your WebSocket route you can `await` for messages and send messages.

```Python hl_lines="49 50 51 52 53"
{!./src/websockets/tutorial001.py!}
```

You can receive and send binary, text, and JSON data.

To learn more about the options, check Starlette's documentation for:

* <a href="https://www.starlette.io/applications/" target="_blank">Applications (`websocket_route`)</a>.
* <a href="https://www.starlette.io/websockets/" target="_blank">The `WebSocket` class</a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" target="_blank">Class-based WebSocket handling</a>.


## Test it

If your file is named `main.py`, run your application with:

```bash
uvicorn main:app --reload
```

Open your browser at <a href="http://127.0.0.1:8000" target="_blank">http://127.0.0.1:8000</a>.

You will see a simple page like:

<img src="/img/tutorial/websockets/image01.png">

You can type messages in the input box, and send them:

<img src="/img/tutorial/websockets/image02.png">

And your **FastAPI** application with WebSockets will respond back:

<img src="/img/tutorial/websockets/image03.png">

You can send (and receive) many messages:

<img src="/img/tutorial/websockets/image04.png">

And all of them will use the same WebSocket connection.
