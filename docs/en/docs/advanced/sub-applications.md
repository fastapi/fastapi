# Sub Applications - Mounts { #sub-applications-mounts }

If you need to have two independent FastAPI applications, with their own independent OpenAPI and their own docs UIs, you can have a main app and "mount" one (or more) sub-application(s).

## Mounting a **FastAPI** application { #mounting-a-fastapi-application }

"Mounting" means adding a completely "independent" application in a specific path, that then takes care of handling everything under that path, with the _path operations_ declared in that sub-application.

### Top-level application { #top-level-application }

First, create the main, top-level, **FastAPI** application, and its *path operations*:

{* ../../docs_src/sub_applications/tutorial001.py hl[3, 6:8] *}

### Sub-application { #sub-application }

Then, create your sub-application, and its *path operations*.

This sub-application is just another standard FastAPI application, but this is the one that will be "mounted":

{* ../../docs_src/sub_applications/tutorial001.py hl[11, 14:16] *}

### Mount the sub-application { #mount-the-sub-application }

In your top-level application, `app`, mount the sub-application, `subapi`.

In this case, it will be mounted at the path `/subapi`:

{* ../../docs_src/sub_applications/tutorial001.py hl[11, 19] *}

### Check the automatic API docs { #check-the-automatic-api-docs }

Now, run the `fastapi` command with your file:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

And open the docs at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic API docs for the main app, including only its own _path operations_:

<img src="/img/tutorial/sub-applications/image01.png">

And then, open the docs for the sub-application, at <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

You will see the automatic API docs for the sub-application, including only its own _path operations_, all under the correct sub-path prefix `/subapi`:

<img src="/img/tutorial/sub-applications/image02.png">

If you try interacting with any of the two user interfaces, they will work correctly, because the browser will be able to talk to each specific app or sub-app.

### Technical Details: `root_path` { #technical-details-root-path }

When you mount a sub-application as described above, FastAPI will take care of communicating the mount path for the sub-application using a mechanism from the ASGI specification called a `root_path`.

That way, the sub-application will know to use that path prefix for the docs UI.

And the sub-application could also have its own mounted sub-applications and everything would work correctly, because FastAPI handles all these `root_path`s automatically.

You will learn more about the `root_path` and how to use it explicitly in the section about [Behind a Proxy](behind-a-proxy.md){.internal-link target=_blank}.
