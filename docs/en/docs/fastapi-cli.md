# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface">CLI</abbr>** is a command line program that you can use to serve your FastAPI app, manage your FastAPI project, and more.

When you install FastAPI (e.g. with `pip install "fastapi[standard]"`), it comes with a command line program you can run in the terminal.

To run your FastAPI app for development, you can use the `fastapi dev` command:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip

For production you would use `fastapi run` instead of `fastapi dev`. 🚀

///

Internally, **FastAPI CLI** uses [Uvicorn](https://www.uvicorn.dev), a high-performance, production-ready, ASGI server. 😎

The `fastapi` CLI will try to detect automatically the FastAPI app to run, assuming it's an object called `app` in a file `main.py` (or a couple other variants).

But you can configure explicitly the app to use.

## Configure the app `entrypoint` in `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

You can configure where your app is located in a `pyproject.toml` file like:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

That `entrypoint` will tell the `fastapi` command that it should import the app like:

```python
from main import app
```

If your code was structured like:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Then you would set the `entrypoint` as:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

which would be equivalent to:

```python
from backend.main import app
```

### `fastapi dev` with path { #fastapi-dev-with-path }

You can also pass the file path to the `fastapi dev` command, and it will guess the FastAPI app object to use:

```console
$ fastapi dev main.py
```

But you would have to remember to pass the correct path every time you call the `fastapi` command.

Additionally, other tools might not be able to find it, for example the [VS Code Extension](editor-support.md) or [FastAPI Cloud](https://fastapicloud.com), so it is recommended to use the `entrypoint` in `pyproject.toml`.

## `fastapi dev` { #fastapi-dev }

Running `fastapi dev` initiates development mode.

By default, **auto-reload** is enabled, automatically reloading the server when you make changes to your code. This is resource-intensive and could be less stable than when it's disabled. You should only use it for development. It also listens on the IP address `127.0.0.1`, which is the IP for your machine to communicate with itself alone (`localhost`).

## `fastapi run` { #fastapi-run }

Executing `fastapi run` starts FastAPI in production mode.

By default, **auto-reload** is disabled. It also listens on the IP address `0.0.0.0`, which means all the available IP addresses, this way it will be publicly accessible to anyone that can communicate with the machine. This is how you would normally run it in production, for example, in a container.

In most cases you would (and should) have a "termination proxy" handling HTTPS for you on top, this will depend on how you deploy your application, your provider might do this for you, or you might need to set it up yourself.

/// tip

You can learn more about it in the [deployment documentation](deployment/index.md).

///
