You can add headers to your response.

Create a response as described in <a href="https://fastapi.tiangolo.com/tutorial/response-directly/" target="_blank">Return a Response directly</a> and pass the headers as an additional parameter:

```Python hl_lines="10 11 12"
{!./src/response_headers/tutorial001.py!}
```

!!! tip
    Have in mind that custom proprietary headers can be added <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" target="_blank">using the 'X-' prefix</a>.

    But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your <a href="https://fastapi.tiangolo.com/tutorial/cors/" target="_blank">CORS configurations</a>, using the parameter `expose_headers` documented in <a href="https://www.starlette.io/middleware/#corsmiddleware" target="_blank">Starlette's CORS docs</a>.
