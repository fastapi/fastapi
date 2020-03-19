You can serve static files automatically from a directory using `StaticFiles`.

## Install `aiofiles`

First you need to install `aiofiles`:

<div class="termy">

```console
$ pip install aiofiles

---> 100%
```

</div>

## Use `StaticFiles`

* Import `StaticFiles`.
* "Mount" a `StaticFiles()` instance in a specific path.

```Python hl_lines="2 6"
{!./src/static_files/tutorial001.py!}
```

!!! note "Technical Details"
    You could also use `from starlette.staticfiles import StaticFiles`.

    **FastAPI** provides the same `starlette.staticfiles` as `fastapi.staticfiles` just as a convenience for you, the developer. But it actually comes directly from Starlette.

### What is "Mounting"

"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

This is different from using an `APIRouter` as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.

You can read more about this in the **Advanced User Guide**.

## Details

The first `"/static"` refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with `"/static"` will be handled by it.

The `directory="static"` refers to the name of the directory that contains your static files.

The `name="static"` gives it a name that can be used internally by **FastAPI**.

All these parameters can be different than "`static`", adjust them with the needs and specific details of your own application.

## More info

For more details and options check <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette's docs about Static Files</a>.
