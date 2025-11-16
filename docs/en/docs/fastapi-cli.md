```markdown
# FastAPI CLI { #fastapi-cli }

**FastAPI CLI** is a command-line tool that helps you serve your FastAPI application, manage your project, and perform various development tasks.

When you install FastAPI (e.g. with `pip install "fastapi[standard]"`), it includes the fastapi-cli package, which provides the `fastapi` command in your terminal.

To run your FastAPI app for development, you can use the `fastapi dev` command:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

The command line program called `fastapi` is **FastAPI CLI**.

FastAPI CLI takes the path to your Python file (e.g. `main.py`), automatically detects the FastAPI instance (usually named `app`), determines how it should be imported, and starts the server for you.

For production, you should use `fastapi run` instead. 🚀

Internally, **FastAPI CLI** uses <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, a high-performance, production-ready, ASGI server. 😎

## `fastapi dev` { #fastapi-dev }

Running `fastapi dev` starts FastAPI in development mode.

By default, **auto-reload** is enabled, automatically reloading the server when you make changes to your code. Auto-reload is resource-intensive and may be less stable than running with it disabled. You should only use it for development. It also listens on the IP address `127.0.0.1`, which is the address your machine uses to communicate with itself (`localhost`).

## `fastapi run` { #fastapi-run }

Running `fastapi run` starts FastAPI in production mode.

By default, **auto-reload** is disabled. It also listens on `0.0.0.0`, which makes the application accessible on all available network interfaces. This is typically how you run a production server, such as inside a container.

In most cases, you should have a “termination proxy” handling HTTPS in front of your application. Depending on your deployment setup, your hosting provider may handle this, or you may need to configure it yourself.

/// tip

You can learn more about it in the [deployment documentation](deployment/index.md){.internal-link target=_blank}.

///
```
