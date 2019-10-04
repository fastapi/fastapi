Up to now, you have been declaring the parts of the request that you need with their types.

Taking data from:

* The path as parameters.
* Headers.
* Cookies.
* etc.

And by doing so, **FastAPI** is validating that data, converting it and generating documentation for your API automatically.

But there are situations where you might need to access the `Request` object directly.

## Details about the `Request` object

As **FastAPI** is actually **Starlette** underneath, with a layer of several tools on top, you can use Starlette's <a href="https://www.starlette.io/requests/" target="_blank">`Request`</a> object directly when you need to.

It would also mean that if you get data from the `Request` object directly (for example, read the body) it won't be validated, converted or annotated (with OpenAPI, for the automatic documentation) by FastAPI.

Although any other parameter declared normally (for example, the body with a Pydantic model) would still be validated, converted, annotated, etc.

But there are specific cases where it's useful to get the `Request` object.

## Use the `Request` object directly

Let's imagine you want to get the client's IP address/host inside of your *path operation function*.

For that you need to access the request directly.

### Import the `Request`

First, import the `Request` class from Starlette:

```Python hl_lines="2"
{!./src/using_request_directly/tutorial001.py!}
```

### Declare the `Request` parameter

Then declare a *path operation function* parameter with the type being the `Request` class:

```Python hl_lines="8"
{!./src/using_request_directly/tutorial001.py!}
```

!!! tip
    Note that in this case, we are declaring a path parameter besides the request parameter.

    So, the path parameter will be extracted, validated, converted to the specified type and annotated with OpenAPI.

    The same way, you can declare any other parameter as normally, and additionally, get the `Request` too.

## `Request` documentation

You can read more details about the <a href="https://www.starlette.io/requests/" target="_blank">`Request` object in the official Starlette documentation site</a>.

## Using a custom `Request` class

!!! danger
    This is an "advanced" feature.
    
    If you are just starting with **FastAPI** you might want to skip this section.

In some cases, it may be desirable to override the logic used by the `Request` class.

In particular, this may be a good alternative to middleware if you want to read or manipulate the request body before it is processed by your application.

Some use cases include:

* converting non-JSON request bodies to JSON (e.g., `msgpack`)
* decompressing gzip-compressed request bodies
* automatically logging all request bodies
* accessing the request body in an exception handler

### Handling custom request body encodings
Let's see how to make use of a custom `Request` subclass to decompress gzip requests.

First, we create a `GzipRequest` class, which will override `Request.body` to decompress the body in the presence of an appropriate header: 

```Python hl_lines="10"
{!./src/using_request_directly/tutorial002.py!}
```

Next, we create a custom subclass of `fastapi.routing.APIRoute` that will make use of the `GzipRequest`:

```Python hl_lines="20"
{!./src/using_request_directly/tutorial002.py!}
```

!!! info
    The `get_app` method uses all of the information stored on the `APIRoute` to *build* a callable that accepts a `Request`, and returns a `Response`.

    The name doesn't refer to your *whole app*, it just reflects the additional pre- and post-processing logic beyond the endpoint call.

The only thing the result of `GzipRequest.get_app` does differently is start by converting the `Request` to a `GzipRequest`.

After that, all of the processing logic is the same.

But because of our changes in `GzipRequest.body`, the request body can will be automatically decompressed when it is loaded by **FastAPI**.     

## Accessing the request body in an exception handler  

We can also use this same approach to access the request body in an exception handler. 

All we need to do is handle the request inside a `try`/`except` block:

```Python hl_lines="15"
{!./src/using_request_directly/tutorial003.py!}
```

If an exception occurs, the`Request` instance will still be in scope, so we can read and make use of the request body when handling the error: 

```Python hl_lines="18"
{!./src/using_request_directly/tutorial003.py!}
```
