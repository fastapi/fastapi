# HTTP QUERY

Typically, when you want to read data you use `GET`. If you need to send complex data (like a large JSON object) to filter that data, you traditionally had to use `POST` because `GET` requests does not support request bodies.

However, using `POST` for read-only operations isn't semantically correct, as `POST` implies that you are creating or modifying data.

There is a newer HTTP method called **QUERY**. It is designed exactly for this: performing safe, idempotent read operations that require a request body.

## Using `QUERY`

In **FastAPI**, you can use the `QUERY` method using the `@app.query()` decorator.

It works similarly to `@app.post()`, allowing you to receive Pydantic models in the body, but it signals that the operation is a read-only query.


{* ../../docs_src/http_query/tutorial001.py hl[7] *}

### Testing it

You can test it using an HTTP client that supports the `QUERY` method.

Because it allows a body, you can send complex filters without hitting URL length limits common with `GET` query parameters.

### Technical Details

The `QUERY` method is defined in the [IETF HTTP QUERY Method Draft](https://www.ietf.org/archive/id/draft-ietf-httpbis-safe-method-w-body-02.html). It is considered:

*   **Safe**: It does not alter the state of the server (read-only).
*   **Idempotent**: Making the same request multiple times yields the same result.

