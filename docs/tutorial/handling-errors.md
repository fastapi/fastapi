There are many situations in where you need to notify an error to the client that is using your API.

This client could be a browser with a frontend, the code from someone else, an IoT device, etc.

You could need to tell that client that:

* He doesn't have enough privileges for that operation.
* He doesn't have access to that resource.
* The item he was trying to access doesn't exist.
* etc.

In these cases, you would normally return an **HTTP status code** in the range of **400** (from 400 to 499).

This is similar to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in the request.

The status codes in the 400 range mean that there was an error from the client.

Remember all those **"404 Not Found"** errors (and jokes)?

## Use `HTTPException`

To return HTTP responses with errors to the client you use `HTTPException`.

### Import `HTTPException`

```Python hl_lines="1"
{!./src/handling_errors/tutorial001.py!}
```

### Raise an `HTTPException` in your code

`HTTPException` is a normal Python exception with additional data relevant for APIs.

Because it's a Python exception, you don't `return` it, you `raise` it.

This also means that if you are inside a utility function that you are calling inside of your path operation function, and you raise the `HTTPException` from inside of that utility function, it won't run the rest of the code in the path operation function, it will terminate that request right away and send the HTTP error from the `HTTPException` to the client.

The benefit of raising an exception over `return`ing a value will be more evident in the section about Dependencies and Security.

In this example, when the client request an item by an ID that doesn't exist, raise an exception with a status code of `404`:

```Python hl_lines="11"
{!./src/handling_errors/tutorial001.py!}
```

### The resulting response

If the client requests `http://example.com/items/foo` (an `item_id` `"foo"`), he will receive an HTTP status code of 200, and a JSON response of:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

But if the client requests `http://example.com/items/bar` (a non-existent `item_id` `"bar"`), he will receive an HTTP status code of 404 (the "not found" error), and a JSON response of:

```JSON
{
  "detail": "Item not found"
}
```

!!! tip
    When raising an `HTTPException`, you can pass any value that can be converted to JSON as the parameter `detail`, not only `str`.

    You could pass a `dict`, a `list`, etc.

    They are handled automatically by **FastAPI** and converted to JSON.

## Add custom headers

There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.

You probably won't need to use it directly in your code.

But in case you needed it for an advanced scenario, you can add custom headers:

```Python hl_lines="14"
{!./src/handling_errors/tutorial002.py!}
```

## Install custom exception handlers

You can add custom exception handlers with <a href="https://www.starlette.io/exceptions/" target="_blank">the same exception utilities from Starlette</a>.

Let's say you have a custom exception `UnicornException` that you (or a library you use) might `raise`.

And you want to handle this exception globally with FastAPI.

You could add a custom exception handler with `@app.exception_handler()`:

```Python hl_lines="6 7 8 14 15 16 17 18 24"
{!./src/handling_errors/tutorial003.py!}
```

Here, if you request `/unicorns/yolo`, the *path operation* will `raise` a `UnicornException`.

But it will be handled by the `unicorn_exception_handler`.

So, you will receive a clean error, with an HTTP status code of `418` and a JSON content of:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

## Override the default exception handlers

**FastAPI** has some default exception handlers.

These handlers are in charge or returning the default JSON responses when you `raise` an `HTTPException` and when the request has invalid data.

You can override these exception handlers with your own.

### Override request validation exceptions

When a request contains invalid data, **FastAPI** internally raises a `RequestValidationError`.

And it also includes a default exception handler for it.

To override it, import the `RequestValidationError` and use it with `@app.exception_handler(RequestValidationError)` to decorate the exception handler.

The exception handler will receive a `Request` and the exception.

```Python hl_lines="2 14 15 16"
{!./src/handling_errors/tutorial004.py!}
```

Now, if you go to `/items/foo`, instead of getting the default JSON error with:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

you will get a text version, with:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs `ValidationError`

!!! warning
    These are technical details that you might skip if it's not important for you now.

`RequestValidationError` is a sub-class of Pydantic's <a href="https://pydantic-docs.helpmanual.io/#error-handling" target="_blank">`ValidationError`</a>.

**FastAPI** uses it so that, if you use a Pydantic model in `response_model`, and your data has an error, you will see the error in your log.

But the client/user will not see it. Instead, the client will receive an "Internal Server Error" with a HTTP status code `500`.

It should be this way because if you have a Pydantic `ValidationError` in your *response* or anywhere in your code (not in the client's *request*), it's actually a bug in your code.

And while you fix it, your clients/users shouldn't have access to internal information about the error, as that could expose a security vulnerability.

### Override the `HTTPException` error handler

The same way, you can override the `HTTPException` handler.

For example, you could want to return a plain text response instead of JSON for these errors:

```Python hl_lines="1 3 9 10 11 22"
{!./src/handling_errors/tutorial004.py!}
```

#### FastAPI's `HTTPException` vs Starlette's `HTTPException`

**FastAPI** has its own `HTTPException`.

And **FastAPI**'s `HTTPException` error class inherits from Starlette's `HTTPException` error class.

The only difference, is that **FastAPI**'s `HTTPException` allows you to add headers to be included in the response.

This is needed/used internally for OAuth 2.0 and some security utilities.

So, you can keep raising **FastAPI**'s `HTTPException` as normally in your code.

But when you register an exception handler, you should register it for Starlette's `HTTPException`.

This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises an `HTTPException`, your handler will be able to catch handle it.

In this example, to be able to have both `HTTPException`s in the same code, Starlette's exceptions is renamed to `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### Re-use **FastAPI**'s exception handlers

You could also just want to use the exception somehow, but then use the same default exception handlers from **FastAPI**.

You can import and re-use the default exception handlers from `fastapi.exception_handlers`:

```Python hl_lines="2 3 4 5 15 21"
{!./src/handling_errors/tutorial005.py!}
```

In this example, you are just `print`ing the error with a very expressive notification.

But you get the idea, you can use the exception and then just re-use the default exception handlers.
