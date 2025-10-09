# Custom Request and APIRoute class { #custom-request-and-apiroute-class }

In some cases, you may want to override the logic used by the `Request` and `APIRoute` classes.

In particular, this may be a good alternative to logic in a middleware.

For example, if you want to read or manipulate the request body before it is processed by your application.

/// danger

This is an "advanced" feature.

If you are just starting with **FastAPI** you might want to skip this section.

///

## Use cases { #use-cases }

Some use cases include:

* Converting non-JSON request bodies to JSON (e.g. <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Decompressing gzip-compressed request bodies.
* Automatically logging all request bodies.

## Handling custom request body encodings { #handling-custom-request-body-encodings }

Let's see how to make use of a custom `Request` subclass to decompress gzip requests.

And an `APIRoute` subclass to use that custom request class.

### Create a custom `GzipRequest` class { #create-a-custom-gziprequest-class }

/// tip

This is a toy example to demonstrate how it works, if you need Gzip support, you can use the provided [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank}.

///

First, we create a `GzipRequest` class, which will overwrite the `Request.body()` method to decompress the body in the presence of an appropriate header.

If there's no `gzip` in the header, it will not try to decompress the body.

That way, the same route class can handle gzip compressed or uncompressed requests.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[8:15] *}

### Create a custom `GzipRoute` class { #create-a-custom-gziproute-class }

Next, we create a custom subclass of `fastapi.routing.APIRoute` that will make use of the `GzipRequest`.

This time, it will overwrite the method `APIRoute.get_route_handler()`.

This method returns a function. And that function is what will receive a request and return a response.

Here we use it to create a `GzipRequest` from the original request.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[18:26] *}

/// note | Technical Details

A `Request` has a `request.scope` attribute, that's just a Python `dict` containing the metadata related to the request.

A `Request` also has a `request.receive`, that's a function to "receive" the body of the request.

The `scope` `dict` and `receive` function are both part of the ASGI specification.

And those two things, `scope` and `receive`, are what is needed to create a new `Request` instance.

To learn more about the `Request` check <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">Starlette's docs about Requests</a>.

///

The only thing the function returned by `GzipRequest.get_route_handler` does differently is convert the `Request` to a `GzipRequest`.

Doing this, our `GzipRequest` will take care of decompressing the data (if necessary) before passing it to our *path operations*.

After that, all of the processing logic is the same.

But because of our changes in `GzipRequest.body`, the request body will be automatically decompressed when it is loaded by **FastAPI** when needed.

## Accessing the request body in an exception handler { #accessing-the-request-body-in-an-exception-handler }

/// tip

To solve this same problem, it's probably a lot easier to use the `body` in a custom handler for `RequestValidationError` ([Handling Errors](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

But this example is still valid and it shows how to interact with the internal components.

///

We can also use this same approach to access the request body in an exception handler.

All we need to do is handle the request inside a `try`/`except` block:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[13,15] *}

If an exception occurs, the`Request` instance will still be in scope, so we can read and make use of the request body when handling the error:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[16:18] *}

## Custom `APIRoute` class in a router { #custom-apiroute-class-in-a-router }

You can also set the `route_class` parameter of an `APIRouter`:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[26] *}

In this example, the *path operations* under the `router` will use the custom `TimedRoute` class, and will have an extra `X-Response-Time` header in the response with the time it took to generate the response:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[13:20] *}

## Experimental: HTTP QUERY method { #experimental-http-query-method }

/// warning

This is an experimental feature for the non-standard HTTP QUERY method. Use with caution.

///

FastAPI and `APIRouter` expose a `.query()` decorator for the experimental HTTP QUERY method, as defined in the <a href="https://www.ietf.org/archive/id/draft-ietf-httpbis-safe-method-w-body-02.html" class="external-link" target="_blank">IETF draft for "safe method with body"</a>.

The QUERY method works at runtime and can be used like any other HTTP method decorator:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SearchQuery(BaseModel):
    text: str
    limit: int = 10

@app.query("/search")
def search_items(query: SearchQuery):
    return {"results": f"Searching for: {query.text}"}
```

### Limitations { #query-method-limitations }

* **Not shown in interactive docs**: The QUERY method will not appear in the OpenAPI schema or interactive documentation (Swagger UI, ReDoc) because the OpenAPI specification does not define "query" operations.
* **Limited client support**: Not all HTTP clients and proxies support the QUERY method.

/// tip

For maximum interoperability, prefer using **POST** for operations that require a request body. The QUERY method is only useful in specialized scenarios where you need to follow the IETF draft specification.

///
