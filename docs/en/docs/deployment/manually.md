# Deploy manually

You can deploy **FastAPI** manually as well.

You just need to install an ASGI compatible server like:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, a lightning-fast ASGI server, built on uvloop and httptools.

    <div class="termy">

    ```console
    $ pip install uvicorn[standard]

    ---> 100%
    ```

    </div>

    !!! tip
        By adding the `standard`, Uvicorn will install and use some recommended extra dependencies.
        
        That including `uvloop`, the high-performance drop-in replacement for `asyncio`, that provides the big concurrency performance boost.

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, an ASGI server also compatible with HTTP/2.

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...or any other ASGI server.

And run your application the same way you have done in the tutorials, but without the `--reload` option, e.g.:

=== "Uvicorn"

    <div class="termy">

    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80

    <span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    ```

    </div>

=== "Hypercorn"

    <div class="termy">

    ```console
    $ hypercorn main:app --bind 0.0.0.0:80

    Running on 0.0.0.0:8080 over http (CTRL + C to quit)
    ```

    </div>

You might want to set up some tooling to make sure it is restarted automatically if it stops.

You might also want to install <a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a> and <a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">use it as a manager for Uvicorn</a>, or use Hypercorn with multiple workers.

Making sure to fine-tune the number of workers, etc.

But if you are doing all that, you might just use the Docker image that does it automatically.
