# Custom Response Classes - File, HTML, Redirect, Streaming, etc.

There are several custom response classes you can use to create an instance and return them directly from your *path operations*.

Read more about it in the [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).

You can import them directly from `fastapi.responses`:

```python
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)
```

## FastAPI Responses

There were a couple of custom FastAPI response classes that were intended to optimize JSON performance.

However, they are now deprecated as you will now get better performance by using a [Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/).

That way, Pydantic will serialize the data into JSON bytes on the Rust side, which will achieve better performance than these custom JSON responses.

Read more about it in [Custom Response - HTML, Stream, File, others - `orjson` or Response Model](https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model).

::: fastapi.responses.UJSONResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.ORJSONResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

## Starlette Responses

You can read more about all of them in the [FastAPI docs for Custom Response](https://fastapi.tiangolo.com/advanced/custom-response/) and in the [Starlette docs about Responses](https://starlette.dev/responses/).

::: fastapi.responses.FileResponse
    options:
        members:
            - chunk_size
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.HTMLResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.JSONResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.PlainTextResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.RedirectResponse
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.Response
    options:
        members:
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie

::: fastapi.responses.StreamingResponse
    options:
        members:
            - body_iterator
            - charset
            - status_code
            - media_type
            - body
            - background
            - raw_headers
            - render
            - init_headers
            - headers
            - set_cookie
            - delete_cookie
