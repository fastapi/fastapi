There are at least two situations where you could need to create your **FastAPI** application using some specific paths.

But then you need to set them up to be served with a path prefix.

It could happen if you have a:

* **Proxy** server.
* You are "**mounting**" a FastAPI application inside another FastAPI application (or inside another ASGI application, like Starlette).

## Proxy

Having a proxy in this case means that you could declare a path at `/app`, but then, you could need to add a layer on top (the Proxy) that would put your **FastAPI** application under a path like `/api/v1`.

In this case, the original path `/app` will actually be served at `/api/v1/app`.

Even though your application "thinks" it is serving at `/app`.

And the Proxy could be re-writing the path "on the fly" to keep your application convinced that it is serving at `/app`.

Up to here, everything would work as normally.

But then, when you open the integrated docs, they would expect to get the OpenAPI schema at `/openapi.json`, instead of `/api/v1/openapi.json`.

So, the frontend (that runs in the browser) would try to reach `/openapi.json` and wouldn't be able to get the OpenAPI schema.

So, it's needed that the frontend looks for the OpenAPI schema at `/api/v1/openapi.json`.

And it's also needed that the returned JSON OpenAPI schema has the defined path at `/api/v1/app` (behind the proxy) instead of `/app`.

---

For these cases, you can declare an `openapi_prefix` parameter in your `FastAPI` application.

See the section below, about "mounting", for an example.


## Mounting a **FastAPI** application

"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

You could want to do this if you have several "independent" applications that you want to separate, having their own independent OpenAPI schema and user interfaces.

### Top-level application

First, create the main, top-level, **FastAPI** application, and its path operations:

```Python hl_lines="3 6 7 8"
{!./src/sub_applications/tutorial001.py!}
```

### Sub-application

Then, create your sub-application, and its path operations.

This sub-application is just another standard FastAPI application, but this is the one that will be "mounted".

When creating the sub-application, use the parameter `openapi_prefix`. In this case, with a prefix of `/subapi`:

```Python hl_lines="11 14 15 16"
{!./src/sub_applications/tutorial001.py!}
```

### Mount the sub-application

In your top-level application, `app`, mount the sub-application, `subapi`.

Here you need to make sure you use the same path that you used for the `openapi_prefix`, in this case, `/subapi`:

```Python hl_lines="11 19"
{!./src/sub_applications/tutorial001.py!}
```

## Check the automatic API docs

Now, run `uvicorn`, if your file is at `main.py`, it would be:

```bash
uvicorn main:app --reload
```

And open the docs at <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic API docs for the main app, including only its own paths:

<img src="/img/tutorial/sub-applications/image01.png">


And then, open the docs for the sub-application, at <a href="http://127.0.0.1:8000/subapi/docs" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

You will see the automatic API docs for the sub-application, including only its own sub-paths, with their correct prefix:

<img src="/img/tutorial/sub-applications/image02.png">


If you try interacting with any of the two user interfaces, they will work, because the browser will be able to talk to the correct path (or sub-path).