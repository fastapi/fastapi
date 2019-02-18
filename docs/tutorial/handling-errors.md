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

### Adding custom headers

There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.

You probably won't need to use it directly in your code.

But in case you needed it for an advanced scenario, you can add custom headers:


```Python hl_lines="14"
{!./src/handling_errors/tutorial002.py!}
```

### Installing custom handlers

If you need to add other custom exception handlers, or override the default one (that sends the errors as JSON), you can use <a href="https://www.starlette.io/exceptions/" target="_blank">the same exception utilities from Starlette</a>.

For example, you could override the default exception handler with:

```Python hl_lines="2 3 8 9 10"
{!./src/handling_errors/tutorial003.py!}
```

...this would make it return "plain text" responses with the errors, instead of JSON responses.

!!! info
    Note that in this example we set the exception handler with Starlette's `HTTPException` instead of FastAPI's `HTTPException`.

    This would ensure that if you use a plug-in or any other third-party tool that raises Starlette's `HTTPException` directly, it will be catched by your exception handler.
