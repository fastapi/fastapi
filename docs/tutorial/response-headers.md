## Use a `Response` parameter

You can declare a parameter of type `Response` in your *path operation function* (as you can do for cookies), the same way you can declare a `Request` parameter.

And then you can set headers in that *temporal* response object.

```Python hl_lines="2 8 9"
{!./src/response_headers/tutorial002.py!}
```

And then you can return any object you need, as you normally would (a `dict`, a database model, etc).

And if you declared a `response_model`, it will still be used to filter and convert the object you returned.

**FastAPI** will use that *temporal* response to extract the headers (also cookies and status code), and will put them in the final response that contains the value you returned, filtered by any `response_model`.

You can also declare the `Response` parameter in dependencies, and set headers (and cookies) in them.

## Return a `Response` directly

You can also add headers when you return a `Response` directly.

Create a response as described in <a href="https://fastapi.tiangolo.com/tutorial/response-directly/" target="_blank">Return a Response directly</a> and pass the headers as an additional parameter:

```Python hl_lines="10 11 12"
{!./src/response_headers/tutorial001.py!}
```

## Custom Headers

Have in mind that custom proprietary headers can be added <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">using the 'X-' prefix</a>.

But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your <a href="https://fastapi.tiangolo.com/tutorial/cors/" target="_blank">CORS configurations</a>, using the parameter `expose_headers` documented in <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>.
