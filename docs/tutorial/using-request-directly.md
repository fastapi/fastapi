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
