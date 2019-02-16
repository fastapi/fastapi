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

### Adding custom headers

There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.

You probably won't need to use it directly in your code.

But in case you needed it for an advanced scenario, you can add custom headers:


```Python hl_lines="14"
{!./src/handling_errors/tutorial002.py!}
```
