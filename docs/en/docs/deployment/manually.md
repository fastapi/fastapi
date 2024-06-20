# Run a Server Manually

## Use the `fastapi run` Command

In short, use `fastapi run` to serve your FastAPI application:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <font color="#4E9A06">╭─────────── FastAPI CLI - Production mode ───────────╮</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Serving at: http://0.0.0.0:8000                    │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  API docs: http://0.0.0.0:8000/docs                 │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  Running in production mode, for development use:   │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">│  </font><font color="#8AE234"><b>fastapi dev</b></font><font color="#4E9A06">                                        │</font>
 <font color="#4E9A06">│                                                     │</font>
 <font color="#4E9A06">╰─────────────────────────────────────────────────────╯</font>

<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2306215</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8000</b> (Press CTRL+C to quit)
```

</div>

That would work for most of the cases. 😎

You could use that command for example to start your **FastAPI** app in a container, in a server, etc.

## ASGI Servers

Let's go a little deeper into the details.

FastAPI uses a standard for building Python web frameworks and servers called <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>. FastAPI is an ASGI web framework.

The main thing you need to run a **FastAPI** application (or any other ASGI application) in a remote server machine is an ASGI server program like **Uvicorn**, this is the one that comes by default in the `fastapi` command.

There are several alternatives, including:

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>: a high performance ASGI server.
* <a href="https://pgjones.gitlab.io/hypercorn/" class="external-link" target="_blank">Hypercorn</a>: an ASGI server compatible with HTTP/2 and Trio among other features.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: the ASGI server built for Django Channels.

## Server Machine and Server Program

There's a small detail about names to keep in mind. 💡

The word "**server**" is commonly used to refer to both the remote/cloud computer (the physical or virtual machine) and also the program that is running on that machine (e.g. Uvicorn).

Just keep in mind that when you read "server" in general, it could refer to one of those two things.

When referring to the remote machine, it's common to call it **server**, but also **machine**, **VM** (virtual machine), **node**. Those all refer to some type of remote machine, normally running Linux, where you run programs.

## Install the Server Program

When you install FastAPI, it comes with a production server, Uvicorn, and you can start it with the `fastapi run` command.

But you can also install an ASGI server manually:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, a lightning-fast ASGI server, built on uvloop and httptools.

    <div class="termy">

    ```console
    $ pip install "uvicorn[standard]"

    ---> 100%
    ```

    </div>

    !!! tip
        By adding the `standard`, Uvicorn will install and use some recommended extra dependencies.

        That including `uvloop`, the high-performance drop-in replacement for `asyncio`, that provides the big concurrency performance boost.

        When you install FastAPI with something like `pip install fastapi` you already get `uvicorn[standard]` as well.

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, an ASGI server also compatible with HTTP/2.

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...or any other ASGI server.

## Run the Server Program

If you installed an ASGI server manually, you would normally need to pass an import string in a special format for it to import your FastAPI application:

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

!!! note
    The command `uvicorn main:app` refers to:

    * `main`: the file `main.py` (the Python "module").
    * `app`: the object created inside of `main.py` with the line `app = FastAPI()`.

    It is equivalent to:

    ```Python
    from main import app
    ```

!!! warning
    Uvicorn and others support a `--reload` option that is useful during development.

    The `--reload` option consumes much more resources, is more unstable, etc.

    It helps a lot during **development**, but you **shouldn't** use it in **production**.

## Hypercorn with Trio

Starlette and **FastAPI** are based on <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>, which makes them compatible with both Python's standard library <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a> and <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a>.

Nevertheless, Uvicorn is currently only compatible with asyncio, and it normally uses <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a>, the high-performance drop-in replacement for `asyncio`.

But if you want to directly use **Trio**, then you can use **Hypercorn** as it supports it. ✨

### Install Hypercorn with Trio

First you need to install Hypercorn with Trio support:

<div class="termy">

```console
$ pip install "hypercorn[trio]"
---> 100%
```

</div>

### Run with Trio

Then you can pass the command line option `--worker-class` with the value `trio`:

<div class="termy">

```console
$ hypercorn main:app --worker-class trio
```

</div>

And that will start Hypercorn with your app using Trio as the backend.

Now you can use Trio internally in your app. Or even better, you can use AnyIO, to keep your code compatible with both Trio and asyncio. 🎉

## Deployment Concepts

These examples run the server program (e.g Uvicorn), starting **a single process**, listening on all the IPs (`0.0.0.0`) on a predefined port (e.g. `80`).

This is the basic idea. But you will probably want to take care of some additional things, like:

* Security - HTTPS
* Running on startup
* Restarts
* Replication (the number of processes running)
* Memory
* Previous steps before starting

I'll tell you more about each of these concepts, how to think about them, and some concrete examples with strategies to handle them in the next chapters. 🚀
