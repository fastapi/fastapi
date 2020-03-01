You can mount WSGI applications as you saw with [Sub Applications - Behind a Proxy, Mounts](./sub-applications-proxy.md){.internal-link target=_blank}.

For that, you can use the `WSGIMiddleware` and use it to wrap your WSGI application, for example, Flask, Django, etc.

## Using `WSGIMiddleware`

You need to import `WSGIMiddleware`.

Then wrap the WSGI (e.g. Flask) app with the middleware.

And then mount that under a path.

```Python hl_lines="1  3  22"
{!./src/wsgi/tutorial001.py!}
```

## Check it

Now, every request under the path `/v1/` will be handled by the Flask application.

And the rest will be handled by **FastAPI**.

If you run it with Uvicorn and go to <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> you will see the response from Flask:

```txt
Hello, World from Flask!
```

And if you go to <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> you will see the response from FastAPI:

```JSON
{
    "message": "Hello World"
}
```
