You can serve static files automatically from a directory using <a href="https://www.starlette.io/staticfiles/" target="_blank">Starlette's Static Files</a>.

## Install `aiofiles`

First you need to install `aiofiles`:

```bash
pip install aiofiles
```

## Use `StaticFiles`

* Import `StaticFiles` from Starlette.
* "Mount" it the same way you would <a href="https://fastapi.tiangolo.com/tutorial/sub-applications-proxy/" target="_blank">mount a Sub-Application</a>.

```Python hl_lines="2 6"
{!./src/static_files/tutorial001.py!}
```

Then you could have a directory `./static/` with some files that will be served directly.

## Details

The first `"/static"` refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with `"/static"` will be handled by it.

The `directory="static"` refers to the name of the directory that contains your static files.

The `name="static"` gives it a name that can be used internally by **FastAPI**.

All these parameters can be different than "`static`", adjust them with the needs and specific details of your own application.

## More info

For more details and options check <a href="https://www.starlette.io/staticfiles/" target="_blank">Starlette's docs about Static Files</a>.
