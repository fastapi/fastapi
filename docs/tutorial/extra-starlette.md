It's possible to use **Starlette** objects in **FastAPI**

For instance, should you need to access the <a href="https://github.com/encode/starlette/blob/37782e7a553986d0c4111dc423d52fb4f872c437/starlette/requests.py#L118">Request</a> object within a given route
it's as simple as writing:

```Python hl_lines="27"
{!./src/extra_starlette/tutorial001.py!}
```

This way you can in this example access the <a href="https://github.com/encode/starlette/blob/3270762c161dc9708a4685b0c3090ff25f870245/starlette/middleware/database.py"> DatabaseMiddleware <a/> object that 
Starlette put in `request.database`