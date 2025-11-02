# Run a Server Manually { #run-a-server-manually }

## Use the `fastapi run` Command { #use-the-fastapi-run-command }

In short, use `fastapi run` to serve your FastAPI application:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

That would work for most of the cases. 😎

You could use that command for example to start your **FastAPI** app in a container, in a server, etc.

## ASGI Servers { #asgi-servers }

Let's go a little deeper into the details.

FastAPI uses a standard for building Python web frameworks and servers called <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>. FastAPI is an ASGI web framework.

The main thing you need to run a **FastAPI** application (or any other ASGI application) in a remote server machine is an ASGI server program like **Uvicorn**, this is the one that comes by default in the `fastapi` command.

There are several alternatives, including:

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>: a high performance ASGI server.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: an ASGI server compatible with HTTP/2 and Trio among other features.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: the ASGI server built for Django Channels.
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>: A Rust HTTP server for Python applications.
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>: NGINX Unit is a lightweight and versatile web application runtime.

## Server Machine and Server Program { #server-machine-and-server-program }

There's a small detail about names to keep in mind. 💡

The word "**server**" is commonly used to refer to both the remote/cloud computer (the physical or virtual machine) and also the program that is running on that machine (e.g. Uvicorn).

Just keep in mind that when you read "server" in general, it could refer to one of those two things.

When referring to the remote machine, it's common to call it **server**, but also **machine**, **VM** (virtual machine), **node**. Those all refer to some type of remote machine, normally running Linux, where you run programs.

## Install the Server Program { #install-the-server-program }

When you install FastAPI, it comes with a production server, Uvicorn, and you can start it with the `fastapi run` command.

But you can also install an ASGI server manually.

Make sure you create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then you can install the server application.

For example, to install Uvicorn:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

A similar process would apply to any other ASGI server program.

/// tip

By adding the `standard`, Uvicorn will install and use some recommended extra dependencies.

That including `uvloop`, the high-performance drop-in replacement for `asyncio`, that provides the big concurrency performance boost.

When you install FastAPI with something like `pip install "fastapi[standard]"` you already get `uvicorn[standard]` as well.

///

## Run the Server Program { #run-the-server-program }

If you installed an ASGI server manually, you would normally need to pass an import string in a special format for it to import your FastAPI application:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note

The command `uvicorn main:app` refers to:

* `main`: the file `main.py` (the Python "module").
* `app`: the object created inside of `main.py` with the line `app = FastAPI()`.

It is equivalent to:

```Python
from main import app
```

///

Each alternative ASGI server program would have a similar command, you can read more in their respective documentation.

/// warning

Uvicorn and other servers support a `--reload` option that is useful during development.

The `--reload` option consumes much more resources, is more unstable, etc.

It helps a lot during **development**, but you **shouldn't** use it in **production**.

///

## Deployment Concepts { #deployment-concepts }

These examples run the server program (e.g Uvicorn), starting **a single process**, listening on all the IPs (`0.0.0.0`) on a predefined port (e.g. `80`).

This is the basic idea. But you will probably want to take care of some additional things, like:

* Security - HTTPS
* Running on startup
* Restarts
* Replication (the number of processes running)
* Memory
* Previous steps before starting

I'll tell you more about each of these concepts, how to think about them, and some concrete examples with strategies to handle them in the next chapters. 🚀
