# Exceptions - `HTTPException` and `WebSocketException`

These are the exceptions that you can raise to show errors to the client.

When you raise an exception, as would happen with normal Python, the rest of the execution is aborted. This way you can raise these exceptions from anywhere in the code to abort a request and show the error to the client.

You can use:

* `HTTPException`
* `WebSocketException`

These exceptions can be imported directly from `fastapi`:

```python
from fastapi import HTTPException, WebSocketException
```

::: fastapi.HTTPException

::: fastapi.WebSocketException
